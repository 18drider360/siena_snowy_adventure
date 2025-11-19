def draw_level_complete_screen(screen, level_num, coins, time):
    """Draw the level completion cutscene as a dialogue with the penguin NPC"""
    # Load font
    try:
        font_large = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 24)
        font_small = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 16)
    except:
        font_large = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 32)
    
    # Calculate time in seconds
    time_seconds = time // 60
    
    # Draw dialogue box (like old RPG games)
    dialogue_box = pygame.Rect(100, 350, S.WINDOW_WIDTH - 200, 200)
    
    # Draw box shadow
    shadow_box = dialogue_box.copy()
    shadow_box.x += 4
    shadow_box.y += 4
    pygame.draw.rect(screen, (0, 0, 0), shadow_box)
    
    # Draw main box with border
    pygame.draw.rect(screen, (255, 255, 255), dialogue_box)
    pygame.draw.rect(screen, (0, 0, 0), dialogue_box, 4)
    
    # Inner padding
    text_area = dialogue_box.inflate(-40, -40)
    
    # NPC Name tag (top-left corner of box)
    name_tag = pygame.Rect(dialogue_box.x + 20, dialogue_box.y - 15, 150, 30)
    pygame.draw.rect(screen, (255, 215, 0), name_tag)  # Gold
    pygame.draw.rect(screen, (0, 0, 0), name_tag, 3)
    
    name_text = font_small.render("PEDRO", True, (0, 0, 0))
    name_rect = name_text.get_rect(center=(name_tag.centerx, name_tag.centery))
    screen.blit(name_text, name_rect)
    
    # Dialogue text lines
    y_offset = text_area.y + 10
    line_spacing = 35
    
    # Line 1: Congratulations
    line1 = font_large.render("Congratulations, Siena!", True, (0, 0, 0))
    screen.blit(line1, (text_area.x, y_offset))
    y_offset += line_spacing + 10
    
    # Line 2: Level complete
    line2 = font_small.render(f"You completed Level {level_num}!", True, (0, 0, 0))
    screen.blit(line2, (text_area.x, y_offset))
    y_offset += line_spacing
    
    # Line 3: Stats intro
    line3 = font_small.render("Here are your results:", True, (0, 0, 0))
    screen.blit(line3, (text_area.x, y_offset))
    y_offset += line_spacing
    
    # Line 4: Coins collected
    line4 = font_small.render(f"  Coins: {coins}", True, (0, 100, 0))
    screen.blit(line4, (text_area.x, y_offset))
    y_offset += line_spacing
    
    # Line 5: Time
    line5 = font_small.render(f"  Time: {time_seconds} seconds", True, (0, 100, 0))
    screen.blit(line5, (text_area.x, y_offset))
    
    # Press Enter prompt (bottom-right)
    prompt_text = font_small.render("Press ENTER >", True, (100, 100, 100))
    prompt_rect = prompt_text.get_rect(bottomright=(dialogue_box.right - 20, dialogue_box.bottom - 15))
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

def draw_spiky_hazard(screen, rect, camera_x):
    """Draw a dangerous spiky ice hazard"""
    draw_x = rect.x - camera_x
    draw_y = rect.y
    
    # Base danger color - dark icy blue with red tint
    base_color = (140, 180, 220)  # Icy blue base
    danger_tint = (200, 100, 120)  # Reddish danger overlay
    
    # Draw the base ice block
    draw_rect = pygame.Rect(draw_x, draw_y, rect.width, rect.height)
    pygame.draw.rect(screen, base_color, draw_rect)
    
    # Add danger gradient overlay (darker at bottom)
    for i in range(rect.height):
        alpha = int(50 * (i / rect.height))  # Gradient from 0 to 50
        gradient_color = (
            base_color[0] - alpha,
            base_color[1] - alpha,
            base_color[2] - alpha
        )
        pygame.draw.line(screen, gradient_color, 
                        (draw_x, draw_y + i), 
                        (draw_x + rect.width, draw_y + i))
    
    # Draw spikes across the top edge
    spike_width = 16  # Width of each spike base
    spike_height = 20  # How tall spikes are
    num_spikes = (rect.width // spike_width) + 1
    
    for i in range(num_spikes):
        spike_x = draw_x + (i * spike_width)
        
        # Skip if off-screen
        if spike_x > draw_x + rect.width - spike_width:
            continue
        
        # Spike triangle points (pointing UP from platform)
        tip_x = spike_x + spike_width // 2
        tip_y = draw_y - spike_height
        left_x = spike_x
        left_y = draw_y
        right_x = spike_x + spike_width
        right_y = draw_y
        
        spike_points = [(tip_x, tip_y), (left_x, left_y), (right_x, right_y)]
        
        # Main spike color (icy white with slight blue)
        spike_color = (230, 240, 250)
        pygame.draw.polygon(screen, spike_color, spike_points)
        
        # Spike outline (darker for definition)
        pygame.draw.polygon(screen, (100, 120, 150), spike_points, 2)
        
        # Add highlight on left side of spike
        highlight_points = [(tip_x, tip_y), (left_x, left_y), (tip_x, tip_y + spike_height // 2)]
        pygame.draw.polygon(screen, (255, 255, 255), highlight_points, 1)
        
        # Add red danger glow at tip (warning!)
        danger_tip = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.circle(danger_tip, (255, 100, 100, 120), (6, 6), 6)
        screen.blit(danger_tip, (tip_x - 6, tip_y - 3))
    
    # Draw danger outline around entire hazard
    pygame.draw.rect(screen, (255, 50, 50), draw_rect, 3)  # Red warning border
    
    # Add pulsing danger effect (optional - you can remove if too much)
    import time
    pulse = int(abs(((time.time() * 3) % 2) - 1) * 30)  # Pulsing value 0-30
    danger_outline_color = (255, 100 + pulse, 100 + pulse)
    pygame.draw.rect(screen, danger_outline_color, draw_rect, 2)


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


def draw_death_screen(screen):
    """Draw the death screen overlay"""
    # Create semi-transparent black overlay
    overlay = pygame.Surface((S.WINDOW_WIDTH, S.WINDOW_HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(200)  # Semi-transparent
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

def draw_game_hud(screen, coins_collected, level_time, world_name):
    """Draw the top HUD with coins, world, and time like Super Mario"""
    # Load Fixedsys font
    try:
        font = pygame.font.Font("assets/fonts/Fixedsys500c.ttf", 24)
    except:
        try:
            font = pygame.font.SysFont('arial', 36, bold=True)
        except:
            font = pygame.font.Font(None, 36)
    
    # Calculate time in seconds
    time_seconds = level_time // 60
    
    # Create HUD text
    coins_text = font.render(f"COINS", True, (0, 0, 0))
    coins_value = font.render(f"{coins_collected}", True, (0, 0, 0))
    
    world_text = font.render(f"WORLD", True, (0, 0, 0))
    world_value = font.render(f"{world_name}", True, (0, 0, 0))
    
    time_text = font.render(f"TIME", True, (0, 0, 0))
    time_value = font.render(f"{time_seconds}", True, (0, 0, 0))
    
    # Position HUD elements very close to center
    screen_width = S.WINDOW_WIDTH
    
    # Left-center section - COINS
    coins_label_x = screen_width // 2 - 100
    screen.blit(coins_text, (coins_label_x, 10))
    # Center the value under the label
    coins_value_x = coins_label_x + (coins_text.get_width() - coins_value.get_width()) // 2
    screen.blit(coins_value, (coins_value_x, 40))
    
    # Center section - WORLD
    world_label_x = screen_width // 2 + 100
    screen.blit(world_text, (world_label_x, 10))
    # Center the value under the label
    world_value_x = world_label_x + (world_text.get_width() - world_value.get_width()) // 2
    screen.blit(world_value, (world_value_x, 40))
    
    # Right-center section - TIME
    time_label_x = screen_width // 2 + 300
    screen.blit(time_text, (time_label_x, 10))
    # Center the value under the label
    time_value_x = time_label_x + (time_text.get_width() - time_value.get_width()) // 2
    screen.blit(time_value, (time_value_x, 40))

def main():
    pygame.init()
    screen = pygame.display.set_mode((S.WINDOW_WIDTH, S.WINDOW_HEIGHT))
    pygame.display.set_caption(S.TITLE)
    clock = pygame.time.Clock()

    # --- GLOBAL SETTINGS ---
    SHOW_HITBOXES = False  # Disable all hitbox debugging
    
    # --- AUDIO TOGGLES ---
    ENABLE_MUSIC = False  # Set to False to disable background music
    ENABLE_SOUND = False  # Set to False to disable sound effects
    
    # --- DEBUG TOGGLES ---
    SHOW_ENEMIES = True
    SHOW_PLATFORMS = True
    SHOW_HAZARDS = True
    SHOW_GROUND = False  # Ground is invisible (still has collision)

    # --- PROGRESSION SYSTEM ---
    progression = GameProgression()
    
    # --- MUSIC SETUP ---
    if ENABLE_MUSIC:
        try:
            pygame.mixer.music.load("assets/music/main_theme.ogg")
            pygame.mixer.music.set_volume(0.6)  # 60% volume (adjust as needed)
            pygame.mixer.music.play(-1)  # -1 means loop forever
        except Exception as e:
            print(f"Could not load music: {e}")
    
    # --- SOUND EFFECTS ---
    if ENABLE_SOUND:
        try:
            # Try new location first, fall back to old location
            try:
                death_sound = pygame.mixer.Sound("assets/sounds/death.wav")
            except:
                death_sound = pygame.mixer.Sound("assets/music/death.wav")
            death_sound.set_volume(0.6)
        except Exception as e:
            print(f"Could not load death sound: {e}")
            death_sound = None
        
        try:
            # Try new location first, fall back to old location
            try:
                stage_clear_sound = pygame.mixer.Sound("assets/sounds/stage_clear.wav")
            except:
                stage_clear_sound = pygame.mixer.Sound("assets/music/stage_clear.wav")
            stage_clear_sound.set_volume(0.7)
        except Exception as e:
            print(f"Could not load stage clear sound: {e}")
            stage_clear_sound = None
        
        try:
            jump_sound = pygame.mixer.Sound("assets/sounds/jump.ogg")
            jump_sound.set_volume(0.4)
        except Exception as e:
            print(f"Could not load jump sound: {e}")
            jump_sound = None
        
        try:
            double_jump_sound = pygame.mixer.Sound("assets/sounds/double_jump.ogg")
            double_jump_sound.set_volume(0.4)
        except Exception as e:
            print(f"Could not load double jump sound: {e}")
            double_jump_sound = None
        
        try:
            coin_sound = pygame.mixer.Sound("assets/sounds/coin.ogg")
            coin_sound.set_volume(0.2)
        except Exception as e:
            print(f"Could not load coin sound: {e}")
            coin_sound = None
        
        try:
            bump_sound = pygame.mixer.Sound("assets/sounds/bump.ogg")
            bump_sound.set_volume(0.2)
        except Exception as e:
            print(f"Could not load bump sound: {e}")
            bump_sound = None
        
        try:
            land_enemy_sound = pygame.mixer.Sound("assets/sounds/land_enemy.ogg")
            land_enemy_sound.set_volume(0.3)
        except Exception as e:
            print(f"Could not load land enemy sound: {e}")
            land_enemy_sound = None
        
        try:
            land_slime_sound = pygame.mixer.Sound("assets/sounds/land_slime.ogg")
            land_slime_sound.set_volume(0.3)
        except Exception as e:
            print(f"Could not load land slime sound: {e}")
            land_slime_sound = None
        
        try:
            enemy_projectile_sound = pygame.mixer.Sound("assets/sounds/enemy_projectile.ogg")
            enemy_projectile_sound.set_volume(0.2)
        except Exception as e:
            print(f"Could not load enemy projectile sound: {e}")
            enemy_projectile_sound = None
    else:
        death_sound = None
        stage_clear_sound = None
        jump_sound = None
        double_jump_sound = None
        coin_sound = None
        bump_sound = None
        land_enemy_sound = None
        land_slime_sound = None
        enemy_projectile_sound = None
    
    # Game state
    game_over = False
    level_complete = False
    cutscene_active = False
    death_fade_alpha = 0
    death_fade_speed = 5
    death_animation_timer = 0
    death_animation_delay = 90  # 3 seconds at 60 FPS (adjust as needed)
    show_death_screen = False
    
    # --- GAME STATS ---
    coins_collected = 0
    level_time = 0  # Time in frames (divide by 60 for seconds)

    # --- BUILD LEVEL USING LEVEL MANAGER ---
    bg_color, platforms, hazards, level_width, player, enemies, projectiles, coins, world_name, goal_npc = \
        LevelManager.load_level(progression.current_level, progression)

    # --- LOAD PARALLAX BACKGROUND ---
    image_paths = [
        "assets/images/backgrounds/mountains/5.png",
        "assets/images/backgrounds/mountains/4.png",
        "assets/images/backgrounds/mountains/3.png",
        "assets/images/backgrounds/mountains/2.png",
        "assets/images/backgrounds/mountains/1.png",
    ]
    background = ParallaxBackground(image_paths, level_width)

    # --- HEALTH UI SETUP ---
    health_ui = HealthDisplay()
    enemy_health_ui = EnemyHealthDisplay()
    roll_stamina_ui = RollStaminaDisplay()
    spin_charge_ui = SpinChargeDisplay()

    camera_x = 0

    # --- GAME LOOP ---
    running = True
    while running:
        dt = clock.tick(S.FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                # Jump (only if not dead)
                if not game_over:
                    if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                        player.jump(jump_sound if ENABLE_SOUND else None, 
                                   double_jump_sound if ENABLE_SOUND else None)

                if not game_over:
                    if event.key == pygame.K_e:
                        # E key only triggers spin attack now
                        player.spin_attack()
                
                # Restart on Enter when death screen is showing
                if show_death_screen and event.key == pygame.K_RETURN:
                    # Restart the game by calling main() recursively
                    main()
                    return
                
                # Restart anytime with Shift+Enter
                keys = pygame.key.get_pressed()
                if event.key == pygame.K_RETURN and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
                    main()
                    return

        # Check if player is dead
        if player.health <= 0 and not game_over:
            game_over = True
            death_fade_alpha = 0
            death_animation_timer = 0
            show_death_screen = False
            if ENABLE_MUSIC:
                pygame.mixer.music.stop()  # Stop music on death
            if ENABLE_SOUND and death_sound:
                death_sound.play()  # Play death sound effect

        # Handle death animation delay
        if game_over and not show_death_screen:
            death_animation_timer += 1
            if death_animation_timer >= death_animation_delay:
                show_death_screen = True

        # --- UPDATE (only if not game over and not in cutscene) ---
        if not game_over and not cutscene_active:
            # Increment level timer
            level_time += 1
            
            keys = pygame.key.get_pressed()
            
            player.update(keys)
            
            # --- LEFT BOUNDARY WALL (prevent player from going off-screen left) ---
            if player.rect.left < 0:
                player.rect.left = 0
                player.update_hitbox_position()
            
            # --- CHECK LEVEL GOAL NPC ---
            if goal_npc and not level_complete and player.hitbox.colliderect(goal_npc.trigger_zone):
                level_complete = True
                cutscene_active = True
                if ENABLE_MUSIC:
                    pygame.mixer.music.stop()  # Stop music on level complete
                if ENABLE_SOUND and stage_clear_sound:
                    stage_clear_sound.play()  # Play victory sound
                # Complete the level in progression system
                progression.complete_level(
                    level_num=progression.current_level,
                    coins_collected=coins_collected,
                    time_taken=level_time,
                    deaths=0  # Not tracking deaths
                )
            
            # --- CHECK HAZARDS FIRST (before platform collision adjusts position) ---
            if SHOW_HAZARDS:  # Only check hazards if they're enabled
                for hazard in hazards:
                    if player.hitbox.colliderect(hazard):
                        if not game_over:  # Only trigger once
                            player.health = 0
                            player.die()
                            game_over = True
                            death_fade_alpha = 0
                            death_animation_timer = 0
                            show_death_screen = False
                            if ENABLE_MUSIC:
                                pygame.mixer.music.stop()  # Stop music
                            if ENABLE_SOUND and death_sound:
                                death_sound.play()  # Play death sound
                        break
            
            # --- PLATFORM COLLISION ---
            player.on_ground = False  # Reset each frame
            
            if SHOW_PLATFORMS:  # Only collide with platforms if they're enabled
                for platform in platforms:
                    # Check if hitbox is touching or overlapping platform
                    # Add a small tolerance (5 pixels) to catch cases where player is resting on platform
                    tolerance = 5
                    touching_from_top = (
                        player.hitbox.right > platform.left and 
                        player.hitbox.left < platform.right and
                        player.hitbox.bottom >= platform.top - tolerance and
                        player.hitbox.bottom <= platform.top + tolerance and
                        player.vel_y >= 0
                    )
                    
                    if touching_from_top:
                        # Player is on top of platform - adjust RECT based on where hitbox should be
                        
                        # Calculate how much to adjust the rect
                        # We want hitbox.bottom to be at platform.top
                        hitbox_offset = player.rect.bottom - player.hitbox.bottom
                        player.rect.bottom = platform.top + hitbox_offset
                        
                        player.vel_y = 0
                        player.on_ground = True
                        player.has_double_jump = False
                        player.update_hitbox_position()
                        
                    elif player.hitbox.colliderect(platform):
                        # Calculate overlap on each axis
                        overlap_left = player.hitbox.right - platform.left
                        overlap_right = platform.right - player.hitbox.left
                        overlap_top = player.hitbox.bottom - platform.top
                        overlap_bottom = platform.bottom - player.hitbox.top
                        
                        # Find the smallest overlap (this is the side we collided from)
                        min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
                        
                        # Landing on platform from above
                        if min_overlap == overlap_top and player.vel_y >= 0:
                            
                            # Adjust rect so that hitbox ends up at platform.top
                            hitbox_offset = player.rect.bottom - player.hitbox.bottom
                            player.rect.bottom = platform.top + hitbox_offset
                            
                            player.vel_y = 0
                            player.on_ground = True
                            player.has_double_jump = False
                            player.update_hitbox_position()
                        
                        # Hitting platform from below
                        elif min_overlap == overlap_bottom and player.vel_y < 0:
                            
                            # Adjust rect so hitbox top aligns with platform bottom
                            hitbox_offset_top = player.hitbox.top - player.rect.top
                            player.rect.top = platform.bottom - hitbox_offset_top
                            
                            player.vel_y = 0
                            player.update_hitbox_position()
                        
                        # Side collisions
                        elif min_overlap == overlap_left:
                            
                            hitbox_offset_x = player.hitbox.left - player.rect.left
                            player.rect.left = platform.left - hitbox_offset_x - player.hitbox.width
                            
                            player.update_hitbox_position()
                        elif min_overlap == overlap_right:
                            
                            hitbox_offset_x = player.hitbox.left - player.rect.left
                            player.rect.left = platform.right - hitbox_offset_x
                            
                            player.update_hitbox_position()
            
            # Update enemies (they add projectiles to the group)
            if SHOW_ENEMIES:  # Only update enemies if they're enabled
                for enemy in enemies:
                    enemy.update(player=player, projectile_group=projectiles)
            
            # --- ENEMY PLATFORM COLLISION ---
            if SHOW_ENEMIES:  # Only handle enemy collisions if they're enabled
                for enemy in enemies:
                    # Skip if enemy is dead
                    if getattr(enemy, 'is_dead', False):
                        continue
                    
                    # Apply gravity if enemy has it
                    if hasattr(enemy, 'vel_y'):
                        enemy.vel_y += enemy.gravity
                        enemy.rect.y += enemy.vel_y
                    else:
                        # Add gravity properties if they don't exist
                        enemy.vel_y = 0
                        enemy.gravity = 0.6
                    
                    # Reset on_ground state
                    enemy_on_ground = False
                    
                    # Check collision with all platforms AND hazards (enemies can walk on hazards)
                    all_walkable = platforms + hazards if SHOW_HAZARDS else platforms
                    for platform in all_walkable:
                        # Check if enemy hitbox is near or touching platform
                        tolerance = 5
                        touching_from_top = (
                            enemy.hitbox.right > platform.left and 
                            enemy.hitbox.left < platform.right and
                            enemy.hitbox.bottom >= platform.top - tolerance and
                            enemy.hitbox.bottom <= platform.top + tolerance and
                            enemy.vel_y >= 0
                        )
                        
                        if touching_from_top:
                            # Enemy is on platform
                            hitbox_offset = enemy.rect.bottom - enemy.hitbox.bottom
                            enemy.rect.bottom = platform.top + hitbox_offset
                            enemy.vel_y = 0
                            enemy_on_ground = True
                            enemy.update_hitbox_position()
                            
                            # Check if enemy is at patrol edge - make them turn around
                            if hasattr(enemy, 'patrol_left') and hasattr(enemy, 'patrol_right'):
                                # Check if they're about to walk off the platform edge
                                if enemy.direction == -1:  # Moving left
                                    # If left edge of hitbox is past platform left edge, turn around
                                    if enemy.hitbox.left <= platform.left + 10:
                                        enemy.direction = 1
                                        enemy.facing_right = True
                                elif enemy.direction == 1:  # Moving right
                                    # If right edge of hitbox is past platform right edge, turn around
                                    if enemy.hitbox.right >= platform.right - 10:
                                        enemy.direction = -1
                                        enemy.facing_right = False
                            
                            break  # Found a platform, stop checking
                        
                        elif enemy.hitbox.colliderect(platform):
                            # Handle other collision types if needed
                            overlap_left = enemy.hitbox.right - platform.left
                            overlap_right = platform.right - enemy.hitbox.left
                            overlap_top = enemy.hitbox.bottom - platform.top
                            overlap_bottom = platform.bottom - enemy.hitbox.top
                            
                            min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
                            
                            if min_overlap == overlap_top and enemy.vel_y >= 0:
                                hitbox_offset = enemy.rect.bottom - enemy.hitbox.bottom
                                enemy.rect.bottom = platform.top + hitbox_offset
                                enemy.vel_y = 0
                                enemy_on_ground = True
                                enemy.update_hitbox_position()
                            elif min_overlap == overlap_bottom and enemy.vel_y < 0:
                                hitbox_offset_top = enemy.hitbox.top - enemy.rect.top
                                enemy.rect.top = platform.bottom - hitbox_offset_top
                                enemy.vel_y = 0
                                enemy.update_hitbox_position()
            
            # Update projectiles (snowballs, iceballs, fireballs, spikes)
            projectiles.update()
            
            # Check for newly spawned projectiles that need sound
            if ENABLE_SOUND and enemy_projectile_sound:
                for projectile in projectiles:
                    if hasattr(projectile, 'spawn_sound') and projectile.spawn_sound:
                        enemy_projectile_sound.play()
                        projectile.spawn_sound = False  # Only play once
            
            # Update coins
            coins.update()
            
            # Update goal NPC (if exists)
            if goal_npc:
                goal_npc.update()

            # --- COLLISION DETECTION ---
            if SHOW_ENEMIES:  # Only check enemy collisions if they're enabled
                for enemy in enemies:
                    # Get enemy's power vulnerability settings (default to all False if not present)
                    vulnerable_to = getattr(enemy, 'vulnerable_to', {
                        'stomp': False,
                        'spin_attack': False,
                        'roll': False
                    })
                    
                    # Check body hitbox collision
                    if player.hitbox.colliderect(enemy.hitbox):
                        # --- SPIN ATTACK DETECTION (check FIRST for priority) ---
                        if player.is_spinning:
                            # Player is spin attacking - ALWAYS protected
                            if vulnerable_to.get('spin_attack', False):
                                # Enemy is vulnerable to spin attack - deal damage to enemy
                                if enemy.take_damage(1):
                                    # Optional: slight bounce for player on successful hit
                                    player.vel_y = -8
                            # If enemy is NOT vulnerable, spin attack still protects player
                            # (no damage to either party)
                        
                        # --- ROLL DETECTION ---
                        elif player.is_rolling:
                            # Player is rolling
                            if vulnerable_to.get('roll', False):
                                # Enemy is vulnerable to roll - deal damage to enemy
                                enemy.take_damage(1)
                            else:
                                # Enemy is NOT vulnerable to roll - player takes damage
                                if not player.invincible:
                                    knockback_direction = 1 if player.rect.centerx < enemy.rect.centerx else -1
                                    player.take_damage(1, knockback_direction)
                                    if ENABLE_SOUND and bump_sound:
                                        bump_sound.play()
                        
                        # --- STOMP DETECTION ---
                        elif player.vel_y > 0 and player.hitbox.bottom <= enemy.hitbox.top + 15:
                            # Player is coming from above (falling onto enemy's head)
                            if vulnerable_to.get('stomp', False):
                                # Enemy is vulnerable to stomp - deal damage to enemy
                                enemy.take_damage(1)
                                player.vel_y = -15  # Always bounce player up on stomp
                                
                                # Play appropriate stomp sound
                                if ENABLE_SOUND:
                                    # Check if enemy is a slime
                                    if hasattr(enemy, '__class__') and 'Slime' in enemy.__class__.__name__:
                                        if land_slime_sound:
                                            land_slime_sound.play()
                                    else:
                                        if land_enemy_sound:
                                            land_enemy_sound.play()
                            else:
                                # Enemy is NOT vulnerable to stomp - player takes damage
                                if not player.invincible:
                                    knockback_direction = 1 if player.rect.centerx < enemy.rect.centerx else -1
                                    player.take_damage(1, knockback_direction)
                                    if ENABLE_SOUND and bump_sound:
                                        bump_sound.play()
                        
                        # --- NORMAL COLLISION (no special power active) ---
                        else:
                            # Regular side collision - player takes damage and knockback
                            if not player.invincible and not player.is_spinning:
                                knockback_direction = 1 if player.rect.centerx < enemy.rect.centerx else -1
                                player.take_damage(1, knockback_direction)
                                if ENABLE_SOUND and bump_sound:
                                    bump_sound.play()
                    
                    # Check sword hitbox collision (for Swordsman enemy)
                    if hasattr(enemy, 'sword_hitbox_active') and enemy.sword_hitbox_active:
                        if player.hitbox.colliderect(enemy.sword_hitbox):
                            # Sword always damages player UNLESS player is spin attacking
                            if not player.invincible and not player.is_spinning:
                                knockback_direction = 1 if player.rect.centerx < enemy.rect.centerx else -1
                                player.take_damage(1, knockback_direction)
                                if ENABLE_SOUND and bump_sound:
                                    bump_sound.play()
                    
                    # Check punch hitbox collision (for Snowy enemy)
                    if hasattr(enemy, 'punch_hitbox_active') and enemy.punch_hitbox_active:
                        if player.hitbox.colliderect(enemy.punch_hitbox):
                            # Punch always damages player UNLESS player is spin attacking
                            if not player.invincible and not player.is_spinning:
                                damage = getattr(enemy, 'punch_damage', 1)
                                knockback_direction = 1 if player.rect.centerx < enemy.rect.centerx else -1
                                player.take_damage(damage, knockback_direction)
                                if ENABLE_SOUND and bump_sound:
                                    bump_sound.play()
            
            # Check projectile hits (snowballs, iceballs, fireballs, spikes)
            if SHOW_ENEMIES:  # Only check projectiles if enemies are enabled
                for projectile in projectiles:
                    if player.hitbox.colliderect(projectile.rect):
                        # Projectiles don't damage player if they're spin attacking
                        if not player.is_spinning:
                            # Knockback away from projectile
                            knockback_direction = 1 if player.rect.centerx < projectile.rect.centerx else -1
                            player.take_damage(1, knockback_direction)
                            if ENABLE_SOUND and bump_sound:
                                bump_sound.play()
                        # Always destroy the projectile on contact (even during spin)
                        projectile.kill()
            
            # --- COIN COLLECTION ---
            for coin in coins:
                if player.hitbox.colliderect(coin.hitbox):
                    coin.collect()
                    coins_collected += 1
                    if ENABLE_SOUND and coin_sound:
                        coin_sound.play()

            # --- CAMERA FOLLOW ---
            if player.rect.centerx - camera_x > S.WINDOW_WIDTH * 0.6:
                camera_x = player.rect.centerx - S.WINDOW_WIDTH * 0.6
            elif player.rect.centerx - camera_x < S.WINDOW_WIDTH * 0.4:
                camera_x = player.rect.centerx - S.WINDOW_WIDTH * 0.4

            camera_x = max(0, min(camera_x, level_width - S.WINDOW_WIDTH))
        elif cutscene_active:
            # --- CUTSCENE MODE ---
            # Keep updating NPC animation during cutscene (if exists)
            if goal_npc:
                goal_npc.update()
            
            # Wait for player to press Enter to continue
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                # TODO: Load next level or return to menu
                # For now, just restart the game
                print(f"✨ Level {progression.current_level} Complete!")
                print(f"📊 Coins: {coins_collected}, Time: {level_time//60}s")
                main()  # Restart for now
                return
        else:
            # Still update player animation even when dead to show death animation
            keys = pygame.key.get_pressed()
            player.update(keys)

        # --- RENDER ---
        screen.fill((50, 50, 80))
        
        background.draw(screen, camera_x)

        # Draw hazard platforms (SPIKY ICE - deadly!) - only if enabled
        if SHOW_HAZARDS:
            for hazard in hazards:
                draw_spiky_hazard(screen, hazard, camera_x)
                
                if SHOW_HITBOXES:
                    # Draw hitbox outline
                    draw_rect = pygame.Rect(hazard.x - camera_x, hazard.y, hazard.width, hazard.height)
                    pygame.draw.rect(screen, (255, 0, 0), draw_rect, 3)  # Bright red outline

        # Draw platforms with brick texture
        if SHOW_PLATFORMS:
            platforms_to_draw = platforms
            if not SHOW_GROUND:
                # Skip ground segments (first 8 platforms in the list for new level)
                platforms_to_draw = platforms[8:]
            
            for platform in platforms_to_draw:
                # Draw brick pattern
                draw_brick_platform(screen, platform, camera_x)
                
                # Optional: Draw platform outline for hitbox debugging
                if SHOW_HITBOXES:
                    draw_rect = pygame.Rect(platform.x - camera_x, platform.y, platform.width, platform.height)
                    pygame.draw.rect(screen, (255, 255, 0), draw_rect, 2)

        # Draw enemies - only if enabled
        if SHOW_ENEMIES:
            for enemy in enemies:
                screen.blit(enemy.image, (enemy.rect.x - camera_x, enemy.rect.y))
                
                # Draw enemy health above them
                enemy_health_ui.draw(screen, enemy, camera_x)
                
                if SHOW_HITBOXES:
                    # Draw body hitbox (yellow)
                    debug_hitbox = enemy.hitbox.copy()
                    debug_hitbox.x -= camera_x
                    pygame.draw.rect(screen, (255, 255, 0), debug_hitbox, 2)
                    
                    # Draw sword hitbox if active (for Swordsman) - red
                    if hasattr(enemy, 'sword_hitbox_active') and enemy.sword_hitbox_active:
                        debug_sword_hitbox = enemy.sword_hitbox.copy()
                        debug_sword_hitbox.x -= camera_x
                        pygame.draw.rect(screen, (255, 0, 0), debug_sword_hitbox, 2)
                    
                    # Draw punch hitbox if active (for Snowy) - red
                    if hasattr(enemy, 'punch_hitbox_active') and enemy.punch_hitbox_active:
                        debug_punch_hitbox = enemy.punch_hitbox.copy()
                        debug_punch_hitbox.x -= camera_x
                        pygame.draw.rect(screen, (255, 0, 0), debug_punch_hitbox, 2)
        
        # Draw projectiles (snowballs, iceballs, fireballs, spikes) - only if enemies enabled
        if SHOW_ENEMIES:
            for projectile in projectiles:
                screen.blit(projectile.image, (projectile.rect.x - camera_x, projectile.rect.y))
        
        # Draw coins
        for coin in coins:
            screen.blit(coin.image, (coin.rect.x - camera_x, coin.rect.y))
            
            if SHOW_HITBOXES:
                coin.draw_hitbox(screen, camera_x)
        
        # Draw goal NPC (if exists)
        if goal_npc:
            screen.blit(goal_npc.image, (goal_npc.rect.x - camera_x, goal_npc.rect.y))
            
            if SHOW_HITBOXES:
                goal_npc.draw_trigger_zone(screen, camera_x)

        # Draw player
        screen.blit(player.image, (player.rect.x - camera_x, player.rect.y))
        
        if SHOW_HITBOXES:
            # Draw player hitbox (cyan)
            debug_player_hitbox = player.hitbox.copy()
            debug_player_hitbox.x -= camera_x
            pygame.draw.rect(screen, (0, 255, 255), debug_player_hitbox, 2)
            
            # Draw player rect outline (green)
            debug_player_rect = player.rect.copy()
            debug_player_rect.x -= camera_x
            pygame.draw.rect(screen, (0, 255, 0), debug_player_rect, 2)

        # --- DRAW UI ---
        health_ui.draw(screen, player.health, player.max_health)
        roll_stamina_ui.draw(screen, player, camera_x)
        spin_charge_ui.draw(screen, player, camera_x)
        
        # Draw game HUD (coins, world, time)
        draw_game_hud(screen, coins_collected, level_time, world_name)
        
        # --- DEBUG: DRAW PLAYER POSITION ---
        if SHOW_HITBOXES:  # Only show when hitboxes are enabled
            try:
                debug_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 12)
            except:
                debug_font = pygame.font.Font(None, 24)
            
            # Show player X and Y position
            pos_text = debug_font.render(f"X: {int(player.rect.x)} Y: {int(player.rect.y)}", True, (255, 255, 0))
            # Draw with black outline for visibility
            screen.blit(pos_text, (10, S.WINDOW_HEIGHT - 30))
 
        

        # --- DEATH SCREEN (only show after animation delay) ---
        if show_death_screen:
            # Fade in death screen
            if death_fade_alpha < 255:
                death_fade_alpha = min(255, death_fade_alpha + death_fade_speed)
            
            draw_death_screen(screen)
        
        # --- LEVEL COMPLETE CUTSCENE ---
        if cutscene_active:
            draw_level_complete_screen(screen, progression.current_level, coins_collected, level_time)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()