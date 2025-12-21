"""
Game Logging System
Centralized logging configuration for the game
"""

import logging
import sys
from pathlib import Path


class GameLogger:
    """Manages logging configuration for the game"""

    _initialized = False

    @classmethod
    def setup(cls, level=logging.INFO, log_file=None):
        """
        Setup logging configuration

        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional file path to write logs to
        """
        if cls._initialized:
            return

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        # Root logger configuration
        root_logger = logging.getLogger()
        root_logger.setLevel(level)
        root_logger.addHandler(console_handler)

        # File handler (optional)
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)

        cls._initialized = True

        # Log startup
        logger = logging.getLogger(__name__)
        logger.info("Logging system initialized")

    @classmethod
    def get_logger(cls, name):
        """
        Get a logger instance

        Args:
            name: Logger name (usually __name__)

        Returns:
            Logger instance
        """
        if not cls._initialized:
            cls.setup()
        return logging.getLogger(name)


def get_logger(name):
    """
    Convenience function to get a logger

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    return GameLogger.get_logger(name)


# Initialize logging on import
GameLogger.setup(level=logging.INFO)
