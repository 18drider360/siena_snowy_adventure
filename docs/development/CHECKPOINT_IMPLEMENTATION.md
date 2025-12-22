# Checkpoints Feature Implementation

This document outlines the complete implementation of the checkpoints feature.

## Status: PARTIALLY COMPLETED

### Completed:
1. ✅ Added `checkpoints_enabled` to GameProgression class
2. ✅ Updated save/load system to persist checkpoint setting
3. ✅ Updated scoreboard submit_score to include checkpoints parameter

### Remaining Implementation:

## 1. Update Settings UI (PlayerProfileScreen in username_input.py)

Add checkpoints toggle below difficulty selection:

```python
# In __init__, add after self.difficulty:
self.checkpoints_enabled = checkpoints_enabled  # New parameter

# Add method to get checkpoints toggle rect
def get_checkpoints_toggle_rect(self):
    """Get rect for checkpoints toggle"""
    screen_width = self.screen.get_width()
    return pygame.Rect(screen_width // 2 - 200, 410, 400, 50)

# Update handle_event to toggle checkpoints
# Add spacebar or click handling to toggle self.checkpoints_enabled

# Update draw method to show checkpoints toggle with "ON/OFF" state
```

## 2. Define Checkpoint Positions

Add to LevelManager class in progression.py:

```python
# In LevelManager class
CHECKPOINTS = {
    1: [(2500,)],  # Level 1: 1 checkpoint at x=2500
    2: [(3000,), (6000,)],  # Level 2: 2 checkpoints
    3: [(3500,), (7500,)],  # Level 3: 2 checkpoints
    4: [(4000,), (9000,), (14000,)]  # Level 4: 3 checkpoints
}
```

## 3. Add Checkpoint Visual System

Create a simple flag/checkpoint marker class:

```python
class Checkpoint:
    def __init__(self, x):
        self.x = x
        self.y = 400  # Ground level
        self.rect = pygame.Rect(x, 350, 40, 50)
        self.reached = False

    def draw(self, screen, camera_offset):
        # Draw flag pole and flag
        pole_x = self.x - camera_offset
        color = (0, 255, 0) if self.reached else (200, 200, 200)
        # Pole
        pygame.draw.line(screen, (100, 50, 0), (pole_x, 350), (pole_x, 400), 3)
        # Flag
        points = [(pole_x, 350), (pole_x + 30, 365), (pole_x, 380)]
        pygame.draw.polygon(screen, color, points)
```

## 4. Update Game State (main.py)

Add checkpoint tracking to game state:

```python
# After loading level, create checkpoints
checkpoints = []
if progression.checkpoints_enabled and level_num in LevelManager.CHECKPOINTS:
    for cp_x in LevelManager.CHECKPOINTS[level_num]:
        checkpoints.append(Checkpoint(cp_x))

# Track furthest checkpoint reached
furthest_checkpoint_index = -1
last_checkpoint_x = 0

# In game loop, check if player passed a checkpoint
for i, checkpoint in enumerate(checkpoints):
    if not checkpoint.reached and player.rect.centerx >= checkpoint.x:
        checkpoint.reached = True
        furthest_checkpoint_index = i
        last_checkpoint_x = checkpoint.x
        # Play checkpoint sound/effect

# Draw checkpoints (only if enabled)
if progression.checkpoints_enabled:
    for checkpoint in checkpoints:
        checkpoint.draw(screen, camera_offset)
```

## 5. Update Death Screen (rendering.py)

Modify `draw_game_over_screen` to add checkpoint option:

```python
def draw_game_over_screen(screen, selected_option=0, checkpoints_enabled=False):
    # ...existing code...

    if checkpoints_enabled:
        options = ["RESTART LEVEL", "NEAREST CHECKPOINT", "MAIN MENU"]
    else:
        options = ["RESTART LEVEL", "MAIN MENU"]

    # Update button rendering to handle 3 options
    # Return selected option: "RESTART", "CHECKPOINT", or "MENU"
```

## 6. Update Main Game Loop (main.py)

Handle checkpoint respawn:

```python
# In death handling
death_result = show_game_over_screen(...)
if death_result == "CHECKPOINT":
    # Respawn at checkpoint
    player.rect.x = last_checkpoint_x
    player.rect.y = 300
    player.health = player.max_health
    player.is_dead = False
    game_state.game_over = False
    # Don't reset deaths or time!
    continue  # Continue game loop
elif death_result == "RESTART":
    # Full restart
    return "RESTART_LEVEL"
```

## 7. Update Scoreboard Save (save_system.py)

Already done - checkpoints parameter added to submit_score.

Update main.py to pass checkpoints:

```python
SaveSystem.submit_score(
    username=current_username,
    level_num=level_num,
    time_taken=game_state.time_elapsed,
    coins_collected=coins_collected,
    difficulty=progression.difficulty,
    checkpoints_enabled=progression.checkpoints_enabled  # ADD THIS
)
```

## 8. Update Scoreboard UI (ui/scoreboard.py)

Add checkpoints column and filter:

```python
# In ScoreboardUI class
# Add checkpoints filter toggle (similar to difficulty filter)
self.checkpoint_filter = None  # None, True (On), or False (Off)

# Update draw_scoreboard_table to:
# 1. Add "Checkpoints" column header
# 2. Display "On" or "Off" for each score
# 3. Filter scores based on checkpoint_filter

# Add UI elements to toggle checkpoint filter
# Add keyboard shortcuts (C key?) to toggle filter
```

## Files Modified So Far:
- ✅ src/utils/progression.py (added checkpoints_enabled field)
- ✅ src/utils/save_system.py (added checkpoints to save/load/submit)

## Files Still Need Changes:
- src/ui/username_input.py (add checkpoints toggle to settings)
- src/utils/progression.py (add CHECKPOINTS positions)
- main.py (add checkpoint logic, tracking, drawing, respawning)
- src/rendering/rendering.py (update death screen for checkpoint option)
- src/ui/scoreboard.py (add checkpoints column and filter)
- src/rendering/game_screens.py (pass checkpoints_enabled to settings screen)

## Testing Checklist:
- [ ] Can toggle checkpoints in settings
- [ ] Checkpoints save/load correctly
- [ ] Checkpoints appear in levels when enabled
- [ ] Passing checkpoint marks it as reached
- [ ] Death screen shows checkpoint option when enabled
- [ ] Can respawn at checkpoint with same time
- [ ] Scoreboard shows checkpoint status
- [ ] Can filter scoreboard by checkpoints
- [ ] Old scores show "Off" for checkpoints
