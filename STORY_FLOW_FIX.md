# Story Flow Fix - Continuous Dialogue Before Tutorial

## Problem
When completing a level, the story dialogue was split with tutorial screens in the middle:
1. Level complete dialogue
2. **Tutorial screens** ← Interrupting the story
3. Next level intro dialogue

This broke the narrative flow and felt disconnected.

## Solution
Reorganized the flow so ALL story dialogue plays together, then tutorials, then gameplay.

---

## New Flow Structure

### Level 1 (First Time)
```
1. Opening story (5 scenes)
2. Level 1 intro dialogue (1 scene)
3. Tutorial screens (Basic abilities + Level 1 enemies)
4. Level 1 gameplay
```

### Levels 2-4 (After Completing Previous Level)
```
1. Previous level complete dialogue (3-4 scenes)
2. Next level intro dialogue (2-5 scenes)
3. Tutorial screens (New ability + enemies for this level)
4. Level gameplay
```

### Example: Completing Level 1 → Starting Level 2
**Old flow:**
```
Beat Level 1
→ LEVEL_1_COMPLETE_SIENA dialogue
→ LEVEL_1_COMPLETE_PEDRO dialogue
→ LEVEL_1_PEDRO_FORWARD dialogue
→ Tutorial screens ← Breaks story flow
→ LEVEL_2_ARRIVAL dialogue ← Story continues after tutorial
→ LEVEL_2_PEDRO_INTRO dialogue
→ Level 2 gameplay
```

**New flow:**
```
Beat Level 1
→ LEVEL_1_COMPLETE_SIENA dialogue
→ LEVEL_1_COMPLETE_PEDRO dialogue
→ LEVEL_1_PEDRO_FORWARD dialogue
→ LEVEL_2_ARRIVAL dialogue       } All story together
→ LEVEL_2_PEDRO_INTRO dialogue   }
→ Tutorial screens ← Now comes after ALL dialogue
→ Level 2 gameplay
```

---

## Technical Implementation

### Changes Made in [main.py](main.py)

**1. Level 1 Start (Lines 1157-1165)**
```python
# Show opening story + Level 1 intro before Level 1
if progression.current_level == 1 and 'opening' not in stories_shown:
    show_story_cutscene('opening', disable_audio=DISABLE_ALL_AUDIO)
    stories_shown.add('opening')

    # Also show Level 1 intro after opening
    if 'level_1_intro' not in stories_shown:
        show_story_cutscene('level_1_intro', disable_audio=DISABLE_ALL_AUDIO)
        stories_shown.add('level_1_intro')
```

**2. Level Complete → Next Level (Lines 1182-1207)**
```python
elif game_result == "NEXT_LEVEL":
    # Show post-level story for completed level
    post_level_key = f'level_{completed_level}_complete'
    if post_level_key not in stories_shown:
        show_story_cutscene(post_level_key, disable_audio=DISABLE_ALL_AUDIO)
        stories_shown.add(post_level_key)

    # Show ending if Level 4 complete
    if completed_level == 4 and 'ending' not in stories_shown:
        show_story_cutscene('ending', disable_audio=DISABLE_ALL_AUDIO)
        stories_shown.add('ending')

    # Show pre-level story for NEXT level (NEW: moved here)
    pre_level_key = f'level_{progression.current_level}_intro'
    if pre_level_key not in stories_shown:
        show_story_cutscene(pre_level_key, disable_audio=DISABLE_ALL_AUDIO)
        stories_shown.add(pre_level_key)

    # NOW show tutorials (after all dialogue)
    show_level_transition(progression.current_level, disable_audio=DISABLE_ALL_AUDIO)
    tutorials_shown.add(progression.current_level)
```

**3. Removed Duplicate Pre-Level Check**
The old code had pre-level dialogue at the top of the loop, which caused it to show AFTER tutorials. This has been removed and consolidated into the NEXT_LEVEL handler.

---

## Complete Flow by Level

### Starting Game → Level 1
```
[START GAME]
↓
Opening Story (5 scenes)
  - OPENING_LOST
  - OPENING_PEDRO_APPEARS
  - OPENING_PEDRO_OFFER
  - OPENING_SIENA_ACCEPTS
  - OPENING_PEDRO_TUTORIAL
↓
Level 1 Intro (1 scene)
  - LEVEL_1_INTRO
↓
Tutorial Screens
  - Basic Abilities
  - Level 1 Enemies
↓
[LEVEL 1 GAMEPLAY]
```

### Level 1 Complete → Level 2
```
[BEAT LEVEL 1]
↓
Level 1 Complete Story (3 scenes)
  - LEVEL_1_COMPLETE_SIENA
  - LEVEL_1_COMPLETE_PEDRO
  - LEVEL_1_PEDRO_FORWARD
↓
Level 2 Intro Story (2 scenes)
  - LEVEL_2_ARRIVAL
  - LEVEL_2_PEDRO_INTRO
↓
Tutorial Screens
  - Roll Ability
  - Level 2 Enemies
↓
[LEVEL 2 GAMEPLAY]
```

### Level 2 Complete → Level 3
```
[BEAT LEVEL 2]
↓
Level 2 Complete Story (3 scenes)
  - LEVEL_2_COMPLETE_SIENA
  - LEVEL_2_PEDRO_PROUD
  - LEVEL_2_MOUNTAIN_PREVIEW
↓
Level 3 Intro Story (5 scenes)
  - LEVEL_3_DOUBT
  - LEVEL_3_FAMILY_MEMORY
  - LEVEL_3_PEDRO_BELIEF
  - LEVEL_3_PEDRO_WARNING
  - LEVEL_3_PEDRO_ENCOURAGEMENT
↓
Tutorial Screens
  - Spin Attack Ability
  - Level 3 Enemies
↓
[LEVEL 3 GAMEPLAY]
```

### Level 3 Complete → Level 4
```
[BEAT LEVEL 3]
↓
Level 3 Complete Story (4 scenes)
  - LEVEL_3_SUMMIT_TRIUMPH
  - LEVEL_3_PEDRO_REVELATION
  - LEVEL_3_NORTHERN_LIGHTS_VIEW
  - LEVEL_3_PEDRO_FINAL_PUSH
↓
Level 4 Intro Story (4 scenes)
  - LEVEL_4_LIGHTS_ARRIVAL
  - LEVEL_4_PEDRO_WARNING
  - LEVEL_4_PEDRO_GOODBYE
  - LEVEL_4_SIENA_READY
↓
Tutorial Screens
  - Level 4 Intro
  - Level 4 Enemies
↓
[LEVEL 4 GAMEPLAY]
```

### Level 4 Complete → Ending
```
[BEAT LEVEL 4]
↓
Level 4 Complete Story (skipped - goes to ending)
↓
Ending Story (6 scenes)
  - ENDING_ARRIVAL
  - ENDING_REUNION
  - ENDING_SIENA_EXPLAINS
  - ENDING_PEDRO_THANKS
  - ENDING_PEDRO_GONE
  - ENDING_FINAL
↓
[RETURN TO MAIN MENU]
```

---

## Benefits

✅ **Continuous narrative** - All story dialogue flows naturally without interruption
✅ **Better pacing** - Story beats complete before practical tutorial
✅ **Clear separation** - Story → Tutorial → Gameplay is logical and clean
✅ **Emotional flow** - Level completion celebration + next level setup happens together
✅ **No confusion** - Players get all context before seeing "how to play" screens

---

## Key Changes Summary

| What Changed | Before | After |
|-------------|--------|-------|
| **Level start** | Pre-level dialogue at loop start | Only for Level 1 with opening |
| **Level complete** | Post-level → Tutorial → Pre-level (next loop) | Post-level → Pre-level → Tutorial |
| **Tutorial timing** | Between dialogue sequences | After all dialogue |
| **Story flow** | Interrupted by tutorials | Continuous, then tutorials |

---

## Testing Checklist

To verify the new flow works correctly:

- [ ] Start new game → Opening + Level 1 intro play together
- [ ] Tutorial screens show after opening/intro
- [ ] Beat Level 1 → Level 1 complete + Level 2 intro play together
- [ ] Tutorial screens show after both dialogue sequences
- [ ] Level 2 starts immediately after tutorial
- [ ] Repeat for Levels 2→3 and 3→4
- [ ] Level 4 complete → Ending plays
- [ ] No duplicate dialogue shown
- [ ] No tutorials interrupting story

---

**Updated:** 2025-12-20
**Issue:** Tutorials interrupting story flow
**Solution:** Moved pre-level dialogue to NEXT_LEVEL handler
**Files Modified:** main.py (lines 1157-1207)
