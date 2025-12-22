# Changes needed for main.py to integrate checkpoints

## 1. Add import at the top
```python
from src.ui.checkpoint import Checkpoint
```

## 2. After loading level, create checkpoints (around line 107, after level loading)
```python
# Create checkpoints if enabled
checkpoints = []
furthest_checkpoint_index = -1
last_checkpoint_position = (100, 300)  # Default spawn

if progression.checkpoints_enabled and level_num in LevelManager.CHECKPOINTS:
    for checkpoint_x in LevelManager.CHECKPOINTS[level_num]:
        checkpoints.append(Checkpoint(checkpoint_x))
```

## 3. In main game loop, check for checkpoint reach (around line 160, in game loop)
```python
# Check if player reached any checkpoints
if progression.checkpoints_enabled:
    for i, checkpoint in enumerate(checkpoints):
        if checkpoint.check_player_reached(player):
            furthest_checkpoint_index = i
            last_checkpoint_position = (checkpoint.x, 300)
            # Optional: play checkpoint sound
            # audio_manager.play_sound('checkpoint')
```

## 4. Draw checkpoints (in render section, around line 400, before UI drawing)
```python
# Draw checkpoints if enabled
if progression.checkpoints_enabled:
    for checkpoint in checkpoints:
        checkpoint.draw(screen, camera_offset)
```

## 5. Update death handling to show checkpoint option

Find the section that shows game over screen (around line 450-500). Currently looks like:
```python
result = draw_game_over_screen(screen, selected_option)
```

Change to pass checkpoints_enabled and handle checkpoint respawn:
```python
has_checkpoint = progression.checkpoints_enabled and furthest_checkpoint_index >= 0
result = draw_game_over_screen(screen, selected_option, checkpoints_enabled=has_checkpoint)

if result == "CHECKPOINT":
    # Respawn at last checkpoint
    player.rect.x, player.rect.y = last_checkpoint_position
    player.health = player.max_health
    player.is_dead = False
    player.invincible = True
    player.invincible_timer = player.invincible_duration
    game_state.game_over = False
    # DO NOT reset game_state.time_elapsed or game_state.deaths!
    # Time continues from where it was
    continue  # Continue game loop without full restart
elif result == "RESTART":
    # Full restart
    return "RESTART_LEVEL"
elif result == "MENU":
    return "MAIN_MENU"
```

## 6. Update score submission (find SaveSystem.submit_score call, around line 190)

Currently:
```python
SaveSystem.submit_score(
    username=current_username,
    level_num=level_num,
    time_taken=game_state.time_elapsed,
    coins_collected=coins_collected,
    difficulty=progression.difficulty
)
```

Change to:
```python
SaveSystem.submit_score(
    username=current_username,
    level_num=level_num,
    time_taken=game_state.time_elapsed,
    coins_collected=coins_collected,
    difficulty=progression.difficulty,
    checkpoints_enabled=progression.checkpoints_enabled
)
```

## Summary of main.py changes:
1. Import Checkpoint class
2. Create checkpoints list after level load
3. Check for checkpoint reach in game loop
4. Draw checkpoints in render section
5. Update death screen to handle checkpoint respawn
6. Pass checkpoints_enabled to submit_score

After these changes, test:
- Checkpoints appear when enabled
- Passing checkpoint marks it as reached (green)
- Can respawn at checkpoint after death
- Time continues from death time
- Scores are saved with checkpoint status
