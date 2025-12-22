# Text Position Configuration Guide

## Overview
Each story scene can now have its dialogue/narration text positioned at either the **top** or **bottom** of the screen when a background image is displayed.

## How to Configure

### In `src/data/story_data.py`:

Add the `'text_position'` key to any scene dictionary:

```python
EXAMPLE_SCENE = {
    'type': 'dialogue',
    'speaker': 'Pedro',
    'background_image': 'assets/images/dialogue/example.png',
    'text_position': 'bottom',  # Options: 'top' or 'bottom'
    'lines': [
        "This text will appear at the bottom of the screen!",
        "",
        "[Press ENTER to continue]"
    ]
}
```

### Default Behavior
- If `'text_position'` is **not specified**, text defaults to **'top'**
- All existing scenes without this key will display text at the top (no breaking changes)

## Examples

### Text at Top (Default)
```python
SCENE_TOP = {
    'type': 'narration',
    'speaker': None,
    'background_image': 'assets/images/dialogue/scene_top.png',
    # No text_position specified - defaults to 'top'
    'lines': [
        "Text appears at the top of the screen.",
        "[Press ENTER to continue]"
    ]
}
```

### Text at Bottom (Explicit)
```python
SCENE_BOTTOM = {
    'type': 'dialogue',
    'speaker': 'Siena',
    'background_image': 'assets/images/dialogue/scene_bottom.png',
    'text_position': 'bottom',  # Explicitly set to bottom
    'lines': [
        "Text appears at the bottom of the screen.",
        "[Press ENTER to continue]"
    ]
}
```

### Text at Top (Explicit)
```python
SCENE_TOP_EXPLICIT = {
    'type': 'dialogue',
    'speaker': 'Pedro',
    'background_image': 'assets/images/dialogue/scene_top.png',
    'text_position': 'top',  # Explicitly set to top
    'lines': [
        "Text appears at the top of the screen.",
        "[Press ENTER to continue]"
    ]
}
```

## When to Use Bottom Positioning

Consider using `'text_position': 'bottom'` when:

1. **Important visual elements are at the top** of the background image
   - Character faces, sky, northern lights, etc.
2. **Action or focal point is in upper portion** of the image
   - Summit views, mountain peaks, aurora displays
3. **Creating visual variety** throughout the story
   - Mix top and bottom positioning to keep presentation fresh

## When to Use Top Positioning (Default)

Top positioning works well when:

1. **Important visual elements are at the bottom** of the image
   - Ground, paths, lower landscape elements
2. **Traditional subtitle style** is desired
   - Most cutscenes and films use top or bottom subtitles
3. **Character is in lower portion** of the image
   - Siena walking, standing poses at bottom

## Text Overlay Specifications

- **Overlay Height:** 140 pixels
- **Overlay Width:** Full screen width (1000px at base resolution)
- **Overlay Color:** Dark semi-transparent (RGB: 5, 10, 20 with alpha 200)
- **Text Font:** Arial, 18px (for narration/dialogue)
- **Speaker Font:** Arial, 24px bold (for speaker names)
- **Text Color:** White (255, 255, 255)

## Missing Images Handling

**Important:** If a `background_image` file doesn't exist, the system will:
1. Catch the FileNotFoundError gracefully
2. Fall back to the gradient background
3. Display text in the centered dialogue box (original style)
4. **Not crash or break the game**

This means you can safely reference image files that don't exist yet, and the game will still work!

## Example Scenes from Your Story

### Currently All Default to Top
All your current scenes default to top positioning. Here are some suggestions for moving specific scenes to bottom:

```python
# Scenes that might work well with BOTTOM positioning:

# Level 3 summit - focus on the vista below
LEVEL_3_SUMMIT_TRIUMPH = {
    'text_position': 'bottom',  # Add this
    # ... rest of scene data
}

# Level 4 aurora arrival - aurora is in sky (top)
LEVEL_4_LIGHTS_ARRIVAL = {
    'text_position': 'bottom',  # Add this
    # ... rest of scene data
}

# Opening lost scene - if Siena is in upper portion
OPENING_LOST = {
    'text_position': 'bottom',  # Add this if character is at top
    # ... rest of scene data
}
```

## Quick Reference

| Position | Value      | Overlay Location          | Use When                        |
|----------|------------|---------------------------|---------------------------------|
| Top      | `'top'`    | Top 140px of screen       | Default, focal point at bottom  |
| Bottom   | `'bottom'` | Bottom 140px of screen    | Focal point at top of image     |

## Testing Your Changes

After adding `'text_position'` to scenes:

1. **Syntax Check:**
   ```bash
   python3 -m py_compile src/data/story_data.py
   ```

2. **Run Game:**
   ```bash
   python3 main.py
   ```

3. **Test Each Scene:**
   - Navigate through story sequences
   - Verify text appears at intended position
   - Check that text is readable over background

## Notes

- This feature **only affects scenes with background images**
- Scenes without `'background_image'` always use centered dialogue box
- Ending scenes (without images) are not affected
- Text positioning is per-scene, allowing fine control over presentation

---

**Created:** 2025-12-20
**Feature Added:** Text Position Configuration for Story Scenes
