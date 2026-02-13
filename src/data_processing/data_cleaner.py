"""
Neteja i filtratge de dades.
Principi SRP: Única responsabilitat de netejar i filtrar dades.
"""
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


class DataCleaner:
    """Neteja i filtra dades de jugadors."""
    
    @staticmethod
    def validate_required_columns(df: pd.DataFrame, required_cols: list) -> bool:
        """
        Valida que existeixin les columnes requerides.
        
        Args:
            df: DataFrame a validar
            required_cols: Llista de columnes requerides
            
        Returns:
            True si totes les columnes existeixen
            
        Raises:
            ValueError: Si alguna columna no existeix
        """
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            raise ValueError(f"Falten columnes requerides: {missing_cols}")
        
        logger.info("Validació de columnes requerides: OK")
        return True
    
    @staticmethod
    def validate_numeric_ranges(df: pd.DataFrame, validations: dict) -> pd.DataFrame:
        """
        Valida que les columnes numèriques estiguin dins dels rangs esperats.
        
        Args:
            df: DataFrame a validar
            validations: Dict amb format {'columna': {'min': val, 'max': val}}
            
        Returns:
            DataFrame filtrat amb valors vàlids
        """
        initial_count = len(df)
        
        for col, ranges in validations.items():
            if col in df.columns:
                if 'min' in ranges:
                    df = df[df[col] >= ranges['min']]
                if 'max' in ranges:
                    df = df[df[col] <= ranges['max']]
        
        removed = initial_count - len(df)
        if removed > 0:
            logger.warning(f"Eliminats {removed} registres per valors fora de rang")
        
        return df
    
    @staticmethod
    def validate_percentages(df: pd.DataFrame, pct_cols: list) -> pd.DataFrame:
        """
        Valida que els percentatges estiguin entre 0 i 1.
        
        Args:
            df: DataFrame
            pct_cols: Columnes de percentatges
            
        Returns:
            DataFrame amb percentatges vàlids
        """
        for col in pct_cols:
            if col in df.columns:
                # Marcar valors invàlids
                invalid_mask = (df[col] < 0) | (df[col] > 1)
                invalid_count = invalid_mask.sum()
                
                if invalid_count > 0:
                    logger.warning(f"Columna '{col}': {invalid_count} valors fora de [0, 1]")
                    # Clip a 0-1
                    df[col] = df[col].clip(0, 1)
        
        return df
    
    @staticmethod
    def filter_by_minutes(df: pd.DataFrame, min_minutes: float = 0) -> pd.DataFrame:
        """
        Filtra jugadors per minuts jugats.
        
        Args:
            df: DataFrame de jugadors
            min_minutes: Mínim de minuts jugats
            
        Returns:
            DataFrame filtrat
        """
        initial_count = len(df)
        df_filtered = df[df['minutes'] > min_minutes].copy()
        removed = initial_count - len(df_filtered)
        
        logger.info(f"Filtrats {removed} registres amb minuts <= {min_minutes}")
        return df_filtered
    
    @staticmethod
    def filter_by_games_played(df: pd.DataFrame, min_games: int, 
                               player_id_col: str = 'player_feb_id') -> pd.DataFrame:
        """
        Filtra jugadors per nombre mínim de partits jugats.
        
        Args:
            df: DataFrame de jugadors
            min_games: Nombre mínim de partits
            player_id_col: Nom de la columna amb l'ID del jugador
            
        Returns:
            DataFrame filtrat
        """
        games_per_player = df.groupby(player_id_col).size().reset_index(name='num_games')
        valid_players = games_per_player[games_per_player['num_games'] >= min_games][player_id_col]
        
        initial_count = df[player_id_col].nunique()
        df_filtered = df[df[player_id_col].isin(valid_players)].copy()
        final_count = df_filtered[player_id_col].nunique()
        
        logger.info(f"Filtrats jugadors: {initial_count} -> {final_count} "
                   f"(mínim {min_games} partits)")
        return df_filtered
    
    @staticmethod
    def handle_missing_values(df: pd.DataFrame, strategy: str = 'drop', 
                             fill_value: float = 0) -> pd.DataFrame:
        """
        Gestiona valors nuls en el DataFrame.
        
        Args:
            df: DataFrame
            strategy: Estratègia ('drop', 'fill')
            fill_value: Valor per omplir si strategy='fill'
            
        Returns:
            DataFrame sense valors nuls
        """
        initial_nulls = df.isnull().sum().sum()
        
        if strategy == 'drop':
            df_clean = df.dropna()
        elif strategy == 'fill':
            df_clean = df.fillna(fill_value)
        else:
            raise ValueError(f"Estratègia no vàlida: {strategy}")
        
        final_nulls = df_clean.isnull().sum().sum()
        logger.info(f"Valors nuls: {initial_nulls} -> {final_nulls} (estratègia: {strategy})")
        
        return df_clean
    
    @staticmethod
    def remove_duplicates(df: pd.DataFrame, subset: list = None) -> pd.DataFrame:
        """
        Elimina duplicats del DataFrame.
        
        Args:
            df: DataFrame
            subset: Columnes a considerar per duplicats
            
        Returns:
            DataFrame sense duplicats
        """
        initial_count = len(df)
        df_clean = df.drop_duplicates(subset=subset)
        removed = initial_count - len(df_clean)
        
        logger.info(f"Eliminats {removed} duplicats")
        return df_clean
