"""
Enginyeria de característiques.
Principi SRP: Única responsabilitat de crear i transformar característiques.
"""
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


class FeatureEngineer:
    """Crea i transforma característiques per anàlisi."""
    
    @staticmethod
    def convert_seconds_to_minutes(df: pd.DataFrame, seconds_col: str = 'minutes', 
                                   new_col: str = 'minutes_played') -> pd.DataFrame:
        """
        Converteix segons a minuts.
        
        Args:
            df: DataFrame
            seconds_col: Columna amb segons
            new_col: Nom de la nova columna
            
        Returns:
            DataFrame amb nova columna
        """
        df[new_col] = df[seconds_col] / 60
        logger.info(f"Creada columna '{new_col}' des de '{seconds_col}'")
        return df
    
    @staticmethod
    def normalize_per_minutes(df: pd.DataFrame, stats_cols: list, 
                             minutes_col: str = 'minutes_played', 
                             target_minutes: int = 36) -> pd.DataFrame:
        """
        Normalitza estadístiques per minuts jugats.
        
        Args:
            df: DataFrame
            stats_cols: Llista de columnes a normalitzar
            minutes_col: Columna amb minuts jugats
            target_minutes: Minuts de referència per normalització
            
        Returns:
            DataFrame amb estadístiques normalitzades
        """
        for stat in stats_cols:
            if stat in df.columns:
                new_col = f'{stat}_per{target_minutes}'
                df[new_col] = (df[stat] / df[minutes_col]) * target_minutes
        
        logger.info(f"Normalitzades {len(stats_cols)} estadístiques a {target_minutes} minuts")
        return df
    
    @staticmethod
    def calculate_shooting_percentages(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula percentatges de tir.
        
        Args:
            df: DataFrame amb estadístiques de tir
            
        Returns:
            DataFrame amb percentatges calculats
        """
        df['fg2_pct'] = np.where(df['2pa'] > 0, df['2pm'] / df['2pa'], 0)
        df['fg3_pct'] = np.where(df['3pa'] > 0, df['3pm'] / df['3pa'], 0)
        df['ft_pct'] = np.where(df['fta'] > 0, df['ftm'] / df['fta'], 0)
        
        logger.info("Calculats percentatges de tir (FG2%, FG3%, FT%)")
        return df
    
    @staticmethod
    def calculate_usage_rates(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula taxes d'ús de tirs.
        
        Args:
            df: DataFrame amb estadístiques de tir
            
        Returns:
            DataFrame amb taxes d'ús
        """
        df['usage_2p'] = np.where(df['fga'] > 0, df['2pa'] / df['fga'], 0)
        df['usage_3p'] = np.where(df['fga'] > 0, df['3pa'] / df['fga'], 0)
        
        logger.info("Calculades taxes d'ús de tir (2P, 3P)")
        return df
    
    @staticmethod
    def calculate_interior_stats(df: pd.DataFrame, 
                                 zones_made: list, 
                                 zones_attempted: list) -> pd.DataFrame:
        """
        Calcula estadístiques de tir interior.
        
        Args:
            df: DataFrame
            zones_made: Columnes de tirs anotats en zones interiors
            zones_attempted: Columnes de tirs intentats en zones interiors
            
        Returns:
            DataFrame amb estadístiques de tir interior
        """
        interior_made = df[zones_made].sum(axis=1)
        interior_attempted = df[zones_attempted].sum(axis=1)
        
        df['interior_pct'] = np.where(interior_attempted > 0, 
                                       interior_made / interior_attempted, 0)
        df['interior_freq'] = np.where(df['fga'] > 0, 
                                        interior_attempted / df['fga'], 0)
        
        logger.info("Calculades estadístiques de tir interior")
        return df
    
    @staticmethod
    def calculate_exterior_stats(df: pd.DataFrame, 
                                  zones_made: list, 
                                  zones_attempted: list) -> pd.DataFrame:
        """
        Calcula estadístiques de tir exterior.
        
        Args:
            df: DataFrame
            zones_made: Columnes de tirs anotats en zones exteriors
            zones_attempted: Columnes de tirs intentats en zones exteriors
            
        Returns:
            DataFrame amb estadístiques de tir exterior
        """
        exterior_made = df[zones_made].sum(axis=1)
        exterior_attempted = df[zones_attempted].sum(axis=1)
        
        df['exterior_pct'] = np.where(exterior_attempted > 0, 
                                       exterior_made / exterior_attempted, 0)
        df['exterior_freq'] = np.where(df['fga'] > 0, 
                                        exterior_attempted / df['fga'], 0)
        
        logger.info("Calculades estadístiques de tir exterior")
        return df
    
    @staticmethod
    def calculate_possessions(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula les possessions estimades per jugador (contribució individual).
        
        Aquesta és la contribució individual del jugador a les possessions
        de l'equip. S'utilitza per calcular l'OER individual.
        
        NOTA: Les possessions a nivell d'EQUIP es calculen al pipeline
        (etl_pipeline.py) usant FEB3_teams_statistics per al càlcul del DER.
        
        Fórmula: Possessions = FGA + 0.44 × FTA - ORB + TOV
        (Font: Basketball Reference - estimació estàndard NBA)
        
        Args:
            df: DataFrame amb estadístiques del jugador
            
        Returns:
            DataFrame amb possessions calculades
        """
        from ..config import FREE_THROW_POSSESSION_FACTOR
        
        df['possessions'] = (
            df['fga'] + 
            (FREE_THROW_POSSESSION_FACTOR * df['fta']) - 
            df['orb'] + 
            df['tov']
        )
        
        logger.info("Calculades possessions per jugador")
        return df
    
    @staticmethod
    def calculate_oer(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula l'Offensive Efficiency Rating (OER).
        
        OER = 100 × (Punts anotats / Possessions)
        
        Args:
            df: DataFrame amb punts i possessions
            
        Returns:
            DataFrame amb OER calculat
        """
        from ..config import EFFICIENCY_MULTIPLIER
        
        df['oer'] = np.where(
            df['possessions'] > 0,
            EFFICIENCY_MULTIPLIER * (df['pts'] / df['possessions']),
            0
        )
        
        logger.info("Calculat OER (Offensive Efficiency Rating)")
        return df
    
    @staticmethod
    def calculate_true_shooting_pct(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula el True Shooting Percentage (TS%).
        
        TS% = PTS / (2 × (FGA + 0.44 × FTA))
        
        Args:
            df: DataFrame amb estadístiques de tir
            
        Returns:
            DataFrame amb TS% calculat
        """
        from ..config import FREE_THROW_POSSESSION_FACTOR
        
        true_shooting_attempts = 2 * (df['fga'] + FREE_THROW_POSSESSION_FACTOR * df['fta'])
        
        df['true_shooting_pct'] = np.where(
            true_shooting_attempts > 0,
            df['pts'] / true_shooting_attempts,
            0
        )
        
        logger.info("Calculat True Shooting % (TS%)")
        return df
    
    @staticmethod
    def calculate_der(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula el Defensive Efficiency Rating (DER).
        
        DER = 100 × (Punts rival / Possessions rival)
        
        IMPORTANT: Aquesta funció assumeix que ja existeix 'opponent_possessions'
        i 'opponent_pts' calculats prèviament al pipeline.
        
        Args:
            df: DataFrame amb possessions i punts del rival
            
        Returns:
            DataFrame amb DER calculat
        """
        from ..config import EFFICIENCY_MULTIPLIER
        
        df['der'] = np.where(
            df['opponent_possessions'] > 0,
            EFFICIENCY_MULTIPLIER * (df['opponent_pts'] / df['opponent_possessions']),
            0
        )
        
        logger.info("Calculat DER (Defensive Efficiency Rating)")
        return df
    
    @staticmethod
    def apply_all_transformations(df: pd.DataFrame, stats_to_normalize: list,
                                  interior_zones_made: list,
                                  interior_zones_attempted: list,
                                  exterior_zones_made: list = None,
                                  exterior_zones_attempted: list = None,
                                  target_minutes: int = 36) -> pd.DataFrame:
        """
        Aplica totes les transformacions de característiques.
        
        Args:
            df: DataFrame original
            stats_to_normalize: Estadístiques a normalitzar
            interior_zones_made: Zones interiors (anotats)
            interior_zones_attempted: Zones interiors (intentats)
            exterior_zones_made: Zones exteriors (anotats)
            exterior_zones_attempted: Zones exteriors (intentats)
            target_minutes: Minuts de referència
            
        Returns:
            DataFrame transformat
        """
        df = FeatureEngineer.convert_seconds_to_minutes(df)
        df = FeatureEngineer.normalize_per_minutes(df, stats_to_normalize, 
                                                   target_minutes=target_minutes)
        df = FeatureEngineer.calculate_shooting_percentages(df)
        df = FeatureEngineer.calculate_usage_rates(df)
        df = FeatureEngineer.calculate_interior_stats(df, interior_zones_made, 
                                                       interior_zones_attempted)
        
        # Zones exteriors (si es proporcionen les columnes)
        if exterior_zones_made and exterior_zones_attempted:
            df = FeatureEngineer.calculate_exterior_stats(df, exterior_zones_made,
                                                          exterior_zones_attempted)
        
        # Mètriques avançades
        df = FeatureEngineer.calculate_possessions(df)
        df = FeatureEngineer.calculate_oer(df)
        df = FeatureEngineer.calculate_true_shooting_pct(df)
        
        # DER només si existeixen dades del rival
        if 'opponent_possessions' in df.columns and 'opponent_pts' in df.columns:
            df = FeatureEngineer.calculate_der(df)
        
        logger.info("Totes les transformacions de característiques aplicades")
        return df
