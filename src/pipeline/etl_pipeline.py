"""
Pipeline complet d'ETL.
Principi SRP: Orquestra el procés complet d'ETL.
Principi DRY: Evita duplicació usant els mòduls especialitzats.
"""
import pandas as pd
from typing import Dict, Optional
import logging

from ..database import MongoDBClient
from ..data_processing import DataLoader, DataCleaner, FeatureEngineer, DataAggregator
from ..preprocessing import DataScaler
from ..utils import FileHandler
from ..config import (
    MONGO_URI, DB_NAME, DEFAULT_SEASON, DEFAULT_COMPETITION,
    MIN_GAMES_THRESHOLD, MIN_MINUTES_THRESHOLD, STATS_TO_NORMALIZE,
    INTERIOR_ZONES_MADE, INTERIOR_ZONES_ATTEMPTED,
    EXTERIOR_ZONES_MADE, EXTERIOR_ZONES_ATTEMPTED,
    FEATURES_FOR_CLUSTERING, FEATURES_FOR_EDA,
    MINUTES_NORMALIZATION, PROCESSED_DATA_DIR, OUTPUT_SCALED_FILE,
    OUTPUT_RAW_FILE, OUTPUT_AGGREGATED_FILE, SCALER_TYPE,
    HANDLE_INFINITY, FILL_NA_VALUE
)

logger = logging.getLogger(__name__)


class ETLPipeline:
    """Pipeline complet d'ETL per dades de jugadors."""
    
    def __init__(self, mongo_uri: str = MONGO_URI, db_name: str = DB_NAME):
        """
        Inicialitza el pipeline ETL.
        
        Args:
            mongo_uri: URI de MongoDB
            db_name: Nom de la base de dades
        """
        self.mongo_client = MongoDBClient(mongo_uri, db_name)
        self.data_loader = DataLoader(self.mongo_client)
        self.data_cleaner = DataCleaner()
        self.feature_engineer = FeatureEngineer()
        self.data_aggregator = DataAggregator()
        self.scaler = DataScaler(scaler_type=SCALER_TYPE)
        self.file_handler = FileHandler()
        
        logger.info("Pipeline ETL inicialitzat")
    
    def connect_database(self) -> bool:
        """
        Connecta a la base de dades.
        
        Returns:
            True si la connexió és exitosa
        """
        return self.mongo_client.connect()
    
    def extract(self, season: str = DEFAULT_SEASON, 
                competition: str = DEFAULT_COMPETITION) -> Dict[str, pd.DataFrame]:
        """
        Extreu dades de MongoDB (jugadors i equips).
        
        Args:
            season: Temporada a filtrar
            competition: Competició a filtrar
            
        Returns:
            Diccionari amb DataFrames de jugadors i equips
        """
        logger.info(f"Extraient dades: {season} - {competition}")
        
        query = {
            'season_id': season,
            'competition_name': competition,
            'minutes': {'$gt': 0}  # Filtrar minutes=0 a nivell de query (més eficient)
        }
        
        df_players = self.data_loader.load_players_statistics(query)
        logger.info(f"Extrets {len(df_players)} registres de jugadors")
        
        # Carregar estadístiques d'equips per calcular DER
        query_teams = {
            'season_id': season,
            'competition_name': competition
        }
        df_teams = self.data_loader.load_teams_statistics(query_teams)
        logger.info(f"Extrets {len(df_teams)} registres d'equips")
        
        return {'players': df_players, 'teams': df_teams}
    
    def transform(self, data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """
        Transforma les dades afegint DER (Defensive Efficiency Rating).
        
        Args:
            data: Diccionari amb DataFrames de jugadors i equips
            
        Returns:
            Diccionari amb DataFrames transformats
        """
        logger.info("Iniciant transformació de dades")
        
        df = data['players'].copy()
        df_teams = data['teams'].copy()
        
        # Calcular possessions dels equips
        from ..config import FREE_THROW_POSSESSION_FACTOR
        df_teams['team_possessions'] = (
            df_teams['fga'] + 
            (FREE_THROW_POSSESSION_FACTOR * df_teams['fta']) - 
            df_teams['orb'] + 
            df_teams['tov']
        )
        
        # Per cada partit, identificar el rival i les seves possessions
        opponent_data = []
        for match_id in df['match_feb_id'].unique():
            teams_in_match = df_teams[df_teams['match_feb_id'] == match_id]
            
            if len(teams_in_match) == 2:
                for idx, team_row in teams_in_match.iterrows():
                    opponent_row = teams_in_match[teams_in_match['team_feb_id'] != team_row['team_feb_id']].iloc[0]
                    opponent_data.append({
                        'match_feb_id': match_id,
                        'team_feb_id': team_row['team_feb_id'],
                        'opponent_possessions': opponent_row['team_possessions'],
                        'opponent_pts': opponent_row['pts']
                    })
        
        df_opponents = pd.DataFrame(opponent_data)
        
        # Merge amb dades de jugadors
        df = df.merge(df_opponents, on=['match_feb_id', 'team_feb_id'], how='left')
        logger.info("Dades de rivals afegides per càlcul de DER")
        
        # Neteja (minutes=0 ja filtrat a la query)
        df = self.data_cleaner.filter_by_games_played(df, MIN_GAMES_THRESHOLD)
        
        # Feature engineering
        df = self.feature_engineer.apply_all_transformations(
            df, 
            STATS_TO_NORMALIZE,
            INTERIOR_ZONES_MADE,
            INTERIOR_ZONES_ATTEMPTED,
            EXTERIOR_ZONES_MADE,
            EXTERIOR_ZONES_ATTEMPTED,
            MINUTES_NORMALIZATION
        )
        
        # Construir llista completa de features a agregar:
        # 1) FEATURES_FOR_CLUSTERING: 20 features per al model
        # 2) FEATURES_FOR_EDA: 4 features per anàlisi/visualització (no s'escalen)
        features_for_clustering = FEATURES_FOR_CLUSTERING.copy()
        
        # Validar DER
        if 'opponent_possessions' in df.columns and 'opponent_pts' in df.columns and 'der' in df.columns:
            if 'der' not in features_for_clustering:
                features_for_clustering.append('der')
        else:
            features_for_clustering = [f for f in features_for_clustering if f != 'der']
            logger.warning("DER no es pot calcular - dades de rivals no disponibles")
        
        # Features EDA: només les que existeixen al DataFrame
        features_for_eda = [f for f in FEATURES_FOR_EDA if f in df.columns]
        
        # Llista completa per agregar (sense duplicats)
        all_features_to_aggregate = features_for_clustering.copy()
        for f in features_for_eda:
            if f not in all_features_to_aggregate:
                all_features_to_aggregate.append(f)
        
        logger.info(f"Features clustering: {len(features_for_clustering)}, EDA: {len(features_for_eda)}, Total: {len(all_features_to_aggregate)}")
        
        # Agregació amb TOTES les features
        df_aggregated = self.data_aggregator.aggregate_by_player(
            df, all_features_to_aggregate
        )
        
        # Seleccionar NOMÉS features de clustering per escalar
        player_info = df_aggregated[['player_feb_id', 'player_name']].copy()
        features = df_aggregated[features_for_clustering].copy()
        
        # Escalat
        features_scaled, features_clean = self.scaler.fit_transform(
            features, 
            handle_infinity=HANDLE_INFINITY,
            fill_na=FILL_NA_VALUE
        )
        
        logger.info("Transformació completada")
        
        return {
            'player_info': player_info,
            'features_raw': features_clean,
            'features_scaled': features_scaled,
            'aggregated': df_aggregated,
            'full_data': df_aggregated  # Inclou totes les dades agregades
        }
    
    def load(self, dataframes: Dict[str, pd.DataFrame], 
             output_dir: str = None):
        """
        Guarda les dades processades.
        
        Args:
            dataframes: Diccionari amb DataFrames a guardar
            output_dir: Directori de sortida (opcional)
        """
        from pathlib import Path
        
        output_path = Path(output_dir) if output_dir else PROCESSED_DATA_DIR
        
        logger.info(f"Guardant dades a {output_path}")
        
        # Combinar info del jugador amb features escalades
        df_final_scaled = pd.concat([
            dataframes['player_info'].reset_index(drop=True),
            dataframes['features_scaled'].reset_index(drop=True)
        ], axis=1)
        
        # Guardar arxius
        files_to_save = {
            OUTPUT_SCALED_FILE: df_final_scaled,
            OUTPUT_RAW_FILE: dataframes['features_raw'],
            OUTPUT_AGGREGATED_FILE: dataframes['aggregated']
        }
        
        self.file_handler.save_multiple_csv(files_to_save, output_path)
        logger.info("Dades guardades correctament")
    
    def run(self, season: str = DEFAULT_SEASON, 
            competition: str = DEFAULT_COMPETITION,
            output_dir: str = None) -> Dict[str, pd.DataFrame]:
        """
        Executa el pipeline complet d'ETL.
        
        Args:
            season: Temporada a processar
            competition: Competició a processar
            output_dir: Directori de sortida
            
        Returns:
            Diccionari amb DataFrames processats
        """
        logger.info("="*60)
        logger.info("INICIANT PIPELINE ETL")
        logger.info("="*60)
        
        if not self.connect_database():
            raise RuntimeError("No s'ha pogut connectar a la base de dades")
        
        try:
            data_raw = self.extract(season, competition)
            dataframes = self.transform(data_raw)
            self.load(dataframes, output_dir)
            
            logger.info("="*60)
            logger.info("PIPELINE ETL COMPLETAT CORRECTAMENT")
            logger.info("="*60)
            
            return dataframes
            
        finally:
            self.mongo_client.disconnect()
