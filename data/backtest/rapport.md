# Backtest des règles swing v3
Généré le 13/11/2026 15:16 — 514 titres (S&P 500 + Nasdaq 100 actuels), signaux du 2021-11-12 au 2026-11-12.
Dates de résultats connues pour 514 titres sur 514.

## Résultats par setup — V1 : plan v3 (moitié à 1,5R, suiveur plus bas veille, 2,5R)

### Sur 5 ans
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 1777 | 45.6 | 0.11 | -0.358 | 1.22 | 1.91 | 6.4 | 11 |
| R2 | 50 | 56.0 | 0.125 | 0.128 | 1.49 | 3.06 | 7.9 | 4 |
| R3 (demi-taille) | 1474 | 49.9 | 0.1 | -0.005 | 1.26 | 1.39 | 8.6 | 13 |
| **R1+R2+R3 (v3)** | 3301 | 47.7 | 0.106 | -0.131 | 1.24 | 1.69 | 7.4 | 9 |
| v3.1 R1 (recul ≥ 15 %) | 700 | 47.4 | 0.159 | -0.248 | 1.37 | 3.25 | 6.3 | 9 |
| v3.1 R2 (sans tendance) | 1128 | 49.5 | 0.134 | -0.014 | 1.32 | 2.2 | 7.6 | 8 |
| v3.1 R3 (en correction) | 691 | 54.6 | 0.17 | 0.17 | 1.46 | 2.35 | 8.8 | 7 |
| **v3.1 total (sans REIT)** | 2519 | 50.3 | 0.151 | 0.017 | 1.37 | 2.54 | 7.6 | 10 |
| **Panique (leaders au rebond)** | 1571 | 52.6 | 0.11 | 0.068 | 1.27 | 3.25 | 7.4 | 11 |
| Témoin R2 large | 1261 | 49.5 | 0.135 | -0.015 | 1.31 | 2.17 | 7.6 | 11 |
| Témoin Zone sans setup | 9672 | 46.5 | 0.054 | -0.191 | 1.12 | 1.16 | 7.3 | 13 |

### Sur les 2 dernières années
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 728 | 47.1 | 0.163 | -0.242 | 1.4 | 3.46 | 6.2 | 11 |
| R2 | 23 | 43.5 | -0.188 | -0.401 | 0.69 | -2.77 | 7.4 | 3 |
| R3 (demi-taille) | 559 | 46.2 | 0.075 | -0.144 | 1.19 | 1.07 | 8.3 | 9 |
| **R1+R2+R3 (v3)** | 1310 | 46.6 | 0.119 | -0.184 | 1.31 | 2.34 | 7.1 | 10 |
| v3.1 R1 (recul ≥ 15 %) | 310 | 50.0 | 0.244 | -0.02 | 1.61 | 5.42 | 6.0 | 9 |
| v3.1 R2 (sans tendance) | 452 | 48.5 | 0.067 | -0.045 | 1.17 | 1.18 | 7.4 | 9 |
| v3.1 R3 (en correction) | 215 | 52.6 | 0.163 | 0.15 | 1.41 | 2.23 | 8.3 | 6 |
| **v3.1 total (sans REIT)** | 977 | 49.8 | 0.144 | -0.004 | 1.38 | 2.76 | 7.2 | 10 |
| **Panique (leaders au rebond)** | 551 | 55.0 | 0.049 | 0.101 | 1.14 | 1.56 | 7.5 | 6 |
| Témoin R2 large | 517 | 48.7 | 0.079 | -0.027 | 1.19 | 1.31 | 7.5 | 9 |
| Témoin Zone sans setup | 3870 | 47.4 | 0.078 | -0.122 | 1.19 | 1.76 | 7.3 | 12 |

## Résultats par setup — V2 : moitié à 1,5R puis clôture sous EMA10

### Sur 5 ans
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 1777 | 45.5 | 0.111 | -0.365 | 1.22 | 1.92 | 6.9 | 11 |
| R2 | 50 | 56.0 | 0.088 | 0.128 | 1.37 | 2.29 | 8.3 | 4 |
| R3 (demi-taille) | 1474 | 49.9 | 0.104 | -0.005 | 1.26 | 1.43 | 9.3 | 13 |
| **R1+R2+R3 (v3)** | 3301 | 47.6 | 0.107 | -0.135 | 1.24 | 1.7 | 8.0 | 9 |
| v3.1 R1 (recul ≥ 15 %) | 700 | 47.4 | 0.178 | -0.248 | 1.42 | 3.62 | 6.9 | 9 |
| v3.1 R2 (sans tendance) | 1128 | 49.5 | 0.147 | -0.014 | 1.34 | 2.38 | 8.1 | 8 |
| v3.1 R3 (en correction) | 691 | 54.6 | 0.175 | 0.17 | 1.47 | 2.42 | 9.5 | 7 |
| **v3.1 total (sans REIT)** | 2519 | 50.3 | 0.163 | 0.017 | 1.4 | 2.74 | 8.2 | 10 |
| **Panique (leaders au rebond)** | 1571 | 52.6 | 0.109 | 0.068 | 1.27 | 3.21 | 7.8 | 11 |
| Témoin R2 large | 1261 | 49.5 | 0.144 | -0.015 | 1.33 | 2.3 | 8.1 | 11 |
| Témoin Zone sans setup | 9672 | 46.4 | 0.052 | -0.192 | 1.12 | 1.11 | 7.9 | 13 |

### Sur les 2 dernières années
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 728 | 47.1 | 0.168 | -0.242 | 1.42 | 3.61 | 6.8 | 11 |
| R2 | 23 | 43.5 | -0.199 | -0.401 | 0.64 | -3.19 | 8.0 | 3 |
| R3 (demi-taille) | 559 | 46.2 | 0.071 | -0.144 | 1.17 | 1.0 | 8.9 | 9 |
| **R1+R2+R3 (v3)** | 1310 | 46.6 | 0.12 | -0.184 | 1.32 | 2.37 | 7.7 | 10 |
| v3.1 R1 (recul ≥ 15 %) | 310 | 50.0 | 0.258 | -0.02 | 1.66 | 5.86 | 6.6 | 9 |
| v3.1 R2 (sans tendance) | 452 | 48.5 | 0.09 | -0.045 | 1.22 | 1.58 | 8.0 | 9 |
| v3.1 R3 (en correction) | 215 | 52.6 | 0.153 | 0.15 | 1.38 | 2.08 | 9.0 | 6 |
| **v3.1 total (sans REIT)** | 977 | 49.8 | 0.157 | -0.004 | 1.42 | 3.05 | 7.8 | 10 |
| **Panique (leaders au rebond)** | 551 | 55.0 | 0.044 | 0.101 | 1.13 | 1.4 | 7.7 | 6 |
| Témoin R2 large | 517 | 48.7 | 0.099 | -0.027 | 1.24 | 1.66 | 8.0 | 9 |
| Témoin Zone sans setup | 3870 | 47.4 | 0.078 | -0.122 | 1.18 | 1.71 | 7.9 | 12 |

## Résultats par setup — V3 : tout à 2R

### Sur 5 ans
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 1777 | 42.1 | 0.111 | -0.634 | 1.2 | 1.82 | 6.8 | 11 |
| R2 | 50 | 56.0 | 0.12 | 0.128 | 1.44 | 2.73 | 8.4 | 4 |
| R3 (demi-taille) | 1474 | 48.9 | 0.111 | -0.048 | 1.28 | 1.55 | 9.0 | 13 |
| **R1+R2+R3 (v3)** | 3301 | 45.3 | 0.111 | -0.218 | 1.23 | 1.71 | 7.8 | 12 |
| v3.1 R1 (recul ≥ 15 %) | 700 | 43.9 | 0.176 | -0.528 | 1.38 | 3.45 | 6.8 | 9 |
| v3.1 R2 (sans tendance) | 1128 | 47.0 | 0.132 | -0.094 | 1.29 | 2.06 | 8.0 | 12 |
| v3.1 R3 (en correction) | 691 | 53.4 | 0.186 | 0.136 | 1.5 | 2.58 | 9.1 | 7 |
| **v3.1 total (sans REIT)** | 2519 | 47.9 | 0.159 | -0.088 | 1.36 | 2.59 | 7.9 | 10 |
| **Panique (leaders au rebond)** | 1571 | 50.4 | 0.102 | 0.009 | 1.23 | 2.77 | 7.8 | 11 |
| Témoin R2 large | 1261 | 47.0 | 0.134 | -0.094 | 1.28 | 2.02 | 8.0 | 11 |
| Témoin Zone sans setup | 9672 | 44.2 | 0.054 | -0.278 | 1.12 | 1.15 | 7.8 | 19 |

### Sur les 2 dernières années
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 728 | 43.0 | 0.164 | -0.551 | 1.38 | 3.44 | 6.6 | 11 |
| R2 | 23 | 43.5 | -0.234 | -0.401 | 0.56 | -3.99 | 8.2 | 3 |
| R3 (demi-taille) | 559 | 45.6 | 0.098 | -0.162 | 1.24 | 1.38 | 8.5 | 9 |
| **R1+R2+R3 (v3)** | 1310 | 44.1 | 0.129 | -0.281 | 1.31 | 2.43 | 7.5 | 10 |
| v3.1 R1 (recul ≥ 15 %) | 310 | 46.1 | 0.284 | -0.235 | 1.65 | 6.07 | 6.4 | 9 |
| v3.1 R2 (sans tendance) | 452 | 45.4 | 0.079 | -0.166 | 1.16 | 1.21 | 7.7 | 9 |
| v3.1 R3 (en correction) | 215 | 52.1 | 0.191 | 0.133 | 1.48 | 2.62 | 8.5 | 6 |
| **v3.1 total (sans REIT)** | 977 | 47.1 | 0.169 | -0.135 | 1.4 | 3.06 | 7.5 | 10 |
| **Panique (leaders au rebond)** | 551 | 53.0 | 0.038 | 0.05 | 1.09 | 1.01 | 7.8 | 6 |
| Témoin R2 large | 517 | 45.8 | 0.094 | -0.144 | 1.19 | 1.36 | 7.7 | 9 |
| Témoin Zone sans setup | 3870 | 45.4 | 0.084 | -0.196 | 1.19 | 1.84 | 7.8 | 13 |

## Résultats par setup — V4 : position : moitié à 2R, reste tenu jusqu'à clôture sous EMA20, 60 séances max

### Sur 5 ans
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 1777 | 39.2 | 0.138 | -1.0 | 1.25 | 2.56 | 11.7 | 11 |
| R2 | 50 | 48.0 | 0.227 | -0.082 | 1.7 | 5.27 | 14.0 | 4 |
| R3 (demi-taille) | 1474 | 44.2 | 0.127 | -0.522 | 1.26 | 1.81 | 14.8 | 9 |
| **R1+R2+R3 (v3)** | 3301 | 41.5 | 0.135 | -1.0 | 1.26 | 2.27 | 13.1 | 15 |
| v3.1 R1 (recul ≥ 15 %) | 700 | 41.4 | 0.221 | -1.0 | 1.48 | 4.98 | 12.1 | 9 |
| v3.1 R2 (sans tendance) | 1128 | 42.4 | 0.104 | -1.0 | 1.19 | 1.7 | 12.7 | 19 |
| v3.1 R3 (en correction) | 691 | 45.6 | 0.17 | -0.507 | 1.35 | 2.42 | 14.3 | 8 |
| **v3.1 total (sans REIT)** | 2519 | 43.0 | 0.155 | -1.0 | 1.32 | 2.81 | 13.0 | 13 |
| **Panique (leaders au rebond)** | 1571 | 43.6 | 0.103 | -0.695 | 1.19 | 2.87 | 12.3 | 11 |
| Témoin R2 large | 1261 | 42.4 | 0.104 | -1.0 | 1.18 | 1.65 | 12.7 | 21 |
| Témoin Zone sans setup | 9672 | 39.7 | 0.071 | -1.0 | 1.14 | 1.59 | 13.1 | 19 |

### Sur les 2 dernières années
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 728 | 40.2 | 0.22 | -1.0 | 1.47 | 4.86 | 11.9 | 8 |
| R2 | 23 | 39.1 | 0.086 | -1.0 | 1.33 | 3.52 | 13.3 | 3 |
| R3 (demi-taille) | 559 | 45.4 | 0.142 | -0.448 | 1.3 | 2.03 | 14.4 | 10 |
| **R1+R2+R3 (v3)** | 1310 | 42.4 | 0.184 | -1.0 | 1.41 | 3.63 | 13.0 | 9 |
| v3.1 R1 (recul ≥ 15 %) | 310 | 43.2 | 0.347 | -1.0 | 1.75 | 7.83 | 12.3 | 9 |
| v3.1 R2 (sans tendance) | 452 | 41.6 | 0.062 | -1.0 | 1.1 | 0.91 | 11.9 | 11 |
| v3.1 R3 (en correction) | 215 | 48.4 | 0.181 | -0.195 | 1.4 | 2.59 | 14.0 | 7 |
| **v3.1 total (sans REIT)** | 977 | 43.6 | 0.179 | -1.0 | 1.39 | 3.47 | 12.5 | 10 |
| **Panique (leaders au rebond)** | 551 | 45.7 | 0.074 | -0.237 | 1.11 | 1.65 | 11.7 | 8 |
| Témoin R2 large | 517 | 42.6 | 0.074 | -1.0 | 1.12 | 1.05 | 11.9 | 12 |
| Témoin Zone sans setup | 3870 | 41.5 | 0.152 | -1.0 | 1.3 | 3.36 | 13.4 | 14 |

## Résultats par setup — V5 : position avec stop sur clôture (au lieu d'en séance)

### Sur 5 ans
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 1777 | 44.9 | 0.127 | -0.745 | 1.24 | 2.71 | 13.5 | 10 |
| R2 | 50 | 50.0 | 0.197 | -0.012 | 1.53 | 4.53 | 15.5 | 4 |
| R3 (demi-taille) | 1474 | 48.8 | 0.153 | -0.072 | 1.29 | 2.17 | 16.0 | 9 |
| **R1+R2+R3 (v3)** | 3301 | 46.7 | 0.14 | -0.295 | 1.26 | 2.5 | 14.6 | 13 |
| v3.1 R1 (recul ≥ 15 %) | 700 | 47.4 | 0.243 | -0.42 | 1.52 | 5.96 | 14.0 | 8 |
| v3.1 R2 (sans tendance) | 1128 | 49.1 | 0.145 | -0.064 | 1.23 | 2.3 | 14.6 | 7 |
| v3.1 R3 (en correction) | 691 | 50.7 | 0.221 | 0.036 | 1.43 | 3.09 | 15.5 | 8 |
| **v3.1 total (sans REIT)** | 2519 | 49.1 | 0.193 | -0.088 | 1.37 | 3.53 | 14.7 | 10 |
| **Panique (leaders au rebond)** | 1571 | 49.2 | 0.112 | -0.027 | 1.17 | 2.86 | 13.8 | 10 |
| Témoin R2 large | 1261 | 48.8 | 0.137 | -0.118 | 1.21 | 2.1 | 14.5 | 10 |
| Témoin Zone sans setup | 9672 | 45.3 | 0.096 | -0.346 | 1.18 | 2.15 | 15.0 | 19 |

### Sur les 2 dernières années
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 728 | 46.0 | 0.238 | -0.472 | 1.48 | 5.6 | 13.7 | 8 |
| R2 | 23 | 43.5 | 0.088 | -1.045 | 1.23 | 2.76 | 15.0 | 2 |
| R3 (demi-taille) | 559 | 49.9 | 0.155 | -0.028 | 1.3 | 2.19 | 15.7 | 10 |
| **R1+R2+R3 (v3)** | 1310 | 47.6 | 0.2 | -0.206 | 1.42 | 4.09 | 14.6 | 9 |
| v3.1 R1 (recul ≥ 15 %) | 310 | 49.4 | 0.436 | -0.067 | 1.9 | 10.15 | 14.6 | 7 |
| v3.1 R2 (sans tendance) | 452 | 48.5 | 0.089 | -0.097 | 1.1 | 1.03 | 13.8 | 10 |
| v3.1 R3 (en correction) | 215 | 53.0 | 0.177 | 0.16 | 1.36 | 2.51 | 15.0 | 7 |
| **v3.1 total (sans REIT)** | 977 | 49.7 | 0.218 | -0.007 | 1.42 | 4.25 | 14.3 | 10 |
| **Panique (leaders au rebond)** | 551 | 50.6 | 0.033 | 0.034 | 0.99 | -0.1 | 13.0 | 7 |
| Témoin R2 large | 517 | 48.9 | 0.1 | -0.067 | 1.12 | 1.19 | 13.7 | 8 |
| Témoin Zone sans setup | 3870 | 47.8 | 0.204 | -0.16 | 1.37 | 4.48 | 15.3 | 14 |

## Plan R1+R2+R3 (V1) par année
| Année | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| 2021 | 48 | 37.5 | -0.094 | -1.0 | 0.74 | -2.66 | 7.3 | 6 |
| 2022 | 697 | 49.5 | 0.109 | -0.04 | 1.21 | 1.44 | 7.8 | 6 |
| 2023 | 734 | 49.5 | 0.098 | -0.05 | 1.2 | 1.26 | 7.7 | 9 |
| 2024 | 575 | 45.2 | 0.09 | -0.281 | 1.17 | 1.23 | 7.2 | 13 |
| 2025 | 735 | 47.5 | 0.137 | -0.144 | 1.43 | 2.97 | 7.2 | 8 |
| 2026 | 512 | 46.7 | 0.105 | -0.192 | 1.22 | 1.75 | 7.0 | 9 |

## Plan (V1) selon le marché au signal
| Marché | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| SPY et QQQ au-dessus de l'EMA50 | 2018 | 44.4 | 0.062 | -0.295 | 1.13 | 1.0 | 7.1 | 12 |
| SPY ou QQQ sous l'EMA50 | 1283 | 52.8 | 0.175 | 0.121 | 1.44 | 2.79 | 7.9 | 11 |

## Plan (V1) selon le score de setup du scan
| Score | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| 0-4 | 575 | 49.4 | 0.076 | -0.024 | 1.2 | 1.13 | 8.5 | 9 |
| 5-6 | 648 | 50.0 | 0.123 | 0.003 | 1.3 | 1.68 | 8.4 | 8 |
| 7-8 | 1497 | 46.7 | 0.108 | -0.243 | 1.21 | 1.67 | 6.8 | 12 |
| 9-10 | 581 | 46.0 | 0.111 | -0.235 | 1.27 | 2.32 | 6.9 | 12 |

## Plan (V1) selon le recul depuis le plus haut
| Recul | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| -50 à -35 % | 350 | 54.0 | 0.209 | 0.148 | 1.62 | 2.96 | 8.9 | 8 |
| -35 à -25 % | 440 | 50.9 | 0.072 | 0.018 | 1.19 | 1.04 | 8.6 | 12 |
| -25 à -20 % | 504 | 49.0 | 0.157 | -0.064 | 1.34 | 2.43 | 7.6 | 8 |
| -20 à -15 % | 681 | 47.4 | 0.122 | -0.165 | 1.34 | 2.51 | 7.1 | 7 |
| -15 à -10 % | 1326 | 44.6 | 0.062 | -0.382 | 1.11 | 0.87 | 6.7 | 14 |

## Plan (V1) par secteur
| Secteur | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
|  | 75 | 45.3 | 0.146 | -0.218 | 1.37 | 3.9 | 5.9 | 5 |
| Communication Services | 158 | 44.3 | 0.16 | -0.307 | 1.54 | 4.27 | 7.4 | 8 |
| Consumer Discretionary | 383 | 45.2 | 0.06 | -0.292 | 1.12 | 0.94 | 7.2 | 6 |
| Consumer Staples | 200 | 47.0 | 0.053 | -0.113 | 1.09 | 0.6 | 7.4 | 11 |
| Energy | 200 | 52.0 | 0.225 | 0.096 | 1.4 | 2.82 | 8.0 | 7 |
| Financials | 451 | 49.4 | 0.068 | -0.041 | 1.16 | 1.0 | 8.0 | 8 |
| Health Care | 303 | 49.5 | 0.146 | -0.053 | 1.35 | 2.12 | 7.5 | 12 |
| Industrials | 423 | 49.4 | 0.11 | -0.03 | 1.24 | 1.56 | 7.5 | 8 |
| Information Technology | 637 | 46.8 | 0.124 | -0.235 | 1.26 | 2.16 | 7.2 | 9 |
| Materials | 168 | 50.0 | 0.192 | 0.018 | 1.41 | 2.79 | 6.8 | 6 |
| Real Estate | 173 | 40.5 | -0.065 | -0.353 | 0.82 | -1.22 | 7.1 | 5 |
| Utilities | 130 | 50.0 | 0.098 | -0.021 | 1.24 | 1.43 | 7.6 | 4 |

## Raisons de sortie (plan, V1)
| Raison | Trades | R moyen |
|---|---|---|
| T2 | 299 | 2.21 |
| durée max | 12 | 1.16 |
| stop | 1183 | -1.00 |
| stop (gap) | 155 | -1.21 |
| stop temps | 755 | -0.02 |
| suiveur/BE | 744 | 1.32 |
| veille résultats | 153 | 0.52 |

## Entonnoir des signaux
| Famille | Signaux | Résultats trop proches | Stop > 2 ATR | < 2 actions | Ordre non exécuté | Trades |
|---|---|---|---|---|---|---|
| plan | 13028 | 1647 | 218 | 5362 | 2500 | 3301 |
| plan31 | 8386 | 1164 | 648 | 2606 | 1449 | 2519 |
| r2_large | 2989 | 321 | 618 | 403 | 386 | 1261 |
| zone | 22729 | 4446 | 0 | 8611 | 0 | 9672 |
| panique | 2263 | 393 | 31 | 268 | 0 | 1571 |

## Compte de 2 000 $ simulé (plafonds de risque, 2 lignes par secteur, cash)
| Scénario | Période | Valeur finale | Perf. | Drawdown max | Trades/mois | Positions moy. | SPY |
|---|---|---|---|---|---|---|---|
| v3.1 actuelle (sorties V1) | 5 ans | 5060 $ | +153.0 % | -9.9 % | 13.9 | 4.02 | +73.2 % (dd -24.5 %) |
| v3.1 actuelle (sorties V1) | 2 ans | 3427 $ | +71.4 % | -13.0 % | 14.1 | 3.91 | +29.8 % (dd -18.8 %) |
| v3.1 avec gestion position (V4) | 5 ans | 5210 $ | +160.5 % | -11.0 % | 9.1 | 5.33 | +73.2 % (dd -24.5 %) |
| v3.1 avec gestion position (V4) | 2 ans | 3145 $ | +57.2 % | -11.2 % | 8.0 | 4.57 | +29.8 % (dd -18.8 %) |
| Panique seule (V4) | 5 ans | 2198 $ | +9.9 % | -35.2 % | 2.3 | 1.1 | +73.2 % (dd -24.5 %) |
| Panique seule (V4) | 2 ans | 1958 $ | -2.1 % | -22.8 % | 2.3 | 0.97 | +29.8 % (dd -18.8 %) |
| Panique seule, stop sur clôture (V5) | 5 ans | 2558 $ | +27.9 % | -21.3 % | 2.2 | 1.28 | +73.2 % (dd -24.5 %) |
| Panique seule, stop sur clôture (V5) | 2 ans | 1756 $ | -12.2 % | -29.9 % | 2.0 | 0.98 | +29.8 % (dd -18.8 %) |
| v4 : panique + v3.1 (V4) | 5 ans | 4335 $ | +116.7 % | -20.8 % | 9.5 | 5.11 | +73.2 % (dd -24.5 %) |
| v4 : panique + v3.1 (V4) | 2 ans | 2769 $ | +38.5 % | -21.0 % | 9.1 | 4.79 | +29.8 % (dd -18.8 %) |
| v4 : panique + v3.1, stop sur clôture (V5) | 5 ans | 4389 $ | +119.4 % | -32.2 % | 7.8 | 4.93 | +73.2 % (dd -24.5 %) |
| v4 : panique + v3.1, stop sur clôture (V5) | 2 ans | 2771 $ | +38.6 % | -27.3 % | 8.5 | 5.01 | +29.8 % (dd -18.8 %) |

## Limites
- Univers actuel des indices : biais du survivant, plutôt favorable.
- Pas de filtre sur la cause de la baisse (fondamental) : en réel, une partie des pertes serait évitée, mais aussi quelques gains.
- Pas de frais ni de glissement hors gaps.
- Stop et objectif touchés la même séance : le stop est compté (prudent).
