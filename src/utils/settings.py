# utils/settings.py
# Game settings and constants

import os

# Load version from VERSION file
def _load_version():
    import sys
    # Handle PyInstaller bundles
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller bundle
        bundle_dir = sys._MEIPASS
        version_file = os.path.join(bundle_dir, 'VERSION')
    else:
        # Running from source
        version_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'VERSION')

    try:
        with open(version_file, 'r') as f:
            return f.read().strip()
    except:
        return "1.1.2"  # Fallback version

CURRENT_VERSION = _load_version()

# Game render resolution (internal resolution)
WINDOW_WIDTH = 1000  # Increased from 800 to show more horizontally
WINDOW_HEIGHT = 600

# Display scale factor - now dynamic, user can resize window
# Default scale factor (0.8 = 800x480 default window size)
# This is the initial value; will be updated dynamically as window is resized
DISPLAY_SCALE = 0.8  # Default: smaller window that works on any Mac

# Current display scale - updated dynamically during gameplay
# This is the live scale factor that should be used for coordinate conversions
current_display_scale = DISPLAY_SCALE


def enforce_aspect_ratio(requested_width, requested_height):
    """
    Enforce 5:3 aspect ratio while respecting BOTH width and height constraints.

    This ensures the window fits within the provided bounds, critical for
    fullscreen on ultrawide/wide monitors where width >> height.

    Args:
        requested_width: Maximum width available (e.g., monitor width)
        requested_height: Maximum height available (e.g., monitor height)

    Returns:
        tuple: (width, height) maintaining 5:3 ratio, fitting within bounds

    Example:
        User drags to 800x400:
        enforce_aspect_ratio(800, 400) -> (800, 480)

        Fullscreen on 3440x1440 ultrawide:
        enforce_aspect_ratio(3440, 1440) -> (2400, 1440) with letterboxing
    """
    aspect_ratio = WINDOW_WIDTH / WINDOW_HEIGHT  # 1000/600 = 1.666...

    # Calculate two possible sizes that maintain 5:3 aspect ratio:
    # 1. Width-limited: use full width, calculate height
    width_limited_height = int(requested_width / aspect_ratio)

    # 2. Height-limited: use full height, calculate width
    height_limited_width = int(requested_height * aspect_ratio)

    # Choose the size that fits within BOTH width and height constraints
    if width_limited_height <= requested_height:
        # Width is the limiting factor - use full width
        final_width = requested_width
        final_height = width_limited_height
    else:
        # Height is the limiting factor - use full height
        final_width = height_limited_width
        final_height = requested_height

    # Enforce minimum size (400x240 minimum for usability)
    min_width = 400
    min_height = int(min_width / aspect_ratio)  # 240
    if final_width < min_width:
        final_width = min_width
        final_height = min_height

    return (final_width, final_height)


FPS = 60
TITLE = "Siena's Snowy Adventure"

# Audio Settings
MASTER_AUDIO_ENABLED = True  # Set to False to disable ALL audio (music + sound effects)

# Colors (R,G,B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY = (170, 200, 255)
