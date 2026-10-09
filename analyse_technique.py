"""
analyse_technique.py
--------------------
Télécharge les cours via yfinance, calcule les indicateurs techniques avec
pandas-ta et produit :
  - synthese.csv / synthese.json : une ligne par ticker (dernière séance)
  - historique.csv : les dernières séances de chaque ticker, indicateurs compris
  - statut.json : date d'exécution, tickers en échec, date de dernière séance

Signal : pullback sur EMA20 en tendance haussière, confirmation RSI et/ou MACD
(chacune désactivable). Achat uniquement.

Usage :
    python analyse_technique.py --fichier tickers.txt --sortie data
    python analyse_technique.py BNP.PA SAF.PA            # test rapide
    python analyse_technique.py --fichier tickers.txt --excel   # + fichier Excel
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
import pandas_ta as ta
import yfinance as yf

# =============================================================================
# PARAMÈTRES
# =============================================================================

PERIODE = "2y"        # historique téléchargé (≥ 1y pour l'EMA200)
INTERVALLE = "1d"

EMA_COURTE = 20
EMA_MOYENNE = 50
EMA_LONGUE_1 = 100
EMA_LONGUE_2 = 200
RSI_LONGUEUR = 14
MACD_RAPIDE, MACD_LENTE, MACD_SIGNAL = 12, 26, 9
ATR_LONGUEUR = 14

UTILISER_CONFIRMATION_RSI = True
UTILISER_CONFIRMATION_MACD = True
RSI_ZONE_MIN = 40
RSI_ZONE_MAX = 60
TOLERANCE_EMA20_PCT = 1.0
FENETRE_PULLBACK = 3

LIQUIDITE_MIN = 1_000_000           # volume moyen 20 j × cours (devise locale)
SEANCES_HISTORIQUE = 260            # séances gardées par ticker dans historique.csv
GROUPES_SANS_VOLUME = {"INDICES"}   # pas de contrôle de liquidité

FUSEAU = ZoneInfo("Europe/Paris")

# =============================================================================


def telecharger(ticker: str, tentatives: int = 3) -> pd.DataFrame | None:
    """Historique OHLCV ajusté d'un ticker, avec relances."""
    for essai in range(1, tentatives + 1):
        try:
            df = yf.Ticker(ticker).history(
                period=PERIODE, interval=INTERVALLE, auto_adjust=True
            )
            if df is not None and not df.empty:
                df = df[["Open", "High", "Low", "Close", "Volume"]].dropna(
                    subset=["Close"]
                )
                df.index = df.index.tz_localize(None)
                return df
        except Exception as e:
            print(f"  ! {ticker} : essai {essai}/{tentatives} échoué ({e})")
        time.sleep(2 * essai)
    return None


def calculer_indicateurs(df: pd.DataFrame) -> pd.DataFrame:
    c = df["Close"]
    for n in (EMA_COURTE, EMA_MOYENNE, EMA_LONGUE_1, EMA_LONGUE_2):
        df[f"EMA{n}"] = ta.ema(c, length=n) if len(df) >= n else float("nan")
    df["SMA50"] = ta.sma(c, length=50) if len(df) >= 50 else float("nan")
    df["SMA200"] = ta.sma(c, length=200) if len(df) >= 200 else float("nan")
    df["RSI"] = ta.rsi(c, length=RSI_LONGUEUR)

    macd = ta.macd(c, fast=MACD_RAPIDE, slow=MACD_LENTE, signal=MACD_SIGNAL)
    suffixe = f"{MACD_RAPIDE}_{MACD_LENTE}_{MACD_SIGNAL}"
    df["MACD"] = macd[f"MACD_{suffixe}"]
    df["MACD_signal"] = macd[f"MACDs_{suffixe}"]
    df["MACD_hist"] = macd[f"MACDh_{suffixe}"]

    df["ATR"] = ta.atr(df["High"], df["Low"], c, length=ATR_LONGUEUR)
    df["Vol_moy20"] = df["Volume"].rolling(20).mean()
    df["Vol_ratio"] = df["Volume"] / df["Vol_moy20"]
    return df


def r(x, n=2):
    """Arrondi tolérant aux valeurs manquantes (None dans le JSON)."""
    return None if pd.isna(x) else round(float(x), n)


def evaluer(ticker: str, groupe: str, libelle: str, df: pd.DataFrame) -> dict:
    d, p = df.iloc[-1], df.iloc[-2]
    ema_c, ema_m, ema_l = f"EMA{EMA_COURTE}", f"EMA{EMA_MOYENNE}", f"EMA{EMA_LONGUE_2}"

    if pd.isna(d[ema_l]):
        tendance, tendance_haussiere = "Indéterminée", False
    elif d["Close"] > d[ema_l] and d[ema_m] > d[ema_l]:
        tendance, tendance_haussiere = "Haussière", True
    elif d["Close"] < d[ema_l] and d[ema_m] < d[ema_l]:
        tendance, tendance_haussiere = "Baissière", False
    else:
        tendance, tendance_haussiere = "Neutre", False

    recent = df.iloc[-FENETRE_PULLBACK:]
    seuil = recent[ema_c] * (1 + TOLERANCE_EMA20_PCT / 100)
    pullback = bool((recent["Low"] <= seuil).any()) and d["Close"] > d[ema_c]

    rsi_ok = bool(RSI_ZONE_MIN <= d["RSI"] <= RSI_ZONE_MAX and d["RSI"] > p["RSI"])
    croisement_macd_haut = d["MACD"] > d["MACD_signal"] and p["MACD"] <= p["MACD_signal"]
    croisement_macd_bas = d["MACD"] < d["MACD_signal"] and p["MACD"] >= p["MACD_signal"]
    macd_ok = bool(d["MACD_hist"] > p["MACD_hist"] or croisement_macd_haut)

    conditions = [tendance_haussiere, pullback]
    if UTILISER_CONFIRMATION_RSI:
        conditions.append(rsi_ok)
    if UTILISER_CONFIRMATION_MACD:
        conditions.append(macd_ok)
    signal_achat = all(conditions)

    evenements = []
    if croisement_macd_haut:
        evenements.append("Croisement MACD haussier")
    if croisement_macd_bas:
        evenements.append("Croisement MACD baissier")
    if not pd.isna(d["SMA200"]) and not pd.isna(p["SMA200"]):
        if d["SMA50"] > d["SMA200"] and p["SMA50"] <= p["SMA200"]:
            evenements.append("Golden cross")
        if d["SMA50"] < d["SMA200"] and p["SMA50"] >= p["SMA200"]:
            evenements.append("Death cross")
    if d["RSI"] >= 70:
        evenements.append("RSI suracheté")
    if d["RSI"] <= 30:
        evenements.append("RSI survendu")

    un_an = df.iloc[-252:]
    if groupe in GROUPES_SANS_VOLUME or d["Vol_moy20"] == 0 or pd.isna(d["Vol_moy20"]):
        liquidite = "n/a"
    else:
        liquidite = "OK" if d["Vol_moy20"] * d["Close"] >= LIQUIDITE_MIN else "Faible"

    return {
        "groupe": groupe,
        "ticker": ticker,
        "libelle": libelle,
        "date_seance": df.index[-1].strftime("%Y-%m-%d"),
        "ouverture": r(d["Open"], 4),
        "plus_haut": r(d["High"], 4),
        "plus_bas": r(d["Low"], 4),
        "cloture": r(d["Close"], 4),
        "cloture_veille": r(p["Close"], 4),
        "var_jour_pct": r((d["Close"] / p["Close"] - 1) * 100),
        "volume": r(d["Volume"], 0),
        "volume_vs_moy20": r(d["Vol_ratio"]),
        "plus_haut_52s": r(un_an["High"].max(), 4),
        "plus_bas_52s": r(un_an["Low"].min(), 4),
        "tendance": tendance,
        "dist_ema20_pct": r((d["Close"] / d[ema_c] - 1) * 100),
        "ema20": r(d[ema_c], 4),
        "ema50": r(d[ema_m], 4),
        "ema100": r(d[f"EMA{EMA_LONGUE_1}"], 4),
        "ema200": r(d[ema_l], 4),
        "sma50": r(d["SMA50"], 4),
        "sma200": r(d["SMA200"], 4),
        "rsi": r(d["RSI"], 1),
        "rsi_veille": r(p["RSI"], 1),
        "macd": r(d["MACD"], 4),
        "macd_signal": r(d["MACD_signal"], 4),
        "macd_hist": r(d["MACD_hist"], 4),
        "macd_hist_veille": r(p["MACD_hist"], 4),
        "atr_pct": r(d["ATR"] / d["Close"] * 100),
        "pullback_ema20": pullback,
        "rsi_ok": rsi_ok,
        "macd_ok": macd_ok,
        "signal_achat": signal_achat,
        "liquidite": liquidite,
        "evenements": ", ".join(evenements),
    }


def lire_fichier_tickers(chemin: str) -> list[tuple[str, str, str]]:
    """Lit un fichier de tickers organisé en sections [GROUPE].
    Ligne : TICKER  # libellé (facultatif). Renvoie (groupe, ticker, libellé)."""
    groupe, resultat = "AUTRES", []
    for ligne in Path(chemin).read_text(encoding="utf-8").splitlines():
        ligne = ligne.strip()
        if not ligne or ligne.startswith("#"):
            continue
        if ligne.startswith("[") and ligne.endswith("]"):
            groupe = ligne[1:-1].strip().upper()
            continue
        ticker, _, libelle = ligne.partition("#")
        resultat.append((groupe, ticker.strip(), libelle.strip()))
    return resultat


def exporter(synthese, historiques, statut, sortie: Path, excel: bool):
    sortie.mkdir(parents=True, exist_ok=True)
    synthese.to_csv(sortie / "synthese.csv", index=False)
    (sortie / "synthese.json").write_text(
        json.dumps(synthese.to_dict(orient="records"), ensure_ascii=False, indent=1),
        encoding="utf-8",
    )
    blocs = []
    for t, df in historiques.items():
        h = df.iloc[-SEANCES_HISTORIQUE:].copy()
        h.insert(0, "Ticker", t)
        h.index.name = "Date"
        blocs.append(h.round(4))
    pd.concat(blocs).to_csv(sortie / "historique.csv")
    (sortie / "statut.json").write_text(
        json.dumps(statut, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    if excel:
        synthese.to_excel(sortie / "synthese.xlsx", index=False)


def main():
    parser = argparse.ArgumentParser(description="Analyse technique multi-tickers")
    parser.add_argument("tickers", nargs="*", help="ex. BNP.PA SAF.PA GOOGL")
    parser.add_argument("--fichier", help="fichier de tickers (sections [GROUPE])")
    parser.add_argument("--sortie", default="data", help="dossier de sortie")
    parser.add_argument("--excel", action="store_true", help="exporter aussi en .xlsx")
    args = parser.parse_args()

    if args.fichier:
        liste = lire_fichier_tickers(args.fichier)
    elif args.tickers:
        liste = [("AUTRES", t, "") for t in args.tickers]
    else:
        parser.error("indiquez des tickers ou --fichier tickers.txt")

    debut = datetime.now(FUSEAU)
    print(f"Analyse de {len(liste)} ticker(s) — {debut:%d/%m/%Y %H:%M} (Paris)\n")

    lignes, historiques, echecs = [], {}, []
    vus = set()
    for groupe, t, libelle in liste:
        if t in vus:              # un ticker présent dans deux sections
            continue
        vus.add(t)
        print(f"→ [{groupe}] {t}")
        df = telecharger(t)
        if df is None or len(df) < 35:
            print(f"  ! {t} : données absentes ou historique trop court")
            echecs.append({"ticker": t, "groupe": groupe, "libelle": libelle})
            continue
        df = calculer_indicateurs(df)
        historiques[t] = df
        lignes.append(evaluer(t, groupe, libelle, df))
        time.sleep(0.5)

    if not lignes:
        print("\nAucune donnée exploitable.")
        sys.exit(1)

    synthese = pd.DataFrame(lignes)
    statut = {
        "genere_le": datetime.now(FUSEAU).isoformat(timespec="seconds"),
        "nb_ok": len(lignes),
        "nb_echecs": len(echecs),
        "echecs": echecs,
        "derniere_seance_par_ticker": {l["ticker"]: l["date_seance"] for l in lignes},
        "signaux_achat": [l["ticker"] for l in lignes if l["signal_achat"]],
        "parametres": {
            "confirmation_rsi": UTILISER_CONFIRMATION_RSI,
            "confirmation_macd": UTILISER_CONFIRMATION_MACD,
            "rsi_zone": [RSI_ZONE_MIN, RSI_ZONE_MAX],
            "tolerance_ema20_pct": TOLERANCE_EMA20_PCT,
            "fenetre_pullback": FENETRE_PULLBACK,
        },
    }
    exporter(synthese, historiques, statut, Path(args.sortie), args.excel)

    vue = synthese[["groupe", "ticker", "cloture", "var_jour_pct", "tendance",
                    "dist_ema20_pct", "rsi", "signal_achat", "evenements"]]
    print("\n" + vue.to_string(index=False))
    print(f"\nSignaux d'achat : {', '.join(statut['signaux_achat']) or 'aucun'}")
    if echecs:
        print(f"Échecs : {', '.join(e['ticker'] for e in echecs)}")
    print(f"Fichiers écrits dans : {Path(args.sortie).resolve()}")


if __name__ == "__main__":
    main()
