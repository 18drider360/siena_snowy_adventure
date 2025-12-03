"""
Game Screens Module
Handles title screen, level transitions, and educational screens
"""

import sys
import pygame
from utils import settings as S
from title_screen import TitleScreen, LevelSelectScreen, ControlsScreen
from ui.scoreboard import show_scoreboard
from ui.username_input import PlayerProfileScreen
from rendering import (
    draw_level_transition_screen, draw_new_ability_screen,
    draw_level_4_intro_screen, draw_basic_abilities_screen,
    draw_new_enemies_screen
)


def scale_mouse_pos(mouse_pos):
    """Convert mouse position from display coordinates to internal render coordinates"""
    return (int(mouse_pos[0] / S.DISPLAY_SCALE), int(mouse_pos[1] / S.DISPLAY_SCALE))


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
            # Only start music if nothing is playing
            if not pygame.mixer.music.get_busy():
                # Title screen uses Oh Xmas.mp3
                pygame.mixer.music.load("assets/music/Oh Xmas.mp3")
                pygame.mixer.music.set_volume(0.6)
                pygame.mixer.music.play(-1)  # Loop forever
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

                if result == "START GAME":
                    return "START"  # Start level 1
                elif result == "LEVEL SELECTION":
                    current_screen = "LEVEL_SELECT"
                    level_select = LevelSelectScreen(max_level=progression.max_level_reached)  # Use actual progression
                elif result == "SCOREBOARD":
                    current_screen = "SCOREBOARD"
                elif result == "CONTROLS":
                    current_screen = "CONTROLS"
                    controls_screen = ControlsScreen()
                elif result == "SETTINGS":
                    current_screen = "SETTINGS"
                    # Create profile screen with username and difficulty from progression
                    profile_screen = PlayerProfileScreen(screen, progression.username, progression.difficulty)

            elif current_screen == "SETTINGS":
                result = profile_screen.handle_event(event)
                if result == "BACK":
                    # Save difficulty change back to progression (username is read-only)
                    progression.difficulty = profile_screen.difficulty
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

            elif current_screen == "CONTROLS":
                result = controls_screen.handle_input(event)

                if result == "BACK":
                    current_screen = "TITLE"

        # Update and draw current screen
        if current_screen == "TITLE":
            title_screen.update()
            title_screen.draw(screen)
        elif current_screen == "LEVEL_SELECT":
            level_select.draw(screen)
        elif current_screen == "CONTROLS":
            controls_screen.draw(screen)
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

    # Start tutorial music (same as main menu) if not already playing
    if not disable_audio:
        try:
            # Only start music if nothing is playing
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load("assets/music/Oh Xmas.mp3")
                pygame.mixer.music.set_volume(0.6)
                pygame.mixer.music.play(-1)  # Loop forever
        except Exception as e:
            print(f"Could not load tutorial music: {e}")

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

    # Play transition music only if not already playing (disabled for development)
    # try:
    #     # Check if music is already playing
    #     if not pygame.mixer.music.get_busy():
    #         pygame.mixer.music.load("assets/music/Oh Xmas.mp3")
    #         pygame.mixer.music.set_volume(0.5)
    #         pygame.mixer.music.play(-1)  # Loop indefinitely
    # except Exception as e:
    #     print(f"Could not load transition music: {e}")

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

    # Stop transition music when done
    if not disable_audio:
        try:
            pygame.mixer.music.stop()
        except:
            pass

    return "CONTINUE"
