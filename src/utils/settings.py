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

# Display scale factor (2.0 = 1600x1200, 2.5 = 2000x1500, etc.)
DISPLAY_SCALE = 1.4  # Change this to make window bigger/smaller

FPS = 60
TITLE = "Siena's Snowy Adventure"

# Audio Settings
MASTER_AUDIO_ENABLED = True  # Set to False to disable ALL audio (music + sound effects)

# Colors (R,G,B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY = (170, 200, 255)
