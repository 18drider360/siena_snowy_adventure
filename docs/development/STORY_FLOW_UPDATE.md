# Story Flow Update - Tutorial Screens Repositioned

## Changes Made

### Removed Tutorial Dialogue from Story Sequences
The `LEVEL_2_ROLL_TRAINING` and `LEVEL_3_SPIN_TRAINING` dialogue scenes have been **removed** from the story cutscene sequences.

These were dialogue scenes where Pedro verbally teaches abilities, but they were interrupting the narrative flow.

## New Flow Structure

### Before (Old Flow):
```
Level 2:
1. Story dialogue (LEVEL_2_ARRIVAL)
2. Story dialogue (LEVEL_2_ROLL_TRAINING) ← Tutorial dialogue mixed in
3. Story dialogue (LEVEL_2_PEDRO_INTRO)
4. Tutorial screen (Roll ability) ← Actual tutorial screen
5. Level starts

Level 3:
1. Story dialogue (LEVEL_3_DOUBT)
2. Story dialogue (LEVEL_3_FAMILY_MEMORY)
3. Story dialogue (LEVEL_3_PEDRO_BELIEF)
4. Story dialogue (LEVEL_3_PEDRO_WARNING)
5. Story dialogue (LEVEL_3_SPIN_TRAINING) ← Tutorial dialogue mixed in
6. Story dialogue (LEVEL_3_PEDRO_ENCOURAGEMENT)
7. Tutorial screen (Spin Attack ability) ← Actual tutorial screen
8. Level starts
```

### After (New Flow):
```
Level 2:
1. Story dialogue (LEVEL_2_ARRIVAL)
2. Story dialogue (LEVEL_2_PEDRO_INTRO)
3. Tutorial screen (Roll ability) ← Last thing before level
4. Level starts

Level 3:
1. Story dialogue (LEVEL_3_DOUBT)
2. Story dialogue (LEVEL_3_FAMILY_MEMORY)
3. Story dialogue (LEVEL_3_PEDRO_BELIEF)
4. Story dialogue (LEVEL_3_PEDRO_WARNING)
5. Story dialogue (LEVEL_3_PEDRO_ENCOURAGEMENT)
6. Tutorial screen (Spin Attack ability) ← Last thing before level
7. Level starts
```

## Benefits

1. **Cleaner narrative flow** - All story dialogue plays together without interruption
2. **Better tutorial timing** - Tutorial screens appear immediately before the level where the ability is needed
3. **Less redundancy** - No need to explain abilities twice (once in dialogue, once in tutorial screen)

## Technical Details

### Files Modified:
- **[src/data/story_data.py](src/data/story_data.py:667-682)** - Removed training scenes from sequences

### Removed from `level_2_intro`:
- `LEVEL_2_ROLL_TRAINING` (dialogue scene)

### Removed from `level_3_intro`:
- `LEVEL_3_SPIN_TRAINING` (dialogue scene)

### Tutorial Screens Still Show:
The actual tutorial screens still appear via `show_level_transition()` in [main.py](main.py:1170):
- **Level 1:** Basic abilities + Level 1 enemies
- **Level 2:** Roll ability + Level 2 enemies
- **Level 3:** Spin Attack ability + Level 3 enemies
- **Level 4:** Level 4 intro + Level 4 enemies

These tutorial screens are the **last thing** shown before each level starts.

## Current Flow for Each Level

### Level 1:
```
Opening story (5 scenes) → Level 1 intro dialogue → Tutorial screens → Level 1 gameplay
```

### Level 2:
```
Level 1 complete dialogue (3 scenes) → Level 2 intro dialogue (2 scenes) → Tutorial screens → Level 2 gameplay
```

### Level 3:
```
Level 2 complete dialogue (3 scenes) → Level 3 intro dialogue (5 scenes) → Tutorial screens → Level 3 gameplay
```

### Level 4:
```
Level 3 complete dialogue (4 scenes) → Level 4 intro dialogue (4 scenes) → Tutorial screens → Level 4 gameplay
```

### Ending:
```
Level 4 complete → Ending story (6 scenes) → Return to main menu
```

## Note on Removed Scenes

The `LEVEL_2_ROLL_TRAINING` and `LEVEL_3_SPIN_TRAINING` scenes **still exist** in the story_data.py file but are **not used** in any sequence. They can be:
- Kept as reference/documentation
- Deleted if you want to clean up the file
- Repurposed for other use

The actual tutorial functionality comes from the tutorial screens, not these dialogue scenes.

## Testing

To verify the new flow:

1. Start a new game
2. Observe that all story dialogue plays together
3. Tutorial screens appear last before each level
4. No duplicate ability explanations

---

**Updated:** 2025-12-20
**Change:** Repositioned tutorial screens to appear last before level starts
**Files Modified:** src/data/story_data.py
