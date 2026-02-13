"""
Carregador de dades des de MongoDB.
Principi SRP: Única responsabilitat de carregar dades des de la base de dades.
"""
from typing import Dict, List, Optional
import pandas as pd
import logging

from ..database import MongoDBClient

logger = logging.getLogger(__name__)


class DataLoader:
    """Carrega dades des de MongoDB a DataFrames de pandas."""
    
    def __init__(self, mongo_client: MongoDBClient):
        """
        Inicialitza el carregador de dades.
        
        Args:
            mongo_client: Client de MongoDB
        """
        self.mongo_client = mongo_client
    
    def load_players_statistics(self, query: Optional[Dict] = None) -> pd.DataFrame:
        """
        Carrega estadístiques de jugadors.
        
        Args:
            query: Filtre de cerca MongoDB
            
        Returns:
            DataFrame amb estadístiques de jugadors
        """
        from ..config import COLLECTION_PLAYERS_STATS
        
        data = self.mongo_client.find(COLLECTION_PLAYERS_STATS, query)
        df = pd.DataFrame(data)
        
        logger.info(f"Carregats {len(df)} registres de jugadors")
        return df
    
    def load_teams_statistics(self, query: Optional[Dict] = None) -> pd.DataFrame:
        """
        Carrega estadístiques d'equips.
        
        Args:
            query: Filtre de cerca MongoDB
            
        Returns:
            DataFrame amb estadístiques d'equips
        """
        from ..config import COLLECTION_TEAMS_STATS
        
        data = self.mongo_client.find(COLLECTION_TEAMS_STATS, query)
        df = pd.DataFrame(data)
        
        logger.info(f"Carregats {len(df)} registres d'equips")
        return df
    
    def load_players_shots(self, query: Optional[Dict] = None) -> pd.DataFrame:
        """
        Carrega dades de tirs de jugadors.
        
        Args:
            query: Filtre de cerca MongoDB
            
        Returns:
            DataFrame amb dades de tirs
        """
        from ..config import COLLECTION_PLAYERS_SHOTS
        
        data = self.mongo_client.find(COLLECTION_PLAYERS_SHOTS, query)
        df = pd.DataFrame(data)
        
        logger.info(f"Carregats {len(df)} registres de tirs")
        return df
    
    def get_available_seasons(self, collection_name: str) -> List[str]:
        """
        Obté temporades disponibles.
        
        Args:
            collection_name: Nom de la col·lecció
            
        Returns:
            Llista de temporades ordenades
        """
        seasons = self.mongo_client.get_distinct_values(collection_name, 'season_id')
        return sorted(seasons)
    
    def get_available_competitions(self, collection_name: str) -> List[str]:
        """
        Obté competicions disponibles.
        
        Args:
            collection_name: Nom de la col·lecció
            
        Returns:
            Llista de competicions ordenades
        """
        competitions = self.mongo_client.get_distinct_values(
            collection_name, 'competition_name'
        )
        return sorted(competitions)
