"""
Configuració general del projecte.
Centralitza totes les constants i paràmetres configurables.
"""
from pathlib import Path


# Configuració de MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "feb_db"
COLLECTION_PLAYERS_STATS = "FEB3_players_statistics"
COLLECTION_TEAMS_STATS = "FEB3_teams_statistics"
COLLECTION_PLAYERS_SHOTS = "FEB3_players_shots"

# Filtres de dades
DEFAULT_SEASON = "2024-2025"
DEFAULT_COMPETITION = "Liga EBA"
MIN_GAMES_THRESHOLD = 5
MIN_MINUTES_THRESHOLD = 0

# Feature Engineering
SECONDS_PER_MINUTE = 60
MINUTES_NORMALIZATION = 36
STATS_TO_NORMALIZE = [
    'pts', 'ast', 'trb', 'stl', 'blk', 'tov',
    'fga', 'fgm', '3pa', '3pm', '2pa', '2pm', 'fta', 'ftm'
]

# Coeficients per càlcul de possessions i eficiències
FREE_THROW_POSSESSION_FACTOR = 0.44  # Factor estàndard per FTA en possessions
EFFICIENCY_MULTIPLIER = 100  # Multiplicador per OER/DER (per 100 possessions)

# Zones de tir interior (PC=Pintura Central, PL/PR=Pintura Lateral, MBL/MBR=Mitja-Baixa)
INTERIOR_ZONES_MADE = ['rc_pc_m', 'rc_pl_m', 'rc_pr_m', 'rc_mbl_m', 'rc_mbr_m']
INTERIOR_ZONES_ATTEMPTED = ['rc_pc_a', 'rc_pl_a', 'rc_pr_a', 'rc_mbl_a', 'rc_mbr_a']

# Zones de tir exterior (MEL/MER=Mitja-Exterior, C3L/C3R=Cantonada 3, Ce3L/Ce3R=Centre 3, E3L/E3R=Esquerra/Dreta 3)
EXTERIOR_ZONES_MADE = ['rc_mel_m', 'rc_mer_m', 'rc_c3l_m', 'rc_c3r_m', 'rc_ce3l_m', 'rc_ce3r_m', 'rc_e3l_m', 'rc_e3r_m']
EXTERIOR_ZONES_ATTEMPTED = ['rc_mel_a', 'rc_mer_a', 'rc_c3l_a', 'rc_c3r_a', 'rc_ce3l_a', 'rc_ce3r_a', 'rc_e3l_a', 'rc_e3r_a']

# Features per clustering
# NOTA: interior_pct eliminada (r=0.97 amb fg2_pct - multicolinealitat severa)
# NOTA: interior_freq eliminada (r=0.92 amb usage_2p - duplicació)
FEATURES_FOR_CLUSTERING = [
    'pts_per36', 'ast_per36', 'trb_per36', 'stl_per36', 'blk_per36', 'tov_per36',
    'fga_per36', '3pa_per36', '2pa_per36',
    'fg2_pct', 'fg3_pct', 'ft_pct',
    'usage_2p', 'usage_3p',
    'oer', 'der', 'true_shooting_pct',  # Métriques avançades (ofensiva, defensiva, eficàcia)
    'orb', 'drb', 'pf'
]

# Features addicionals per EDA/visualització (NO s'inclouen al clustering per multicolinealitat)
# interior_pct: r=0.91 amb fg2_pct | exterior_pct: r=0.81 amb fg3_pct
# interior_freq: r=0.73 amb usage_2p | exterior_freq: r=0.63 amb usage_3p
FEATURES_FOR_EDA = [
    'interior_pct', 'interior_freq',
    'exterior_pct', 'exterior_freq',
]

# Rutes del projecte
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
RAW_DATA_DIR = DATA_DIR / "raw"
MODELS_DIR = BASE_DIR / "models"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"

# Noms dels arxius de sortida
OUTPUT_SCALED_FILE = "players_features_scaled.csv"
OUTPUT_RAW_FILE = "players_features_raw.csv"
OUTPUT_AGGREGATED_FILE = "players_aggregated.csv"

# Configuració de visualització
PLOT_STYLE = 'seaborn-v0_8-darkgrid'
PLOT_PALETTE = 'husl'
PLOT_FIGSIZE_SMALL = (10, 6)
PLOT_FIGSIZE_MEDIUM = (15, 10)
PLOT_FIGSIZE_LARGE = (16, 14)

# Configuració de normalització
SCALER_TYPE = "standard"  # "standard" o "minmax"
HANDLE_INFINITY = True
FILL_NA_VALUE = 0

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
