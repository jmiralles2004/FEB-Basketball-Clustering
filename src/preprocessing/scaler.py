"""
Escalat i normalització de dades.
Principi SRP: Única responsabilitat d'escalar i normalitzar dades.
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class DataScaler:
    """Escala i normalitza característiques numèriques."""
    
    def __init__(self, scaler_type: str = 'standard'):
        """
        Inicialitza l'escalador.
        
        Args:
            scaler_type: Tipus d'escalador ('standard' o 'minmax')
        """
        if scaler_type == 'standard':
            self.scaler = StandardScaler()
        elif scaler_type == 'minmax':
            self.scaler = MinMaxScaler()
        else:
            raise ValueError(f"Tipus d'escalador no vàlid: {scaler_type}")
        
        self.scaler_type = scaler_type
        logger.info(f"Inicialitzat escalador: {scaler_type}")
    
    def fit_transform(self, df: pd.DataFrame, 
                     handle_infinity: bool = True,
                     fill_na: float = 0) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Ajusta i transforma les dades.
        
        Args:
            df: DataFrame amb característiques numèriques
            handle_infinity: Si True, reemplaça infinits amb NaN
            fill_na: Valor per omplir NaN
            
        Returns:
            Tupla (dades_escalades, dades_originals_netes)
        """
        df_clean = df.copy()
        
        if handle_infinity:
            df_clean = df_clean.replace([np.inf, -np.inf], np.nan)
            logger.info("Valors infinits reemplaçats amb NaN")
        
        df_clean = df_clean.fillna(fill_na)
        logger.info(f"Valors NaN omplerts amb {fill_na}")
        
        scaled_data = self.scaler.fit_transform(df_clean)
        df_scaled = pd.DataFrame(scaled_data, columns=df_clean.columns)
        
        logger.info(f"Dades escalades: {df_scaled.shape}")
        return df_scaled, df_clean
    
    def transform(self, df: pd.DataFrame,
                 handle_infinity: bool = True,
                 fill_na: float = 0) -> pd.DataFrame:
        """
        Transforma dades usant escalador ja ajustat.
        
        Args:
            df: DataFrame amb característiques numèriques
            handle_infinity: Si True, reemplaça infinits amb NaN
            fill_na: Valor per omplir NaN
            
        Returns:
            DataFrame escalat
        """
        df_clean = df.copy()
        
        if handle_infinity:
            df_clean = df_clean.replace([np.inf, -np.inf], np.nan)
        
        df_clean = df_clean.fillna(fill_na)
        
        scaled_data = self.scaler.transform(df_clean)
        df_scaled = pd.DataFrame(scaled_data, columns=df_clean.columns)
        
        return df_scaled
    
    def inverse_transform(self, df_scaled: pd.DataFrame) -> pd.DataFrame:
        """
        Reverteix la transformació.
        
        Args:
            df_scaled: DataFrame escalat
            
        Returns:
            DataFrame en escala original
        """
        original_data = self.scaler.inverse_transform(df_scaled)
        df_original = pd.DataFrame(original_data, columns=df_scaled.columns)
        
        return df_original
