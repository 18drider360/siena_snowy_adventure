"""
Rendering Module
Contains all drawing functions for the game including screens, platforms, hazards, HUD, etc.
"""

import pygame
from utils import settings as S


def draw_level_complete_screen(screen, level_num, coins, time, username="Player", selected_button="continue"):
    """Draw the level completion cutscene with winter theme

    Args:
        selected_button: "continue" or "menu" - which button is selected

    Returns:
        tuple: (continue_rect, menu_rect) - button rectangles for click detection
    """
    import math

    # Load font
    try:
        font_title = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 28)
        font_large = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 20)
        font_medium = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 16)
        font_small = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 14)
    except:
        font_title = pygame.font.Font(None, 56)
        font_large = pygame.font.Font(None, 40)
        font_medium = pygame.font.Font(None, 32)
        font_small = pygame.font.Font(None, 28)

    # Calculate time in seconds
    time_seconds = time // 60

    # Winter colors
    frost_blue = (200, 220, 255)
    ice_white = (240, 250, 255)
    snow_shadow = (180, 200, 230)
    gold = (255, 215, 0)
    text_dark = (40, 60, 90)

    # Draw frosted dialogue box with winter theme
    box_width = 650
    box_height = 380
    dialogue_box = pygame.Rect((S.WINDOW_WIDTH - box_width) // 2, 150, box_width, box_height)

    # Draw soft glow behind box
    glow_surface = pygame.Surface((dialogue_box.width + 40, dialogue_box.height + 40), pygame.SRCALPHA)
    glow_color = (100, 180, 255, 60)
    for i in range(20, 0, -2):
        alpha = int(60 * (i / 20))
        color = (100, 180, 255, alpha)
        glow_rect = pygame.Rect(20 - i, 20 - i, dialogue_box.width + i * 2, dialogue_box.height + i * 2)
        pygame.draw.rect(glow_surface, color, glow_rect, border_radius=15)
    screen.blit(glow_surface, (dialogue_box.x - 20, dialogue_box.y - 20))

    # Create frosted glass effect
    frost_surface = pygame.Surface((dialogue_box.width, dialogue_box.height), pygame.SRCALPHA)
    frost_surface.fill((230, 240, 255, 220))
    screen.blit(frost_surface, dialogue_box.topleft)

    # Draw decorative ice border
    border_width = 6
    pygame.draw.rect(screen, ice_white, dialogue_box, border_width, border_radius=12)
    pygame.draw.rect(screen, frost_blue, dialogue_box, 3, border_radius=12)

    # Draw animated snowflakes around the box
    current_time = pygame.time.get_ticks() / 1000.0
    for i in range(12):
        angle = (current_time * 0.5 + i * (360 / 12)) % 360
        rad = math.radians(angle)
        radius = 220
        x = dialogue_box.centerx + int(math.cos(rad) * radius)
        y = dialogue_box.centery + int(math.sin(rad) * radius)

        # Draw small snowflake
        size = 12
        snowflake_color = (200, 220, 255, 180)
        # Create snowflake on surface with alpha
        snowflake_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.line(snowflake_surf, snowflake_color, (size, 0), (size, size * 2), 2)
        pygame.draw.line(snowflake_surf, snowflake_color, (0, size), (size * 2, size), 2)
        pygame.draw.line(snowflake_surf, snowflake_color, (3, 3), (size * 2 - 3, size * 2 - 3), 2)
        pygame.draw.line(snowflake_surf, snowflake_color, (size * 2 - 3, 3), (3, size * 2 - 3), 2)
        screen.blit(snowflake_surf, (x - size, y - size))

    # Draw Pedro the Penguin above the dialogue box
    penguin_x = dialogue_box.centerx - 20
    penguin_y = dialogue_box.y - 60  # Moved down 30 pixels total
    scale = 0.4  # Even smaller penguin

    body_width = int(60 * scale)
    body_height = int(80 * scale)
    head_radius = int(25 * scale)

    # Body (black oval)
    pygame.draw.ellipse(screen, (40, 40, 40),
                      (penguin_x, penguin_y, body_width, body_height))

    # Belly (white)
    pygame.draw.ellipse(screen, (255, 255, 255),
                      (penguin_x + int(10 * scale), penguin_y + int(15 * scale),
                       int(40 * scale), int(50 * scale)))

    # Head (black circle)
    pygame.draw.circle(screen, (40, 40, 40),
                     (penguin_x + body_width // 2, penguin_y - int(10 * scale)),
                     head_radius)

    # Eyes (white)
    pygame.draw.circle(screen, (255, 255, 255),
                     (penguin_x + int(22 * scale), penguin_y - int(12 * scale)),
                     int(6 * scale))
    pygame.draw.circle(screen, (255, 255, 255),
                     (penguin_x + int(38 * scale), penguin_y - int(12 * scale)),
                     int(6 * scale))

    # Pupils (black)
    pygame.draw.circle(screen, (0, 0, 0),
                     (penguin_x + int(24 * scale), penguin_y - int(10 * scale)),
                     int(3 * scale))
    pygame.draw.circle(screen, (0, 0, 0),
                     (penguin_x + int(40 * scale), penguin_y - int(10 * scale)),
                     int(3 * scale))

    # Beak (orange)
    beak_points = [
        (penguin_x + int(30 * scale), penguin_y - int(5 * scale)),
        (penguin_x + int(35 * scale), penguin_y),
        (penguin_x + int(30 * scale), penguin_y + int(2 * scale))
    ]
    pygame.draw.polygon(screen, (255, 140, 0), beak_points)

    # Feet (orange)
    pygame.draw.ellipse(screen, (255, 140, 0),
                      (penguin_x + int(8 * scale), penguin_y + int(75 * scale),
                       int(20 * scale), int(10 * scale)))
    pygame.draw.ellipse(screen, (255, 140, 0),
                      (penguin_x + int(32 * scale), penguin_y + int(75 * scale),
                       int(20 * scale), int(10 * scale)))

    # NPC Name tag with icy theme (below penguin)
    name_tag_width = 180
    name_tag_height = 40
    name_tag = pygame.Rect(dialogue_box.centerx - name_tag_width // 2, dialogue_box.y - 25, name_tag_width, name_tag_height)

    # Name tag background with gradient effect
    name_bg = pygame.Surface((name_tag.width, name_tag.height), pygame.SRCALPHA)
    name_bg.fill((100, 180, 255, 240))
    screen.blit(name_bg, name_tag.topleft)
    pygame.draw.rect(screen, ice_white, name_tag, 4, border_radius=8)
    pygame.draw.rect(screen, gold, name_tag, 2, border_radius=8)

    name_text = font_medium.render("PEDRO", True, ice_white)
    name_rect = name_text.get_rect(center=(name_tag.centerx, name_tag.centery))
    # Draw text shadow
    shadow_text = font_medium.render("PEDRO", True, (50, 80, 120))
    screen.blit(shadow_text, (name_rect.x + 2, name_rect.y + 2))
    screen.blit(name_text, name_rect)

    # Content area
    content_y = dialogue_box.y + 50

    # Title with shadow effect
    title_text = font_title.render("LEVEL COMPLETE!", True, gold)
    title_shadow = font_title.render("LEVEL COMPLETE!", True, (180, 150, 0))
    title_rect = title_text.get_rect(center=(dialogue_box.centerx, content_y))
    screen.blit(title_shadow, (title_rect.x + 3, title_rect.y + 3))
    screen.blit(title_text, title_rect)

    content_y += 60

    # Congratulations message
    congrats = font_large.render(f"Great job, {username}!", True, text_dark)
    congrats_rect = congrats.get_rect(center=(dialogue_box.centerx, content_y))
    screen.blit(congrats, congrats_rect)

    content_y += 50

    # Stats box with frosted background
    stats_box = pygame.Rect(dialogue_box.x + 80, content_y, dialogue_box.width - 160, 140)
    stats_bg = pygame.Surface((stats_box.width, stats_box.height), pygame.SRCALPHA)
    stats_bg.fill((255, 255, 255, 160))
    screen.blit(stats_bg, stats_box.topleft)
    pygame.draw.rect(screen, frost_blue, stats_box, 3, border_radius=8)

    stats_y = stats_box.y + 20

    # Level info
    level_text = font_medium.render(f"Level {level_num} Complete", True, text_dark)
    level_rect = level_text.get_rect(center=(stats_box.centerx, stats_y))
    screen.blit(level_text, level_rect)
    stats_y += 40

    # Coins with icon color
    coins_text = font_medium.render(f"Coins: {coins}", True, (220, 160, 0))
    coins_rect = coins_text.get_rect(center=(stats_box.centerx, stats_y))
    screen.blit(coins_text, coins_rect)
    stats_y += 35

    # Time
    time_text = font_medium.render(f"Time: {time_seconds}s", True, (80, 140, 200))
    time_rect = time_text.get_rect(center=(stats_box.centerx, stats_y))
    screen.blit(time_text, time_rect)

    # Draw action buttons at bottom
    button_y = dialogue_box.bottom - 55
    button_width = 250
    button_height = 40
    button_spacing = 30

    # Continue button (left)
    continue_rect = pygame.Rect(
        dialogue_box.centerx - button_width - button_spacing // 2,
        button_y,
        button_width,
        button_height
    )

    # Main Menu button (right)
    menu_rect = pygame.Rect(
        dialogue_box.centerx + button_spacing // 2,
        button_y,
        button_width,
        button_height
    )

    # Helper function to draw button
    def draw_button(rect, text, is_selected):
        # Glow if selected
        if is_selected:
            glow_rect = rect.inflate(8, 8)
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            glow_surface.fill((255, 200, 0, 80))
            screen.blit(glow_surface, glow_rect.topleft)

        # Button background
        button_color = (100, 180, 255) if is_selected else (80, 120, 180)
        pygame.draw.rect(screen, button_color, rect, border_radius=8)

        # Button border
        border_color = (150, 200, 255) if is_selected else (100, 150, 200)
        pygame.draw.rect(screen, border_color, rect, 3, border_radius=8)

        # Button text
        text_color = (255, 255, 255)
        button_text = font_small.render(text, True, text_color)
        text_rect = button_text.get_rect(center=rect.center)
        screen.blit(button_text, text_rect)

    draw_button(continue_rect, "CONTINUE", selected_button == "continue")
    draw_button(menu_rect, "MAIN MENU", selected_button == "menu")

    return (continue_rect, menu_rect)


def draw_level_transition_screen(screen, next_level_num):
    """Draw transition screen between levels"""
    # Load font
    try:
        font_large = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 32)
        font_small = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 16)
    except:
        font_large = pygame.font.Font(None, 56)
        font_small = pygame.font.Font(None, 32)
    
    # Black background
    screen.fill((0, 0, 0))
    
    # Main text
    text1 = font_large.render(f"LEVEL {next_level_num}", True, (255, 255, 255))
    text1_rect = text1.get_rect(center=(S.WINDOW_WIDTH // 2, S.WINDOW_HEIGHT // 2 - 50))
    screen.blit(text1, text1_rect)
    
    # Level name
    level_names = {
        1: "WINTER WELCOME",
        2: "SNOW CABIN",
        3: "MOUNTAIN CLIMB",
        4: "NORTHERN LIGHTS"
    }
    level_name = level_names.get(next_level_num, f"LEVEL {next_level_num}")
    
    text2 = font_small.render(level_name, True, (200, 200, 200))
    text2_rect = text2.get_rect(center=(S.WINDOW_WIDTH // 2, S.WINDOW_HEIGHT // 2 + 20))
    screen.blit(text2, text2_rect)
    
    # Press Enter prompt
    text3 = font_small.render("Press ENTER to continue", True, (150, 150, 150))
    text3_rect = text3.get_rect(center=(S.WINDOW_WIDTH // 2, S.WINDOW_HEIGHT // 2 + 80))
    screen.blit(text3, text3_rect)


def draw_new_ability_screen(screen, ability_name="Roll"):
    """Draw screen showing new ability unlocked with animated sprite"""
    # Load font
    try:
        font_large = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 28)
        font_medium = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 18)
        font_small = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 14)
    except:
        font_large = pygame.font.Font(None, 48)
        font_medium = pygame.font.Font(None, 32)
        font_small = pygame.font.Font(None, 24)

    # Black background
    screen.fill((0, 0, 0))

    # Title
    title_text = font_large.render("NEW ABILITY UNLOCKED!", True, (255, 215, 0))  # Gold
    title_rect = title_text.get_rect(center=(S.WINDOW_WIDTH // 2, 80))
    screen.blit(title_text, title_rect)

    # Ability name
    ability_text = font_large.render(ability_name.upper(), True, (255, 255, 255))
    ability_rect = ability_text.get_rect(center=(S.WINDOW_WIDTH // 2, 150))
    screen.blit(ability_text, ability_rect)

    # Load and display ability animation sprite (animated loop)
    try:
        if ability_name == "Roll":
            sprite_sheet = pygame.image.load("assets/images/siena/Roll.png").convert_alpha()
            frame_count = 4
        elif ability_name == "Spin Attack":
            sprite_sheet = pygame.image.load("assets/images/siena/Spin Attack.png").convert_alpha()
            frame_count = 7
        else:
            sprite_sheet = None
            frame_count = 0

        if sprite_sheet:
            sheet_width = sprite_sheet.get_width()
            frame_width = sheet_width // frame_count
            frame_height = sprite_sheet.get_height()

            # Use pygame.time to create animation
            current_time = pygame.time.get_ticks()
            frame_index = (current_time // 80) % frame_count  # Change frame every 80ms

            frame_x = int(frame_index * frame_width)
            frame = sprite_sheet.subsurface((frame_x, 0, frame_width, frame_height))

            # Scale up significantly for visibility
            scale_factor = 5
            scaled_frame = pygame.transform.scale(frame,
                                                  (int(frame_width * scale_factor), int(frame_height * scale_factor)))

            # Center the sprite
            sprite_rect = scaled_frame.get_rect(center=(S.WINDOW_WIDTH // 2, S.WINDOW_HEIGHT // 2))
            screen.blit(scaled_frame, sprite_rect)
    except Exception as e:
        print(f"Could not load {ability_name} animation: {e}")

    # Controls text
    y_offset = S.WINDOW_HEIGHT // 2 + 120
    controls_text = font_medium.render("HOW TO USE:", True, (200, 200, 200))
    controls_rect = controls_text.get_rect(center=(S.WINDOW_WIDTH // 2, y_offset))
    screen.blit(controls_text, controls_rect)

    y_offset += 50
    if ability_name == "Roll":
        instruction1 = font_small.render("Hold DOWN + LEFT/RIGHT", True, (150, 150, 150))
        instruction1_rect = instruction1.get_rect(center=(S.WINDOW_WIDTH // 2, y_offset))
        screen.blit(instruction1, instruction1_rect)

        y_offset += 35
        instruction2 = font_small.render("to perform a roll attack!", True, (150, 150, 150))
        instruction2_rect = instruction2.get_rect(center=(S.WINDOW_WIDTH // 2, y_offset))
        screen.blit(instruction2, instruction2_rect)
    elif ability_name == "Spin Attack":
        instruction1 = font_small.render("Press E while in air", True, (150, 150, 150))
        instruction1_rect = instruction1.get_rect(center=(S.WINDOW_WIDTH // 2, y_offset))
        screen.blit(instruction1, instruction1_rect)

        y_offset += 35
        instruction2 = font_small.render("to perform a spin attack!", True, (150, 150, 150))
        instruction2_rect = instruction2.get_rect(center=(S.WINDOW_WIDTH // 2, y_offset))
        screen.blit(instruction2, instruction2_rect)

    # Press Enter prompt
    prompt_text = font_small.render("Press ENTER to continue", True, (100, 100, 100))
    prompt_rect = prompt_text.get_rect(center=(S.WINDOW_WIDTH // 2, S.WINDOW_HEIGHT - 50))
    screen.blit(prompt_text, prompt_rect)


def draw_level_4_intro_screen(screen):
    """Draw intro screen for Level 4 - Northern Lights"""
    # Load font
    try:
        font_large = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 32)
        font_medium = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 20)
        font_small = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 14)
    except:
        font_large = pygame.font.Font(None, 56)
        font_medium = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 24)

    # Black background
    screen.fill((0, 0, 0))

    # Main text - LEVEL 4
    text1 = font_large.render("LEVEL 4", True, (255, 255, 255))
    text1_rect = text1.get_rect(center=(S.WINDOW_WIDTH // 2, S.WINDOW_HEIGHT // 2 - 60))
    screen.blit(text1, text1_rect)

    # Level name - NORTHERN LIGHTS
    text2 = font_medium.render("NORTHERN LIGHTS", True, (100, 255, 200))  # Aurora colors
    text2_rect = text2.get_rect(center=(S.WINDOW_WIDTH // 2, S.WINDOW_HEIGHT // 2 + 10))
    screen.blit(text2, text2_rect)

    # Press Enter prompt
    text3 = font_small.render("Press ENTER to continue", True, (150, 150, 150))
    text3_rect = text3.get_rect(center=(S.WINDOW_WIDTH // 2, S.WINDOW_HEIGHT // 2 + 90))
    screen.blit(text3, text3_rect)


def draw_basic_abilities_screen(screen):
    """Draw screen showing all basic abilities for Level 1"""
    # Load font
    try:
        font_large = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 24)
        font_small = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 10)
        font_tiny = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 8)
    except:
        font_large = pygame.font.Font(None, 40)
        font_small = pygame.font.Font(None, 18)
        font_tiny = pygame.font.Font(None, 14)

    # Black background
    screen.fill((0, 0, 0))

    # Title
    title_text = font_large.render("YOUR ABILITIES", True, (100, 200, 255))  # Light blue
    title_rect = title_text.get_rect(center=(S.WINDOW_WIDTH // 2, 50))
    screen.blit(title_text, title_rect)

    # Define abilities in 2x2 grid
    abilities = [
        {
            "name": "Jump",
            "sprite_path": "assets/images/siena/Jump.png",
            "frames": 2,
            "instruction": "Press SPACE or UP",
            "grid_pos": (0, 0)  # top-left
        },
        {
            "name": "Double Jump",
            "sprite_path": "assets/images/siena/Flap.png",
            "frames": 2,
            "instruction": "Press SPACE or UP (in air)",
            "grid_pos": (1, 0)  # top-right
        },
        {
            "name": "Crouch",
            "sprite_path": "assets/images/siena/Crouch.png",
            "frames": 1,
            "instruction": "Hold DOWN",
            "grid_pos": (0, 1)  # bottom-left
        },
        {
            "name": "Stomp",
            "sprite_path": "assets/images/2 Elkman/Elkman_idle.png",
            "frames": 4,
            "instruction": "Land on enemy",
            "grid_pos": (1, 1),  # bottom-right
            "is_stomp": True  # Special flag for stomp display
        }
    ]

    # Grid layout
    grid_cols = 2
    grid_rows = 2
    cell_width = S.WINDOW_WIDTH // grid_cols
    cell_height = (S.WINDOW_HEIGHT - 150) // grid_rows
    start_y = 120

    current_time = pygame.time.get_ticks()

    for ability in abilities:
        col, row = ability["grid_pos"]
        center_x = (col * cell_width) + (cell_width // 2)
        center_y = start_y + (row * cell_height) + (cell_height // 2)

        # Load and animate sprite
        try:
            if ability.get("is_stomp"):
                # For stomp, show player landing on enemy
                # Load player falling sprite (use jump frame)
                player_sheet = pygame.image.load("assets/images/siena/Jump.png").convert_alpha()
                player_frames = 2
                player_width = player_sheet.get_width() // player_frames
                player_height = player_sheet.get_height()
                # Use second frame (falling) - extract properly
                player_frame_surface = pygame.Surface((player_width, player_height), pygame.SRCALPHA)
                player_frame_surface.blit(player_sheet, (0, 0), (player_width, 0, player_width, player_height))
                scaled_player = pygame.transform.scale(player_frame_surface, (int(player_width * 2), int(player_height * 2)))

                # Load enemy sprite
                enemy_sheet = pygame.image.load(ability["sprite_path"]).convert_alpha()
                enemy_frame_count = ability["frames"]
                enemy_width = enemy_sheet.get_width() // enemy_frame_count
                enemy_height = enemy_sheet.get_height()
                frame_index = (current_time // 150) % enemy_frame_count
                frame_x = int(frame_index * enemy_width)
                # Extract single frame properly
                enemy_frame_surface = pygame.Surface((enemy_width, enemy_height), pygame.SRCALPHA)
                enemy_frame_surface.blit(enemy_sheet, (0, 0), (frame_x, 0, enemy_width, enemy_height))
                # Make Elkman smaller - scale factor 1.5 instead of 2
                scaled_enemy = pygame.transform.scale(enemy_frame_surface, (int(enemy_width * 1.5), int(enemy_height * 1.5)))

                # Position player's feet on enemy's head - better alignment
                # Move Elkman left and down, move Siena much further down
                enemy_rect = scaled_enemy.get_rect(center=(center_x - 15, center_y + 10))
                player_rect = scaled_player.get_rect(midbottom=(center_x, enemy_rect.top + 90))

                screen.blit(scaled_enemy, enemy_rect)
                screen.blit(scaled_player, player_rect)

            else:
                # Normal ability animation
                sprite_sheet = pygame.image.load(ability["sprite_path"]).convert_alpha()
                frame_count = ability["frames"]
                sheet_width = sprite_sheet.get_width()
                frame_width = sheet_width // frame_count
                frame_height = sprite_sheet.get_height()

                if frame_count > 1:
                    frame_index = (current_time // 150) % frame_count
                else:
                    frame_index = 0

                # Extract single frame from sprite sheet
                frame_x = int(frame_index * frame_width)
                # Create a new surface for just this frame to avoid subsurface issues
                frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                frame.blit(sprite_sheet, (0, 0), (frame_x, 0, frame_width, frame_height))

                scale_factor = 3
                scaled_frame = pygame.transform.scale(frame,
                                                     (int(frame_width * scale_factor), int(frame_height * scale_factor)))

                sprite_rect = scaled_frame.get_rect(center=(center_x, center_y))
                screen.blit(scaled_frame, sprite_rect)

        except Exception as e:
            print(f"Could not load ability sprite {ability['name']}: {e}")

        # Ability name
        name_text = font_small.render(ability["name"], True, (255, 255, 255))
        name_rect = name_text.get_rect(center=(center_x, center_y - 80))
        screen.blit(name_text, name_rect)

        # Instruction
        instruction_text = font_tiny.render(ability["instruction"], True, (180, 180, 180))
        instruction_rect = instruction_text.get_rect(center=(center_x, center_y + 80))
        screen.blit(instruction_text, instruction_rect)

    # Press Enter prompt
    prompt_text = font_small.render("Press ENTER to continue", True, (100, 100, 100))
    prompt_rect = prompt_text.get_rect(center=(S.WINDOW_WIDTH // 2, S.WINDOW_HEIGHT - 40))
    screen.blit(prompt_text, prompt_rect)


def draw_new_enemies_screen(screen, level_num=2):
    """Draw screen showing new enemies for the upcoming level"""
    # Load font
    try:
        font_large = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 28)
        font_medium = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 16)
        font_small = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 12)
    except:
        font_large = pygame.font.Font(None, 48)
        font_medium = pygame.font.Font(None, 28)
        font_small = pygame.font.Font(None, 20)

    # Black background
    screen.fill((0, 0, 0))

    # Title - simple "ENEMIES AHEAD!" for all levels
    title_text = font_large.render("ENEMIES AHEAD!", True, (255, 50, 50))  # Red
    title_rect = title_text.get_rect(center=(S.WINDOW_WIDTH // 2, 60))
    screen.blit(title_text, title_rect)

    # Define enemy info per level
    if level_num == 1:
        enemies = [
            {
                "name": "Elkman",
                "sprite_path": "assets/images/2 Elkman/Elkman_idle.png",
                "frame_count": 4,
                "health": 1,
                "type": "Projectile",
                "vulnerable_to": ["Stomp", "Spin Attack"]
            },
            {
                "name": "Spiked Slime",
                "sprite_path": "assets/images/4 Spiked_slime/Spiked_slime_idle.png",
                "frame_count": 4,
                "health": 1,
                "type": "Projectile",
                "vulnerable_to": ["Stomp", "Roll"]
            }
        ]
    elif level_num == 2:
        enemies = [
            {
                "name": "Frost Golem",
                "sprite_path": "assets/images/3 Frost_golem/Frost_golem_idle.png",
                "frame_count": 4,
                "health": 1,
                "type": "Projectile",
                "vulnerable_to": ["Roll", "Stomp"]
            },
            {
                "name": "Swordsman",
                "sprite_path": "assets/images/5 Swordsman/Swordsman_idle.png",
                "frame_count": 4,
                "health": 2,
                "type": "Melee",
                "vulnerable_to": ["Roll", "Stomp"]
            }
        ]
    elif level_num == 3:
        enemies = [
            {
                "name": "Snowy",
                "sprite_path": "assets/images/1 Snowy/Snowy_idle.png",
                "frame_count": 4,
                "health": 3,
                "type": "Ranged",
                "vulnerable_to": ["Spin Attack", "Stomp"]
            },
            {
                "name": "Northerner",
                "sprite_path": "assets/images/6 Northerner/Northerner_idle.png",
                "frame_count": 4,
                "health": 2,
                "type": "Melee",
                "vulnerable_to": ["Spin Attack", "Stomp"]
            }
        ]
    elif level_num == 4:
        enemies = [
            {
                "name": "Elkman",
                "sprite_path": "assets/images/2 Elkman/Elkman_idle.png",
                "frame_count": 4,
                "health": 1,
                "type": "Basic",
                "vulnerable_to": ["Spin Attack", "Stomp"]
            },
            {
                "name": "Snowy",
                "sprite_path": "assets/images/1 Snowy/Snowy_idle.png",
                "frame_count": 4,
                "health": 3,
                "type": "Chaser",
                "vulnerable_to": ["Spin Attack", "Stomp"]
            },
            {
                "name": "Northerner",
                "sprite_path": "assets/images/6 Northerner/Northerner_idle.png",
                "frame_count": 4,
                "health": 2,
                "type": "Ranged",
                "vulnerable_to": ["Spin Attack", "Stomp"]
            },
            {
                "name": "Swordsman",
                "sprite_path": "assets/images/5 Swordsman/Swordsman_idle.png",
                "frame_count": 4,
                "health": 2,
                "type": "Melee",
                "vulnerable_to": ["Roll", "Stomp"]
            },
            {
                "name": "Frost Golem",
                "sprite_path": "assets/images/3 Frost_golem/Frost_golem_idle.png",
                "frame_count": 4,
                "health": 3,
                "type": "Ranged",
                "vulnerable_to": ["Roll", "Stomp"]
            },
            {
                "name": "Spiked Slime",
                "sprite_path": "assets/images/4 Spiked_slime/Spiked_slime_idle.png",
                "frame_count": 4,
                "health": 1,
                "type": "Hazard",
                "vulnerable_to": ["Stomp", "Roll"]
            }
        ]
    else:
        # No enemies defined for this level
        enemies = []

    # Display enemies side by side - adjust spacing based on enemy count
    num_enemies = len(enemies)

    if num_enemies >= 6:
        # Level 4: 6 enemies in 2 rows of 3 - centered layout
        enemy_spacing = 280  # Fixed spacing between columns
        total_width = enemy_spacing * 2  # Width for 3 columns
        start_x = (S.WINDOW_WIDTH - total_width) // 2  # Center horizontally
        y_start = 0  # Centered vertically (moved up 100px from original 100)
    elif num_enemies >= 3:
        # 3+ enemies - medium spacing
        enemy_spacing = S.WINDOW_WIDTH // 4
        start_x = enemy_spacing
        y_start = 140
    else:
        # 2 enemies or less - wide spacing
        enemy_spacing = S.WINDOW_WIDTH // 3
        start_x = enemy_spacing - 40
        y_start = 140

    for i, enemy_data in enumerate(enemies):
        if num_enemies >= 6:
            # Arrange 6 enemies in 2 rows of 3
            row = i // 3  # 0 for first row, 1 for second row
            col = i % 3   # 0, 1, 2 for columns
            x_pos = start_x + (col * enemy_spacing)
            # Move top row down 15px, keep bottom row at original position
            if row == 0:
                y_pos = 15  # Top row moved down 15px
            else:
                y_pos = 250  # Bottom row stays at original spacing (0 + 250)
        else:
            x_pos = start_x + (i * enemy_spacing * 1.5)
            y_pos = y_start  # Use y_start for non-6-enemy layouts

            # Special adjustment for Elkman in 2-enemy layouts
            if enemy_data["name"] == "Elkman" and num_enemies <= 2:
                x_pos -= 50

        # Load and display enemy sprite with animation
        try:
            enemy_sheet = pygame.image.load(enemy_data["sprite_path"]).convert_alpha()
            frame_count = enemy_data["frame_count"]
            sheet_width = enemy_sheet.get_width()
            frame_width = sheet_width // frame_count
            frame_height = enemy_sheet.get_height()

            # Animate the sprite - cycle through frames
            current_time = pygame.time.get_ticks()
            frame_index = (current_time // 150) % frame_count  # Change frame every 150ms

            frame_x = int(frame_index * frame_width)
            frame = enemy_sheet.subsurface((frame_x, 0, frame_width, frame_height))

            # Scale for visibility - can be bigger with 2-row layout
            scale_factor = 2.2 if num_enemies >= 6 else 2.5
            scaled_frame = pygame.transform.scale(frame,
                                                 (int(frame_width * scale_factor), int(frame_height * scale_factor)))

            # Position sprite - with extra left shift for specific enemies
            if enemy_data["name"] == "Elkman":
                sprite_x_pos = x_pos - 20
            elif enemy_data["name"] in ["Frost Golem", "Swordsman"]:
                sprite_x_pos = x_pos - 20
            elif enemy_data["name"] in ["Snowy", "Northerner"]:
                sprite_x_pos = x_pos - 20
            else:
                sprite_x_pos = x_pos
            sprite_rect = scaled_frame.get_rect(center=(sprite_x_pos, y_pos + 80))
            screen.blit(scaled_frame, sprite_rect)
        except Exception as e:
            print(f"Could not load enemy sprite: {e}")

        # Enemy name (uses original x_pos, not adjusted)
        # Use smaller font and tighter spacing for 6 enemies
        name_font = font_small if num_enemies >= 6 else font_medium
        name_text = name_font.render(enemy_data["name"], True, (255, 255, 255))
        name_y = y_pos + 150 if num_enemies >= 6 else y_pos + 200
        name_rect = name_text.get_rect(center=(x_pos, name_y))
        screen.blit(name_text, name_rect)

        # Health - more compact label for 6 enemies
        health_y = name_y + 25 if num_enemies >= 6 else y_pos + 230
        health_label = "HP:" if num_enemies >= 6 else "Health:"
        health_text = font_small.render(f"{health_label} {enemy_data['health']}", True, (255, 100, 100))
        health_rect = health_text.get_rect(center=(x_pos, health_y))
        screen.blit(health_text, health_rect)

        # Type
        type_y = health_y + 20 if num_enemies >= 6 else y_pos + 255
        type_label = enemy_data['type'] if num_enemies >= 6 else f"Type: {enemy_data['type']}"
        type_text = font_small.render(type_label, True, (200, 200, 200))
        type_rect = type_text.get_rect(center=(x_pos, type_y))
        screen.blit(type_text, type_rect)

        # Vulnerable to
        vuln_y = type_y + 25 if num_enemies >= 6 else y_pos + 285
        vuln_text = font_small.render("Weak to:", True, (100, 255, 100))
        vuln_rect = vuln_text.get_rect(center=(x_pos, vuln_y))
        screen.blit(vuln_text, vuln_rect)

        # List vulnerabilities - more compact spacing for 6 enemies
        vuln_spacing = 18 if num_enemies >= 6 else 25
        vuln_start = vuln_y + 20 if num_enemies >= 6 else y_pos + 310
        for j, vuln in enumerate(enemy_data["vulnerable_to"]):
            vuln_item = font_small.render(f"- {vuln}", True, (150, 255, 150))
            vuln_item_rect = vuln_item.get_rect(center=(x_pos, vuln_start + (j * vuln_spacing)))
            screen.blit(vuln_item, vuln_item_rect)

    # Press Enter prompt
    prompt_text = font_medium.render("Press ENTER to continue", True, (100, 100, 100))
    prompt_rect = prompt_text.get_rect(center=(S.WINDOW_WIDTH // 2, S.WINDOW_HEIGHT - 50))
    screen.blit(prompt_text, prompt_rect)


# main.py
import sys
import pygame
from utils import settings as S
from utils.progression import GameProgression, LevelManager
from utils.background import ParallaxBackground
from ui.health_display import HealthDisplay
from ui.enemy_health_display import EnemyHealthDisplay
from ui.spin_charge_display import SpinChargeDisplay
from ui.roll_stamina_display import RollStaminaDisplay
from title_screen import TitleScreen, LevelSelectScreen, ControlsScreen
from menus import PauseMenu, DeathMenu
from audio_manager import AudioManager

# GLOBAL AUDIO CONTROL - Set to True to completely disable ALL audio
# This is controlled by settings.MASTER_AUDIO_ENABLED
DISABLE_ALL_AUDIO = not S.MASTER_AUDIO_ENABLED

def draw_spiky_hazard(screen, rect, camera_x):
    """Draw an animated flame hazard using Fiyah.png sprite sheet"""
    import time

    draw_x = rect.x - camera_x
    draw_y = rect.y

    # Load fire sprite sheet (cache it to avoid reloading every frame)
    if not hasattr(draw_spiky_hazard, 'fire_sheet'):
        try:
            # Load image and convert to format with alpha channel
            fire_img = pygame.image.load("assets/images/objects/Fiyah.png").convert_alpha()

            # Manually replace all gray pixels with transparency
            width, height = fire_img.get_size()
            for x in range(width):
                for y in range(height):
                    r, g, b, a = fire_img.get_at((x, y))
                    # If pixel is gray (close to 165, 165, 165), make it transparent
                    if abs(r - 165) < 10 and abs(g - 165) < 10 and abs(b - 165) < 10:
                        fire_img.set_at((x, y), (r, g, b, 0))  # Set alpha to 0

            draw_spiky_hazard.fire_sheet = fire_img
        except Exception as e:
            print(f"Could not load fire sprite: {e}")
            draw_spiky_hazard.fire_sheet = None

    fire_sheet = draw_spiky_hazard.fire_sheet

    if fire_sheet:
        # Sprite sheet has 6 frames: 3 on top row, 3 on bottom row
        sheet_width = fire_sheet.get_width()
        sheet_height = fire_sheet.get_height()

        # Each frame is 1/3 of width and 1/2 of height
        frame_width = sheet_width // 3
        frame_height = sheet_height // 2

        # Animate through the 6 frames
        current_time = pygame.time.get_ticks()
        frame_duration = 100  # milliseconds per frame
        frame_index = (current_time // frame_duration) % 6

        # Calculate which row and column
        frame_row = frame_index // 3  # 0 for top row, 1 for bottom row
        frame_col = frame_index % 3   # 0, 1, or 2

        # Extract the current frame
        frame_x = frame_col * frame_width
        frame_y = frame_row * frame_height
        frame = fire_sheet.subsurface((frame_x, frame_y, frame_width, frame_height))

        # Scale frame to fit hazard height
        scale_factor = rect.height / frame_height
        scaled_width = int(frame_width * scale_factor)
        scaled_height = rect.height
        scaled_frame = pygame.transform.scale(frame, (scaled_width, scaled_height))

        # Tile fire sprites across the hazard width
        num_fires = (rect.width // scaled_width) + 1

        for i in range(num_fires):
            fire_x = draw_x + (i * scaled_width)

            # Don't draw beyond the hazard bounds
            if fire_x < draw_x + rect.width:
                screen.blit(scaled_frame, (fire_x, draw_y))
    else:
        # Fallback: draw a simple red rectangle if image fails to load
        pygame.draw.rect(screen, (255, 100, 0), (draw_x, draw_y, rect.width, rect.height))

    # ORIGINAL FIRE HAZARD CODE (commented out for easy restoration):
    # """Draw an animated fire hazard"""
    # # Get time for animation
    # current_time = time.time()
    #
    # # Base colors for fire
    # dark_red = (120, 0, 0)
    # red = (200, 30, 0)
    # orange = (255, 120, 0)
    # yellow = (255, 220, 50)
    #
    # # Draw dark base
    # pygame.draw.rect(screen, dark_red, draw_rect)
    #
    # # Draw animated fire layers from bottom to top
    # num_layers = 5
    # for layer in range(num_layers):
    #     layer_height = rect.height // num_layers
    #     layer_y = draw_y + rect.height - (layer * layer_height)
    #
    #     # Animate with different speeds per layer
    #     wave_offset = math.sin(current_time * (3 + layer)) * 8
    #
    #     # Color gets brighter toward top
    #     if layer == 0:
    #         color = red
    #     elif layer == 1:
    #         color = (220, 50, 0)
    #     elif layer == 2:
    #         color = orange
    #     elif layer == 3:
    #         color = (255, 180, 30)
    #     else:
    #         color = yellow
    #
    #     # Draw wavy fire layer
    #     for x in range(0, rect.width, 4):
    #         wave = math.sin((x / 10) + current_time * 5 + layer) * 6
    #         layer_rect = pygame.Rect(
    #             draw_x + x,
    #             layer_y + wave + wave_offset - layer_height,
    #             4,
    #             layer_height + 4
    #         )
    #         pygame.draw.rect(screen, color, layer_rect)
    #
    # # --- DRAW ANIMATED FLAMES ON TOP ---
    # flame_width = 12
    # flame_height = 20
    # num_flames = (rect.width // flame_width) + 1
    #
    # for i in range(num_flames):
    #     flame_x = draw_x + (i * flame_width)
    #
    #     if flame_x > draw_x + rect.width - flame_width:
    #         continue
    #
    #     # Animate each flame independently
    #     flame_offset = math.sin(current_time * 8 + i * 0.5) * 8
    #     flame_stretch = abs(math.sin(current_time * 6 + i)) * 10
    #
    #     # Draw flame as elongated ellipse
    #     tip_x = flame_x + flame_width // 2
    #     tip_y = int(draw_y - flame_height - flame_stretch + flame_offset)
    #     base_y = draw_y
    #
    #     # Yellow core (brightest)
    #     pygame.draw.ellipse(screen, yellow,
    #                       (tip_x - 3, tip_y, 6, int(flame_height * 0.5)))
    #
    #     # Orange middle
    #     pygame.draw.ellipse(screen, orange,
    #                       (tip_x - 5, tip_y + 5, 10, int(flame_height * 0.7)))
    #
    #     # Red outer
    #     pygame.draw.ellipse(screen, red,
    #                       (tip_x - 6, tip_y + 10, 12, flame_height))
    #
    #     # Add glow at tip
    #     glow_surface = pygame.Surface((24, 24), pygame.SRCALPHA)
    #     pygame.draw.circle(glow_surface, (255, 255, 100, 100), (12, 12), 12)
    #     screen.blit(glow_surface, (tip_x - 12, tip_y - 8))
    #
    # # Draw pulsing orange/yellow border around fire hazard
    # pulse = int(abs(((current_time * 5) % 2) - 1) * 100)  # Pulsing value 0-100
    # border_color = (255, 100 + pulse, 0)
    # pygame.draw.rect(screen, border_color, draw_rect, 3)


def draw_brick_platform(screen, rect, camera_x):
    """Draw a snowy/icy brick platform with individual blocks"""
    # Brick dimensions
    brick_width = 32
    brick_height = 16
    
    # Offset for camera
    draw_x = rect.x - camera_x
    draw_y = rect.y
    
    # Calculate how many bricks fit
    cols = (rect.width // brick_width) + 1
    rows = (rect.height // brick_height) + 1
    
    for row in range(rows):
        for col in range(cols):
            # Offset every other row for brick pattern
            x_offset = (brick_width // 2) if row % 2 == 1 else 0
            
            brick_x = draw_x + (col * brick_width) + x_offset
            brick_y = draw_y + (row * brick_height)
            
            # Only draw if brick is within platform bounds and on screen
            if brick_x + brick_width < draw_x or brick_x > draw_x + rect.width:
                continue
            if brick_y + brick_height < draw_y or brick_y > draw_y + rect.height:
                continue
            
            # Clip brick to platform boundaries
            brick_rect = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
            clip_rect = brick_rect.clip(pygame.Rect(draw_x, draw_y, rect.width, rect.height))
            
            if clip_rect.width <= 0 or clip_rect.height <= 0:
                continue
            
            # Draw snowy/icy brick with shading for 3D effect
            # Main brick color (light blue-white ice)
            brick_color = (200, 220, 240)  # Icy blue-white
            pygame.draw.rect(screen, brick_color, clip_rect)
            
            # Top highlight (bright white snow/ice)
            highlight_color = (240, 250, 255)  # Almost pure white
            if clip_rect.height > 2:
                pygame.draw.rect(screen, highlight_color, (clip_rect.x, clip_rect.y, clip_rect.width, 2))
            
            # Left highlight
            if clip_rect.width > 2:
                pygame.draw.rect(screen, highlight_color, (clip_rect.x, clip_rect.y, 2, clip_rect.height))
            
            # Bottom shadow (darker blue-grey)
            shadow_color = (120, 140, 170)  # Cool shadow
            if clip_rect.height > 2:
                pygame.draw.rect(screen, shadow_color, (clip_rect.x, clip_rect.bottom - 2, clip_rect.width, 2))
            
            # Right shadow
            if clip_rect.width > 2:
                pygame.draw.rect(screen, shadow_color, (clip_rect.right - 2, clip_rect.y, 2, clip_rect.height))
            
            # Brick outline (medium blue-grey for icy definition)
            pygame.draw.rect(screen, (100, 120, 150), clip_rect, 1)


def draw_icy_brick_platform(screen, rect, camera_x):
    """Draw a dark blue icy brick platform with individual blocks"""
    # Brick dimensions
    brick_width = 32
    brick_height = 16

    # Offset for camera
    draw_x = rect.x - camera_x
    draw_y = rect.y

    # Calculate how many bricks fit
    cols = (rect.width // brick_width) + 1
    rows = (rect.height // brick_height) + 1

    for row in range(rows):
        for col in range(cols):
            # Offset every other row for brick pattern
            x_offset = (brick_width // 2) if row % 2 == 1 else 0

            brick_x = draw_x + (col * brick_width) + x_offset
            brick_y = draw_y + (row * brick_height)

            # Only draw if brick is within platform bounds and on screen
            if brick_x + brick_width < draw_x or brick_x > draw_x + rect.width:
                continue
            if brick_y + brick_height < draw_y or brick_y > draw_y + rect.height:
                continue

            # Clip brick to platform boundaries
            brick_rect = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
            clip_rect = brick_rect.clip(pygame.Rect(draw_x, draw_y, rect.width, rect.height))

            if clip_rect.width <= 0 or clip_rect.height <= 0:
                continue

            # Draw dark blue icy brick with shading for 3D effect
            # Main brick color (dark blue ice)
            brick_color = (50, 100, 150)  # Dark blue ice
            pygame.draw.rect(screen, brick_color, clip_rect)

            # Top highlight (lighter blue)
            highlight_color = (70, 120, 180)  # Lighter blue highlight
            if clip_rect.height > 2:
                pygame.draw.rect(screen, highlight_color, (clip_rect.x, clip_rect.y, clip_rect.width, 2))

            # Left highlight
            if clip_rect.width > 2:
                pygame.draw.rect(screen, highlight_color, (clip_rect.x, clip_rect.y, 2, clip_rect.height))

            # Bottom shadow (darker blue)
            shadow_color = (30, 70, 110)  # Very dark blue shadow
            if clip_rect.height > 2:
                pygame.draw.rect(screen, shadow_color, (clip_rect.x, clip_rect.bottom - 2, clip_rect.width, 2))

            # Right shadow
            if clip_rect.width > 2:
                pygame.draw.rect(screen, shadow_color, (clip_rect.right - 2, clip_rect.y, 2, clip_rect.height))

            # Brick outline (deep blue for definition)
            pygame.draw.rect(screen, (20, 50, 90), clip_rect, 1)


def draw_northern_lights_ground(screen, rect, camera_x):
    """Draw glowing northern lights ground with animated aurora colors"""
    import math

    # Brick dimensions
    brick_width = 32
    brick_height = 16

    # Offset for camera
    draw_x = rect.x - camera_x
    draw_y = rect.y

    # Calculate how many bricks fit
    cols = (rect.width // brick_width) + 1
    rows = (rect.height // brick_height) + 1

    # Animated color cycle based on time
    time = pygame.time.get_ticks() / 1000.0  # Time in seconds

    for row in range(rows):
        for col in range(cols):
            # Offset every other row for brick pattern
            x_offset = (brick_width // 2) if row % 2 == 1 else 0

            brick_x = draw_x + (col * brick_width) + x_offset
            brick_y = draw_y + (row * brick_height)

            # Only draw if brick is within platform bounds and on screen
            if brick_x + brick_width < draw_x or brick_x > draw_x + rect.width:
                continue
            if brick_y + brick_height < draw_y or brick_y > draw_y + rect.height:
                continue

            # Clip brick to platform boundaries
            brick_rect = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
            clip_rect = brick_rect.clip(pygame.Rect(draw_x, draw_y, rect.width, rect.height))

            if clip_rect.width <= 0 or clip_rect.height <= 0:
                continue

            # Create animated aurora colors (green/purple/blue)
            # Use position and time for wave effect
            phase = (col * 0.3 + row * 0.2 + time * 0.8) % 1.0

            if phase < 0.33:
                # Green aurora
                r = int(50 + phase * 300)
                g = int(150 + math.sin(phase * math.pi) * 80)
                b = int(100 + phase * 100)
            elif phase < 0.66:
                # Purple aurora
                adjusted_phase = (phase - 0.33) * 3
                r = int(120 + math.sin(adjusted_phase * math.pi) * 80)
                g = int(50 + adjusted_phase * 100)
                b = int(150 + math.sin(adjusted_phase * math.pi) * 80)
            else:
                # Blue aurora
                adjusted_phase = (phase - 0.66) * 3
                r = int(50 + adjusted_phase * 80)
                g = int(100 + adjusted_phase * 100)
                b = int(180 + math.sin(adjusted_phase * math.pi) * 70)

            # Clamp values
            brick_color = (min(255, max(0, r)), min(255, max(0, g)), min(255, max(0, b)))
            pygame.draw.rect(screen, brick_color, clip_rect)

            # Add glow effect (lighter center)
            glow_color = (min(255, r + 40), min(255, g + 40), min(255, b + 40))
            if clip_rect.width > 4 and clip_rect.height > 4:
                glow_rect = pygame.Rect(clip_rect.x + 2, clip_rect.y + 2, clip_rect.width - 4, clip_rect.height - 4)
                pygame.draw.rect(screen, glow_color, glow_rect)

            # Subtle brick outline
            outline_color = (max(0, r - 30), max(0, g - 30), max(0, b - 30))
            pygame.draw.rect(screen, outline_color, clip_rect, 1)


def draw_snowy_ground(screen, rect, camera_x):
    """Draw snowy ground blocks with brick texture"""
    # Brick dimensions
    brick_width = 32
    brick_height = 16

    # Offset for camera
    draw_x = rect.x - camera_x
    draw_y = rect.y

    # Calculate how many bricks fit
    cols = (rect.width // brick_width) + 1
    rows = (rect.height // brick_height) + 1

    for row in range(rows):
        for col in range(cols):
            # Offset every other row for brick pattern
            x_offset = (brick_width // 2) if row % 2 == 1 else 0

            brick_x = draw_x + (col * brick_width) + x_offset
            brick_y = draw_y + (row * brick_height)

            # Only draw if brick is within platform bounds and on screen
            if brick_x + brick_width < draw_x or brick_x > draw_x + rect.width:
                continue
            if brick_y + brick_height < draw_y or brick_y > draw_y + rect.height:
                continue

            # Clip brick to platform boundaries
            brick_rect = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
            clip_rect = brick_rect.clip(pygame.Rect(draw_x, draw_y, rect.width, rect.height))

            if clip_rect.width <= 0 or clip_rect.height <= 0:
                continue

            # Draw snowy white brick with shading
            # Main brick color (pure white snow)
            brick_color = (255, 255, 255)
            pygame.draw.rect(screen, brick_color, clip_rect)
            
            # Top highlight (bright sparkly snow)
            highlight_color = (255, 255, 255)
            if clip_rect.height > 2:
                pygame.draw.rect(screen, highlight_color, (clip_rect.x, clip_rect.y, clip_rect.width, 2))
            
            # Left highlight (bright)
            if clip_rect.width > 2:
                pygame.draw.rect(screen, (245, 250, 255), (clip_rect.x, clip_rect.y, 2, clip_rect.height))
            
            # Bottom shadow (light blue-grey snow shadow)
            shadow_color = (220, 230, 240)
            if clip_rect.height > 2:
                pygame.draw.rect(screen, shadow_color, (clip_rect.x, clip_rect.bottom - 2, clip_rect.width, 2))
            
            # Right shadow
            if clip_rect.width > 2:
                pygame.draw.rect(screen, shadow_color, (clip_rect.right - 2, clip_rect.y, 2, clip_rect.height))
            
            # Brick outline (light grey for snow definition)
            pygame.draw.rect(screen, (200, 210, 220), clip_rect, 1)


def draw_wooden_platform(screen, rect, camera_x):
    """Draw wooden platforms with brick texture"""
    # Brick dimensions
    brick_width = 32
    brick_height = 16
    
    # Offset for camera
    draw_x = rect.x - camera_x
    draw_y = rect.y
    
    # Calculate how many bricks fit
    cols = (rect.width // brick_width) + 1
    rows = (rect.height // brick_height) + 1
    
    for row in range(rows):
        for col in range(cols):
            # Offset every other row for brick pattern
            x_offset = (brick_width // 2) if row % 2 == 1 else 0
            
            brick_x = draw_x + (col * brick_width) + x_offset
            brick_y = draw_y + (row * brick_height)
            
            # Only draw if brick is within platform bounds and on screen
            if brick_x + brick_width < draw_x or brick_x > draw_x + rect.width:
                continue
            if brick_y + brick_height < draw_y or brick_y > draw_y + rect.height:
                continue
            
            # Clip brick to platform boundaries
            brick_rect = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
            clip_rect = brick_rect.clip(pygame.Rect(draw_x, draw_y, rect.width, rect.height))
            
            if clip_rect.width <= 0 or clip_rect.height <= 0:
                continue
            
            # Draw wooden brick with shading
            # Main brick color (brown wood)
            brick_color = (139, 90, 60)  # Medium brown wood
            pygame.draw.rect(screen, brick_color, clip_rect)
            
            # Top highlight (lighter brown)
            highlight_color = (180, 120, 80)
            if clip_rect.height > 2:
                pygame.draw.rect(screen, highlight_color, (clip_rect.x, clip_rect.y, clip_rect.width, 2))
            
            # Left highlight
            if clip_rect.width > 2:
                pygame.draw.rect(screen, highlight_color, (clip_rect.x, clip_rect.y, 2, clip_rect.height))
            
            # Bottom shadow (dark brown)
            shadow_color = (80, 50, 30)
            if clip_rect.height > 2:
                pygame.draw.rect(screen, shadow_color, (clip_rect.x, clip_rect.bottom - 2, clip_rect.width, 2))
            
            # Right shadow
            if clip_rect.width > 2:
                pygame.draw.rect(screen, shadow_color, (clip_rect.right - 2, clip_rect.y, 2, clip_rect.height))
            
            # Brick outline (dark brown)
            pygame.draw.rect(screen, (60, 40, 20), clip_rect, 1)


def draw_death_screen(screen):
    """Draw the death screen overlay"""
    # Create semi-transparent black overlay
    overlay = pygame.Surface((S.WINDOW_WIDTH, S.WINDOW_HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(0)  # Semi-transparent (reduced from 200 for better visibility)
    screen.blit(overlay, (0, 0))
    
    # Load Fixedsys font
    try:
        font_large = pygame.font.Font("assets/fonts/Fixedsys500c.ttf", 48)
        font_small = pygame.font.Font("assets/fonts/Fixedsys500c.ttf", 28)
    except:
        font_large = pygame.font.Font(None, 72)
        font_small = pygame.font.Font(None, 48)
    
    text1 = font_large.render("Oh no! You died.", True, (255, 255, 255))
    text2 = font_small.render("Press Enter to restart.", True, (200, 200, 200))
    
    text1_rect = text1.get_rect(center=(S.WINDOW_WIDTH // 2, S.WINDOW_HEIGHT // 2 - 40))
    text2_rect = text2.get_rect(center=(S.WINDOW_WIDTH // 2, S.WINDOW_HEIGHT // 2 + 40))
    
    screen.blit(text1, text1_rect)
    screen.blit(text2, text2_rect)

def draw_game_hud(screen, coins_collected, level_time, world_name, difficulty="Medium", coins_remaining=0):
    """Draw the top HUD with coins, world, and time like Super Mario"""
    # Load Fixedsys font
    try:
        font = pygame.font.Font("assets/fonts/Fixedsys500c.ttf", 24)
        small_font = pygame.font.Font("assets/fonts/Fixedsys500c.ttf", 18)
    except:
        try:
            font = pygame.font.SysFont('arial', 36, bold=True)
            small_font = pygame.font.SysFont('arial', 24, bold=True)
        except:
            font = pygame.font.Font(None, 36)
            small_font = pygame.font.Font(None, 24)

    # Calculate time in seconds
    time_seconds = level_time // 60

    # Use white text for levels 2 and 4 due to dark/snowy backgrounds
    text_color = (255, 255, 255) if world_name in ["1-2", "1-4"] else (0, 0, 0)

    # Create HUD text
    coins_text = font.render(f"COINS", True, text_color)
    coins_value = font.render(f"{coins_collected}", True, text_color)

    world_text = font.render(f"WORLD", True, text_color)
    world_value = font.render(f"{world_name}", True, text_color)

    time_text = font.render(f"TIME", True, text_color)
    time_value = font.render(f"{time_seconds}", True, text_color)

    # Position HUD elements - adjusted to accommodate hearts while keeping TIME visible
    screen_width = S.WINDOW_WIDTH

    # Left-center section - COINS (moved a bit more right)
    coins_label_x = screen_width // 2 - 30
    screen.blit(coins_text, (coins_label_x, 10))
    # Center the value under the label
    coins_value_x = coins_label_x + (coins_text.get_width() - coins_value.get_width()) // 2
    screen.blit(coins_value, (coins_value_x, 40))

    # Center section - WORLD (moved a bit more right)
    world_label_x = screen_width // 2 + 170
    screen.blit(world_text, (world_label_x, 10))
    # Center the value under the label
    world_value_x = world_label_x + (world_text.get_width() - world_value.get_width()) // 2
    screen.blit(world_value, (world_value_x, 40))

    # Right-center section - TIME (moved a few pixels left)
    time_label_x = screen_width // 2 + 340
    screen.blit(time_text, (time_label_x, 10))
    # Center the value under the label
    time_value_x = time_label_x + (time_text.get_width() - time_value.get_width()) // 2
    screen.blit(time_value, (time_value_x, 40))

    # Difficulty and coins remaining (top left, below hearts)
    difficulty_text = small_font.render(f"Difficulty: {difficulty.upper()}", True, text_color)
    screen.blit(difficulty_text, (20, 75))

    # Coins remaining on second line
    coins_text = small_font.render(f"({coins_remaining} coins remaining)", True, text_color)
    screen.blit(coins_text, (20, 95))
