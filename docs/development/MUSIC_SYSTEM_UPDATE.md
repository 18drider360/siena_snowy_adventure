# Music System Update - Dialogue Music

## Overview

Updated the game to use three distinct music tracks for different game contexts:

1. **Menu Music** - `Oh Xmas.mp3` (title screen, settings, scoreboard, etc.)
2. **Gameplay Music** - `main_theme.ogg` (during level gameplay)
3. **Dialogue Music** - `dialogue.wav` (story cutscenes and tutorial screens)

All tracks loop indefinitely during their respective contexts.

---

## Music Flow

### Starting the Game
```
Launch Game
↓
Title Screen → Oh Xmas.mp3 (menu music)
↓
Select "Start Game" or Level
↓
Opening Story Cutscenes → dialogue.wav switches here
↓
Level 1 Intro Cutscene → dialogue.wav continues
↓
Tutorial Screens → dialogue.wav continues
↓
Level 1 Gameplay Starts → main_theme.ogg switches here
```

### Between Levels
```
Complete Level 1
↓
Level 1 Complete Story → dialogue.wav switches here
↓
Level 2 Intro Story → dialogue.wav continues
↓
Tutorial Screens → dialogue.wav continues
↓
Level 2 Gameplay Starts → main_theme.ogg switches here
```

### Returning to Menu
```
Pause Menu / Death Menu
↓
Select "Main Menu"
↓
Title Screen → Oh Xmas.mp3 switches here
```

---

## Technical Implementation

### Files Modified

#### 1. [src/rendering/game_screens.py](src/rendering/game_screens.py)

**`show_story_cutscene()` function (Lines 267-278):**
```python
# Start dialogue music - only load if not already playing dialogue music
global _current_music_track
if not disable_audio:
    try:
        # Only load dialogue.wav if we're not already playing it
        if _current_music_track != "dialogue.wav":
            pygame.mixer.music.load("assets/music/dialogue.wav")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)  # Loop indefinitely
            _current_music_track = "dialogue.wav"
    except Exception as e:
        print(f"Could not load cutscene music: {e}")
```
**Key Feature:** Uses `_current_music_track` global variable to track which music is playing and avoid restarting dialogue.wav on each scene transition.

**`show_level_transition()` function (Lines 532-543):**
```python
# Play dialogue music for tutorial/transition screens - only load if not already playing dialogue music
global _current_music_track
if not disable_audio:
    try:
        # Only load dialogue.wav if we're not already playing it
        if _current_music_track != "dialogue.wav":
            pygame.mixer.music.load("assets/music/dialogue.wav")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)  # Loop indefinitely
            _current_music_track = "dialogue.wav"
    except Exception as e:
        print(f"Could not load dialogue music: {e}")
```
**Key Feature:** Checks `_current_music_track` - if already "dialogue.wav", continues playing without restarting.

**`show_educational_screens()` function (Lines 444-456):**
```python
# Continue playing dialogue music (should already be playing from show_level_transition)
global _current_music_track
if not disable_audio:
    try:
        # Only load dialogue.wav if somehow it's not already playing
        if _current_music_track != "dialogue.wav":
            pygame.mixer.music.load("assets/music/dialogue.wav")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)  # Loop forever
            _current_music_track = "dialogue.wav"
    except Exception as e:
        print(f"Could not load dialogue music: {e}")
```
**Key Feature:** Ensures dialogue music continues through ability/enemy tutorial screens. Also removed music.stop() call that was interrupting the music.

**Title Screen (Lines 335-342):**
```python
global _current_music_track
# Only load Oh Xmas if not already playing it
if _current_music_track != "Oh Xmas.mp3":
    pygame.mixer.music.load("assets/music/Oh Xmas.mp3")
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1)
    _current_music_track = "Oh Xmas.mp3"
```

#### 2. [main.py](main.py)

**After First Tutorial (Lines 1173-1181):**
```python
# Switch back to gameplay music after tutorials
if not DISABLE_ALL_AUDIO:
    try:
        import src.rendering.game_screens as gs
        pygame.mixer.music.load("assets/music/main_theme.ogg")
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)
        gs._current_music_track = "main_theme.ogg"  # Update tracker
    except Exception as e:
        logger.debug(f"Could not load gameplay music: {e}")
```

**After Level Transition (Lines 1218-1226):**
```python
# Switch back to gameplay music after tutorials
if not DISABLE_ALL_AUDIO:
    try:
        import src.rendering.game_screens as gs
        pygame.mixer.music.load("assets/music/main_theme.ogg")
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)
        gs._current_music_track = "main_theme.ogg"  # Update tracker
    except Exception as e:
        logger.debug(f"Could not load gameplay music: {e}")
```

---

## Music Tracking System

A global variable `_current_music_track` is used to track which music file is currently loaded:

```python
# In src/rendering/game_screens.py
_current_music_track = None
```

This variable is updated whenever music is loaded:
- Set to `"Oh Xmas.mp3"` when menu music starts
- Set to `"dialogue.wav"` when story/tutorial music starts
- Set to `"main_theme.ogg"` when gameplay music starts

Before loading any music, the code checks if that track is already loaded. If it is, the music continues playing without interruption.

---

## Music Track Details

### Oh Xmas.mp3 (Menu Music)
- **Volume:** 0.5
- **Loop:** Infinite
- **Plays during:**
  - Title screen
  - Settings menu
  - Scoreboard
  - Any menu navigation

### main_theme.ogg (Gameplay Music)
- **Volume:** 0.6
- **Loop:** Infinite
- **Plays during:**
  - All level gameplay (Levels 1-4)
  - Loaded by default in AudioManager
  - Resumes after death/respawn

### dialogue.wav (Dialogue/Tutorial Music)
- **Volume:** 0.5
- **Loop:** Infinite
- **Plays during:**
  - All story cutscenes (opening, level intros, level complete, ending)
  - All tutorial/transition screens
  - Any narrative moment
- **Important:** Plays continuously without restarting between scenes
  - Starts once when first cutscene begins
  - Continues uninterrupted through all dialogue scenes
  - Continues through tutorial screens
  - Only stops when gameplay music takes over

---

## Music Transitions

The game seamlessly switches between music tracks at these points:

| From | To | Trigger Point |
|------|-----|--------------|
| Menu Music | Dialogue Music | Start game → Opening story begins |
| Dialogue Music | Gameplay Music | Tutorial screens end → Level starts |
| Gameplay Music | Dialogue Music | Level complete → Story cutscene begins |
| Dialogue Music | Gameplay Music | Story + tutorials end → Next level starts |
| Gameplay Music | Menu Music | Return to main menu |
| Menu Music | Menu Music | Navigate between menus (no change) |

---

## Audio Settings Control

All music respects the audio settings:

**In [src/utils/settings.py](src/utils/settings.py:15):**
```python
MASTER_AUDIO_ENABLED = True  # Master switch for all audio
```

**In [config.yaml](config.yaml):**
```yaml
audio:
  master_enabled: true
  music_enabled: true
  sound_enabled: true
  music_volume: 0.6
  sound_volume: 1.0
```

If `MASTER_AUDIO_ENABLED = False`, all music and sound effects are disabled globally.

---

## Benefits

✅ **Distinct Atmospheres** - Each game context has its own musical identity
✅ **Seamless Transitions** - Music switches automatically at natural transition points
✅ **Looping** - All tracks loop infinitely, no awkward silence
✅ **Continuous Dialogue Music** - dialogue.wav plays uninterrupted through all scenes and tutorials
✅ **No Restarts** - Pressing ENTER to advance scenes doesn't restart the music
✅ **Immersive** - Dialogue music creates narrative atmosphere separate from gameplay
✅ **Professional Feel** - Music changes enhance game polish and player experience

---

## Testing

To verify the music system works correctly:

1. **Start game** → Should hear Oh Xmas.mp3
2. **Click "Start Game"** → Music should switch to dialogue.wav when opening story begins
3. **Progress through story** → dialogue.wav continues through all cutscenes
4. **Tutorial screens appear** → dialogue.wav continues
5. **Level 1 starts** → Music should switch to main_theme.ogg
6. **Complete Level 1** → Music should switch to dialogue.wav when story appears
7. **Level 2 starts** → Music should switch back to main_theme.ogg
8. **Return to menu** → Music should switch to Oh Xmas.mp3

---

**Updated:** 2025-12-20
**Feature:** Three-track music system with contextual switching
**Files Modified:**
- [src/rendering/game_screens.py](src/rendering/game_screens.py) - Dialogue music in cutscenes/tutorials
- [main.py](main.py) - Gameplay music after tutorials
**Music Files:**
- assets/music/Oh Xmas.mp3 (menu)
- assets/music/main_theme.ogg (gameplay)
- assets/music/dialogue.wav (narrative)
