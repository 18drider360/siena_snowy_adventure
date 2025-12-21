#!/usr/bin/env python3
"""
Fix imports after restructuring
Updates all Python files to use new src/ structure
"""

import os
import re
from pathlib import Path

# Mapping of old imports to new imports
IMPORT_MAPPINGS = {
    # Core systems
    r'from game_logging import': 'from src.core.game_logging import',
    r'from audio_manager import': 'from src.core.audio_manager import',
    r'from font_manager import': 'from src.core.font_manager import',
    r'from config_loader import': 'from src.core.config_loader import',
    r'from game_state import': 'from src.core.game_state import',
    r'from input_handler import': 'from src.core.input_handler import',
    r'from level_data import': 'from src.core.level_data import',
    r'from game_controller import': 'from src.core.game_controller import',
    r'from performance import': 'from src.core.performance import',
    r'import collision_physics': 'from src.core import collision_physics',
    r'import constants': 'from src.core import constants',

    # Rendering
    r'from rendering import': 'from src.rendering.rendering import',
    r'from game_screens import': 'from src.rendering.game_screens import',
    r'from menus import': 'from src.rendering.menus import',

    # Utils
    r'from utils import': 'from src.utils import',
    r'from utils\.': 'from src.utils.',

    # UI
    r'from ui import': 'from src.ui import',
    r'from ui\.': 'from src.ui.',

    # Entities
    r'from player import': 'from src.entities.player import',
    r'from player\.': 'from src.entities.player.',
    r'from enemies import': 'from src.entities.enemies import',
    r'from enemies\.': 'from src.entities.enemies.',

    # Levels
    r'from levels\.': 'from src.levels.',
}

def fix_file_imports(filepath):
    """Fix imports in a single file"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()

        original_content = content

        # Apply all import mappings
        for old_pattern, new_import in IMPORT_MAPPINGS.items():
            content = re.sub(old_pattern, new_import, content)

        # Only write if changed
        if content != original_content:
            with open(filepath, 'w') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Fix imports in all Python files"""
    root = Path('.')

    # Find all Python files
    python_files = []

    # Include src directory
    python_files.extend(root.glob('src/**/*.py'))

    # Include tests
    python_files.extend(root.glob('tests/**/*.py'))

    # Include root level files
    for file in ['title_screen.py']:
        if (root / file).exists():
            python_files.append(root / file)

    fixed_count = 0
    total_count = len(python_files)

    print(f"Fixing imports in {total_count} files...")

    for filepath in python_files:
        if fix_file_imports(filepath):
            print(f"✓ Fixed: {filepath}")
            fixed_count += 1

    print(f"\nCompleted: {fixed_count}/{total_count} files updated")

if __name__ == '__main__':
    main()
