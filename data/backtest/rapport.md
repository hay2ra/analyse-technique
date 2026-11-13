# Backtest des règles swing v3
Généré le 13/11/2026 15:55 — 514 titres (S&P 500 + Nasdaq 100 actuels), signaux du 2021-11-13 au 2026-11-13.
Dates de résultats connues pour 514 titres sur 514.

## Résultats par setup — V1 : plan v3 (moitié à 1,5R, suiveur plus bas veille, 2,5R)

### Sur 5 ans
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 1778 | 45.6 | 0.11 | -0.368 | 1.22 | 1.91 | 6.4 | 11 |
| R2 | 50 | 56.0 | 0.125 | 0.128 | 1.49 | 3.06 | 7.9 | 4 |
| R3 (demi-taille) | 1473 | 49.9 | 0.101 | -0.003 | 1.26 | 1.4 | 8.6 | 13 |
| **R1+R2+R3 (v3)** | 3301 | 47.7 | 0.106 | -0.131 | 1.24 | 1.7 | 7.4 | 9 |
| v3.1 R1 (recul ≥ 15 %) | 701 | 47.4 | 0.158 | -0.255 | 1.37 | 3.23 | 6.3 | 9 |
| v3.1 R2 (sans tendance) | 1128 | 49.6 | 0.137 | -0.012 | 1.32 | 2.24 | 7.6 | 8 |
| v3.1 R3 (en correction) | 690 | 54.6 | 0.171 | 0.17 | 1.47 | 2.38 | 8.8 | 7 |
| **v3.1 total (sans REIT)** | 2519 | 50.3 | 0.152 | 0.022 | 1.37 | 2.56 | 7.6 | 10 |
| **Panique (leaders au rebond)** | 1579 | 52.4 | 0.109 | 0.062 | 1.27 | 3.18 | 7.4 | 11 |
| Témoin R2 large | 1261 | 49.6 | 0.138 | -0.013 | 1.32 | 2.2 | 7.6 | 11 |
| Témoin Zone sans setup | 9684 | 46.4 | 0.053 | -0.192 | 1.12 | 1.15 | 7.3 | 13 |

### Sur les 2 dernières années
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 727 | 47.0 | 0.16 | -0.247 | 1.4 | 3.44 | 6.2 | 11 |
| R2 | 23 | 43.5 | -0.188 | -0.401 | 0.69 | -2.77 | 7.4 | 3 |
| R3 (demi-taille) | 558 | 46.2 | 0.077 | -0.142 | 1.19 | 1.1 | 8.3 | 9 |
| **R1+R2+R3 (v3)** | 1308 | 46.6 | 0.119 | -0.19 | 1.31 | 2.33 | 7.1 | 10 |
| v3.1 R1 (recul ≥ 15 %) | 310 | 50.0 | 0.244 | -0.02 | 1.61 | 5.42 | 6.0 | 9 |
| v3.1 R2 (sans tendance) | 451 | 48.6 | 0.069 | -0.042 | 1.18 | 1.24 | 7.4 | 9 |
| v3.1 R3 (en correction) | 215 | 52.6 | 0.163 | 0.15 | 1.41 | 2.23 | 8.3 | 6 |
| **v3.1 total (sans REIT)** | 976 | 49.9 | 0.145 | -0.004 | 1.38 | 2.79 | 7.2 | 10 |
| **Panique (leaders au rebond)** | 559 | 54.4 | 0.046 | 0.092 | 1.12 | 1.38 | 7.5 | 6 |
| Témoin R2 large | 516 | 48.8 | 0.081 | -0.026 | 1.2 | 1.36 | 7.4 | 9 |
| Témoin Zone sans setup | 3880 | 47.4 | 0.077 | -0.122 | 1.19 | 1.75 | 7.3 | 12 |

## Résultats par setup — V2 : moitié à 1,5R puis clôture sous EMA10

### Sur 5 ans
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 1778 | 45.5 | 0.111 | -0.378 | 1.22 | 1.92 | 6.9 | 11 |
| R2 | 50 | 56.0 | 0.088 | 0.128 | 1.37 | 2.29 | 8.3 | 4 |
| R3 (demi-taille) | 1473 | 49.9 | 0.104 | -0.003 | 1.27 | 1.44 | 9.3 | 13 |
| **R1+R2+R3 (v3)** | 3301 | 47.6 | 0.107 | -0.135 | 1.24 | 1.71 | 8.0 | 9 |
| v3.1 R1 (recul ≥ 15 %) | 701 | 47.4 | 0.177 | -0.255 | 1.41 | 3.6 | 6.9 | 9 |
| v3.1 R2 (sans tendance) | 1128 | 49.6 | 0.15 | -0.012 | 1.35 | 2.42 | 8.1 | 8 |
| v3.1 R3 (en correction) | 690 | 54.6 | 0.177 | 0.17 | 1.48 | 2.44 | 9.5 | 7 |
| **v3.1 total (sans REIT)** | 2519 | 50.3 | 0.165 | 0.022 | 1.4 | 2.76 | 8.2 | 10 |
| **Panique (leaders au rebond)** | 1579 | 52.4 | 0.108 | 0.062 | 1.26 | 3.13 | 7.8 | 11 |
| Témoin R2 large | 1261 | 49.6 | 0.147 | -0.013 | 1.34 | 2.34 | 8.1 | 11 |
| Témoin Zone sans setup | 9684 | 46.4 | 0.052 | -0.195 | 1.12 | 1.1 | 7.9 | 13 |

### Sur les 2 dernières années
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 727 | 47.0 | 0.166 | -0.247 | 1.41 | 3.59 | 6.8 | 11 |
| R2 | 23 | 43.5 | -0.199 | -0.401 | 0.64 | -3.19 | 8.0 | 3 |
| R3 (demi-taille) | 558 | 46.2 | 0.073 | -0.142 | 1.18 | 1.02 | 8.9 | 9 |
| **R1+R2+R3 (v3)** | 1308 | 46.6 | 0.12 | -0.19 | 1.32 | 2.37 | 7.7 | 10 |
| v3.1 R1 (recul ≥ 15 %) | 310 | 50.0 | 0.258 | -0.02 | 1.66 | 5.86 | 6.6 | 9 |
| v3.1 R2 (sans tendance) | 451 | 48.6 | 0.093 | -0.042 | 1.23 | 1.64 | 8.0 | 9 |
| v3.1 R3 (en correction) | 215 | 52.6 | 0.153 | 0.15 | 1.38 | 2.08 | 9.0 | 6 |
| **v3.1 total (sans REIT)** | 976 | 49.9 | 0.159 | -0.004 | 1.42 | 3.08 | 7.8 | 10 |
| **Panique (leaders au rebond)** | 559 | 54.4 | 0.04 | 0.092 | 1.11 | 1.21 | 7.7 | 6 |
| Témoin R2 large | 516 | 48.8 | 0.101 | -0.026 | 1.25 | 1.71 | 8.0 | 9 |
| Témoin Zone sans setup | 3880 | 47.4 | 0.077 | -0.122 | 1.18 | 1.7 | 7.9 | 12 |

## Résultats par setup — V3 : tout à 2R

### Sur 5 ans
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 1778 | 42.1 | 0.11 | -0.657 | 1.2 | 1.81 | 6.8 | 11 |
| R2 | 50 | 56.0 | 0.12 | 0.128 | 1.44 | 2.73 | 8.4 | 4 |
| R3 (demi-taille) | 1473 | 48.9 | 0.112 | -0.042 | 1.28 | 1.56 | 9.0 | 13 |
| **R1+R2+R3 (v3)** | 3301 | 45.3 | 0.111 | -0.219 | 1.23 | 1.71 | 7.8 | 12 |
| v3.1 R1 (recul ≥ 15 %) | 701 | 43.8 | 0.175 | -0.519 | 1.37 | 3.43 | 6.8 | 9 |
| v3.1 R2 (sans tendance) | 1128 | 47.1 | 0.135 | -0.09 | 1.29 | 2.1 | 8.0 | 12 |
| v3.1 R3 (en correction) | 690 | 53.5 | 0.187 | 0.138 | 1.51 | 2.61 | 9.1 | 7 |
| **v3.1 total (sans REIT)** | 2519 | 47.9 | 0.16 | -0.085 | 1.36 | 2.61 | 7.9 | 10 |
| **Panique (leaders au rebond)** | 1579 | 50.2 | 0.1 | 0.004 | 1.22 | 2.7 | 7.8 | 11 |
| Témoin R2 large | 1261 | 47.1 | 0.136 | -0.088 | 1.29 | 2.05 | 8.0 | 11 |
| Témoin Zone sans setup | 9684 | 44.2 | 0.054 | -0.278 | 1.12 | 1.14 | 7.8 | 19 |

### Sur les 2 dernières années
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 727 | 42.9 | 0.16 | -0.587 | 1.37 | 3.4 | 6.6 | 11 |
| R2 | 23 | 43.5 | -0.234 | -0.401 | 0.56 | -3.99 | 8.2 | 3 |
| R3 (demi-taille) | 558 | 45.7 | 0.1 | -0.16 | 1.24 | 1.41 | 8.5 | 9 |
| **R1+R2+R3 (v3)** | 1308 | 44.1 | 0.128 | -0.282 | 1.31 | 2.42 | 7.5 | 10 |
| v3.1 R1 (recul ≥ 15 %) | 310 | 46.1 | 0.284 | -0.235 | 1.65 | 6.07 | 6.4 | 9 |
| v3.1 R2 (sans tendance) | 451 | 45.5 | 0.082 | -0.15 | 1.17 | 1.27 | 7.7 | 9 |
| v3.1 R3 (en correction) | 215 | 52.1 | 0.191 | 0.133 | 1.48 | 2.62 | 8.5 | 6 |
| **v3.1 total (sans REIT)** | 976 | 47.1 | 0.17 | -0.122 | 1.41 | 3.09 | 7.5 | 10 |
| **Panique (leaders au rebond)** | 559 | 52.4 | 0.035 | 0.043 | 1.07 | 0.84 | 7.8 | 6 |
| Témoin R2 large | 516 | 45.9 | 0.097 | -0.14 | 1.2 | 1.42 | 7.7 | 9 |
| Témoin Zone sans setup | 3880 | 45.4 | 0.084 | -0.196 | 1.19 | 1.83 | 7.8 | 13 |

## Résultats par setup — V4 : position : moitié à 2R, reste tenu jusqu'à clôture sous EMA20, 60 séances max

### Sur 5 ans
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 1778 | 39.1 | 0.138 | -1.0 | 1.25 | 2.55 | 11.8 | 11 |
| R2 | 50 | 48.0 | 0.227 | -0.082 | 1.7 | 5.27 | 14.0 | 4 |
| R3 (demi-taille) | 1473 | 44.2 | 0.128 | -0.518 | 1.26 | 1.82 | 14.8 | 9 |
| **R1+R2+R3 (v3)** | 3301 | 41.5 | 0.135 | -1.0 | 1.26 | 2.27 | 13.1 | 15 |
| v3.1 R1 (recul ≥ 15 %) | 701 | 41.4 | 0.219 | -1.0 | 1.48 | 4.94 | 12.1 | 9 |
| v3.1 R2 (sans tendance) | 1128 | 42.5 | 0.106 | -1.0 | 1.19 | 1.74 | 12.7 | 19 |
| v3.1 R3 (en correction) | 690 | 45.7 | 0.172 | -0.504 | 1.35 | 2.45 | 14.3 | 8 |
| **v3.1 total (sans REIT)** | 2519 | 43.0 | 0.156 | -1.0 | 1.32 | 2.82 | 13.0 | 13 |
| **Panique (leaders au rebond)** | 1579 | 43.4 | 0.101 | -0.678 | 1.19 | 2.8 | 12.2 | 11 |
| Témoin R2 large | 1261 | 42.5 | 0.106 | -1.0 | 1.19 | 1.68 | 12.7 | 21 |
| Témoin Zone sans setup | 9684 | 39.7 | 0.071 | -1.0 | 1.14 | 1.59 | 13.1 | 19 |

### Sur les 2 dernières années
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 727 | 40.2 | 0.218 | -1.0 | 1.47 | 4.83 | 11.8 | 8 |
| R2 | 23 | 39.1 | 0.086 | -1.0 | 1.33 | 3.52 | 13.3 | 3 |
| R3 (demi-taille) | 558 | 45.5 | 0.144 | -0.442 | 1.3 | 2.06 | 14.5 | 10 |
| **R1+R2+R3 (v3)** | 1308 | 42.4 | 0.184 | -1.0 | 1.41 | 3.63 | 13.0 | 9 |
| v3.1 R1 (recul ≥ 15 %) | 310 | 43.2 | 0.347 | -1.0 | 1.75 | 7.83 | 12.3 | 9 |
| v3.1 R2 (sans tendance) | 451 | 41.7 | 0.065 | -1.0 | 1.11 | 0.97 | 11.9 | 11 |
| v3.1 R3 (en correction) | 215 | 48.4 | 0.181 | -0.195 | 1.4 | 2.59 | 14.0 | 7 |
| **v3.1 total (sans REIT)** | 976 | 43.6 | 0.18 | -1.0 | 1.39 | 3.51 | 12.5 | 10 |
| **Panique (leaders au rebond)** | 559 | 45.3 | 0.07 | -0.252 | 1.1 | 1.47 | 11.6 | 8 |
| Témoin R2 large | 516 | 42.6 | 0.076 | -1.0 | 1.12 | 1.11 | 11.9 | 12 |
| Témoin Zone sans setup | 3880 | 41.5 | 0.151 | -1.0 | 1.3 | 3.36 | 13.4 | 14 |

## Résultats par setup — V5 : position avec stop sur clôture (au lieu d'en séance)

### Sur 5 ans
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 1778 | 44.9 | 0.129 | -0.734 | 1.24 | 2.74 | 13.5 | 10 |
| R2 | 50 | 50.0 | 0.197 | -0.012 | 1.53 | 4.53 | 15.5 | 4 |
| R3 (demi-taille) | 1473 | 48.9 | 0.154 | -0.07 | 1.3 | 2.18 | 16.0 | 9 |
| **R1+R2+R3 (v3)** | 3301 | 46.7 | 0.141 | -0.29 | 1.26 | 2.52 | 14.6 | 13 |
| v3.1 R1 (recul ≥ 15 %) | 701 | 47.4 | 0.242 | -0.378 | 1.52 | 5.94 | 14.0 | 8 |
| v3.1 R2 (sans tendance) | 1128 | 49.2 | 0.148 | -0.053 | 1.23 | 2.33 | 14.6 | 7 |
| v3.1 R3 (en correction) | 690 | 50.7 | 0.223 | 0.036 | 1.44 | 3.12 | 15.5 | 8 |
| **v3.1 total (sans REIT)** | 2519 | 49.1 | 0.194 | -0.077 | 1.37 | 3.55 | 14.7 | 10 |
| **Panique (leaders au rebond)** | 1579 | 49.1 | 0.111 | -0.045 | 1.17 | 2.81 | 13.8 | 7 |
| Témoin R2 large | 1261 | 48.9 | 0.139 | -0.106 | 1.21 | 2.13 | 14.5 | 10 |
| Témoin Zone sans setup | 9684 | 45.2 | 0.096 | -0.344 | 1.18 | 2.15 | 14.9 | 19 |

### Sur les 2 dernières années
| Setup | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| R1 | 727 | 45.9 | 0.237 | -0.483 | 1.48 | 5.6 | 13.7 | 8 |
| R2 | 23 | 43.5 | 0.088 | -1.045 | 1.23 | 2.76 | 15.0 | 2 |
| R3 (demi-taille) | 558 | 50.0 | 0.159 | -0.012 | 1.31 | 2.23 | 15.7 | 10 |
| **R1+R2+R3 (v3)** | 1308 | 47.6 | 0.201 | -0.206 | 1.42 | 4.11 | 14.6 | 9 |
| v3.1 R1 (recul ≥ 15 %) | 310 | 49.4 | 0.436 | -0.067 | 1.9 | 10.15 | 14.6 | 7 |
| v3.1 R2 (sans tendance) | 451 | 48.6 | 0.092 | -0.079 | 1.1 | 1.09 | 13.8 | 10 |
| v3.1 R3 (en correction) | 215 | 53.0 | 0.177 | 0.16 | 1.36 | 2.52 | 15.0 | 7 |
| **v3.1 total (sans REIT)** | 976 | 49.8 | 0.22 | -0.006 | 1.43 | 4.28 | 14.3 | 10 |
| **Panique (leaders au rebond)** | 559 | 50.3 | 0.031 | 0.012 | 0.99 | -0.21 | 12.9 | 7 |
| Témoin R2 large | 516 | 49.0 | 0.103 | -0.05 | 1.12 | 1.24 | 13.7 | 8 |
| Témoin Zone sans setup | 3880 | 47.8 | 0.204 | -0.156 | 1.37 | 4.48 | 15.3 | 14 |

## Plan R1+R2+R3 (V1) par année
| Année | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| 2021 | 49 | 38.8 | -0.051 | -1.0 | 0.79 | -2.13 | 7.3 | 6 |
| 2022 | 697 | 49.5 | 0.109 | -0.04 | 1.21 | 1.44 | 7.8 | 6 |
| 2023 | 733 | 49.5 | 0.099 | -0.042 | 1.2 | 1.28 | 7.7 | 9 |
| 2024 | 575 | 45.0 | 0.087 | -0.282 | 1.16 | 1.2 | 7.2 | 13 |
| 2025 | 736 | 47.4 | 0.135 | -0.144 | 1.42 | 2.94 | 7.2 | 8 |
| 2026 | 511 | 46.8 | 0.107 | -0.191 | 1.22 | 1.78 | 7.0 | 9 |

## Plan (V1) selon le marché au signal
| Marché | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| SPY et QQQ au-dessus de l'EMA50 | 2020 | 44.4 | 0.061 | -0.296 | 1.13 | 0.99 | 7.1 | 12 |
| SPY ou QQQ sous l'EMA50 | 1281 | 52.9 | 0.177 | 0.125 | 1.44 | 2.81 | 7.9 | 11 |

## Plan (V1) selon le score de setup du scan
| Score | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| 0-4 | 575 | 49.4 | 0.076 | -0.024 | 1.2 | 1.13 | 8.5 | 9 |
| 5-6 | 647 | 50.1 | 0.125 | 0.007 | 1.31 | 1.71 | 8.4 | 8 |
| 7-8 | 1499 | 46.7 | 0.108 | -0.243 | 1.21 | 1.68 | 6.8 | 12 |
| 9-10 | 580 | 45.9 | 0.109 | -0.246 | 1.27 | 2.3 | 6.9 | 12 |

## Plan (V1) selon le recul depuis le plus haut
| Recul | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
| -50 à -35 % | 350 | 54.0 | 0.209 | 0.148 | 1.62 | 2.96 | 8.9 | 8 |
| -35 à -25 % | 440 | 50.9 | 0.072 | 0.018 | 1.19 | 1.04 | 8.6 | 12 |
| -25 à -20 % | 505 | 48.9 | 0.153 | -0.07 | 1.33 | 2.39 | 7.6 | 8 |
| -20 à -15 % | 682 | 47.4 | 0.121 | -0.166 | 1.33 | 2.49 | 7.1 | 7 |
| -15 à -10 % | 1324 | 44.6 | 0.064 | -0.374 | 1.11 | 0.91 | 6.7 | 14 |

## Plan (V1) par secteur
| Secteur | Trades | % gagnants | R moyen | R médian | Profit factor | $ moyen | Durée moy. | Pire série |
|---|---|---|---|---|---|---|---|---|
|  | 75 | 45.3 | 0.146 | -0.218 | 1.37 | 3.9 | 5.9 | 5 |
| Communication Services | 157 | 44.6 | 0.168 | -0.273 | 1.55 | 4.38 | 7.5 | 8 |
| Consumer Discretionary | 383 | 45.2 | 0.061 | -0.292 | 1.12 | 0.95 | 7.3 | 6 |
| Consumer Staples | 200 | 47.0 | 0.053 | -0.113 | 1.09 | 0.6 | 7.4 | 11 |
| Energy | 200 | 52.0 | 0.225 | 0.096 | 1.4 | 2.82 | 8.0 | 7 |
| Financials | 451 | 49.4 | 0.068 | -0.041 | 1.16 | 1.0 | 8.0 | 8 |
| Health Care | 303 | 49.5 | 0.146 | -0.053 | 1.35 | 2.12 | 7.5 | 12 |
| Industrials | 423 | 49.4 | 0.11 | -0.03 | 1.24 | 1.57 | 7.5 | 8 |
| Information Technology | 637 | 46.8 | 0.124 | -0.235 | 1.26 | 2.16 | 7.2 | 9 |
| Materials | 167 | 49.7 | 0.186 | -0.008 | 1.39 | 2.72 | 6.9 | 6 |
| Real Estate | 174 | 40.2 | -0.075 | -0.43 | 0.81 | -1.31 | 7.1 | 5 |
| Utilities | 131 | 50.4 | 0.112 | 0.009 | 1.27 | 1.59 | 7.5 | 4 |

## Raisons de sortie (plan, V1)
| Raison | Trades | R moyen |
|---|---|---|
| T2 | 300 | 2.21 |
| durée max | 12 | 1.16 |
| stop | 1183 | -1.00 |
| stop (gap) | 155 | -1.21 |
| stop temps | 755 | -0.02 |
| suiveur/BE | 743 | 1.32 |
| veille résultats | 153 | 0.52 |

## Entonnoir des signaux
| Famille | Signaux | Résultats trop proches | Stop > 2 ATR | < 2 actions | Ordre non exécuté | Trades |
|---|---|---|---|---|---|---|
| plan | 13037 | 1657 | 218 | 5363 | 2498 | 3301 |
| plan31 | 8396 | 1172 | 650 | 2607 | 1448 | 2519 |
| r2_large | 2990 | 320 | 619 | 404 | 386 | 1261 |
| zone | 22765 | 4453 | 0 | 8628 | 0 | 9684 |
| panique | 2258 | 379 | 32 | 268 | 0 | 1579 |
| plan31@A | 8396 | 1172 | 650 | 2607 | 1448 | 2519 |
| plan31@B | 8172 | 1150 | 638 | 2185 | 1540 | 2659 |
| plan31@C | 8300 | 1166 | 635 | 2325 | 1499 | 2675 |
| plan31@D | 8117 | 1147 | 632 | 2013 | 1567 | 2758 |

## Compte de 2 000 $ simulé (plafonds de risque, 2 lignes par secteur, cash)
| Scénario | Période | Valeur finale | Perf. | Drawdown max | Trades/mois | Positions moy. | SPY |
|---|---|---|---|---|---|---|---|
| v3.1 actuelle (sorties V1) | 5 ans | 5045 $ | +152.3 % | -9.9 % | 13.9 | 4.02 | +72.8 % (dd -24.5 %) |
| v3.1 actuelle (sorties V1) | 2 ans | 3437 $ | +71.9 % | -11.9 % | 14.1 | 3.9 | +29.4 % (dd -18.8 %) |
| v3.1 avec gestion position (V4) | 5 ans | 4691 $ | +134.5 % | -11.0 % | 9.2 | 5.26 | +72.8 % (dd -24.5 %) |
| v3.1 avec gestion position (V4) | 2 ans | 3158 $ | +57.9 % | -12.6 % | 7.9 | 4.55 | +29.4 % (dd -18.8 %) |
| Panique seule (V4) | 5 ans | 2170 $ | +8.5 % | -35.2 % | 2.3 | 1.11 | +72.8 % (dd -24.5 %) |
| Panique seule (V4) | 2 ans | 1911 $ | -4.5 % | -22.8 % | 2.3 | 0.99 | +29.4 % (dd -18.8 %) |
| Panique seule, stop sur clôture (V5) | 5 ans | 2514 $ | +25.7 % | -21.3 % | 2.2 | 1.29 | +72.8 % (dd -24.5 %) |
| Panique seule, stop sur clôture (V5) | 2 ans | 1724 $ | -13.8 % | -29.9 % | 2.1 | 1.0 | +29.4 % (dd -18.8 %) |
| v4 : panique + v3.1 (V4) | 5 ans | 4732 $ | +136.6 % | -20.8 % | 9.9 | 5.28 | +72.8 % (dd -24.5 %) |
| v4 : panique + v3.1 (V4) | 2 ans | 3064 $ | +53.2 % | -23.0 % | 9.1 | 4.85 | +29.4 % (dd -18.8 %) |
| v4 : panique + v3.1, stop sur clôture (V5) | 5 ans | 4578 $ | +128.9 % | -32.2 % | 7.9 | 4.94 | +72.8 % (dd -24.5 %) |
| v4 : panique + v3.1, stop sur clôture (V5) | 2 ans | 2780 $ | +39.0 % | -27.3 % | 8.5 | 5.01 | +29.4 % (dd -18.8 %) |

## Taille des positions (v3.1, sorties V1)
| Variante | Capital | Risque/trade | Plafond ligne | Période | Valeur finale | Perf. | DD max | Trades/mois | Positions moy. | Investi moyen |
|---|---|---|---|---|---|---|---|---|---|---|
| A | 2000 $ | 30 $ (15 $ R3) | 500 $ | 5 ans | 5045 $ | +152.3 % | -9.9 % | 13.9 | 4.02 | 1650 $ |
| A | 2000 $ | 30 $ (15 $ R3) | 500 $ | 2 ans | 3437 $ | +71.9 % | -11.9 % | 14.1 | 3.9 | 1607 $ |
| B | 2287 $ | 34 $ (17 $ R3) | 570 $ | 5 ans | 5248 $ | +129.5 % | -9.5 % | 14.2 | 4.07 | 1916 $ |
| B | 2287 $ | 34 $ (17 $ R3) | 570 $ | 2 ans | 3815 $ | +66.8 % | -12.3 % | 14.9 | 3.94 | 1880 $ |
| C | 2000 $ | 30 $ (15 $ R3) | 800 $ | 5 ans | 6419 $ | +221.0 % | -9.4 % | 11.0 | 3.25 | 1876 $ |
| C | 2000 $ | 30 $ (15 $ R3) | 800 $ | 2 ans | 3439 $ | +71.9 % | -12.4 % | 10.8 | 2.97 | 1673 $ |
| D | 2287 $ | 34 $ (17 $ R3) | 800 $ | 5 ans | 5928 $ | +159.2 % | -14.4 % | 11.1 | 3.17 | 1951 $ |
| D | 2287 $ | 34 $ (17 $ R3) | 800 $ | 2 ans | 4588 $ | +100.6 % | -11.2 % | 12.1 | 3.31 | 2057 $ |

## Limites
- Univers actuel des indices : biais du survivant, plutôt favorable.
- Pas de filtre sur la cause de la baisse (fondamental) : en réel, une partie des pertes serait évitée, mais aussi quelques gains.
- Pas de frais ni de glissement hors gaps.
- Stop et objectif touchés la même séance : le stop est compté (prudent).
