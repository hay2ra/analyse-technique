# Backtest des règles swing v3
Généré le 09/11/2026 17:30 — 500 titres (S&P 500 + Nasdaq 100 actuels), signaux du 2021-11-09 au 2026-11-09.
Dates de résultats connues pour 500 titres sur 500.

## Résultats par setup — V1 : plan v3 (moitié à 1,5R, suiveur plus bas veille, 2,5R)

### Sur 5 ans
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 1739 | 45.8 | 0.11 | -0.349 | 1.22 | 1.8 | 6.4 | 11 |
| R2 | 50 | 56.0 | 0.125 | 0.128 | 1.49 | 3.07 | 7.9 | 4 |
| R3 (demi-taille) | 1446 | 49.7 | 0.094 | -0.012 | 1.24 | 1.29 | 8.7 | 13 |
| **R1+R2+R3** | 3235 | 47.7 | 0.103 | -0.135 | 1.23 | 1.59 | 7.4 | 9 |
| Témoin R2 large | 1251 | 49.7 | 0.141 | -0.005 | 1.34 | 2.29 | 7.6 | 11 |
| Témoin Zone sans setup | 9456 | 46.6 | 0.055 | -0.18 | 1.13 | 1.16 | 7.4 | 13 |

### Sur les 2 dernières années
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 700 | 47.1 | 0.158 | -0.227 | 1.39 | 3.28 | 6.3 | 11 |
| R2 | 23 | 43.5 | -0.188 | -0.401 | 0.69 | -2.77 | 7.4 | 3 |
| R3 (demi-taille) | 544 | 45.8 | 0.061 | -0.16 | 1.15 | 0.86 | 8.3 | 8 |
| **R1+R2+R3** | 1267 | 46.5 | 0.11 | -0.191 | 1.29 | 2.13 | 7.2 | 10 |
| Témoin R2 large | 513 | 49.1 | 0.085 | -0.021 | 1.21 | 1.47 | 7.5 | 9 |
| Témoin Zone sans setup | 3740 | 47.6 | 0.08 | -0.118 | 1.19 | 1.79 | 7.4 | 12 |

## Résultats par setup — V2 : moitié à 1,5R puis clôture sous EMA10

### Sur 5 ans
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 1739 | 45.7 | 0.111 | -0.352 | 1.22 | 1.82 | 7.0 | 11 |
| R2 | 50 | 56.0 | 0.088 | 0.128 | 1.37 | 2.3 | 8.3 | 4 |
| R3 (demi-taille) | 1446 | 49.7 | 0.097 | -0.012 | 1.25 | 1.34 | 9.3 | 13 |
| **R1+R2+R3** | 3235 | 47.6 | 0.104 | -0.137 | 1.23 | 1.61 | 8.0 | 9 |
| Témoin R2 large | 1251 | 49.7 | 0.15 | -0.005 | 1.35 | 2.43 | 8.1 | 11 |
| Témoin Zone sans setup | 9456 | 46.6 | 0.053 | -0.183 | 1.12 | 1.1 | 7.9 | 13 |

### Sur les 2 dernières années
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 700 | 47.1 | 0.165 | -0.227 | 1.41 | 3.45 | 6.9 | 11 |
| R2 | 23 | 43.5 | -0.199 | -0.401 | 0.65 | -3.19 | 8.0 | 3 |
| R3 (demi-taille) | 544 | 45.8 | 0.059 | -0.16 | 1.14 | 0.8 | 8.9 | 8 |
| **R1+R2+R3** | 1267 | 46.5 | 0.113 | -0.191 | 1.3 | 2.19 | 7.8 | 10 |
| Témoin R2 large | 513 | 49.1 | 0.105 | -0.021 | 1.26 | 1.81 | 8.0 | 9 |
| Témoin Zone sans setup | 3740 | 47.6 | 0.08 | -0.119 | 1.19 | 1.74 | 8.0 | 12 |

## Résultats par setup — V3 : tout à 2R

### Sur 5 ans
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 1739 | 42.2 | 0.107 | -0.606 | 1.19 | 1.66 | 6.8 | 11 |
| R2 | 50 | 56.0 | 0.12 | 0.128 | 1.44 | 2.74 | 8.4 | 4 |
| R3 (demi-taille) | 1446 | 48.8 | 0.105 | -0.054 | 1.26 | 1.45 | 9.0 | 13 |
| **R1+R2+R3** | 3235 | 45.3 | 0.106 | -0.224 | 1.22 | 1.59 | 7.8 | 12 |
| Témoin R2 large | 1251 | 47.3 | 0.143 | -0.081 | 1.31 | 2.2 | 8.0 | 11 |
| Témoin Zone sans setup | 9456 | 44.5 | 0.056 | -0.268 | 1.12 | 1.16 | 7.8 | 19 |

### Sur les 2 dernières années
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 700 | 42.9 | 0.156 | -0.507 | 1.35 | 3.18 | 6.7 | 11 |
| R2 | 23 | 43.5 | -0.234 | -0.401 | 0.56 | -3.99 | 8.2 | 3 |
| R3 (demi-taille) | 544 | 45.4 | 0.087 | -0.175 | 1.2 | 1.2 | 8.6 | 8 |
| **R1+R2+R3** | 1267 | 44.0 | 0.119 | -0.283 | 1.29 | 2.2 | 7.5 | 10 |
| Témoin R2 large | 513 | 46.2 | 0.099 | -0.139 | 1.21 | 1.5 | 7.8 | 9 |
| Témoin Zone sans setup | 3740 | 45.6 | 0.087 | -0.18 | 1.2 | 1.87 | 7.9 | 13 |

## Plan R1+R2+R3 (V1) par année
| Année | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| 2021 | 57 | 38.6 | -0.09 | -1.0 | 0.75 | -2.5 | 7.1 | 6 |
| 2022 | 689 | 49.8 | 0.115 | -0.021 | 1.23 | 1.54 | 7.9 | 6 |
| 2023 | 719 | 49.7 | 0.098 | -0.024 | 1.2 | 1.27 | 7.7 | 8 |
| 2024 | 565 | 45.0 | 0.086 | -0.282 | 1.14 | 1.02 | 7.2 | 13 |
| 2025 | 708 | 47.5 | 0.131 | -0.144 | 1.42 | 2.86 | 7.2 | 8 |
| 2026 | 497 | 46.5 | 0.093 | -0.193 | 1.18 | 1.47 | 7.1 | 8 |

## Plan (V1) selon le marché au signal
| Marché | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| SPY et QQQ au-dessus de l'EMA50 | 1980 | 44.4 | 0.059 | -0.294 | 1.12 | 0.91 | 7.1 | 12 |
| SPY ou QQQ sous l'EMA50 | 1255 | 52.9 | 0.172 | 0.12 | 1.42 | 2.68 | 8.0 | 9 |

## Plan (V1) selon le score de setup du scan
| Score | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| 0-4 | 565 | 49.0 | 0.066 | -0.04 | 1.18 | 0.98 | 8.5 | 8 |
| 5-6 | 642 | 50.0 | 0.12 | 0.003 | 1.28 | 1.59 | 8.4 | 8 |
| 7-8 | 1461 | 46.8 | 0.106 | -0.24 | 1.21 | 1.61 | 6.8 | 12 |
| 9-10 | 567 | 46.0 | 0.113 | -0.224 | 1.26 | 2.17 | 7.0 | 12 |

## Plan (V1) selon le recul depuis le plus haut
| Recul | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| -50 à -35 % | 334 | 54.2 | 0.211 | 0.154 | 1.63 | 2.99 | 9.0 | 8 |
| -35 à -25 % | 431 | 50.6 | 0.059 | 0.01 | 1.15 | 0.85 | 8.6 | 10 |
| -25 à -20 % | 490 | 48.8 | 0.146 | -0.072 | 1.3 | 2.12 | 7.7 | 8 |
| -20 à -15 % | 677 | 47.4 | 0.119 | -0.165 | 1.33 | 2.46 | 7.1 | 7 |
| -15 à -10 % | 1303 | 44.8 | 0.065 | -0.35 | 1.11 | 0.84 | 6.7 | 14 |

## Plan (V1) par secteur
| Secteur | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| Communication Services | 159 | 44.0 | 0.153 | -0.341 | 1.52 | 4.17 | 7.4 | 8 |
| Consumer Discretionary | 381 | 44.9 | 0.054 | -0.296 | 1.1 | 0.76 | 7.3 | 6 |
| Consumer Staples | 201 | 47.3 | 0.056 | -0.109 | 1.09 | 0.59 | 7.4 | 11 |
| Energy | 203 | 51.2 | 0.207 | 0.047 | 1.35 | 2.53 | 7.9 | 7 |
| Financials | 453 | 49.2 | 0.065 | -0.05 | 1.15 | 0.95 | 8.0 | 8 |
| Health Care | 303 | 49.5 | 0.146 | -0.053 | 1.35 | 2.13 | 7.5 | 12 |
| Industrials | 425 | 49.2 | 0.105 | -0.04 | 1.23 | 1.5 | 7.5 | 8 |
| Information Technology | 638 | 46.9 | 0.126 | -0.234 | 1.26 | 2.18 | 7.2 | 9 |
| Materials | 168 | 49.4 | 0.174 | -0.02 | 1.36 | 2.53 | 6.9 | 6 |
| Real Estate | 173 | 41.0 | -0.058 | -0.353 | 0.83 | -1.16 | 7.1 | 5 |
| Utilities | 131 | 51.9 | 0.13 | 0.048 | 1.32 | 1.85 | 7.7 | 4 |

## Raisons de sortie (plan, V1)
| Raison | Trades | R moyen |
|---|---|---|
| T2 | 283 | 2.22 |
| durée max | 12 | 1.16 |
| stop | 1161 | -1.00 |
| stop (gap) | 148 | -1.20 |
| stop temps | 746 | -0.02 |
| suiveur/BE | 733 | 1.32 |
| veille résultats | 152 | 0.52 |

## Entonnoir des signaux
| Famille | Signaux | Résultats trop proches | Stop > 2 ATR | < 2 actions | Ordre non exécuté | Trades |
|---|---|---|---|---|---|---|
| plan | 12430 | 1555 | 211 | 5006 | 2423 | 3235 |
| r2_large | 2942 | 310 | 602 | 399 | 380 | 1251 |
| zone | 21975 | 4299 | 0 | 8220 | 0 | 9456 |

## Compte de 2 000 $ simulé sur 5 ans (plan V1, plafonds de risque et de secteur)
- Valeur finale : **4338 $** (+116.9 %), drawdown max -12.1 %
- SPY sur la même période : +71.6 %, drawdown max -24.5 %
- Trades retenus : 933 ; refusés faute de budget de risque 1322, de place dans le secteur 282, de cash 698 ; positions ouvertes en moyenne 4.54

## Compte de 2 000 $ simulé sur 2 ans (plan V1, plafonds de risque et de secteur)
- Valeur finale : **3334 $** (+66.7 %), drawdown max -7.6 %
- SPY sur la même période : +28.2 %, drawdown max -18.8 %
- Trades retenus : 371 ; refusés faute de budget de risque 431, de place dans le secteur 122, de cash 343 ; positions ouvertes en moyenne 4.68

## Limites
- Univers actuel des indices : biais du survivant, plutôt favorable.
- Pas de filtre sur la cause de la baisse (fondamental) : en réel, une partie des pertes serait évitée, mais aussi quelques gains.
- Pas de frais ni de glissement hors gaps.
- Stop et objectif touchés la même séance : le stop est compté (prudent).
