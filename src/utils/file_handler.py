"""
Gestió d'arxius.
Principi SRP: Única responsabilitat de llegir i escriure arxius.
"""
import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class FileHandler:
    """Gestiona operacions de lectura i escriptura d'arxius."""
    
    @staticmethod
    def ensure_directory_exists(directory: Path):
        """
        Assegura que un directori existeix, creant-lo si és necessari.
        
        Args:
            directory: Ruta del directori
        """
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"Directori assegurat: {directory}")
    
    @staticmethod
    def save_csv(df: pd.DataFrame, filepath: Path, index: bool = False):
        """
        Guarda DataFrame en CSV.
        
        Args:
            df: DataFrame a guardar
            filepath: Ruta de l'arxiu
            index: Si incloure l'índex
        """
        FileHandler.ensure_directory_exists(filepath.parent)
        df.to_csv(filepath, index=index)
        logger.info(f"Arxiu guardat: {filepath}")
    
    @staticmethod
    def load_csv(filepath: Path) -> pd.DataFrame:
        """
        Carrega DataFrame des de CSV.
        
        Args:
            filepath: Ruta de l'arxiu
            
        Returns:
            DataFrame carregat
        """
        df = pd.read_csv(filepath)
        logger.info(f"Arxiu carregat: {filepath} ({len(df)} registres)")
        return df
    
    @staticmethod
    def save_multiple_csv(dataframes: dict, base_dir: Path, index: bool = False):
        """
        Guarda múltiples DataFrames en CSV.
        
        Args:
            dataframes: Diccionari {nom_arxiu: dataframe}
            base_dir: Directori base
            index: Si incloure l'índex
        """
        for filename, df in dataframes.items():
            filepath = base_dir / filename
            FileHandler.save_csv(df, filepath, index)
        
        logger.info(f"Guardats {len(dataframes)} arxius a {base_dir}")
