"""
Script principal per executar el pipeline ETL.
Punt d'entrada per al processament de dades.
"""
from .pipeline import ETLPipeline
from .utils import setup_logger
from .config import LOG_LEVEL, LOG_FORMAT


def main():
    """Funció principal."""
    logger = setup_logger('main', LOG_LEVEL, LOG_FORMAT)
    
    logger.info("Iniciant processament de dades FEB")
    
    pipeline = ETLPipeline()
    
    try:
        results = pipeline.run()
        
        logger.info("\nResum de resultats:")
        logger.info(f"Jugadors processats: {len(results['player_info'])}")
        logger.info(f"Features generades: {len(results['features_raw'].columns)}")
        
    except Exception as e:
        logger.error(f"Error al pipeline: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
