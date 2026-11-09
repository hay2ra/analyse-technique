"""
Backtest des règles swing v3 (setups R1, R2, R3) sur le S&P 500 + Nasdaq 100.

Usage :
    python backtest.py --sortie data/backtest [--annees 5] [--sans-resultats]

Principe
- Chaque séance t, les conditions d'un setup sont évaluées avec les seules
  données connues à la clôture de t (aucun regard vers le futur).
- Ordre stop d'achat juste au-dessus du plus haut de t (R1, R2) ou du haut de
  base (R3), valable 3 séances, annulé si l'ouverture dépasse le prix maximum
  ou si le cours passe sous le stop avant l'exécution.
- Stop sous le dernier plus bas ou sous la base, entre 1 et 2 ATR (au-delà de
  2 ATR : pas de trade). Taille : 30 $ de risque (15 $ en R3), plafond 500 $,
  au moins 2 actions.
- Sorties testées (mêmes entrées) :
    V1 « plan v3 »  : moitié à T1 = 1,5R, stop au prix d'entrée, puis stop
                      suiveur sous le plus bas de la veille ; reste à T2 = 2,5R.
    V2 « EMA10 »    : idem, mais après T1 sortie à la clôture sous l'EMA10.
    V3 « tout à 2R » : tout vendu à 2R, sans vente partielle.
  Pour les trois : stop temps à 10 séances si le titre n'a pas fait +0,5R,
  durée max 20 séances, sortie la veille des résultats.
- Hypothèses prudentes : si le stop et l'objectif sont touchés la même séance,
  on compte le stop ; un gap sous le stop sort à l'ouverture.
- Règles v3.1 (famille « plan31 ») : R2 sans condition de tendance, R1 à
  15 % de recul au moins, R3 seulement si SPY ou QQQ sous l'EMA50, REIT exclus.
- Témoins (pour savoir si les setups apportent quelque chose) :
    « R2 large » : R2 sans les conditions de tendance ni d'EMA50 montante.
    « Zone »     : achat à l'ouverture dès qu'un titre est dans la zone de
                   chasse (recul 10-25 %, tendance intacte), sans setup, stop à
                   1,5 ATR, sorties V1.
- Simulation du compte de 2 000 $ (V1, setups R1 à R3) : risque ouvert max
  120 $ (60 $ si SPY ou QQQ sous l'EMA50), 2 lignes max par secteur, cash.

Limites : univers actuel des indices (biais du survivant, favorable), pas de
filtre fondamental (cause de la baisse), pas de frais (XTB 0 % sur actions US
jusqu'à 100 000 €/mois), dates de résultats yfinance parfois incomplètes.

Sorties : trades.csv, portefeuille.csv, resume.json, rapport.md
"""

import argparse
import json
import math
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

import scan_large as sl

# =============================================================================
# PARAMÈTRES
# =============================================================================

PERIODE = "6y"              # 1 an de préchauffage (plus haut 52 s, EMA200)
ANNEES_TEST = 5             # fenêtre de test (les 2 dernières années à part)
ANNEES_RECENT = 2

CAPITAL = 2000.0
RISQUE, RISQUE_R3 = 30.0, 15.0
PLAFOND_LIGNE = 500.0
PLAFOND_RISQUE, PLAFOND_RISQUE_CORRECTION = 120.0, 60.0
MAX_PAR_SECTEUR = 2

PRIX_MIN = 5.0
VOLUME_MIN = 500_000
CONTACT_ATR = 0.5

VALIDITE_ORDRE = 3          # séances
MARGE_ENTREE = 0.02         # $ au-dessus du plus haut
MAX_ENTREE_R = 0.3          # prix max = déclencheur + 0,3R (on ne court pas)
STOP_MIN_ATR, STOP_MAX_ATR = 1.0, 2.0
STOP_TEMOIN_ATR = 1.5

T1_R, T2_R, TOUT_R = 1.5, 2.5, 2.0
STOP_TEMPS, PROGRES_MIN_R = 10, 0.5
DUREE_MAX = 20
JOURS_RESULTATS_MIN = 7

VARIANTES = ("V1", "V2", "V3")
NOMS_VARIANTES = {"V1": "plan v3 (moitié à 1,5R, suiveur plus bas veille, 2,5R)",
                  "V2": "moitié à 1,5R puis clôture sous EMA10",
                  "V3": "tout à 2R"}

# =============================================================================


# ------------------------------------------------------------------- données

def telecharger(tickers: list[str]) -> dict[str, pd.DataFrame]:
    sl.PERIODE = PERIODE
    donnees = {}
    for i in range(0, len(tickers), sl.TAILLE_LOT):
        lot = tickers[i:i + sl.TAILLE_LOT]
        print(f"→ lot {i // sl.TAILLE_LOT + 1} ({len(lot)} titres)", flush=True)
        try:
            donnees.update(sl.telecharger_lot(lot))
        except Exception as e:
            print(f"  ! lot ignoré : {e}")
        time.sleep(sl.PAUSE_LOT)
    return donnees


def dates_resultats(tickers: list[str], cache: Path) -> dict[str, list[pd.Timestamp]]:
    """Dates de publication passées et futures, avec cache CSV."""
    connues = {}
    if cache.exists():
        c = pd.read_csv(cache, parse_dates=["date"])
        for t, g in c.groupby("ticker"):
            connues[t] = sorted(g["date"].tolist())
    manquants = [t for t in tickers if t not in connues]
    print(f"Dates de résultats : {len(connues)} en cache, {len(manquants)} à chercher", flush=True)
    lignes = []
    for k, t in enumerate(manquants, 1):
        try:
            ed = yf.Ticker(t).get_earnings_dates(limit=28)
            if ed is not None and not ed.empty:
                d = sorted(set(pd.to_datetime(ed.index).tz_localize(None).normalize()))
                connues[t] = d
                lignes += [{"ticker": t, "date": x} for x in d]
        except Exception:
            pass
        if k % 50 == 0:
            print(f"  {k}/{len(manquants)}", flush=True)
        time.sleep(0.3)
    if lignes:
        anciens = pd.read_csv(cache) if cache.exists() else pd.DataFrame()
        pd.concat([anciens, pd.DataFrame(lignes)]).to_csv(cache, index=False)
    return connues


# -------------------------------------------------------------- indicateurs

def preparer(df: pd.DataFrame, ref: pd.DataFrame,
             correction: pd.Series | None = None) -> pd.DataFrame:
    """Indicateurs et signaux, chaque valeur ne dépend que du passé."""
    df = sl.indicateurs(df.copy())
    df["EMA10"] = sl.ema(df["Close"], 10)
    o, h, l, c, v = (df[k] for k in ("Open", "High", "Low", "Close", "Volume"))
    atr = df["ATR"]

    haut52 = h.rolling(252, min_periods=252).max()
    df["recul"] = c / haut52 - 1
    ema50_monte = df["EMA50"] > df["EMA50"].shift(10)
    ema200_monte = df["EMA200"] > df["EMA200"].shift(10)
    tendance = (df["EMA50"] > df["EMA200"]) | ((c > df["EMA200"]) & ema200_monte)
    liquide = (c >= PRIX_MIN) & (df["Vol_moy20"] >= VOLUME_MIN)

    def contact(n):
        e = df[f"EMA{n}"]
        ecart = ((l - e).abs() / atr).rolling(3).min()
        return (ecart <= CONTACT_ATR) & (c >= e - 0.25 * atr)

    c20, c50, c200 = contact(20), contact(50), contact(200)

    amp = h - l
    po, pc = o.shift(), c.shift()
    marteau = (amp > 0) & ((np.minimum(o, c) - l) >= 0.5 * amp) & (c >= l + 0.6 * amp)
    avalement = (pc < po) & (c > o) & (c >= po) & (o <= pc)
    cloture_haute = (amp > 0) & (pc < po) & (c > pc) & (c >= l + 0.67 * amp)
    bougie = marteau | avalement | cloture_haute

    rouge = (c < o).astype(float)
    nb_rouge = rouge.rolling(5).sum().replace(0, np.nan)
    volume_repli = (df["Vol_ratio"].fillna(0) * rouge).rolling(5).sum() / nb_rouge
    plus_bas_monte = l.rolling(10).min() > l.shift(10).rolling(10).min()
    rsi = df["RSI"]
    rsi_monte = rsi > rsi.shift()
    macd_monte = df["MACD_hist"] > df["MACD_hist"].shift()

    ref_c = ref["Close"].reindex(df.index).ffill()
    rs3 = (c / c.shift(63) - ref_c / ref_c.shift(63)) * 100

    score = (2 * (c20 | c50 | c200) + 2 * bougie + (rsi_monte & (rsi < 50))
             + rsi.between(30, 50) + macd_monte + (volume_repli < 0.9)
             + plus_bas_monte + (rs3 > 0) + tendance).clip(upper=10)
    df["score"] = score.astype(int)
    df["rs3"] = rs3

    recul = df["recul"]
    zone = liquide & recul.between(-0.25, -0.10) & tendance & ema50_monte

    # R1 : repli en tendance sur l'EMA20 ou l'EMA50, volume en baisse, reprise
    r1 = zone & (c20 | c50) & bougie & (volume_repli < 1.0)
    stop_r1 = l.rolling(3).min() - 0.1 * atr

    # R2 : test d'un support majeur, RSI passé sous 35 et qui remonte, reprise
    ancien_bas = l.shift(10).rolling(110, min_periods=60).min()
    test_bas = ((l.rolling(3).min() - ancien_bas).abs() / atr) <= 0.75
    support_majeur = c200 | test_bas
    rsi_survendu = (rsi.rolling(5).min() < 35) & rsi_monte
    r2_coeur = rsi_survendu & bougie & support_majeur
    r2 = zone & r2_coeur
    stop_r2 = l.rolling(5).min() - 0.1 * atr
    r2_large = liquide & recul.between(-0.25, -0.10) & r2_coeur

    # R3 : base d'au moins 5 séances après une chute, volume qui s'assèche
    zone3 = liquide & ((recul < -0.25) | ~ema50_monte) & recul.between(-0.50, -0.10)
    haut_base = pd.Series(np.nan, index=df.index)
    bas_base = pd.Series(np.nan, index=df.index)
    for k in range(15, 4, -1):          # la base la plus longue d'abord
        hk, lk = h.rolling(k).max(), l.rolling(k).min()
        ok = (((hk - lk) <= 1.8 * atr)
              & (v.rolling(k).mean() < 0.85 * v.shift(k).rolling(20).mean())
              & (h.shift(k).rolling(20).max() >= hk * 1.10)
              & (c <= hk))
        libre = ok & haut_base.isna()
        haut_base[libre], bas_base[libre] = hk[libre], lk[libre]
    r3 = zone3 & haut_base.notna()

    df["setup"] = ""
    df.loc[r1, "setup"] = "R1"
    df.loc[r2, "setup"] = "R2"
    df.loc[r3 & (df["setup"] == ""), "setup"] = "R3"
    df["declencheur"] = np.where(df["setup"] == "R3", haut_base, h) + MARGE_ENTREE
    df["stop_plan"] = np.select([df["setup"] == "R1", df["setup"] == "R2",
                                 df["setup"] == "R3"],
                                [stop_r1, stop_r2, bas_base - 0.1 * atr], np.nan)
    # Règles v3.1 : R2 sans condition de tendance, R1 à 15 % de recul au moins,
    # R3 seulement quand SPY ou QQQ est sous son EMA50
    corr = (correction.reindex(df.index).ffill().fillna(False).astype(bool)
            if correction is not None else pd.Series(True, index=df.index))
    df["setup31"] = ""
    df.loc[r3 & corr, "setup31"] = "R3"
    df.loc[r1 & (recul <= -0.15), "setup31"] = "R1"
    df.loc[r2_large, "setup31"] = "R2"
    df["declencheur31"] = np.where(df["setup31"] == "R3", haut_base, h) + MARGE_ENTREE
    df["stop31"] = np.select([df["setup31"] == "R1", df["setup31"] == "R2",
                              df["setup31"] == "R3"],
                             [stop_r1, stop_r2, bas_base - 0.1 * atr], np.nan)
    df["r2_large"] = r2_large
    df["stop_r2_large"] = stop_r2
    df["zone"] = zone
    return df


# --------------------------------------------------------------- simulation

def sortir(a: dict, j: int, entree: float, stop0: float, n_act: int,
           variante: str, i_resultats: int | None) -> dict:
    """Déroule une position ouverte à la séance j. Renvoie le résultat."""
    O, H, L, C, E10 = a["O"], a["H"], a["L"], a["C"], a["E10"]
    n = len(C)
    R = entree - stop0
    t1, t2 = entree + T1_R * R, entree + T2_R * R
    cible_unique = entree + TOUT_R * R
    stop, reste, pnl = stop0, n_act, 0.0
    t1_touche, i_t1, n_t1 = False, None, 0
    raison, k = "durée max", j

    for k in range(j, min(n, j + DUREE_MAX)):
        jour = k - j + 1
        o = O[k] if k > j else entree
        # 1. stop (prioritaire en cas de doute)
        if k > j and O[k] <= stop:
            pnl += reste * (O[k] - entree)
            raison = "stop (gap)" if not t1_touche else "suiveur/BE"
            reste = 0
            break
        if L[k] <= stop:
            pnl += reste * (stop - entree)
            raison = "stop" if not t1_touche else "suiveur/BE"
            reste = 0
            break
        # 2. objectifs
        if variante == "V3":
            if H[k] >= cible_unique:
                pnl += reste * (max(cible_unique, o) - entree)
                raison, reste = "objectif 2R", 0
                break
        else:
            if not t1_touche and H[k] >= t1:
                prix = max(t1, o)
                vendre = n_act // 2 if n_act >= 2 else n_act
                pnl += vendre * (prix - entree)
                reste -= vendre
                t1_touche, i_t1, n_t1 = True, k, vendre
                stop = max(stop, entree)
                if reste == 0:
                    raison = "T1"
                    break
            if t1_touche and H[k] >= t2:
                pnl += reste * (max(t2, o) - entree)
                raison, reste = "T2", 0
                break
        # 3. fin de séance
        if i_resultats is not None and k >= i_resultats:
            pnl += reste * (C[k] - entree)
            raison, reste = "veille résultats", 0
            break
        if variante == "V2" and t1_touche and C[k] < E10[k]:
            pnl += reste * (C[k] - entree)
            raison, reste = "clôture < EMA10", 0
            break
        if not t1_touche and jour >= STOP_TEMPS and C[k] < entree + PROGRES_MIN_R * R:
            pnl += reste * (C[k] - entree)
            raison, reste = "stop temps", 0
            break
        if jour >= DUREE_MAX:
            pnl += reste * (C[k] - entree)
            raison, reste = "durée max", 0
            break
        # 4. stop suiveur pour la séance suivante
        if variante == "V1" and t1_touche:
            stop = max(stop, L[k] - 0.01)
    else:
        if reste:                       # fin des données : position encore ouverte
            pnl += reste * (C[k] - entree)
            raison = "ouverte (fin des données)"

    risque = n_act * R
    return {"sortie_idx": k, "pnl": pnl, "R": pnl / risque if risque > 0 else 0.0,
            "raison": raison, "duree": k - j + 1, "t1_idx": i_t1, "n_t1": n_t1,
            "prix_t1": t1}


def simuler(ticker: str, df: pd.DataFrame, famille: str, debut: int,
            resultats: list[pd.Timestamp] | None) -> tuple[list[dict], dict]:
    """Trades d'un titre pour une famille de signaux (une position à la fois)."""
    a = {"O": df["Open"].to_numpy(), "H": df["High"].to_numpy(),
         "L": df["Low"].to_numpy(), "C": df["Close"].to_numpy(),
         "E10": df["EMA10"].to_numpy()}
    atr = df["ATR"].to_numpy()
    dates = df.index
    if famille == "plan":
        signal = (df["setup"] != "").to_numpy()
        declencheur = df["declencheur"].to_numpy()
        stops = df["stop_plan"].to_numpy()
        setups = df["setup"].to_numpy()
    elif famille == "plan31":
        signal = (df["setup31"] != "").to_numpy()
        declencheur = df["declencheur31"].to_numpy()
        stops = df["stop31"].to_numpy()
        setups = df["setup31"].to_numpy()
    elif famille == "r2_large":
        signal = df["r2_large"].to_numpy()
        declencheur = (df["High"] + MARGE_ENTREE).to_numpy()
        stops = df["stop_r2_large"].to_numpy()
        setups = np.full(len(df), "R2 large", dtype=object)
    else:                               # témoin « zone »
        signal = df["zone"].to_numpy()
        declencheur = stops = None
        setups = np.full(len(df), "Zone", dtype=object)

    i_res = None
    if resultats:
        i_res = np.searchsorted(dates.values, np.array(resultats, dtype="datetime64[ns]"))

    compte = {"signaux": 0, "risque_trop_large": 0, "trop_cher": 0, "resultats": 0,
              "non_execute": 0, "execute": 0}
    trades = []
    n = len(df)
    i = debut
    while i < n - 1:
        if not signal[i] or np.isnan(atr[i]):
            i += 1
            continue
        compte["signaux"] += 1
        setup = setups[i]

        # Résultats : prochaine publication et séance de sortie
        i_sortie_res = None
        if i_res is not None:
            futurs = i_res[i_res > i]
            if len(futurs):
                if futurs[0] - i <= JOURS_RESULTATS_MIN:
                    compte["resultats"] += 1
                    i += 1
                    continue
                i_sortie_res = int(futurs[0]) - 1

        # Ordre
        if famille == "zone":
            j, entree = i + 1, a["O"][i + 1]
            stop0 = entree - STOP_TEMOIN_ATR * atr[i]
            budget = RISQUE
            n_act = min(math.floor(budget / (entree - stop0)), math.floor(PLAFOND_LIGNE / entree))
            if n_act < 2:
                compte["trop_cher"] += 1
                i += 1
                continue
        else:
            trig, stop0 = declencheur[i], stops[i]
            risque = trig - stop0
            if risque < STOP_MIN_ATR * atr[i]:
                stop0 = trig - STOP_MIN_ATR * atr[i]
                risque = trig - stop0
            if risque > STOP_MAX_ATR * atr[i]:
                compte["risque_trop_large"] += 1
                i += 1
                continue
            budget = RISQUE_R3 if setup == "R3" else RISQUE
            n_act = min(math.floor(budget / risque), math.floor(PLAFOND_LIGNE / trig))
            if n_act < 2:
                compte["trop_cher"] += 1
                i += 1
                continue
            prix_max = trig + MAX_ENTREE_R * risque
            j, entree = None, None
            for jj in range(i + 1, min(n, i + 1 + VALIDITE_ORDRE)):
                if a["O"][jj] > prix_max:
                    break                           # gap trop haut : annulé
                if a["O"][jj] >= trig:
                    j, entree = jj, a["O"][jj]
                    break
                if a["L"][jj] <= stop0:
                    break                           # invalidé avant exécution
                if a["H"][jj] >= trig:
                    j, entree = jj, trig
                    break
            if j is None:
                compte["non_execute"] += 1
                i += VALIDITE_ORDRE                 # l'ordre a couru ses 3 séances
                continue

        compte["execute"] += 1
        res = {v: sortir(a, j, entree, stop0, n_act, v, i_sortie_res) for v in VARIANTES}
        v1 = res["V1"]
        trade = {
            "ticker": ticker, "famille": famille, "setup": setup,
            "date_signal": dates[i].date(), "date_entree": dates[j].date(),
            "date_sortie": dates[v1["sortie_idx"]].date(),
            "date_t1": dates[v1["t1_idx"]].date() if v1["t1_idx"] is not None else None,
            "entree": round(entree, 2), "stop": round(stop0, 2), "actions": n_act,
            "investi": round(entree * n_act, 2), "risque_usd": round((entree - stop0) * n_act, 2),
            "n_t1": v1["n_t1"], "prix_t1": round(v1["prix_t1"], 2),
            "recul_pct": round(df["recul"].iloc[i] * 100, 1),
            "score": int(df["score"].iloc[i]), "rs3": round(df["rs3"].iloc[i], 1)
            if not np.isnan(df["rs3"].iloc[i]) else None,
            "resultats_connus": resultats is not None,
        }
        for v in VARIANTES:
            trade[f"pnl_{v}"] = round(res[v]["pnl"], 2)
            trade[f"R_{v}"] = round(res[v]["R"], 3)
            trade[f"raison_{v}"] = res[v]["raison"]
            trade[f"duree_{v}"] = res[v]["duree"]
        trades.append(trade)
        i = v1["sortie_idx"] + 1              # une position à la fois par titre
    return trades, compte


# ---------------------------------------------------------------- statistiques

def stats(t: pd.DataFrame, v: str = "V1") -> dict:
    if t.empty:
        return {"trades": 0}
    R, pnl = t[f"R_{v}"], t[f"pnl_{v}"]
    gains, pertes = pnl[pnl > 0].sum(), -pnl[pnl < 0].sum()
    serie = pire = 0
    for x in R:
        serie = serie + 1 if x <= 0 else 0
        pire = max(pire, serie)
    return {
        "trades": int(len(t)),
        "gagnants_pct": round((R > 0).mean() * 100, 1),
        "R_moyen": round(R.mean(), 3),
        "R_median": round(R.median(), 3),
        "R_moyen_gain": round(R[R > 0].mean(), 2) if (R > 0).any() else None,
        "R_moyen_perte": round(R[R <= 0].mean(), 2) if (R <= 0).any() else None,
        "profit_factor": round(gains / pertes, 2) if pertes > 0 else None,
        "pnl_total_usd": round(pnl.sum(), 0),
        "pnl_moyen_usd": round(pnl.mean(), 2),
        "duree_moy": round(t[f"duree_{v}"].mean(), 1),
        "pire_serie_pertes": pire,
    }


def tableau(lignes: list[tuple[str, dict]], titre_col: str) -> str:
    cols = [("trades", "Trades"), ("gagnants_pct", "% gagnants"), ("R_moyen", "R moyen"),
            ("R_median", "R médian"), ("profit_factor", "Profit factor"),
            ("pnl_moyen_usd", "$ moyen"), ("duree_moy", "Durée moy."),
            ("pire_serie_pertes", "Pire série")]
    md = f"| {titre_col} | " + " | ".join(c[1] for c in cols) + " |\n"
    md += "|" + "---|" * (len(cols) + 1) + "\n"
    for nom, s in lignes:
        md += f"| {nom} | " + " | ".join(
            "—" if s.get(k) is None else str(s.get(k)) for k, _ in cols) + " |\n"
    return md


# ----------------------------------------------------------------- portefeuille

def portefeuille(trades: pd.DataFrame, donnees: dict, regime: pd.Series,
                 secteurs: dict, debut: pd.Timestamp,
                 famille: str = "plan") -> tuple[pd.DataFrame, dict]:
    """Compte de 2 000 $ avec plafonds de risque, de secteur et de cash (V1)."""
    t = trades[(trades["famille"] == famille)].copy()
    t["date_entree"] = pd.to_datetime(t["date_entree"])
    t["date_sortie"] = pd.to_datetime(t["date_sortie"])
    t["date_t1"] = pd.to_datetime(t["date_t1"])
    t["secteur"] = t["ticker"].map(secteurs).fillna("?")
    jours = regime.index[regime.index >= debut]
    par_jour = {d: g.sort_values(["score", "rs3"], ascending=False)
                for d, g in t.groupby("date_entree")}

    realise, ouvertes, journal, refus = 0.0, [], [], {"risque": 0, "secteur": 0, "cash": 0}
    pic, dd_max = CAPITAL, 0.0
    retenus = 0
    for d in jours:
        # sorties du jour (les positions sorties libèrent risque et cash)
        restantes = []
        for p in ouvertes:
            if p["date_sortie"] <= d:
                realise += p["pnl_V1"]
            else:
                restantes.append(p)
        ouvertes = restantes

        def risque_ouvert():
            return sum(0 if (pd.notna(p["date_t1"]) and p["date_t1"] < d) else p["risque_usd"]
                       for p in ouvertes)

        def investi():
            return sum(p["investi"] for p in ouvertes)

        plafond = PLAFOND_RISQUE_CORRECTION if regime.get(d, False) else PLAFOND_RISQUE
        for _, p in par_jour.get(d, pd.DataFrame()).iterrows():
            if risque_ouvert() + p["risque_usd"] > plafond:
                refus["risque"] += 1
                continue
            if sum(q["secteur"] == p["secteur"] for q in ouvertes) >= MAX_PAR_SECTEUR:
                refus["secteur"] += 1
                continue
            if investi() + p["investi"] > CAPITAL + realise:
                refus["cash"] += 1
                continue
            ouvertes.append(p.to_dict())
            retenus += 1

        # valeur du compte en fin de séance
        latent = 0.0
        for p in ouvertes:
            c = donnees[p["ticker"]]["Close"].get(d, np.nan)
            if np.isnan(c):
                continue
            vendu = p["n_t1"] if (pd.notna(p["date_t1"]) and p["date_t1"] <= d) else 0
            latent += vendu * (p["prix_t1"] - p["entree"]) + (p["actions"] - vendu) * (c - p["entree"])
        valeur = CAPITAL + realise + latent
        pic = max(pic, valeur)
        dd_max = min(dd_max, valeur / pic - 1)
        journal.append({"date": d.date(), "valeur": round(valeur, 2),
                        "positions": len(ouvertes), "risque_ouvert": round(risque_ouvert(), 2)})

    j = pd.DataFrame(journal)
    resume = {
        "trades_retenus": retenus,
        "refus": refus,
        "valeur_finale": float(j["valeur"].iloc[-1]) if len(j) else CAPITAL,
        "perf_pct": round((j["valeur"].iloc[-1] / CAPITAL - 1) * 100, 1) if len(j) else 0,
        "drawdown_max_pct": round(dd_max * 100, 1),
        "positions_moy": round(j["positions"].mean(), 2) if len(j) else 0,
    }
    return j, resume


# ------------------------------------------------------------------------ main

def main():
    global ANNEES_TEST
    ap = argparse.ArgumentParser()
    ap.add_argument("--sortie", default="data/backtest")
    ap.add_argument("--annees", type=int, default=ANNEES_TEST)
    ap.add_argument("--sans-resultats", action="store_true")
    args = ap.parse_args()
    ANNEES_TEST = args.annees
    sortie = Path(args.sortie)
    sortie.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    univers = sl.lire_univers(Path("data"))
    secteurs = dict(zip(univers["ticker"], univers["secteur"]))
    tickers = univers["ticker"].tolist()
    print(f"Backtest sur {len(tickers)} titres, {ANNEES_TEST} ans de test", flush=True)

    marche = telecharger(["SPY", "QQQ"])
    spy, qqq = marche["SPY"], marche["QQQ"]
    regime = ((spy["Close"] < sl.ema(spy["Close"], 50))
              | (qqq["Close"].reindex(spy.index).ffill()
                 < sl.ema(qqq["Close"], 50).reindex(spy.index).ffill()))
    donnees = telecharger(tickers)
    print(f"{len(donnees)} titres téléchargés", flush=True)

    resultats = {}
    if not args.sans_resultats:
        resultats = dates_resultats(list(donnees), sortie / "dates_resultats.csv")
    fin = spy.index[-1]
    debut = fin - pd.DateOffset(years=ANNEES_TEST)
    debut_recent = fin - pd.DateOffset(years=ANNEES_RECENT)

    tous, comptes = [], {}
    for k, (t, df) in enumerate(donnees.items(), 1):
        try:
            p = preparer(df, spy, regime)
        except Exception as e:
            print(f"  ! {t} : {e}")
            continue
        donnees[t] = p
        i0 = int(np.searchsorted(p.index.values, np.datetime64(debut)))
        i0 = max(i0, 252)
        reit = str(secteurs.get(t, "")).strip().lower() == "real estate"
        for famille in ("plan", "plan31", "r2_large", "zone"):
            if famille == "plan31" and reit:
                continue
            tr, cpt = simuler(t, p, famille, i0, resultats.get(t))
            for tt in tr:
                tt["correction"] = bool(regime.get(pd.Timestamp(tt["date_signal"]), False))
            tous += tr
            for kk, vv in cpt.items():
                comptes.setdefault(famille, {}).setdefault(kk, 0)
                comptes[famille][kk] += vv
        if k % 100 == 0:
            print(f"  {k}/{len(donnees)} titres simulés", flush=True)

    trades = pd.DataFrame(tous)
    trades.to_csv(sortie / "trades.csv", index=False)
    if trades.empty:
        print("Aucun trade.")
        return
    trades["annee"] = pd.to_datetime(trades["date_entree"]).dt.year
    recent = pd.to_datetime(trades["date_entree"]) >= debut_recent
    plan = trades["famille"] == "plan"

    # ---- tableaux
    md = [f"# Backtest des règles swing v3\n",
          f"Généré le {datetime.now(sl.FUSEAU):%d/%m/%Y %H:%M} — {len(donnees)} titres "
          f"(S&P 500 + Nasdaq 100 actuels), signaux du {debut.date()} au {fin.date()}.\n",
          f"Dates de résultats connues pour {len(resultats)} titres sur {len(donnees)}.\n"]
    resume = {"genere_le": datetime.now(sl.FUSEAU).isoformat(timespec="seconds"),
              "periode": [str(debut.date()), str(fin.date())], "nb_titres": len(donnees),
              "nb_titres_dates_resultats": len(resultats), "comptes_signaux": comptes,
              "parametres": {"T1_R": T1_R, "T2_R": T2_R, "TOUT_R": TOUT_R,
                             "stop_temps": STOP_TEMPS, "duree_max": DUREE_MAX,
                             "validite_ordre": VALIDITE_ORDRE}}

    p31 = trades["famille"] == "plan31"
    groupes = [("R1", plan & (trades["setup"] == "R1")),
               ("R2", plan & (trades["setup"] == "R2")),
               ("R3 (demi-taille)", plan & (trades["setup"] == "R3")),
               ("**R1+R2+R3 (v3)**", plan),
               ("v3.1 R1 (recul ≥ 15 %)", p31 & (trades["setup"] == "R1")),
               ("v3.1 R2 (sans tendance)", p31 & (trades["setup"] == "R2")),
               ("v3.1 R3 (en correction)", p31 & (trades["setup"] == "R3")),
               ("**v3.1 total (sans REIT)**", p31),
               ("Témoin R2 large", trades["famille"] == "r2_large"),
               ("Témoin Zone sans setup", trades["famille"] == "zone")]
    resume["par_setup"] = {}
    for v in VARIANTES:
        md.append(f"\n## Résultats par setup — {v} : {NOMS_VARIANTES[v]}\n")
        md.append(f"\n### Sur {ANNEES_TEST} ans\n")
        md.append(tableau([(n, stats(trades[m], v)) for n, m in groupes], "Setup"))
        md.append(f"\n### Sur les {ANNEES_RECENT} dernières années\n")
        md.append(tableau([(n, stats(trades[m & recent], v)) for n, m in groupes], "Setup"))
        resume["par_setup"][v] = {n: {"tout": stats(trades[m], v), "recent": stats(trades[m & recent], v)}
                                  for n, m in groupes}

    tp = trades[plan]
    md.append("\n## Plan R1+R2+R3 (V1) par année\n")
    md.append(tableau([(str(a), stats(g)) for a, g in tp.groupby("annee")], "Année"))
    md.append("\n## Plan (V1) selon le marché au signal\n")
    md.append(tableau([("SPY et QQQ au-dessus de l'EMA50", stats(tp[~tp["correction"]])),
                       ("SPY ou QQQ sous l'EMA50", stats(tp[tp["correction"]]))], "Marché"))
    md.append("\n## Plan (V1) selon le score de setup du scan\n")
    tranches = pd.cut(tp["score"], [-1, 4, 6, 8, 10], labels=["0-4", "5-6", "7-8", "9-10"])
    md.append(tableau([(str(b), stats(g)) for b, g in tp.groupby(tranches, observed=True)], "Score"))
    md.append("\n## Plan (V1) selon le recul depuis le plus haut\n")
    tr_recul = pd.cut(tp["recul_pct"], [-51, -35, -25, -20, -15, -9], labels=[
        "-50 à -35 %", "-35 à -25 %", "-25 à -20 %", "-20 à -15 %", "-15 à -10 %"])
    md.append(tableau([(str(b), stats(g)) for b, g in tp.groupby(tr_recul, observed=True)], "Recul"))
    md.append("\n## Plan (V1) par secteur\n")
    tp = tp.assign(secteur=tp["ticker"].map(secteurs).fillna("?"))
    md.append(tableau([(s, stats(g)) for s, g in tp.groupby("secteur")], "Secteur"))
    md.append("\n## Raisons de sortie (plan, V1)\n")
    md.append("| Raison | Trades | R moyen |\n|---|---|---|\n")
    for r_, g in tp.groupby("raison_V1"):
        md.append(f"| {r_} | {len(g)} | {g['R_V1'].mean():.2f} |\n")

    md.append("\n## Entonnoir des signaux\n")
    md.append("| Famille | Signaux | Résultats trop proches | Stop > 2 ATR | < 2 actions | Ordre non exécuté | Trades |\n|---|---|---|---|---|---|---|\n")
    for f, c in comptes.items():
        md.append(f"| {f} | {c['signaux']} | {c['resultats']} | {c['risque_trop_large']} | "
                  f"{c['trop_cher']} | {c['non_execute']} | {c['execute']} |\n")

    # ---- portefeuille
    for fam, nom_p, deb_p in (("plan", f"{ANNEES_TEST} ans", debut),
                              ("plan", f"{ANNEES_RECENT} ans", debut_recent),
                              ("plan31", f"{ANNEES_TEST} ans v3.1", debut),
                              ("plan31", f"{ANNEES_RECENT} ans v3.1", debut_recent)):
        j, rp = portefeuille(trades[pd.to_datetime(trades["date_entree"]) >= deb_p],
                             donnees, regime, secteurs, deb_p, fam)
        spy_p = spy["Close"][spy.index >= deb_p]
        rp["spy_perf_pct"] = round((spy_p.iloc[-1] / spy_p.iloc[0] - 1) * 100, 1)
        spy_dd = (spy_p / spy_p.cummax() - 1).min()
        rp["spy_drawdown_max_pct"] = round(spy_dd * 100, 1)
        resume[f"portefeuille_{nom_p.replace(' ', '_')}"] = rp
        j.to_csv(sortie / f"portefeuille_{nom_p.replace(' ', '_')}.csv", index=False)
        md.append(f"\n## Compte de 2 000 $ simulé sur {nom_p} (sorties V1, plafonds de risque et de secteur)\n")
        md.append(f"- Valeur finale : **{rp['valeur_finale']:.0f} $** ({rp['perf_pct']:+.1f} %), "
                  f"drawdown max {rp['drawdown_max_pct']} %\n")
        md.append(f"- SPY sur la même période : {rp['spy_perf_pct']:+.1f} %, drawdown max {rp['spy_drawdown_max_pct']} %\n")
        md.append(f"- Trades retenus : {rp['trades_retenus']} ; refusés faute de budget de risque "
                  f"{rp['refus']['risque']}, de place dans le secteur {rp['refus']['secteur']}, "
                  f"de cash {rp['refus']['cash']} ; positions ouvertes en moyenne {rp['positions_moy']}\n")

    md.append("\n## Limites\n- Univers actuel des indices : biais du survivant, plutôt favorable.\n"
              "- Pas de filtre sur la cause de la baisse (fondamental) : en réel, une partie des pertes serait évitée, "
              "mais aussi quelques gains.\n- Pas de frais ni de glissement hors gaps.\n"
              "- Stop et objectif touchés la même séance : le stop est compté (prudent).\n")

    (sortie / "rapport.md").write_text("".join(md), encoding="utf-8")
    with open(sortie / "resume.json", "w", encoding="utf-8") as f:
        json.dump(resume, f, ensure_ascii=False, indent=1, default=str)
    print("".join(md))
    print(f"Terminé en {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
