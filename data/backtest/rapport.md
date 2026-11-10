# Backtest des règles swing v3
Généré le 10/11/2026 14:40 — 514 titres (S&P 500 + Nasdaq 100 actuels), signaux du 2021-11-09 au 2026-11-09.
Dates de résultats connues pour 514 titres sur 514.

## Résultats par setup — V1 : plan v3 (moitié à 1,5R, suiveur plus bas veille, 2,5R)

### Sur 5 ans
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 1784 | 45.7 | 0.109 | -0.378 | 1.22 | 1.89 | 6.4 | 11 |
| R2 | 50 | 56.0 | 0.125 | 0.128 | 1.49 | 3.07 | 7.9 | 4 |
| R3 (demi-taille) | 1475 | 49.8 | 0.097 | -0.007 | 1.25 | 1.35 | 8.6 | 13 |
| **R1+R2+R3 (v3)** | 3309 | 47.7 | 0.104 | -0.137 | 1.23 | 1.67 | 7.4 | 9 |
| v3.1 R1 (recul ≥ 15 %) | 701 | 47.5 | 0.161 | -0.24 | 1.38 | 3.27 | 6.3 | 9 |
| v3.1 R2 (sans tendance) | 1131 | 49.5 | 0.135 | -0.013 | 1.32 | 2.21 | 7.6 | 8 |
| v3.1 R3 (en correction) | 690 | 54.5 | 0.167 | 0.168 | 1.45 | 2.31 | 8.8 | 7 |
| **v3.1 total (sans REIT)** | 2522 | 50.3 | 0.151 | 0.02 | 1.37 | 2.53 | 7.6 | 10 |
| Témoin R2 large | 1265 | 49.5 | 0.135 | -0.015 | 1.31 | 2.16 | 7.6 | 11 |
| Témoin Zone sans setup | 9659 | 46.5 | 0.054 | -0.19 | 1.12 | 1.16 | 7.3 | 13 |

### Sur les 2 dernières années
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 727 | 47.0 | 0.161 | -0.247 | 1.4 | 3.43 | 6.2 | 11 |
| R2 | 23 | 43.5 | -0.188 | -0.401 | 0.69 | -2.77 | 7.4 | 3 |
| R3 (demi-taille) | 558 | 46.1 | 0.072 | -0.144 | 1.18 | 1.03 | 8.3 | 9 |
| **R1+R2+R3 (v3)** | 1308 | 46.6 | 0.116 | -0.192 | 1.31 | 2.3 | 7.1 | 10 |
| v3.1 R1 (recul ≥ 15 %) | 310 | 50.0 | 0.243 | -0.02 | 1.61 | 5.39 | 6.0 | 9 |
| v3.1 R2 (sans tendance) | 453 | 48.6 | 0.068 | -0.042 | 1.17 | 1.19 | 7.5 | 9 |
| v3.1 R3 (en correction) | 214 | 52.3 | 0.155 | 0.145 | 1.39 | 2.11 | 8.4 | 6 |
| **v3.1 total (sans REIT)** | 977 | 49.8 | 0.143 | -0.004 | 1.37 | 2.73 | 7.2 | 10 |
| Témoin R2 large | 519 | 48.7 | 0.077 | -0.027 | 1.18 | 1.28 | 7.5 | 9 |
| Témoin Zone sans setup | 3841 | 47.4 | 0.079 | -0.122 | 1.19 | 1.77 | 7.4 | 12 |

## Résultats par setup — V2 : moitié à 1,5R puis clôture sous EMA10

### Sur 5 ans
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 1784 | 45.6 | 0.11 | -0.392 | 1.22 | 1.89 | 6.9 | 11 |
| R2 | 50 | 56.0 | 0.088 | 0.128 | 1.37 | 2.3 | 8.3 | 4 |
| R3 (demi-taille) | 1475 | 49.8 | 0.101 | -0.007 | 1.26 | 1.39 | 9.3 | 13 |
| **R1+R2+R3 (v3)** | 3309 | 47.6 | 0.105 | -0.139 | 1.24 | 1.67 | 8.0 | 9 |
| v3.1 R1 (recul ≥ 15 %) | 701 | 47.5 | 0.179 | -0.24 | 1.42 | 3.63 | 6.9 | 9 |
| v3.1 R2 (sans tendance) | 1131 | 49.5 | 0.147 | -0.013 | 1.34 | 2.38 | 8.1 | 8 |
| v3.1 R3 (en correction) | 690 | 54.5 | 0.172 | 0.168 | 1.47 | 2.38 | 9.5 | 7 |
| **v3.1 total (sans REIT)** | 2522 | 50.3 | 0.163 | 0.02 | 1.39 | 2.73 | 8.2 | 10 |
| Témoin R2 large | 1265 | 49.5 | 0.144 | -0.015 | 1.33 | 2.29 | 8.1 | 11 |
| Témoin Zone sans setup | 9659 | 46.4 | 0.053 | -0.191 | 1.12 | 1.11 | 7.9 | 13 |

### Sur les 2 dernières années
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 727 | 47.0 | 0.166 | -0.247 | 1.41 | 3.57 | 6.8 | 11 |
| R2 | 23 | 43.5 | -0.199 | -0.401 | 0.65 | -3.19 | 8.0 | 3 |
| R3 (demi-taille) | 558 | 46.1 | 0.067 | -0.144 | 1.16 | 0.95 | 8.9 | 9 |
| **R1+R2+R3 (v3)** | 1308 | 46.6 | 0.117 | -0.192 | 1.31 | 2.33 | 7.7 | 10 |
| v3.1 R1 (recul ≥ 15 %) | 310 | 50.0 | 0.257 | -0.02 | 1.65 | 5.81 | 6.6 | 9 |
| v3.1 R2 (sans tendance) | 453 | 48.6 | 0.09 | -0.042 | 1.22 | 1.57 | 8.0 | 9 |
| v3.1 R3 (en correction) | 214 | 52.3 | 0.145 | 0.145 | 1.36 | 1.96 | 9.0 | 6 |
| **v3.1 total (sans REIT)** | 977 | 49.8 | 0.155 | -0.004 | 1.41 | 3.0 | 7.8 | 10 |
| Témoin R2 large | 519 | 48.7 | 0.097 | -0.027 | 1.23 | 1.62 | 8.0 | 9 |
| Témoin Zone sans setup | 3841 | 47.4 | 0.079 | -0.123 | 1.18 | 1.73 | 7.9 | 12 |

## Résultats par setup — V3 : tout à 2R

### Sur 5 ans
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 1784 | 42.1 | 0.109 | -0.68 | 1.2 | 1.79 | 6.8 | 11 |
| R2 | 50 | 56.0 | 0.12 | 0.128 | 1.44 | 2.74 | 8.4 | 4 |
| R3 (demi-taille) | 1475 | 48.8 | 0.108 | -0.054 | 1.27 | 1.51 | 9.0 | 13 |
| **R1+R2+R3 (v3)** | 3309 | 45.3 | 0.109 | -0.227 | 1.23 | 1.68 | 7.8 | 12 |
| v3.1 R1 (recul ≥ 15 %) | 701 | 43.9 | 0.179 | -0.474 | 1.38 | 3.49 | 6.8 | 9 |
| v3.1 R2 (sans tendance) | 1131 | 47.0 | 0.133 | -0.094 | 1.29 | 2.07 | 8.0 | 12 |
| v3.1 R3 (en correction) | 690 | 53.3 | 0.183 | 0.136 | 1.49 | 2.55 | 9.1 | 7 |
| **v3.1 total (sans REIT)** | 2522 | 47.9 | 0.16 | -0.086 | 1.36 | 2.6 | 8.0 | 10 |
| Témoin R2 large | 1265 | 47.0 | 0.134 | -0.094 | 1.28 | 2.02 | 8.0 | 11 |
| Témoin Zone sans setup | 9659 | 44.3 | 0.054 | -0.277 | 1.12 | 1.15 | 7.8 | 19 |

### Sur les 2 dernières années
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 727 | 42.9 | 0.161 | -0.587 | 1.37 | 3.39 | 6.6 | 11 |
| R2 | 23 | 43.5 | -0.234 | -0.401 | 0.56 | -3.99 | 8.2 | 3 |
| R3 (demi-taille) | 558 | 45.5 | 0.095 | -0.167 | 1.23 | 1.33 | 8.5 | 9 |
| **R1+R2+R3 (v3)** | 1308 | 44.0 | 0.126 | -0.285 | 1.31 | 2.38 | 7.5 | 10 |
| v3.1 R1 (recul ≥ 15 %) | 310 | 46.1 | 0.284 | -0.235 | 1.65 | 6.05 | 6.4 | 9 |
| v3.1 R2 (sans tendance) | 453 | 45.5 | 0.078 | -0.155 | 1.16 | 1.19 | 7.7 | 9 |
| v3.1 R3 (en correction) | 214 | 51.9 | 0.183 | 0.108 | 1.45 | 2.5 | 8.5 | 6 |
| **v3.1 total (sans REIT)** | 977 | 47.1 | 0.166 | -0.135 | 1.4 | 3.02 | 7.5 | 10 |
| Témoin R2 large | 519 | 45.9 | 0.091 | -0.144 | 1.18 | 1.31 | 7.7 | 9 |
| Témoin Zone sans setup | 3841 | 45.4 | 0.085 | -0.195 | 1.19 | 1.86 | 7.8 | 13 |

## Plan R1+R2+R3 (V1) par année
| Année | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| 2021 | 57 | 36.8 | -0.13 | -1.0 | 0.7 | -3.12 | 7.0 | 6 |
| 2022 | 697 | 49.6 | 0.109 | -0.022 | 1.21 | 1.45 | 7.8 | 6 |
| 2023 | 734 | 49.5 | 0.098 | -0.05 | 1.19 | 1.26 | 7.7 | 9 |
| 2024 | 576 | 45.3 | 0.093 | -0.28 | 1.18 | 1.27 | 7.2 | 13 |
| 2025 | 736 | 47.4 | 0.135 | -0.144 | 1.42 | 2.94 | 7.2 | 8 |
| 2026 | 509 | 46.6 | 0.102 | -0.193 | 1.21 | 1.68 | 7.0 | 9 |

## Plan (V1) selon le marché au signal
| Marché | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| SPY et QQQ au-dessus de l'EMA50 | 2029 | 44.4 | 0.06 | -0.297 | 1.13 | 0.97 | 7.1 | 12 |
| SPY ou QQQ sous l'EMA50 | 1280 | 52.9 | 0.175 | 0.123 | 1.43 | 2.77 | 7.9 | 11 |

## Plan (V1) selon le score de setup du scan
| Score | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| 0-4 | 575 | 49.2 | 0.071 | -0.027 | 1.19 | 1.05 | 8.5 | 9 |
| 5-6 | 649 | 49.9 | 0.123 | -0.001 | 1.3 | 1.68 | 8.4 | 8 |
| 7-8 | 1504 | 46.8 | 0.108 | -0.242 | 1.21 | 1.67 | 6.8 | 12 |
| 9-10 | 581 | 45.8 | 0.107 | -0.252 | 1.27 | 2.26 | 6.9 | 12 |

## Plan (V1) selon le recul depuis le plus haut
| Recul | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| -50 à -35 % | 349 | 53.9 | 0.204 | 0.142 | 1.6 | 2.89 | 8.9 | 8 |
| -35 à -25 % | 440 | 50.9 | 0.072 | 0.018 | 1.19 | 1.04 | 8.6 | 12 |
| -25 à -20 % | 505 | 48.9 | 0.153 | -0.07 | 1.33 | 2.38 | 7.6 | 8 |
| -20 à -15 % | 683 | 47.4 | 0.122 | -0.165 | 1.34 | 2.51 | 7.1 | 7 |
| -15 à -10 % | 1332 | 44.6 | 0.061 | -0.392 | 1.11 | 0.85 | 6.7 | 14 |

## Plan (V1) par secteur
| Secteur | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
|  | 75 | 45.3 | 0.146 | -0.218 | 1.37 | 3.9 | 5.9 | 5 |
| Communication Services | 158 | 44.3 | 0.16 | -0.307 | 1.54 | 4.28 | 7.4 | 8 |
| Consumer Discretionary | 382 | 45.0 | 0.059 | -0.294 | 1.12 | 0.91 | 7.3 | 6 |
| Consumer Staples | 200 | 47.0 | 0.052 | -0.113 | 1.09 | 0.56 | 7.4 | 11 |
| Energy | 202 | 51.5 | 0.213 | 0.07 | 1.37 | 2.63 | 7.9 | 7 |
| Financials | 453 | 49.2 | 0.064 | -0.05 | 1.15 | 0.94 | 8.0 | 8 |
| Health Care | 303 | 49.5 | 0.146 | -0.053 | 1.35 | 2.13 | 7.5 | 12 |
| Industrials | 425 | 49.2 | 0.105 | -0.04 | 1.23 | 1.5 | 7.5 | 8 |
| Information Technology | 638 | 46.9 | 0.126 | -0.234 | 1.26 | 2.18 | 7.2 | 9 |
| Materials | 168 | 49.4 | 0.174 | -0.02 | 1.36 | 2.53 | 6.9 | 6 |
| Real Estate | 174 | 40.8 | -0.069 | -0.43 | 0.82 | -1.25 | 7.1 | 5 |
| Utilities | 131 | 51.9 | 0.131 | 0.048 | 1.32 | 1.87 | 7.6 | 4 |

## Raisons de sortie (plan, V1)
| Raison | Trades | R moyen |
|---|---|---|
| T2 | 299 | 2.21 |
| durée max | 12 | 1.16 |
| stop | 1189 | -1.00 |
| stop (gap) | 156 | -1.21 |
| stop temps | 754 | -0.02 |
| suiveur/BE | 746 | 1.32 |
| veille résultats | 153 | 0.52 |

## Entonnoir des signaux
| Famille | Signaux | Résultats trop proches | Stop > 2 ATR | < 2 actions | Ordre non exécuté | Trades |
|---|---|---|---|---|---|---|
| plan | 13006 | 1622 | 216 | 5368 | 2491 | 3309 |
| plan31 | 8361 | 1145 | 645 | 2606 | 1443 | 2522 |
| r2_large | 2980 | 313 | 615 | 403 | 384 | 1265 |
| zone | 22641 | 4405 | 0 | 8577 | 0 | 9659 |

## Compte de 2 000 $ simulé sur 5 ans (sorties V1, plafonds de risque et de secteur)
- Valeur finale : **3613 $** (+80.7 %), drawdown max -16.0 %
- SPY sur la même période : +72.2 %, drawdown max -24.5 %
- Trades retenus : 883 ; refusés faute de budget de risque 1199, de place dans le secteur 234, de cash 993 ; positions ouvertes en moyenne 4.18

## Compte de 2 000 $ simulé sur 2 ans (sorties V1, plafonds de risque et de secteur)
- Valeur finale : **3284 $** (+64.2 %), drawdown max -10.0 %
- SPY sur la même période : +28.6 %, drawdown max -18.8 %
- Trades retenus : 390 ; refusés faute de budget de risque 534, de place dans le secteur 89, de cash 295 ; positions ouvertes en moyenne 4.8

## Compte de 2 000 $ simulé sur 5 ans v3.1 (sorties V1, plafonds de risque et de secteur)
- Valeur finale : **5030 $** (+151.5 %), drawdown max -8.2 %
- SPY sur la même période : +72.2 %, drawdown max -24.5 %
- Trades retenus : 829 ; refusés faute de budget de risque 1279, de place dans le secteur 154, de cash 260 ; positions ouvertes en moyenne 4.05

## Compte de 2 000 $ simulé sur 2 ans v3.1 (sorties V1, plafonds de risque et de secteur)
- Valeur finale : **3394 $** (+69.7 %), drawdown max -13.3 %
- SPY sur la même période : +28.6 %, drawdown max -18.8 %
- Trades retenus : 337 ; refusés faute de budget de risque 452, de place dans le secteur 67, de cash 121 ; positions ouvertes en moyenne 3.92

## Limites
- Univers actuel des indices : biais du survivant, plutôt favorable.
- Pas de filtre sur la cause de la baisse (fondamental) : en réel, une partie des pertes serait évitée, mais aussi quelques gains.
- Pas de frais ni de glissement hors gaps.
- Stop et objectif touchés la même séance : le stop est compté (prudent).
