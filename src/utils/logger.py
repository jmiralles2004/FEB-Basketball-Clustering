"""
Configuració de logging.
Principi SRP: Única responsabilitat de configurar el sistema de logs.
"""
import logging
from pathlib import Path


def setup_logger(name: str = None, log_level: str = 'INFO', 
                log_format: str = None, log_file: Path = None) -> logging.Logger:
    """
    Configura i retorna un logger.
    
    Args:
        name: Nom del logger (None per root logger)
        log_level: Nivell de logging
        log_format: Format dels missatges
        log_file: Ruta de l'arxiu de log (opcional)
        
    Returns:
        Logger configurat
    """
    if log_format is None:
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    if logger.handlers:
        logger.handlers.clear()
    
    formatter = logging.Formatter(log_format)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger
