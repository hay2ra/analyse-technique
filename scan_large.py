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
                          depuis le plus haut 52 semaines, tendance, force
                          relative, score de setup, dates de résultats)
  - scan_historique.csv : les 130 dernières séances des seuls candidats
  - marche.json         : santé du marché (largeur S&P 500, VIX, indices,
                          ETF sectoriels et force relative)
  - univers_scan.csv    : la liste de l'univers (cache)
  - scan_statut.json    : date d'exécution, tailles, échecs

Préfiltre (colonne « candidat ») :
  - cours entre PRIX_MIN et PRIX_MAX, volume moyen 20 j ≥ VOLUME_MIN
  - recul depuis le plus haut 52 semaines entre RECUL_MIN et RECUL_MAX
  - tendance de fond intacte (EMA50 > EMA200, ou cours > EMA200 montante)
    OU recul > 25 % (setup R3 possible, à valider à la main)

Score de setup (0 à 10, colonne « score_setup ») : contact récent avec un
support (EMA20/50/200), bougie de reprise, RSI et MACD qui remontent, volume
en baisse dans le repli, plus bas qui monte, force relative, tendance. Les
titres qui publient leurs résultats dans moins de JOURS_RESULTATS_MIN séances
sont signalés (colonne « resultats_proches ») : à exclure.

Usage :
    python scan_large.py --sortie data
    python scan_large.py --sortie data_test --limite 30   # test rapide
"""

import argparse
import io
import json
import sys
import time
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
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

JOURS_RESULTATS_MIN = 7     # séances minimum avant la prochaine publication
CONTACT_SUPPORT_ATR = 0.5   # plus bas à moins de 0,5 ATR d'une EMA = contact

REFERENCE = "SPY"
MARCHE = {
    "SPY": "S&P 500", "QQQ": "Nasdaq 100", "IWM": "Russell 2000",
    "^VIX": "VIX",
    "XLK": "Technologie", "SMH": "Semi-conducteurs", "XLC": "Communication",
    "XLY": "Consommation discrétionnaire", "XLP": "Consommation de base",
    "XLV": "Santé", "XLF": "Finance", "XLI": "Industrie", "XLE": "Énergie",
    "XLB": "Matériaux", "XLU": "Services aux collectivités",
    "XLRE": "Immobilier",
}

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
            trouve = False
            tables = pd.read_html(io.StringIO(html))
            for table in tables:
                if isinstance(table.columns, pd.MultiIndex):
                    table.columns = [" ".join(map(str, c)) for c in table.columns]
                cols = {str(c).strip().lower(): c for c in table.columns}

                def chercher(*mots):
                    for nom, c in cols.items():
                        if any(m in nom for m in mots):
                            return c
                    return None

                if len(table) < 90:
                    continue
                col_ticker = chercher("symbol", "ticker")
                if col_ticker is None:
                    # Repérage par le contenu : la colonne qui contient les
                    # grands noms de l'indice, quel que soit son intitulé
                    for c in table.columns:
                        valeurs = set(table[c].astype(str).str.strip())
                        if len(valeurs & {"AAPL", "MSFT", "NVDA", "AMZN", "GOOGL"}) >= 3:
                            col_ticker = c
                            break
                col_nom = chercher("security", "company", "name")
                if col_nom is None and col_ticker is not None:
                    autres = [c for c in table.columns if c != col_ticker
                              and not pd.api.types.is_numeric_dtype(table[c])]
                    col_nom = autres[0] if autres else None
                col_secteur = chercher("gics sector", "sector", "industry")
                if col_ticker is None or col_nom is None:
                    print(f"    table ignorée ({len(table)} lignes) : "
                          f"{[str(c) for c in table.columns][:6]}")
                    continue
                trouve = True
                t = pd.DataFrame({
                    "ticker": table[col_ticker].astype(str).str.strip(),
                    "nom": table[col_nom].astype(str).str.strip(),
                    "secteur": table[col_secteur].astype(str).str.strip()
                    if col_secteur is not None else "",
                    "indice": indice,
                })
                blocs.append(t)
                print(f"  {indice} : {len(t)} titres")
                break
            if not trouve:
                print(f"  ! Univers {indice} : aucune table de composants reconnue "
                      f"({len(tables)} tables, tailles {[len(t) for t in tables][:15]})")
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


# ----------------------------------------------------------------- indicateurs

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
    return None if x is None or pd.isna(x) else round(float(x), n)


def perf(c: pd.Series, n: int) -> float:
    return (c.iloc[-1] / c.iloc[-1 - n] - 1) * 100 if len(c) > n else np.nan


def bougie_reprise(df: pd.DataFrame) -> str:
    """Type de bougie de reprise sur la dernière séance ('' si aucune)."""
    d, p = df.iloc[-1], df.iloc[-2]
    amplitude = d["High"] - d["Low"]
    if amplitude <= 0:
        return ""
    corps_bas = min(d["Open"], d["Close"])
    meche_basse = corps_bas - d["Low"]
    if (meche_basse >= 0.5 * amplitude
            and d["Close"] >= d["Low"] + 0.6 * amplitude):
        return "marteau"
    if (p["Close"] < p["Open"] and d["Close"] > d["Open"]
            and d["Close"] >= p["Open"] and d["Open"] <= p["Close"]):
        return "avalement haussier"
    if (p["Close"] < p["Open"] and d["Close"] > p["Close"]
            and d["Close"] >= d["Low"] + 0.67 * amplitude):
        return "clôture haute après baisse"
    return ""


def resumer(t: str, info: dict, df: pd.DataFrame, ref: pd.Series | None) -> dict:
    d, p = df.iloc[-1], df.iloc[-2]
    un_an = df.iloc[-252:]
    haut52 = un_an["High"].max()
    date_haut = un_an["High"].idxmax()
    recul = (d["Close"] / haut52 - 1) * 100
    ema50_monte = d["EMA50"] > df["EMA50"].iloc[-11]
    ema200_monte = d["EMA200"] > df["EMA200"].iloc[-11]
    tendance_ok = bool(d["EMA50"] > d["EMA200"]
                       or (d["Close"] > d["EMA200"] and ema200_monte))
    atr = d["ATR"]

    # Contact avec un support : plus bas des 3 dernières séances proche d'une EMA
    recents = df.iloc[-3:]
    contacts = []
    for n in (20, 50, 200):
        ecart = ((recents["Low"] - recents[f"EMA{n}"]).abs() / atr).min()
        if ecart <= CONTACT_SUPPORT_ATR and d["Close"] >= d[f"EMA{n}"] - 0.25 * atr:
            contacts.append(f"EMA{n}")
    # Volume en baisse dans le repli : séances baissières des 5 dernières
    cinq = df.iloc[-5:]
    baissieres = cinq[cinq["Close"] < cinq["Open"]]
    volume_repli = (r(baissieres["Vol_ratio"].mean())
                    if len(baissieres) else None)
    # Plus bas qui monte : plus bas des 10 dernières séances vs les 10 d'avant
    plus_bas_monte = bool(df["Low"].iloc[-10:].min() > df["Low"].iloc[-20:-10].min())
    bougie = bougie_reprise(df)

    rs1 = rs3 = np.nan
    if ref is not None:
        c = df["Close"]
        ref_al = ref.reindex(c.index).ffill()
        rs1 = perf(c, 21) - perf(ref_al, 21)
        rs3 = perf(c, 63) - perf(ref_al, 63)

    # Score de setup sur 10
    score = 0
    score += 2 if contacts else 0
    score += 2 if bougie else 0
    score += 1 if d["RSI"] > p["RSI"] and d["RSI"] < 50 else 0
    score += 1 if 30 <= d["RSI"] <= 50 else 0
    score += 1 if d["MACD_hist"] > p["MACD_hist"] else 0
    score += 1 if volume_repli is not None and volume_repli < 0.9 else 0
    score += 1 if plus_bas_monte else 0
    score += 1 if not np.isnan(rs3) and rs3 > 0 else 0
    score = min(score + (1 if tendance_ok else 0), 10)

    prix_ok = PRIX_MIN <= d["Close"] <= PRIX_MAX
    volume_ok = d["Vol_moy20"] >= VOLUME_MIN
    recul_ok = RECUL_MIN <= recul <= RECUL_MAX
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
        "dist_ema20_atr": r((d["Close"] - d["EMA20"]) / atr),
        "dist_ema50_atr": r((d["Close"] - d["EMA50"]) / atr),
        "dist_ema200_atr": r((d["Close"] - d["EMA200"]) / atr),
        "ema50_monte": bool(ema50_monte),
        "ema200_monte": bool(ema200_monte),
        "tendance_ok": tendance_ok,
        "rsi": r(d["RSI"], 1),
        "rsi_veille": r(p["RSI"], 1),
        "macd_hist": r(d["MACD_hist"], 4),
        "macd_hist_veille": r(p["MACD_hist"], 4),
        "atr": r(atr, 4),
        "atr_pct": r(atr / d["Close"] * 100),
        "volume_moy20": r(d["Vol_moy20"], 0),
        "volume_ratio": r(d["Vol_ratio"]),
        "volume_repli": volume_repli,
        "support_contact": "+".join(contacts),
        "bougie_reprise": bougie,
        "plus_bas_monte": plus_bas_monte,
        "rs_1m": r(rs1, 1),
        "rs_3m": r(rs3, 1),
        "perf_1m": r(perf(df["Close"], 21), 1),
        "cout_2_actions": r(2 * d["Close"]),
        "r3_possible": bool(recul < -25 or not ema50_monte),
        "score_setup": int(score),
        "candidat": candidat,
        # complétés plus tard pour les candidats
        "prochains_resultats": None,
        "jours_avant_resultats": None,
        "derniers_resultats": None,
        "jours_depuis_resultats": None,
        "resultats_proches": None,
    }


# ------------------------------------------------------------------- données

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


def dates_resultats(ticker: str) -> tuple[date | None, date | None]:
    """(prochaine publication, dernière publication) via yfinance."""
    aujourd_hui = pd.Timestamp(date.today())
    prochaine = derniere = None
    try:
        ed = yf.Ticker(ticker).get_earnings_dates(limit=8)
        if ed is not None and not ed.empty:
            dates = pd.to_datetime(ed.index).tz_localize(None).normalize()
            futures = sorted(x for x in dates if x >= aujourd_hui)
            passees = sorted(x for x in dates if x < aujourd_hui)
            prochaine = futures[0].date() if futures else None
            derniere = passees[-1].date() if passees else None
    except Exception:
        pass
    if prochaine is None:
        try:
            cal = yf.Ticker(ticker).calendar
            liste = cal.get("Earnings Date") if isinstance(cal, dict) else None
            if liste:
                futures = sorted(x for x in liste if pd.Timestamp(x) >= aujourd_hui)
                prochaine = futures[0] if futures else None
        except Exception:
            pass
    return prochaine, derniere


def completer_resultats(lignes: list[dict]) -> int:
    """Ajoute les dates de résultats aux candidats. Renvoie le nombre trouvé."""
    aujourd_hui = date.today()
    trouves = 0
    for ligne in lignes:
        if not ligne["candidat"]:
            continue
        prochaine, derniere = dates_resultats(ligne["ticker"])
        if prochaine:
            jours = int(np.busday_count(aujourd_hui, prochaine))
            ligne["prochains_resultats"] = prochaine.isoformat()
            ligne["jours_avant_resultats"] = jours
            ligne["resultats_proches"] = jours < JOURS_RESULTATS_MIN
            trouves += 1
        if derniere:
            ligne["derniers_resultats"] = derniere.isoformat()
            ligne["jours_depuis_resultats"] = int(np.busday_count(derniere, aujourd_hui))
        time.sleep(0.3)
    return trouves


def sante_marche(lignes: list[dict], marche: dict[str, pd.DataFrame]) -> dict:
    """Largeur du S&P 500, VIX, indices et ETF sectoriels."""
    scan = pd.DataFrame(lignes)
    sp = scan[scan["indice"].str.contains("SP500", na=False)]
    if sp.empty:
        sp = scan
    largeur = {
        "nb_titres": int(len(sp)),
        "pct_au_dessus_ema20": r((sp["cloture"] > sp["ema20"]).mean() * 100, 1),
        "pct_au_dessus_ema50": r((sp["cloture"] > sp["ema50"]).mean() * 100, 1),
        "pct_au_dessus_ema200": r((sp["cloture"] > sp["ema200"]).mean() * 100, 1),
        "pct_proches_plus_haut_52s": r((sp["recul_pct"] >= -2).mean() * 100, 1),
        "pct_recul_plus_20": r((sp["recul_pct"] <= -20).mean() * 100, 1),
        "pct_hausse_du_jour": r((sp["var_jour_pct"] > 0).mean() * 100, 1),
    }
    ref = marche.get(REFERENCE)
    indices = []
    for t, nom in MARCHE.items():
        df = marche.get(t)
        if df is None or len(df) < 210:
            continue
        df = indicateurs(df)
        d = df.iloc[-1]
        c = df["Close"]
        ligne = {
            "ticker": t, "nom": nom,
            "cloture": r(d["Close"]),
            "var_jour_pct": r((d["Close"] / df["Close"].iloc[-2] - 1) * 100),
            "perf_1s": r(perf(c, 5), 1), "perf_1m": r(perf(c, 21), 1),
            "perf_3m": r(perf(c, 63), 1),
            "recul_pct": r((d["Close"] / df["High"].iloc[-252:].max() - 1) * 100, 1),
            "au_dessus_ema20": bool(d["Close"] > d["EMA20"]),
            "au_dessus_ema50": bool(d["Close"] > d["EMA50"]),
            "au_dessus_ema200": bool(d["Close"] > d["EMA200"]),
            "ema20": r(d["EMA20"]), "ema50": r(d["EMA50"]), "ema200": r(d["EMA200"]),
            "rsi": r(d["RSI"], 1),
        }
        if ref is not None and t != REFERENCE and t != "^VIX":
            ref_al = ref["Close"].reindex(c.index).ffill()
            ligne["rs_1m_vs_spy"] = r(perf(c, 21) - perf(ref_al, 21), 1)
            ligne["rs_3m_vs_spy"] = r(perf(c, 63) - perf(ref_al, 63), 1)
        indices.append(ligne)
    return {"largeur_sp500": largeur, "indices_et_secteurs": indices}


# ---------------------------------------------------------------------- main

def main():
    parser = argparse.ArgumentParser(description="Scan large S&P 500 + Nasdaq 100")
    parser.add_argument("--sortie", default="data", help="dossier de sortie")
    parser.add_argument("--limite", type=int, default=0,
                        help="nombre max de titres (test rapide)")
    parser.add_argument("--sans-resultats", action="store_true",
                        help="ne pas récupérer les dates de résultats")
    args = parser.parse_args()
    sortie = Path(args.sortie)

    debut = datetime.now(FUSEAU)
    univers = lire_univers(sortie)
    if args.limite:
        univers = univers.head(args.limite)
    infos = univers.set_index("ticker").to_dict(orient="index")
    tickers = list(infos)
    print(f"Scan large de {len(tickers)} titres — {debut:%d/%m/%Y %H:%M} (Paris)")

    # Indices, VIX et ETF sectoriels d'abord (référence pour la force relative)
    try:
        marche = telecharger_lot(list(MARCHE))
    except Exception as e:
        print(f"  ! Indices et secteurs indisponibles ({e})")
        marche = {}
    ref = marche[REFERENCE]["Close"] if REFERENCE in marche else None

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
                ligne = resumer(t, infos[t], df, ref)
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

    nb_resultats = 0
    if not args.sans_resultats:
        print("Dates de résultats des candidats…")
        nb_resultats = completer_resultats(lignes)

    sortie.mkdir(parents=True, exist_ok=True)
    scan = pd.DataFrame(lignes).sort_values(
        ["candidat", "score_setup", "recul_pct"], ascending=[False, False, True])
    scan.to_csv(sortie / "scan.csv", index=False)

    blocs = []
    for t, df in historiques.items():
        h = df.iloc[-SEANCES_HISTORIQUE:].copy()
        h.insert(0, "Ticker", t)
        h.index.name = "Date"
        blocs.append(h.round(4))
    if blocs:
        pd.concat(blocs).to_csv(sortie / "scan_historique.csv")

    marche_json = sante_marche(lignes, marche)
    marche_json["genere_le"] = datetime.now(FUSEAU).isoformat(timespec="seconds")
    (sortie / "marche.json").write_text(
        json.dumps(marche_json, ensure_ascii=False, indent=1), encoding="utf-8")

    candidats = scan[scan["candidat"]]
    statut = {
        "genere_le": datetime.now(FUSEAU).isoformat(timespec="seconds"),
        "derniere_seance": scan["date_seance"].max(),
        "nb_univers": len(tickers),
        "nb_ok": len(lignes),
        "nb_candidats": int(len(candidats)),
        "nb_candidats_resultats_connus": nb_resultats,
        "nb_candidats_resultats_proches": int((candidats["resultats_proches"] == True).sum()),  # noqa: E712
        "echecs": echecs,
        "filtres": {"prix": [PRIX_MIN, PRIX_MAX], "volume_min": VOLUME_MIN,
                    "recul_pct": [RECUL_MIN, RECUL_MAX],
                    "jours_resultats_min": JOURS_RESULTATS_MIN},
    }
    (sortie / "scan_statut.json").write_text(
        json.dumps(statut, ensure_ascii=False, indent=1), encoding="utf-8")

    l = marche_json["largeur_sp500"]
    print(f"\nLargeur S&P 500 : {l['pct_au_dessus_ema50']} % au-dessus de l'EMA50, "
          f"{l['pct_au_dessus_ema200']} % au-dessus de l'EMA200")
    vue = candidats[["ticker", "secteur", "cloture", "recul_pct", "score_setup",
                     "support_contact", "bougie_reprise", "rs_3m",
                     "jours_avant_resultats"]]
    print(f"{len(candidats)} candidats sur {len(lignes)} titres analysés")
    print(vue.head(30).to_string(index=False))
    if echecs:
        print(f"Échecs ({len(echecs)}) : {', '.join(echecs[:30])}")


if __name__ == "__main__":
    main()
