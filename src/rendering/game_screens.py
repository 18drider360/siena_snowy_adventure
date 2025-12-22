"""
Game Screens Module
Handles title screen, level transitions, and educational screens
"""

import sys
import pygame
from src.utils import settings as S
from src.rendering.screens.title_screen import TitleScreen, LevelSelectScreen, GuideScreen
from src.ui.scoreboard import show_scoreboard
from src.ui.username_input import PlayerProfileScreen
from src.rendering.rendering import (
    draw_level_transition_screen, draw_new_ability_screen,
    draw_level_4_intro_screen, draw_basic_abilities_screen,
    draw_new_enemies_screen
)
from src.data.story_data import STORY_SEQUENCES

# Track which music is currently loaded to avoid restarting
_current_music_track = None


def scale_mouse_pos(mouse_pos):
    """Convert mouse position from display coordinates to internal render coordinates"""
    return (int(mouse_pos[0] / S.DISPLAY_SCALE), int(mouse_pos[1] / S.DISPLAY_SCALE))


def draw_story_scene(screen, scene_data):
    """
    Draw a story cutscene with dialogue or narration

    Args:
        screen: Pygame surface to draw on
        scene_data: Dictionary with 'type', 'speaker', 'lines', optional 'background_image',
                    and optional 'text_position' ('top' or 'bottom', default: 'top')
    """
    # Check if scene has a background image
    has_bg_image = False
    if 'background_image' in scene_data and scene_data['background_image']:
        try:
            # Fill screen with black first (for letterboxing)
            screen.fill((0, 0, 0))

            # Load the background image
            bg_image = pygame.image.load(scene_data['background_image'])
            img_width, img_height = bg_image.get_size()

            # Calculate scaling to fit entire image (letterbox style)
            scale_x = S.WINDOW_WIDTH / img_width
            scale_y = S.WINDOW_HEIGHT / img_height
            scale = min(scale_x, scale_y)  # Use min to fit entire image

            # Scale the image using high-quality smoothscale
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            bg_image = pygame.transform.smoothscale(bg_image, (new_width, new_height))

            # Center the image (creates black bars on sides or top/bottom)
            offset_x = (S.WINDOW_WIDTH - new_width) // 2
            offset_y = (S.WINDOW_HEIGHT - new_height) // 2

            # Blit the centered image
            screen.blit(bg_image, (offset_x, offset_y))
            has_bg_image = True
        except FileNotFoundError:
            # Image file doesn't exist - silently fall through to gradient background
            has_bg_image = False
        except Exception as e:
            # Other errors - print warning but continue
            print(f"Warning: Could not load background image '{scene_data['background_image']}': {e}")
            has_bg_image = False

    # If no background image or failed to load, use gradient background
    if not has_bg_image:
        # Fill background with gradient (dark blue to lighter blue)
        for y in range(S.WINDOW_HEIGHT):
            progress = y / S.WINDOW_HEIGHT
            color = (
                int(10 + 30 * progress),
                int(20 + 50 * progress),
                int(40 + 80 * progress)
            )
            pygame.draw.line(screen, color, (0, y), (S.WINDOW_WIDTH, y))

    # Get text position preference (default to 'top')
    text_position = scene_data.get('text_position', 'top')

    if has_bg_image:
        # For scenes with background images, calculate required box height
        # Count non-empty lines to estimate needed height
        non_empty_lines = [line for line in scene_data['lines'] if line.strip()]
        empty_lines = len([line for line in scene_data['lines'] if not line.strip()])

        # Start with base font size and calculate needed height (reduced from 18/22)
        base_font_size = 16
        base_line_height = 19

        # Calculate if we need speaker space
        speaker_space = 45 if scene_data.get('speaker') else 18

        # Estimate needed height (with some padding)
        estimated_height = speaker_space + (len(non_empty_lines) * base_line_height) + (empty_lines * (base_line_height // 2)) + 18

        # Clamp to reasonable range (min 120, max 220 - reduced from 140-250)
        box_height = max(120, min(220, estimated_height))

        box_width = S.WINDOW_WIDTH
        box_x = 0

        # Position overlay at top or bottom based on preference
        if text_position == 'bottom':
            box_y = S.WINDOW_HEIGHT - box_height
        else:  # default to top
            box_y = 0

        # Draw dark semi-transparent overlay for text readability
        overlay = pygame.Surface((box_width, box_height))
        overlay.set_alpha(200)  # Slightly more opaque for better readability
        overlay.fill((5, 10, 20))  # Darker background
        screen.blit(overlay, (box_x, box_y))

        # No border for full-width overlay
    else:
        # Original centered dialogue box for non-image scenes
        box_width = 700
        box_height = 400
        box_x = (S.WINDOW_WIDTH - box_width) // 2
        box_y = (S.WINDOW_HEIGHT - box_height) // 2

        # Draw box shadow
        shadow_surface = pygame.Surface((box_width, box_height))
        shadow_surface.set_alpha(100)
        shadow_surface.fill((0, 0, 0))
        screen.blit(shadow_surface, (box_x + 5, box_y + 5))

        # Draw main dialogue box (frosted glass effect)
        box_surface = pygame.Surface((box_width, box_height))
        box_surface.set_alpha(220)
        box_surface.fill((240, 245, 255))
        screen.blit(box_surface, (box_x, box_y))

        # Draw box border
        pygame.draw.rect(screen, (60, 90, 140), (box_x, box_y, box_width, box_height), 3)

    # Draw speaker name if dialogue (not narration)
    if scene_data['speaker']:
        if has_bg_image:
            # Smaller, cleaner font for images (anime-style) - reduced from 24
            speaker_font = pygame.font.SysFont('Arial', 20, bold=True)
            speaker_color = (255, 255, 255)
            speaker_text = speaker_font.render(scene_data['speaker'], True, speaker_color)
            speaker_rect = speaker_text.get_rect(centerx=S.WINDOW_WIDTH // 2, top=box_y + 10)
            screen.blit(speaker_text, speaker_rect)

            # Subtle underline
            underline_y = speaker_rect.bottom + 3
            pygame.draw.line(screen, (255, 255, 255),
                            (S.WINDOW_WIDTH // 2 - 50, underline_y),
                            (S.WINDOW_WIDTH // 2 + 50, underline_y), 1)

            text_start_y = box_y + 45
        else:
            # Original style for non-image scenes
            speaker_font = pygame.font.Font(None, 42)
            speaker_color = (20, 50, 100)
            speaker_text = speaker_font.render(scene_data['speaker'], True, speaker_color)
            speaker_rect = speaker_text.get_rect(centerx=S.WINDOW_WIDTH // 2, top=box_y + 20)
            screen.blit(speaker_text, speaker_rect)

            underline_y = speaker_rect.bottom + 5
            pygame.draw.line(screen, (60, 90, 140),
                            (box_x + 50, underline_y),
                            (box_x + box_width - 50, underline_y), 2)

            text_start_y = box_y + 80
    else:
        # Narration - no speaker, text starts higher
        text_start_y = box_y + 15 if has_bg_image else box_y + 40

    # Draw dialogue/narration text
    if has_bg_image:
        # Calculate available space for text
        available_height = box_height - (text_start_y - box_y) - 15  # 15px bottom padding

        # Count lines and estimate if they'll fit
        non_empty_count = len([line for line in scene_data['lines'] if line.strip()])
        empty_count = len([line for line in scene_data['lines'] if not line.strip()])

        # Start with smaller size (reduced from 18/22)
        font_size = 16
        line_height = 19

        # Estimate total needed height
        needed_height = (non_empty_count * line_height) + (empty_count * (line_height // 2))

        # If text won't fit, reduce font size and line height
        if needed_height > available_height:
            # Calculate reduction factor
            reduction_factor = available_height / needed_height
            font_size = max(14, int(font_size * reduction_factor))  # Don't go below 14px
            line_height = max(16, int(line_height * reduction_factor))  # Don't go below 16px

        # Create font with calculated size
        text_font = pygame.font.SysFont('Arial', font_size)
        text_color = (255, 255, 255)

        # Render all lines (they should all fit now)
        current_y = text_start_y
        margin_x = 30  # Side margins
        max_y = box_y + box_height - 10  # Stay within the box

        for line in scene_data['lines']:
            if line.strip() == "":
                # Empty line - add spacing
                current_y += line_height // 2
            else:
                # Render the line
                text_surface = text_font.render(line, True, text_color)
                text_rect = text_surface.get_rect(centerx=S.WINDOW_WIDTH // 2, top=current_y)

                # Draw the line (should always fit now)
                if current_y + line_height <= max_y:
                    screen.blit(text_surface, text_rect)
                    current_y += line_height
                else:
                    # Safety check - this shouldn't happen but render anyway
                    screen.blit(text_surface, text_rect)
                    current_y += line_height
    else:
        # Original font for non-image scenes
        text_font = pygame.font.Font(None, 32)
        line_height = 40
        text_color = (20, 30, 50)

        for i, line in enumerate(scene_data['lines']):
            text_surface = text_font.render(line, True, text_color)
            text_rect = text_surface.get_rect(centerx=S.WINDOW_WIDTH // 2,
                                              top=text_start_y + i * line_height)
            screen.blit(text_surface, text_rect)


def show_story_cutscene(story_key, disable_audio=False):
    """
    Display a story cutscene sequence

    Args:
        story_key: Key from STORY_SEQUENCES to show (e.g., 'opening', 'level_1_intro')
        disable_audio: Whether to disable audio

    Returns:
        str: 'CONTINUE' when finished, 'QUIT' if window closed
    """
    if story_key not in STORY_SEQUENCES:
        return 'CONTINUE'  # Skip if story key doesn't exist

    if not pygame.get_init():
        pygame.init()

    # Create scaled display window
    display_width = int(S.WINDOW_WIDTH * S.DISPLAY_SCALE)
    display_height = int(S.WINDOW_HEIGHT * S.DISPLAY_SCALE)
    display_screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption(S.TITLE)

    # Create internal render surface (800x600)
    screen = pygame.Surface((S.WINDOW_WIDTH, S.WINDOW_HEIGHT))

    clock = pygame.time.Clock()

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

    # Show each scene in the sequence
    scenes = STORY_SEQUENCES[story_key]

    for scene_data in scenes:
        running = True
        while running:
            clock.tick(S.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False  # Move to next scene

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Click anywhere to continue
                    running = False

            # Draw the scene
            draw_story_scene(screen, scene_data)

            # Scale and display
            scaled_surface = pygame.transform.scale(screen, (display_width, display_height))
            display_screen.blit(scaled_surface, (0, 0))
            pygame.display.flip()

    return 'CONTINUE'


def show_title_screen(progression, disable_audio=False):
    """Display title screen and handle menu navigation"""
    # Initialize pygame if not already done
    if not pygame.get_init():
        pygame.init()

    # Create scaled display window
    display_width = int(S.WINDOW_WIDTH * S.DISPLAY_SCALE)
    display_height = int(S.WINDOW_HEIGHT * S.DISPLAY_SCALE)
    display_screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption(S.TITLE)

    # Create internal render surface (800x600) - this is what we draw to
    screen = pygame.Surface((S.WINDOW_WIDTH, S.WINDOW_HEIGHT))

    clock = pygame.time.Clock()

    # Start title screen music (if not already playing)
    if not disable_audio:
        try:
            global _current_music_track
            # Only load Oh Xmas if not already playing it
            if _current_music_track != "Oh Xmas.mp3":
                # Title screen uses Oh Xmas.mp3
                pygame.mixer.music.load("assets/music/Oh Xmas.mp3")
                pygame.mixer.music.set_volume(0.6)
                pygame.mixer.music.play(-1)  # Loop forever
                _current_music_track = "Oh Xmas.mp3"
        except Exception as e:
            print(f"Could not load title music: {e}")

    title_screen = TitleScreen()
    level_select = None
    controls_screen = None
    profile_screen = None
    current_screen = "TITLE"

    running = True
    while running:
        clock.tick(S.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle input based on current screen
            if current_screen == "TITLE":
                result = title_screen.handle_input(event)

                if result == "STORY MODE":
                    return "START"  # Start level 1
                elif result == "LEVEL SELECTION":
                    current_screen = "LEVEL_SELECT"
                    level_select = LevelSelectScreen(max_level=progression.max_level_reached)  # Use actual progression
                elif result == "SCOREBOARD":
                    current_screen = "SCOREBOARD"
                elif result == "GUIDE":
                    current_screen = "GUIDE"
                    guide_screen = GuideScreen()
                elif result == "SETTINGS":
                    current_screen = "SETTINGS"
                    # Create profile screen with username, difficulty, and checkpoints from progression
                    profile_screen = PlayerProfileScreen(screen, progression.username, progression.difficulty, progression.checkpoints_enabled)

            elif current_screen == "SETTINGS":
                result = profile_screen.handle_event(event)
                if result == "BACK":
                    # Save difficulty and checkpoints changes back to progression (username is read-only)
                    progression.difficulty = profile_screen.difficulty
                    progression.checkpoints_enabled = profile_screen.checkpoints_enabled
                    current_screen = "TITLE"

            elif current_screen == "LEVEL_SELECT":
                result = level_select.handle_input(event)

                if result and result.startswith("LEVEL_"):
                    level_num = int(result.split("_")[1])
                    return f"LEVEL_{level_num}"
                elif result == "BACK":
                    current_screen = "TITLE"

            elif current_screen == "SCOREBOARD":
                # Show scoreboard (it handles its own event loop)
                show_scoreboard(display_screen)
                current_screen = "TITLE"  # Return to title screen after

            elif current_screen == "GUIDE":
                result = guide_screen.handle_input(event)

                if result == "BACK":
                    current_screen = "TITLE"

        # Update and draw current screen
        if current_screen == "TITLE":
            title_screen.update()
            title_screen.draw(screen)
        elif current_screen == "LEVEL_SELECT":
            level_select.draw(screen)
        elif current_screen == "GUIDE":
            guide_screen.draw(screen)
        elif current_screen == "SETTINGS":
            profile_screen.update()
            profile_screen.draw()

        # Scale render surface to display screen
        scaled_surface = pygame.transform.scale(screen, (display_width, display_height))
        display_screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()

    return None  # Window was closed


def show_educational_screens(next_level_num, disable_audio=False):
    """Show educational screens for new abilities and enemies"""
    if not pygame.get_init():
        pygame.init()

    # Create scaled display window
    display_width = int(S.WINDOW_WIDTH * S.DISPLAY_SCALE)
    display_height = int(S.WINDOW_HEIGHT * S.DISPLAY_SCALE)
    display_screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption(S.TITLE)

    # Create internal render surface (800x600) - this is what we draw to
    screen = pygame.Surface((S.WINDOW_WIDTH, S.WINDOW_HEIGHT))

    clock = pygame.time.Clock()

    # Continue playing dialogue music (should already be playing from show_level_transition)
    # We don't need to load anything here - just let it continue
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

    # Define what to show for each level
    screens_to_show = []

    if next_level_num == 1:
        # Show basic abilities tutorial and level 1 enemies
        screens_to_show = ["basic_abilities", "level_1_enemies"]
    elif next_level_num == 2:
        # Show roll ability tutorial and level 2 enemies
        screens_to_show = ["roll_ability", "level_2_enemies"]
    elif next_level_num == 3:
        # Show spin attack ability tutorial and level 3 enemies
        screens_to_show = ["spin_attack_ability", "level_3_enemies"]
    elif next_level_num == 4:
        # Show level 4 intro and enemies (Northern Lights)
        screens_to_show = ["level_4_intro", "level_4_enemies"]

    # Show each screen in sequence
    for screen_type in screens_to_show:
        running = True
        while running:
            clock.tick(S.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False  # Move to next screen

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Click anywhere to continue
                    running = False

            # Draw the appropriate screen
            if screen_type == "basic_abilities":
                draw_basic_abilities_screen(screen)
            elif screen_type == "level_1_enemies":
                draw_new_enemies_screen(screen, 1)
            elif screen_type == "roll_ability":
                draw_new_ability_screen(screen, "Roll")
            elif screen_type == "level_2_enemies":
                draw_new_enemies_screen(screen, 2)
            elif screen_type == "spin_attack_ability":
                draw_new_ability_screen(screen, "Spin Attack")
            elif screen_type == "level_3_enemies":
                draw_new_enemies_screen(screen, 3)
            elif screen_type == "level_4_intro":
                draw_level_4_intro_screen(screen)
            elif screen_type == "level_4_enemies":
                draw_new_enemies_screen(screen, 4)

            # Scale render surface to display screen
            scaled_surface = pygame.transform.scale(screen, (display_width, display_height))
            display_screen.blit(scaled_surface, (0, 0))
            pygame.display.flip()


def show_level_transition(next_level_num, disable_audio=False):
    """Display level transition screen with educational content"""
    if not pygame.get_init():
        pygame.init()

    # Create scaled display window
    display_width = int(S.WINDOW_WIDTH * S.DISPLAY_SCALE)
    display_height = int(S.WINDOW_HEIGHT * S.DISPLAY_SCALE)
    display_screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption(S.TITLE)

    # Create internal render surface (800x600) - this is what we draw to
    screen = pygame.Surface((S.WINDOW_WIDTH, S.WINDOW_HEIGHT))

    clock = pygame.time.Clock()

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

    # First show the standard level transition (skip for level 4 - has custom intro)
    if next_level_num != 4:
        running = True
        while running:
            clock.tick(S.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Click anywhere to continue
                    running = False

            draw_level_transition_screen(screen, next_level_num)

            # Scale render surface to display screen
            scaled_surface = pygame.transform.scale(screen, (display_width, display_height))
            display_screen.blit(scaled_surface, (0, 0))
            pygame.display.flip()

    # Then show educational screens if applicable
    show_educational_screens(next_level_num, disable_audio)

    # Don't stop the music here - let it continue until gameplay starts
    # The gameplay music will switch it in main.py

    return "CONTINUE"
