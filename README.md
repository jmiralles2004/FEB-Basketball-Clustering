# Basketball Player Clustering - FEB Liga EBA

Anàlisi i segmentació automàtica de 1.816 jugadors de bàsquet mitjançant Machine Learning no supervisat

Projecte d'anàlisi de dades esportives que aplica **K-Means clustering** i **PCA** a estadístiques reals de la **Federació Espanyola de Bàsquet** (Temporada 2024-2025, Liga EBA). Identifica perfils de jugadors basant-se en rendiment, eficiència i estil de joc.

---

## Taula de Continguts

- [Resultats Principals](#-resultats-principals)
- [Estructura del Projecte](#-estructura-del-projecte)
- [Instal·lació](#-installació)
- [Ús Ràpid](#-ús-ràpid)
- [Tecnologies](#-tecnologies)

---

## Resultats Principals

### 5 Perfils de Jugadors Identificats

| Clúster | Perfil | Jugadors | % | Caracterització |
|---------|--------|----------|---|-----------------|
| C0 | Role Players Limitats | 241 | 13% | Baix volum, rol secundari |
| C1 | Jugadors Interiors | 333 | 18% | Predomini zona pintada |
| C2 | Bases Creadors | 454 | 25% | Alta creació de joc + anotació |
| C3 | Pivots Dominants | 338 | 19% | Rebots + taps + joc interior |
| C4 | Tiradors Exteriors | 450 | 25% | Especialització en tir de 3 |

### Mètriques de Validació

- **Silhouette Score**: 0.135 (estructura moderada)
- **Estabilitat** (50 execucions): ARI = 0.975 (assignacions consistents)
- **PCA**: 54.2% variància en 2 components | 80% amb 7 components

---

## Estructura del Projecte

```
ProjecteClustering/
├── data/processed/          # Dades processades i resultats
├── notebooks/               # Anàlisi Jupyter notebooks
├── reports/figures/         # Visualitzacions generades
├── src/                     # Codi font modular
└── requirements.txt         # Dependències
```

### `/data/processed/`

Fitxers CSV generats pel pipeline:

| Fitxer | Dimensions | Contingut |
|--------|-----------|-----------|
| `players_aggregated.csv` | 1816 × 27 | Features clustering + EDA + info jugador |
| `players_features_raw.csv` | 1816 × 20 | Features sense normalitzar |
| `players_features_scaled.csv` | 1816 × 22 | Features normalitzades (entrada clustering) |
| `players_clustered.csv` | 1816 × 23 | Amb assignació de clúster |
| `player_clusters.csv` | 1816 × 4 | Resum jugador-clúster |

### `/notebooks/`

Notebooks Jupyter amb tot el workflow:

| Notebook | Contingut |
|----------|-----------|
| `01_ETL_EDA.ipynb` | Extracció MongoDB, neteja, feature engineering, EDA |
| `02_Clustering.ipynb` | K-Means, selecció K òptim, PCA, validació estabilitat |
| `03_Visualization.ipynb` | Radar charts, heatmaps, t-SNE, shot charts |

### `/reports/`

Resultats finals del projecte:

- **`cluster_summary.csv`**: Estadístiques descriptives per clúster
- **`figures/`**: Visualitzacions automàtiques
  - `radar_charts.png` - Perfils de clústers
  - `shot_heatmaps_by_cluster.png` - Zones de tir
  - `pca_variance.png` - Scree plot i variància PCA
  - `tsne_visualization.png` - Projeccions 2D/3D
  - `silhouette_per_sample.png` - Qualitat assignacions
  - `cluster_stability.png` - Validació amb 50 seeds
  - Més visualitzacions comparatives...

### `/src/`

Codi modular organitzat per responsabilitats (SOLID):

```
src/
├── config.py                # Configuració centralitzada
├── main.py                  # Punt d'entrada
├── database/
│   └── mongo_client.py      # Connexió MongoDB
├── data_processing/
│   ├── data_loader.py       # Càrrega dades
│   ├── data_cleaner.py      # Neteja i validació
│   ├── feature_engineer.py  # Creació features avançades
│   └── data_aggregator.py   # Agregació per jugador
├── preprocessing/
│   └── scaler.py            # Normalització (StandardScaler)
├── pipeline/
│   └── etl_pipeline.py      # Orquestració ETL complet
└── utils/
    ├── file_handler.py      # Gestió fitxers
    └── logger.py            # Sistema logging
```

**Principis aplicats:**
- **SRP**: Cada mòdul una única responsabilitat
- **DRY**: Zero duplicació de lògica
- **KISS**: Funcions petites i comprensibles

---

## Tecnologies

| Categoria | Tecnologies |
|-----------|------------|
| **Dades** | `pandas`, `numpy`, `pymongo` |
| **ML** | `scikit-learn` (K-Means, PCA, t-SNE, StandardScaler) |
| **Visualització** | `matplotlib`, `seaborn` |
| **Notebooks** | `jupyter`, `notebook` |
| **Testing** | `pytest` |

### Features Clau (20 variables clustering)

- **Per 36 min**: `pts`, `ast`, `trb`, `stl`, `blk`, `tov`, `fga`, `2pa`, `3pa`
- **Percentatges**: `fg2_pct`, `fg3_pct`, `ft_pct`, `true_shooting_pct`
- **Estil joc**: `usage_2p`, `usage_3p`
- **Eficiència**: `oer` (ofensiva), `der` (defensiva)
- **Altres**: `orb`, `drb`, `pf`

*Nota*: 4 features addicionals (`interior_pct`, `interior_freq`, `exterior_pct`, `exterior_freq`) per EDA però excloses del clustering per alta correlació.

---

## Highlights del Projecte

**1.816 jugadors** analitzats  
**20 features** enginyeritzades amb mètriques NBA-style  
**5 perfils** clarament diferenciats  
**Validació robusta** amb 50 seeds aleatoris  
**12+ visualitzacions** automàtiques  
**Arquitectura SOLID** modular i escalable