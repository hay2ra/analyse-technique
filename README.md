# Analyse technique quotidienne

Chaque soir de semaine, GitHub Actions télécharge les cours (Yahoo Finance via
yfinance), calcule les indicateurs (pandas-ta) et enregistre les résultats dans
le dossier `data/`. Les tâches planifiées Claude lisent ces fichiers.

## Horaires (heure de Paris)
- Après la clôture européenne : vers 17h50
- Après la clôture américaine : vers 22h20

GitHub peut décaler un lancement de quelques minutes à une demi-heure.

## Fichiers produits (`data/`)
| Fichier | Contenu |
|---|---|
| `statut.json` | Heure d'exécution, tickers en échec, date de dernière séance par ticker, signaux d'achat |
| `synthese.csv` / `synthese.json` | Une ligne par ticker : cours, OHLC, volume vs moyenne 20 j, EMA 20/50/100/200, SMA 50/200, RSI, MACD (et valeurs de la veille), ATR, tendance, signal pullback |
| `historique.csv` | Les 260 dernières séances de chaque ticker avec tous les indicateurs |

## Modifier la liste des titres
Éditez `tickers.txt` directement sur GitHub (icône crayon), puis « Commit changes ».
Les sections `[PEA]`, `[WATCHLIST]`, `[CTO]`, `[INDICES]` servent à regrouper les titres.

## Lancer à la main
Onglet **Actions** → **Analyse technique quotidienne** → **Run workflow**.

## Signal d'achat (pullback EMA20, achat uniquement)
Tendance haussière (cours et EMA50 > EMA200) + plus bas récent au contact de l'EMA20
avec clôture au-dessus + RSI entre 40 et 60 en hausse + histogramme MACD en hausse.
Les paramètres sont en tête de `analyse_technique.py`.

Aide à la décision uniquement, pas un conseil en investissement.
