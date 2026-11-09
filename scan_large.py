"""
scan_large.py
-------------
Scan large du marché américain pour la stratégie de swing « rachat de ventes
de court terme sur titres sains ».

Univers : composants du S&P 500 et du Nasdaq 100 (≈ 520 titres), lus sur
Wikipédia à chaque exécution. En cas d'échec, la dernière liste enregistrée
(data/univers_scan.csv) est réutilisée.

Produit dans le dossier de sortie :
  - scan.csv            : une ligne par titre de l'univers (indicateurs, recul
                          depuis le plus haut 52 semaines, tendance, filtres)
  - scan_historique.csv : les 130 dernières séances des seuls titres retenus
                          par le préfiltre (pour bâtir un plan de trade)
  - univers_scan.csv    : la liste de l'univers (cache)
  - scan_statut.json    : date d'exécution, tailles, échecs

Préfiltre (colonne « candidat ») :
  - cours entre PRIX_MIN et PRIX_MAX, volume moyen 20 j ≥ VOLUME_MIN
  - recul depuis le plus haut 52 semaines entre RECUL_MIN et RECUL_MAX
  - tendance de fond intacte (EMA50 > EMA200, ou cours > EMA200 montante)
    OU recul > 25 % (setup R3 possible, à valider à la main)

Usage :
    python scan_large.py --sortie data
    python scan_large.py --sortie data_test --limite 30   # test rapide
"""

import argparse
import io
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
import requests
import yfinance as yf

# =============================================================================
# PARAMÈTRES
# =============================================================================

PERIODE = "2y"              # historique téléchargé (EMA200 stabilisée)
TAILLE_LOT = 80             # titres par appel groupé à yfinance
PAUSE_LOT = 3               # secondes entre deux lots

PRIX_MIN, PRIX_MAX = 5.0, 250.0
VOLUME_MIN = 1_000_000      # titres/jour, moyenne 20 séances
RECUL_MIN, RECUL_MAX = -35.0, -10.0   # % depuis le plus haut 52 semaines
SEANCES_HISTORIQUE = 130

SOURCES = {
    "SP500": "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
    "NDX100": "https://en.wikipedia.org/wiki/Nasdaq-100",
}
ENTETES = {"User-Agent": "Mozilla/5.0 (analyse-technique; scan swing personnel)"}

FUSEAU = ZoneInfo("Europe/Paris")

# =============================================================================


def lire_univers(sortie: Path) -> pd.DataFrame:
    """Composants S&P 500 + Nasdaq 100 avec secteur GICS. Cache en secours."""
    cache = sortie / "univers_scan.csv"
    blocs = []
    for indice, url in SOURCES.items():
        try:
            html = requests.get(url, headers=ENTETES, timeout=30).text
            for table in pd.read_html(io.StringIO(html)):
                cols = {str(c).strip().lower(): c for c in table.columns}
                col_ticker = cols.get("symbol") or cols.get("ticker")
                col_nom = cols.get("security") or cols.get("company")
                col_secteur = cols.get("gics sector")
                if col_ticker is None or col_nom is None:
                    continue
                t = pd.DataFrame({
                    "ticker": table[col_ticker].astype(str).str.strip(),
                    "nom": table[col_nom].astype(str).str.strip(),
                    "secteur": table[col_secteur].astype(str).str.strip()
                    if col_secteur is not None else "",
                    "indice": indice,
                })
                if len(t) >= 90:            # la bonne table, pas un encadré
                    blocs.append(t)
                    break
        except Exception as e:
            print(f"  ! Univers {indice} : lecture impossible ({e})")

    if blocs:
        u = pd.concat(blocs)
        # Yahoo note les classes d'actions avec un tiret (BRK.B -> BRK-B)
        u["ticker"] = u["ticker"].str.replace(".", "-", regex=False)
        u = (u.groupby("ticker", as_index=False)
               .agg({"nom": "first", "secteur": "first",
                     "indice": lambda s: "+".join(sorted(set(s)))}))
        if len(u) >= 400:
            sortie.mkdir(parents=True, exist_ok=True)
            u.to_csv(cache, index=False)
            return u
        print(f"  ! Univers incomplet ({len(u)} titres) : utilisation du cache")

    if cache.exists():
        return pd.read_csv(cache).fillna("")
    print("Univers introuvable et pas de cache : arrêt.")
    sys.exit(1)


def ema(s: pd.Series, n: int) -> pd.Series:
    return s.ewm(span=n, adjust=False).mean()


def wilder(s: pd.Series, n: int) -> pd.Series:
    return s.ewm(alpha=1 / n, adjust=False).mean()


def indicateurs(df: pd.DataFrame) -> pd.DataFrame:
    c = df["Close"]
    for n in (10, 20, 50, 200):
        df[f"EMA{n}"] = ema(c, n)
    delta = c.diff()
    hausse = wilder(delta.clip(lower=0), 14)
    baisse = wilder(-delta.clip(upper=0), 14)
    df["RSI"] = 100 - 100 / (1 + hausse / baisse)
    macd = ema(c, 12) - ema(c, 26)
    df["MACD_hist"] = macd - ema(macd, 9)
    tr = pd.concat([df["High"] - df["Low"],
                    (df["High"] - c.shift()).abs(),
                    (df["Low"] - c.shift()).abs()], axis=1).max(axis=1)
    df["ATR"] = wilder(tr, 14)
    df["Vol_moy20"] = df["Volume"].rolling(20).mean()
    df["Vol_ratio"] = df["Volume"] / df["Vol_moy20"]
    return df


def r(x, n=2):
    return None if pd.isna(x) else round(float(x), n)


def resumer(t: str, info: dict, df: pd.DataFrame) -> dict:
    d, p = df.iloc[-1], df.iloc[-2]
    un_an = df.iloc[-252:]
    haut52 = un_an["High"].max()
    date_haut = un_an["High"].idxmax()
    recul = (d["Close"] / haut52 - 1) * 100
    ema50_monte = d["EMA50"] > df["EMA50"].iloc[-11]
    ema200_monte = d["EMA200"] > df["EMA200"].iloc[-11]
    tendance_ok = bool(d["EMA50"] > d["EMA200"]
                       or (d["Close"] > d["EMA200"] and ema200_monte))

    prix_ok = PRIX_MIN <= d["Close"] <= PRIX_MAX
    volume_ok = d["Vol_moy20"] >= VOLUME_MIN
    recul_ok = RECUL_MIN <= recul <= RECUL_MAX
    r3_possible = recul < -25 or not ema50_monte
    candidat = bool(prix_ok and volume_ok and recul_ok
                    and (tendance_ok or recul < -25))

    return {
        "ticker": t,
        "nom": info.get("nom", ""),
        "secteur": info.get("secteur", ""),
        "indice": info.get("indice", ""),
        "date_seance": df.index[-1].strftime("%Y-%m-%d"),
        "ouverture": r(d["Open"], 4),
        "plus_haut": r(d["High"], 4),
        "plus_bas": r(d["Low"], 4),
        "cloture": r(d["Close"], 4),
        "var_jour_pct": r((d["Close"] / p["Close"] - 1) * 100),
        "plus_haut_52s": r(haut52, 4),
        "date_plus_haut_52s": date_haut.strftime("%Y-%m-%d"),
        "recul_pct": r(recul, 1),
        "ema10": r(d["EMA10"], 4),
        "ema20": r(d["EMA20"], 4),
        "ema50": r(d["EMA50"], 4),
        "ema200": r(d["EMA200"], 4),
        "ema50_monte": bool(ema50_monte),
        "ema200_monte": bool(ema200_monte),
        "tendance_ok": tendance_ok,
        "rsi": r(d["RSI"], 1),
        "rsi_veille": r(p["RSI"], 1),
        "macd_hist": r(d["MACD_hist"], 4),
        "macd_hist_veille": r(p["MACD_hist"], 4),
        "atr": r(d["ATR"], 4),
        "atr_pct": r(d["ATR"] / d["Close"] * 100),
        "volume_moy20": r(d["Vol_moy20"], 0),
        "volume_ratio": r(d["Vol_ratio"]),
        "cout_2_actions": r(2 * d["Close"]),
        "r3_possible": bool(r3_possible),
        "candidat": candidat,
    }


def telecharger_lot(tickers: list[str]) -> dict[str, pd.DataFrame]:
    """Téléchargement groupé ; renvoie {ticker: OHLCV} pour les titres valides."""
    brut = yf.download(tickers, period=PERIODE, interval="1d", auto_adjust=True,
                       group_by="ticker", threads=True, progress=False)
    resultat = {}
    for t in tickers:
        try:
            df = brut[t] if isinstance(brut.columns, pd.MultiIndex) else brut
            df = df[["Open", "High", "Low", "Close", "Volume"]].dropna(subset=["Close"])
            if len(df) >= 210:
                df.index = pd.to_datetime(df.index).tz_localize(None)
                resultat[t] = df.copy()
        except Exception:
            pass
    return resultat


def main():
    parser = argparse.ArgumentParser(description="Scan large S&P 500 + Nasdaq 100")
    parser.add_argument("--sortie", default="data", help="dossier de sortie")
    parser.add_argument("--limite", type=int, default=0,
                        help="nombre max de titres (test rapide)")
    args = parser.parse_args()
    sortie = Path(args.sortie)

    debut = datetime.now(FUSEAU)
    univers = lire_univers(sortie)
    if args.limite:
        univers = univers.head(args.limite)
    infos = univers.set_index("ticker").to_dict(orient="index")
    tickers = list(infos)
    print(f"Scan large de {len(tickers)} titres — {debut:%d/%m/%Y %H:%M} (Paris)")

    lignes, historiques, echecs = [], {}, []
    for i in range(0, len(tickers), TAILLE_LOT):
        lot = tickers[i:i + TAILLE_LOT]
        print(f"→ lot {i // TAILLE_LOT + 1} ({len(lot)} titres)")
        try:
            donnees = telecharger_lot(lot)
        except Exception as e:
            print(f"  ! lot en échec ({e}), nouvel essai dans 10 s")
            time.sleep(10)
            try:
                donnees = telecharger_lot(lot)
            except Exception:
                donnees = {}
        for t in lot:
            if t not in donnees:
                echecs.append(t)
                continue
            try:
                df = indicateurs(donnees[t])
                ligne = resumer(t, infos[t], df)
                lignes.append(ligne)
                if ligne["candidat"]:
                    historiques[t] = df
            except Exception as e:
                print(f"  ! {t} : calcul impossible ({e})")
                echecs.append(t)
        time.sleep(PAUSE_LOT)

    if not lignes:
        print("Aucune donnée exploitable.")
        sys.exit(1)

    sortie.mkdir(parents=True, exist_ok=True)
    scan = pd.DataFrame(lignes).sort_values(["candidat", "recul_pct"],
                                            ascending=[False, True])
    scan.to_csv(sortie / "scan.csv", index=False)

    blocs = []
    for t, df in historiques.items():
        h = df.iloc[-SEANCES_HISTORIQUE:].copy()
        h.insert(0, "Ticker", t)
        h.index.name = "Date"
        blocs.append(h.round(4))
    if blocs:
        pd.concat(blocs).to_csv(sortie / "scan_historique.csv")

    statut = {
        "genere_le": datetime.now(FUSEAU).isoformat(timespec="seconds"),
        "derniere_seance": scan["date_seance"].max(),
        "nb_univers": len(tickers),
        "nb_ok": len(lignes),
        "nb_candidats": int(scan["candidat"].sum()),
        "echecs": echecs,
        "filtres": {"prix": [PRIX_MIN, PRIX_MAX], "volume_min": VOLUME_MIN,
                    "recul_pct": [RECUL_MIN, RECUL_MAX]},
    }
    (sortie / "scan_statut.json").write_text(
        json.dumps(statut, ensure_ascii=False, indent=1), encoding="utf-8")

    vue = scan[scan["candidat"]][["ticker", "secteur", "cloture", "recul_pct",
                                  "tendance_ok", "rsi", "atr_pct"]]
    print(f"\n{statut['nb_candidats']} candidats sur {len(lignes)} titres analysés")
    print(vue.head(40).to_string(index=False))
    if echecs:
        print(f"Échecs ({len(echecs)}) : {', '.join(echecs[:30])}")


if __name__ == "__main__":
    main()
