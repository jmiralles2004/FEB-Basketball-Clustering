"""
Client MongoDB per connexió i consultes a la base de dades.
Principi SRP: Única responsabilitat de gestionar la connexió i consultes a MongoDB.
"""
from typing import Dict, List, Optional
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
import logging

logger = logging.getLogger(__name__)


class MongoDBClient:
    """Client per interactuar amb MongoDB."""
    
    def __init__(self, uri: str, db_name: str):
        """
        Inicialitza el client MongoDB.
        
        Args:
            uri: URI de connexió a MongoDB
            db_name: Nom de la base de dades
        """
        self.uri = uri
        self.db_name = db_name
        self._client: Optional[MongoClient] = None
        self._db: Optional[Database] = None
    
    def connect(self) -> bool:
        """
        Estableix connexió amb MongoDB.
        
        Returns:
            True si la connexió és exitosa, False en cas contrari
        """
        try:
            self._client = MongoClient(self.uri)
            self._db = self._client[self.db_name]
            self._client.admin.command('ping')
            logger.info(f"Connexió exitosa a MongoDB: {self.db_name}")
            return True
        except Exception as e:
            logger.error(f"Error connectant a MongoDB: {e}")
            return False
    
    def disconnect(self):
        """Tanca la connexió amb MongoDB."""
        if self._client:
            self._client.close()
            logger.info("Connexió a MongoDB tancada")
    
    @property
    def db(self) -> Database:
        """
        Retorna l'objecte Database.
        
        Returns:
            Objecte Database de pymongo
            
        Raises:
            RuntimeError: Si no hi ha connexió establerta
        """
        if self._db is None:
            raise RuntimeError("No hi ha connexió establerta amb MongoDB")
        return self._db
    
    def get_collection(self, collection_name: str) -> Collection:
        """
        Obté una col·lecció de la base de dades.
        
        Args:
            collection_name: Nom de la col·lecció
            
        Returns:
            Objecte Collection de pymongo
            
        Raises:
            RuntimeError: Si no hi ha connexió establerta
        """
        if self._db is None:
            raise RuntimeError("No hi ha connexió establerta amb MongoDB")
        return self._db[collection_name]
    
    def list_collections(self) -> List[str]:
        """
        Llista totes les col·leccions disponibles.
        
        Returns:
            Llista de noms de col·leccions
        """
        if self._db is None:
            raise RuntimeError("No hi ha connexió establerta amb MongoDB")
        return self._db.list_collection_names()
    
    def count_documents(self, collection_name: str, query: Optional[Dict] = None) -> int:
        """
        Compta documents en una col·lecció.
        
        Args:
            collection_name: Nom de la col·lecció
            query: Filtre de cerca (opcional)
            
        Returns:
            Nombre de documents
        """
        collection = self.get_collection(collection_name)
        query = query or {}
        return collection.count_documents(query)
    
    def find(self, collection_name: str, query: Optional[Dict] = None, 
             projection: Optional[Dict] = None, limit: int = 0) -> List[Dict]:
        """
        Cerca documents en una col·lecció.
        
        Args:
            collection_name: Nom de la col·lecció
            query: Filtre de cerca
            projection: Projecció de camps
            limit: Límit de resultats (0 = sense límit)
            
        Returns:
            Llista de documents
        """
        collection = self.get_collection(collection_name)
        query = query or {}
        cursor = collection.find(query, projection)
        
        if limit > 0:
            cursor = cursor.limit(limit)
        
        return list(cursor)
    
    def get_distinct_values(self, collection_name: str, field: str, 
                           query: Optional[Dict] = None) -> List:
        """
        Obté valors únics d'un camp.
        
        Args:
            collection_name: Nom de la col·lecció
            field: Camp del qual obtenir valors únics
            query: Filtre de cerca (opcional)
            
        Returns:
            Llista de valors únics
        """
        collection = self.get_collection(collection_name)
        query = query or {}
        return collection.distinct(field, query)
