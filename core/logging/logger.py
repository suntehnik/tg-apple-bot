import sys
from loguru import logger


class Logger:
    """Logger configuration and setup."""
    
    @staticmethod
    def setup(log_level="INFO"):
        """
        Configure logging for the application.
        
        Args:
            log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        # Remove default logger
        logger.remove()
        
        # Add stdout logger with specified level
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level=log_level
        )
        
        # Add file logger for errors
        logger.add(
            "logs/errors.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="ERROR",
            rotation="10 MB",
            compression="zip"
        )
        
        logger.info(f"Logger configured with level: {log_level}")
    
    @staticmethod
    def get_logger(name):
        """
        Get a logger instance with the given name.
        
        Args:
            name (str): Logger name
            
        Returns:
            logger: A configured logger instance
        """
        return logger.bind(name=name)