"""
Font Manager
Centralized font loading and caching system
"""

import pygame
from functools import lru_cache
from src.core.game_logging import get_logger

logger = get_logger(__name__)


class FontManager:
    """Manages font loading and caching"""

    # Cache for loaded fonts (key: (font_name, size), value: pygame.font.Font)
    _font_cache = {}

    @classmethod
    def get_font(cls, font_path, size, use_default_on_error=True):
        """
        Get a font, loading and caching it if necessary

        Args:
            font_path: Path to the font file (e.g., "assets/fonts/PressStart2P-Regular.ttf")
                      Can also be None to use system default
            size: Font size in pixels
            use_default_on_error: If True, fall back to default font on error

        Returns:
            pygame.font.Font object
        """
        # Create cache key
        cache_key = (font_path, size)

        # Check cache
        if cache_key in cls._font_cache:
            return cls._font_cache[cache_key]

        # Try to load the font
        try:
            if font_path is None:
                font = pygame.font.Font(None, size)
                logger.debug(f"Loaded default font (size {size})")
            else:
                font = pygame.font.Font(font_path, size)
                logger.debug(f"Loaded font: {font_path} (size {size})")

            # Cache the font
            cls._font_cache[cache_key] = font
            return font

        except (FileNotFoundError, pygame.error, OSError) as e:
            logger.warning(f"Could not load font '{font_path}': {e}")

            if use_default_on_error:
                # Fall back to default font (system font)
                default_size = size * 2  # System fonts are smaller, so double the size
                default_key = (None, default_size)

                if default_key in cls._font_cache:
                    return cls._font_cache[default_key]

                try:
                    font = pygame.font.Font(None, default_size)
                    cls._font_cache[default_key] = font
                    logger.info(f"Using default font (size {default_size}) as fallback")
                    return font
                except Exception as fallback_error:
                    logger.error(f"Could not load default font: {fallback_error}")
                    raise
            else:
                raise

    @classmethod
    def get_press_start_2p(cls, size):
        """
        Convenience method to get the Press Start 2P font (main game font)

        Args:
            size: Font size in pixels

        Returns:
            pygame.font.Font object
        """
        return cls.get_font("assets/fonts/PressStart2P-Regular.ttf", size)

    @classmethod
    def get_default_font(cls, size):
        """
        Get the system default font

        Args:
            size: Font size in pixels

        Returns:
            pygame.font.Font object
        """
        return cls.get_font(None, size)

    @classmethod
    def clear_cache(cls):
        """Clear the font cache (useful for testing or memory management)"""
        cls._font_cache.clear()
        logger.info("Font cache cleared")

    @classmethod
    def get_cache_info(cls):
        """
        Get information about the font cache

        Returns:
            dict: Cache statistics
        """
        return {
            'size': len(cls._font_cache),
            'fonts': list(cls._font_cache.keys())
        }


# Convenience functions
def get_font(font_path, size, use_default_on_error=True):
    """
    Get a font (convenience function)

    Args:
        font_path: Path to font file or None for default
        size: Font size in pixels
        use_default_on_error: Fall back to default font on error

    Returns:
        pygame.font.Font object
    """
    return FontManager.get_font(font_path, size, use_default_on_error)


def get_press_start_2p(size):
    """
    Get the Press Start 2P font (convenience function)

    Args:
        size: Font size in pixels

    Returns:
        pygame.font.Font object
    """
    return FontManager.get_press_start_2p(size)
