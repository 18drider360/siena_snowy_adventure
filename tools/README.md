# Development Tools

This directory contains various development and debugging tools for Siena's Snowy Adventure.

## Directory Structure

```
tools/
├── level_analysis/    # Tools for analyzing and debugging level layouts
└── leaderboard/       # Tools for managing online leaderboard
```

## Level Analysis Tools

Located in `level_analysis/` - these tools help analyze level design, collision detection, and gameplay elements.

### analyze_coin_collisions.py
Analyzes coin placement and collision detection in levels.
```bash
python tools/level_analysis/analyze_coin_collisions.py
```

### analyze_hazard_placement.py
Checks hazard placement and validates safe zones in levels.
```bash
python tools/level_analysis/analyze_hazard_placement.py
```

### analyze_platform_collisions.py
Tests platform collision detection and validates platform configurations.
```bash
python tools/level_analysis/analyze_platform_collisions.py
```

### count_coins.py
Counts total coins per level for balance checking.
```bash
python tools/level_analysis/count_coins.py
```

### generated_level.py
Generates procedural level layouts for testing (experimental).
```bash
python tools/level_analysis/generated_level.py
```

## Leaderboard Tools

Located in `leaderboard/` - these tools help manage and debug the online leaderboard system.

### check_online_scores.py
Views current scores from Firebase online leaderboard.

**Prerequisites:**
- Firebase configured (see `docs/guides/FIREBASE_SETUP.md`)
- `.env` file with `SIENA_ONLINE_ENABLED=true`
- Valid Firebase credentials

**Usage:**
```bash
python tools/leaderboard/check_online_scores.py
```

**What it does:**
- Displays all scores from the online leaderboard
- Shows username, time, difficulty, and checkpoint status
- Organized by level
- Useful for debugging leaderboard submissions

## Running Tools

All tools should be run from the project root directory:

```bash
# From project root
python tools/level_analysis/count_coins.py
python tools/leaderboard/check_online_scores.py
```

## Adding New Tools

When adding new development tools:

1. Place them in the appropriate subdirectory
2. Add path setup if they need to import from `src/`:
   ```python
   import sys
   import os
   sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
   ```
3. Add documentation to this README
4. Make them executable: `chmod +x your_tool.py`
5. Add shebang: `#!/usr/bin/env python3`

## Tool Categories

Consider creating new subdirectories for:
- `audio/` - Audio testing and analysis tools
- `graphics/` - Sprite and rendering debug tools
- `performance/` - Performance profiling tools
- `testing/` - Test generation and automation tools
