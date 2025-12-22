# System Architecture

This document describes the architecture of Siena's Snowy Adventure, including module organization, dependencies, and design patterns.

## Table of Contents

- [Overview](#overview)
- [Directory Structure](#directory-structure)
- [Module Organization](#module-organization)
- [Component Diagrams](#component-diagrams)
- [Data Flow](#data-flow)
- [Key Design Patterns](#key-design-patterns)
- [External Dependencies](#external-dependencies)

## Overview

Siena's Snowy Adventure is a 2D platformer game built with Pygame. The architecture follows a modular design with clear separation of concerns:

- **Game Engine** (core/) - Main game loop, physics, input handling
- **Game Objects** (entities/) - Player, enemies, collectibles
- **Rendering** (rendering/) - Display, animations, UI screens
- **User Interface** (ui/) - Menus, HUD, scoreboards
- **Utilities** (utils/) - Save system, settings, helpers
- **Game Data** (data/) - Level definitions, story content

## Directory Structure

```
siena_snowy_adventure/
├── main.py                      # Entry point
├── pyproject.toml              # Package configuration
├── requirements.txt            # Dependencies
│
├── src/                        # Source code
│   ├── core/                   # Game engine core
│   │   ├── audio_manager.py    # Sound/music management
│   │   ├── game_loop.py        # Main game loop
│   │   ├── input_handler.py    # Keyboard/mouse input
│   │   └── physics.py          # Collision detection, physics
│   │
│   ├── entities/               # Game objects
│   │   ├── player.py           # Player character
│   │   ├── enemies.py          # Enemy entities
│   │   └── collectibles.py     # Coins, power-ups
│   │
│   ├── rendering/              # Graphics and display
│   │   ├── rendering.py        # Core rendering functions
│   │   ├── menus.py            # Pause/death menus
│   │   ├── game_screens.py     # Level transitions, cutscenes
│   │   └── screens/
│   │       └── title_screen.py # Title and level select
│   │
│   ├── ui/                     # User interface components
│   │   ├── scoreboard.py       # Leaderboard display
│   │   ├── username_input.py   # Username entry
│   │   ├── health_display.py   # Player health HUD
│   │   └── *_display.py        # Other HUD elements
│   │
│   ├── utils/                  # Utilities and helpers
│   │   ├── settings.py         # Game configuration
│   │   ├── save_system.py      # Local save management
│   │   ├── progression.py      # Level unlocking
│   │   ├── online_leaderboard.py  # Firebase integration
│   │   └── username_filter.py  # Content moderation
│   │
│   └── data/                   # Game data
│       ├── levels.py           # Level definitions
│       ├── story_data.py       # Dialogue and cutscenes
│       ├── enemy_configs.py    # Enemy stats and behaviors
│       └── dialogue_data.py    # Dialogue trees
│
├── assets/                     # Game assets
│   ├── images/                 # Sprites, backgrounds
│   ├── sounds/                 # Sound effects
│   ├── music/                  # Background music
│   └── fonts/                  # Custom fonts
│
├── tests/                      # Test suite
│   ├── unit/                   # Unit tests
│   └── integration/            # Integration tests
│
├── tools/                      # Development tools
│   ├── level_analysis/         # Level design tools
│   └── leaderboard/            # Leaderboard management
│
└── docs/                       # Documentation
    ├── user/                   # Player guides
    ├── guides/                 # Setup guides
    └── development/            # Technical docs
```

## Module Organization

### Core Modules (src/core/)

**Purpose:** Low-level game engine functionality.

**Responsibilities:**
- Game loop management (60 FPS, state updates, rendering)
- Physics simulation (collision detection, gravity)
- Input handling (keyboard, mouse, gamepad)
- Audio management (music, sound effects)

**Key Classes:**
- `GameLoop` - Main game state machine
- `InputHandler` - Input event processing
- `AudioManager` - Sound/music playback
- `Physics` - Collision and movement

**Dependencies:** pygame, src.utils.settings

---

### Entity Modules (src/entities/)

**Purpose:** Game objects and their behaviors.

**Responsibilities:**
- Player character state and movement
- Enemy AI and behaviors
- Collectible items (coins, checkpoints)
- Entity lifecycle management

**Key Classes:**
- `Player` - Player character with abilities
- `Enemy` - Base enemy class
- `Collectible` - Coins and power-ups

**Dependencies:** pygame, src.core.physics, src.utils.settings

---

### Rendering Modules (src/rendering/)

**Purpose:** Graphics, animations, and screen displays.

**Responsibilities:**
- Drawing game entities and environments
- Screen transitions and cutscenes
- Menu rendering
- Animation management

**Key Functions:**
- `draw_level_complete_screen()` - Level completion UI
- `draw_level_transition_screen()` - Between-level transitions
- `show_title_screen()` - Main menu

**Dependencies:** pygame, src.entities, src.data

---

### UI Modules (src/ui/)

**Purpose:** User interface components and HUD.

**Responsibilities:**
- Score display and leaderboards
- Health and ability indicators
- Username input and validation
- Menu interactions

**Key Classes:**
- `Scoreboard` - Local/online leaderboard display
- `UsernameInput` - Player name entry with filtering
- `HealthDisplay` - Player health HUD
- `SpinChargeDisplay` - Ability cooldown indicator

**Dependencies:** pygame, src.utils, src.rendering

---

### Utility Modules (src/utils/)

**Purpose:** Cross-cutting concerns and helpers.

**Responsibilities:**
- Game settings and configuration
- Save/load functionality
- Progress tracking and unlocks
- Online leaderboard (Firebase)
- Username content filtering

**Key Classes:**
- `SaveSystem` - Local storage management
- `LevelManager` - Progression and unlocking
- `OnlineLeaderboard` - Firebase integration
- `UsernameFilter` - Content moderation (200+ blocked words)

**Dependencies:** firebase_admin, python-dotenv, PyYAML

---

### Data Modules (src/data/)

**Purpose:** Game content and configuration data.

**Responsibilities:**
- Level layouts and platform positions
- Enemy spawn points and behaviors
- Story dialogue and cutscene sequences
- Game balance (enemy stats, coin values)

**Key Data:**
- `LEVELS` - Dictionary of all level configurations
- `STORY_SEQUENCES` - Cutscene dialogue trees
- `ENEMY_CONFIGS` - Enemy stats and AI parameters

**Dependencies:** None (pure data)

## Component Diagrams

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                       main.py                            │
│                    (Entry Point)                         │
└─────────────────────┬───────────────────────────────────┘
                      │
         ┌────────────▼────────────┐
         │    src/core/game_loop   │
         │    (Game State Machine) │
         └────┬──────────────┬─────┘
              │              │
     ┌────────▼────┐    ┌────▼──────────┐
     │ Input       │    │ Audio         │
     │ Handler     │    │ Manager       │
     └─────────────┘    └───────────────┘
              │              │
     ┌────────▼──────────────▼──────────┐
     │      src/entities/                │
     │  (Player, Enemies, Collectibles)  │
     └────────┬──────────────────────────┘
              │
     ┌────────▼──────────────────────────┐
     │    src/rendering/                 │
     │  (Graphics, Screens, Animations)  │
     └────────┬──────────────────────────┘
              │
     ┌────────▼──────────────────────────┐
     │       src/ui/                     │
     │  (HUD, Menus, Scoreboards)        │
     └────────┬──────────────────────────┘
              │
     ┌────────▼──────────────────────────┐
     │      src/utils/                   │
     │  (Save, Settings, Online)         │
     └───────────────────────────────────┘
```

### Data Flow - Gameplay Loop

```
 User Input
     │
     ▼
┌──────────────────┐
│ Input Handler    │
└────────┬─────────┘
         │ Raw Events
         ▼
┌──────────────────┐      ┌──────────────┐
│ Player Entity    │◄─────┤ Physics      │
└────────┬─────────┘      └──────────────┘
         │ Position/State
         ▼
┌──────────────────┐      ┌──────────────┐
│ Collision Check  ├─────►│ Enemies      │
│ (Physics)        │      │ Collectibles │
└────────┬─────────┘      └──────────────┘
         │ Game State
         ▼
┌──────────────────┐      ┌──────────────┐
│ Rendering        ├─────►│ UI Elements  │
│ (Draw Everything)│      │ (HUD)        │
└────────┬─────────┘      └──────────────┘
         │ Frame
         ▼
    Display Screen
```

### Save/Load System Flow

```
┌──────────────────┐
│  Player Action   │
│  (Complete Level)│
└────────┬─────────┘
         │
         ▼
┌──────────────────┐      ┌──────────────────┐
│  SaveSystem      │─────►│  Local Storage   │
│  (Save Score)    │      │  (.json)         │
└────────┬─────────┘      └──────────────────┘
         │
         ▼
┌──────────────────┐
│ Username Filter  │
│ (Validate Name)  │
└────────┬─────────┘
         │ If Valid
         ▼
┌──────────────────┐      ┌──────────────────┐
│ Online Leaderboard│─────►│  Firebase DB     │
│ (Upload Score)   │      │  (Cloud)         │
└──────────────────┘      └──────────────────┘
```

### Online Leaderboard Architecture

```
┌──────────────────┐
│  Scoreboard UI   │
└────────┬─────────┘
         │ Request Scores
         ▼
┌──────────────────┐
│ Online Leaderboard│
│ (Manager)        │
└────────┬─────────┘
         │ Query
         ▼
┌──────────────────┐      ┌──────────────────┐
│ Firebase Admin   │─────►│  Firebase        │
│ SDK              │      │  Realtime DB     │
└────────┬─────────┘      └──────────────────┘
         │ Data
         ▼
┌──────────────────┐
│ Score Filtering  │
│ (Difficulty/     │
│  Checkpoints)    │
└────────┬─────────┘
         │ Filtered Results
         ▼
┌──────────────────┐
│  Display with    │
│  Loading Spinner │
└──────────────────┘
```

## Data Flow

### Level Completion Flow

1. **Player completes level** → `main.py` detects level complete condition
2. **Display level complete screen** → `rendering.draw_level_complete_screen()`
3. **Get username** → `ui.username_input.PlayerProfileScreen()`
4. **Validate username** → `utils.username_filter.validate_username()`
5. **Save score locally** → `utils.save_system.SaveSystem.add_score()`
6. **Upload to online leaderboard** → `utils.online_leaderboard.submit_score()`
7. **Update progression** → `utils.progression.LevelManager.unlock_next_level()`
8. **Show scoreboard** → `ui.scoreboard.show_scoreboard()`

### Game State Machine

```
Title Screen
    │
    ├─► Level Select
    │       │
    │       └─► Start Level
    │               │
    │               ├─► Playing ◄──────┐
    │               │      │           │
    │               │      ├─► Paused ─┘
    │               │      │
    │               │      ├─► Death ─► Restart
    │               │      │
    │               │      └─► Level Complete
    │               │              │
    │               │              ├─► Username Input
    │               │              │
    │               │              └─► Scoreboard
    │               │                      │
    │               └──────────────────────┘
    │
    └─► Settings/Options
```

## Key Design Patterns

### 1. Singleton Pattern
**Used in:** `AudioManager`, `SaveSystem`, `OnlineLeaderboard`

**Purpose:** Ensure single instance of managers throughout game lifecycle.

```python
class SaveSystem:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
```

### 2. State Pattern
**Used in:** Game loop (title, playing, paused, game over)

**Purpose:** Manage different game states with clean transitions.

### 3. Component Pattern
**Used in:** UI elements (health display, spin charge, etc.)

**Purpose:** Modular, reusable UI components.

### 4. Observer Pattern
**Used in:** Input handling, event system

**Purpose:** Decouple input processing from game logic.

### 5. Factory Pattern
**Used in:** Enemy creation, particle systems

**Purpose:** Create entities based on configuration data.

## External Dependencies

### Runtime Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pygame | >=2.6.1 | Game engine, graphics, audio |
| pyyaml | >=6.0 | Configuration file parsing |
| python-dotenv | >=1.0.0 | Environment variable management |
| firebase-admin | >=6.0.0 | Online leaderboard backend |

### Development Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pytest | >=7.0 | Unit testing framework |
| pytest-cov | >=4.0 | Code coverage reporting |
| pyinstaller | >=6.0 | Standalone executable building |

## Performance Considerations

### Frame Rate
- Target: **60 FPS** constant
- Game loop uses fixed time step
- Render optimizations:
  - Sprite batching
  - Dirty rectangle updates
  - Background caching

### Memory Management
- Asset preloading during level load
- Particle system pooling
- Enemy spawn/despawn based on screen bounds
- Sound effect caching (max 10 concurrent sounds)

### Network Optimization
- Firebase queries run in background threads
- Loading spinner during online operations
- Graceful fallback to offline mode
- Score batching (future enhancement)

## Security

### Username Filtering
- 200+ blocked words and variants
- Leetspeak detection (0→o, 1→i, 3→e, etc.)
- Pattern matching for obfuscation
- URL detection and blocking
- Special character validation

### Firebase Security
- Environment variables for credentials
- Never commit firebase-key.json
- Read-only access for leaderboard queries
- Write operations require validation
- Rate limiting on submissions

## Testing Strategy

### Unit Tests (`tests/unit/`)
- Username filter validation (65 test cases)
- Physics collision detection
- Save/load functionality
- Score calculation

### Integration Tests (`tests/integration/`)
- Level completion flow
- Online leaderboard submission
- User progression system
- Audio playback

### Manual Testing
- Full gameplay playthroughs
- Performance profiling
- Cross-platform compatibility
- Accessibility features

## Future Enhancements

### Planned Improvements
1. **Multiplayer Support** - Local co-op gameplay
2. **Cloud Saves** - Cross-device progression
3. **Achievement System** - Unlockable rewards
4. **Replay System** - Record and playback runs
5. **Level Editor** - Community level creation
6. **Mod Support** - Custom content loading

### Technical Debt
- [ ] Refactor large rendering.py file
- [ ] Add type hints throughout codebase
- [ ] Implement event bus for decoupling
- [ ] Add logging framework
- [ ] Create automated build pipeline

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on:
- Code style and formatting
- Pull request process
- Testing requirements
- Documentation standards

## Additional Resources

- [User Guide](user/USER_GUIDE.md) - How to play
- [Firebase Setup](guides/FIREBASE_SETUP.md) - Online leaderboard configuration
- [Testing Guide](guides/TESTING.md) - Running tests
- [Tools Documentation](../tools/README.md) - Development utilities
