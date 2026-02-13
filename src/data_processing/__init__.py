"""
Mòdul de processament de dades.
Responsabilitat: ETL, neteja i transformació de dades.
"""
from .data_loader import DataLoader
from .data_cleaner import DataCleaner
from .feature_engineer import FeatureEngineer
from .data_aggregator import DataAggregator

__all__ = ['DataLoader', 'DataCleaner', 'FeatureEngineer', 'DataAggregator']
