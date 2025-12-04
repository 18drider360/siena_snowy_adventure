# main.py
import sys
import pygame
from utils import settings as S
from utils.progression import GameProgression, LevelManager
from utils.save_system import SaveSystem
from utils.background import ParallaxBackground
from ui.health_display import HealthDisplay
from ui.enemy_health_display import EnemyHealthDisplay
from ui.spin_charge_display import SpinChargeDisplay
from ui.roll_stamina_display import RollStaminaDisplay
from menus import PauseMenu, DeathMenu
from audio_manager import AudioManager
from game_screens import show_title_screen, show_level_transition
from rendering import (
    draw_level_complete_screen,
    draw_spiky_hazard, draw_brick_platform, draw_icy_brick_platform,
    draw_northern_lights_ground, draw_snowy_ground, draw_wooden_platform,
    draw_death_screen, draw_game_hud
)
import collision_physics as collision
import constants as C

# GLOBAL AUDIO CONTROL - Set to True to completely disable ALL audio
# This is controlled by settings.MASTER_AUDIO_ENABLED
DISABLE_ALL_AUDIO = not S.MASTER_AUDIO_ENABLED


def main(progression):
    # Initialize pygame if not already done
    if not pygame.get_init():
        pygame.init()

    # Disable audio mixer if DISABLE_ALL_AUDIO is True
    if DISABLE_ALL_AUDIO:
        try:
            pygame.mixer.quit()
        except:
            pass

    # Create scaled display window
    display_width = int(S.WINDOW_WIDTH * S.DISPLAY_SCALE)
    display_height = int(S.WINDOW_HEIGHT * S.DISPLAY_SCALE)
    display_screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption(S.TITLE)

    # Create internal render surface (800x600) - this is what we draw to
    screen = pygame.Surface((S.WINDOW_WIDTH, S.WINDOW_HEIGHT))

    clock = pygame.time.Clock()

    # --- LOAD GAME CONFIGURATION ---
    from config_loader import get_config
    config = get_config()

    # --- GLOBAL SETTINGS ---
    SHOW_HITBOXES = config.get('debug.show_hitboxes', False)

    # --- AUDIO TOGGLES ---
    # These are controlled by settings.MASTER_AUDIO_ENABLED
    ENABLE_MUSIC = S.MASTER_AUDIO_ENABLED  # Background music (main menu, in-game)
    ENABLE_SOUND = S.MASTER_AUDIO_ENABLED  # Sound effects (character sounds, jumps, attacks, coins, etc.)

    # --- DEBUG TOGGLES (loaded from config.yaml) ---
    DEBUG_UNLOCK_ALL_LEVELS = config.get('debug.unlock_all_levels', True)
    DEBUG_INVINCIBILITY = config.get('debug.invincibility', False)
    SHOW_ENEMIES = config.get('debug.show_enemies', True)
    SHOW_PLATFORMS = config.get('debug.show_platforms', True)
    SHOW_HAZARDS = config.get('debug.show_hazards', True)
    SHOW_GROUND = config.get('debug.show_ground', False)

    # --- AUDIO MANAGER ---
    audio_manager = AudioManager(enable_music=ENABLE_MUSIC, enable_sound=ENABLE_SOUND)
    audio_manager.play_music(loop=True)
    
    # Game state
    game_over = False
    level_complete = False
    cutscene_active = False
    cutscene_selected_button = "continue"  # "continue" or "menu"
    paused = False  # NEW: Pause state
    death_fade_alpha = 0
    death_fade_speed = 5
    death_animation_timer = 0
    death_animation_delay = 90  # 3 seconds at 60 FPS (adjust as needed)
    show_death_screen = False
    
    # --- MENU SYSTEMS ---
    pause_menu = PauseMenu()
    death_menu = DeathMenu()
    
    # --- GAME STATS ---
    coins_collected = 0
    level_time = 0  # Time in frames (divide by 60 for seconds)

    # --- BUILD LEVEL USING LEVEL MANAGER ---
    bg_color, platforms, hazards, level_width, player, enemies, projectiles, coins, world_name, goal_npc, background_layers, moving_platforms, disappearing_platforms, appearing_platforms = \
        LevelManager.load_level(progression.current_level, progression)

    # Save the original static platforms (we'll rebuild the full list each frame with dynamic platforms)
    static_platforms = platforms.copy()

    # --- LOAD PARALLAX BACKGROUND (now level-specific) ---
    background = ParallaxBackground(background_layers, level_width)

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

        # Handle events differently based on game state
        if not cutscene_active:
            # Normal game event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    # --- PAUSE TOGGLE (check this FIRST) ---
                    if event.key == pygame.K_ESCAPE:
                        if not game_over and not cutscene_active:
                            paused = not paused  # Toggle pause
                            if paused:
                                pause_menu.selected_index = 0  # Reset selection
                                audio_manager.pause_music()  # Pause music
                            else:
                                audio_manager.unpause_music()  # Resume music
                        elif paused:
                            paused = False  # ESC also unpauses
                            audio_manager.unpause_music()  # Resume music
                        continue  # Don't process other keys when pressing ESC

                    # Handle pause menu input (only if paused)
                    if paused:
                        result = pause_menu.handle_input(event)
                        if result == "CONTINUE":
                            paused = False
                            audio_manager.unpause_music()  # Resume music
                        elif result == "RESTART":
                            audio_manager.stop_music()  # Stop music before restart
                            return "RESTART"  # Signal to restart
                        elif result == "MAIN MENU":
                            audio_manager.stop_music()  # Stop music before returning to menu
                            return "MAIN_MENU"  # Return to title screen
                        continue  # Skip other inputs while paused

                    # Handle death menu input (only if showing death screen)
                    if show_death_screen:
                        result = death_menu.handle_input(event)
                        if result == "RESTART":
                            audio_manager.stop_music()  # Stop music before restart
                            return "RESTART"  # Signal to restart
                        elif result == "MAIN MENU":
                            audio_manager.stop_music()  # Stop music before returning to menu
                            return "MAIN_MENU"  # Return to title screen
                        continue  # Skip other inputs on death screen

                    # Jump (only if not dead, not paused, and not on death screen)
                    if not game_over and not paused and not show_death_screen:
                        if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                            player.jump(audio_manager.get_sound('jump'),
                                       audio_manager.get_sound('double_jump'))

                    if not game_over and not paused and not show_death_screen:
                        if event.key == pygame.K_e:
                            # E key only triggers spin attack now
                            player.spin_attack(audio_manager.get_sound('spin_attack'))

                    # Restart anytime with Shift+Enter (kept for convenience)
                    keys = pygame.key.get_pressed()
                    if event.key == pygame.K_RETURN and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
                        return "RESTART"

                # --- MOUSE EVENT HANDLING ---
                elif event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                    # Handle pause menu mouse input (only if paused)
                    if paused:
                        result = pause_menu.handle_input(event)
                        if result == "CONTINUE":
                            paused = False
                            audio_manager.unpause_music()  # Resume music
                        elif result == "RESTART":
                            audio_manager.stop_music()  # Stop music before restart
                            return "RESTART"  # Signal to restart
                        elif result == "MAIN MENU":
                            audio_manager.stop_music()  # Stop music before returning to menu
                            return "MAIN_MENU"  # Return to title screen

                    # Handle death menu mouse input (only if showing death screen)
                    elif show_death_screen:
                        result = death_menu.handle_input(event)
                        if result == "RESTART":
                            audio_manager.stop_music()  # Stop music before restart
                            return "RESTART"  # Signal to restart
                        elif result == "MAIN MENU":
                            audio_manager.stop_music()  # Stop music before returning to menu
                            return "MAIN_MENU"  # Return to title screen

        # Check if player is dead
        if player.health <= 0 and not game_over:
            game_over = True
            death_fade_alpha = 0
            death_animation_timer = 0
            show_death_screen = False
            if ENABLE_MUSIC and not DISABLE_ALL_AUDIO:
                audio_manager.stop_music()  # Stop music on death
            audio_manager.play_sound('death')  # Play death sound effect

        # Handle death animation delay
        if game_over and not show_death_screen:
            death_animation_timer += 1
            if death_animation_timer >= death_animation_delay:
                show_death_screen = True

        # --- UPDATE (only if not game over, not in cutscene, and not paused) ---
        if not game_over and not cutscene_active and not paused:
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
                # Check if player has collected enough coins for their difficulty level
                coins_required = progression.get_coin_requirement(progression.current_level)
                if coins_collected >= coins_required:
                    level_complete = True
                    cutscene_active = True
                    audio_manager.stop_music()  # Stop music on level complete
                    audio_manager.play_sound('stage_clear')  # Play victory sound
                    # Complete the level in progression system
                    progression.complete_level(
                        level_num=progression.current_level,
                        coins_collected=coins_collected,
                        time_taken=level_time,
                        deaths=0  # Not tracking deaths
                    )

                    # Submit score to scoreboard
                    SaveSystem.submit_score(
                        username=current_username,
                        level_num=progression.current_level,
                        time_taken=level_time,
                        coins_collected=coins_collected,
                        difficulty=progression.difficulty
                    )

                    # Save progress to disk
                    if SaveSystem.save_progress(progression, current_username):
                        print(f"💾 Progress saved! Level {progression.current_level} complete.")
                # If not enough coins, nothing happens - player just stands there
            
            # --- CHECK HAZARDS FIRST (before platform collision adjusts position) ---
            if SHOW_HAZARDS:  # Only check hazards if they're enabled
                for hazard in hazards:
                    if player.hitbox.colliderect(hazard):
                        if not game_over and not DEBUG_INVINCIBILITY:  # Only trigger once (unless invincible)
                            player.health = 0
                            player.die()
                            game_over = True
                            death_fade_alpha = 0
                            death_animation_timer = 0
                            show_death_screen = False
                            audio_manager.stop_music()  # Stop music
                            audio_manager.play_sound('death')  # Play death sound
                        break

            # --- CHECK FOR FALLING OFF THE MAP (pit death) ---
            if player.rect.y > 550:  # Player has fallen below the screen (screen height = 600)
                if not game_over and not DEBUG_INVINCIBILITY:
                    player.health = 0
                    player.die()
                    game_over = True
                    death_fade_alpha = 0
                    death_animation_timer = 0
                    show_death_screen = False
                    audio_manager.stop_music()  # Stop music
                    audio_manager.play_sound('death')  # Play death sound

            # --- PLATFORM COLLISION ---
            player.on_ground = False  # Reset each frame

            if SHOW_PLATFORMS:  # Only collide with platforms if they're enabled
                player.on_ground = collision.check_platform_collision_player(player, platforms)
            
            # --- PRE-UPDATE ENEMY EDGE DETECTION ---
            # ONLY stop enemies at GROUND-LEVEL edges (holes in the ground)
            if SHOW_ENEMIES:
                all_walkable = platforms  # Enemies pass through hazards, only collide with platforms

                for enemy in enemies:
                    # Skip if enemy is dead or doesn't have direction
                    if getattr(enemy, 'is_dead', False) or not hasattr(enemy, 'direction'):
                        continue

                    # Reset edge flag
                    enemy.at_platform_edge = False

                    # Find the platform the enemy is currently standing on
                    current_platform = None
                    tolerance = 10

                    for platform in all_walkable:
                        if (enemy.hitbox.bottom >= platform.top - tolerance and
                            enemy.hitbox.bottom <= platform.top + tolerance and
                            enemy.hitbox.right > platform.left and
                            enemy.hitbox.left < platform.right):
                            current_platform = platform
                            break

                    if current_platform:
                        # Only apply edge detection if enemy is on a GROUND platform
                        # Ground platforms are typically at Y=400 (±30 pixels tolerance)
                        is_ground_platform = abs(current_platform.top - 400) <= 30

                        if is_ground_platform:
                            # Check ahead in the direction the enemy will move
                            look_ahead = enemy.hitbox.width // 2  # Look ahead half the enemy's width

                            if enemy.direction == -1:  # Moving left
                                # Check if we're at or past the left edge
                                if enemy.hitbox.left - look_ahead <= current_platform.left:
                                    enemy.direction = 1
                                    enemy.facing_right = True
                                    enemy.at_platform_edge = True
                            elif enemy.direction == 1:  # Moving right
                                # Check if we're at or past the right edge
                                if enemy.hitbox.right + look_ahead >= current_platform.right:
                                    enemy.direction = -1
                                    enemy.facing_right = False
                                    enemy.at_platform_edge = True

                            # SPECIAL: Spiked Slimes should avoid walking onto hazards
                            from enemies.spiked_slime import SpikedSlime
                            if isinstance(enemy, SpikedSlime) and SHOW_HAZARDS:
                                # Check if there's a hazard ahead
                                hazard_check_distance = 40

                                for hazard in hazards:
                                    # Check if hazard is ahead in movement direction
                                    if enemy.direction == -1:  # Moving left
                                        if (hazard.right >= enemy.hitbox.left - hazard_check_distance and
                                            hazard.left < enemy.hitbox.left and
                                            abs(hazard.top - enemy.hitbox.bottom) < 50):
                                            # Hazard ahead! Turn around
                                            enemy.direction = 1
                                            enemy.facing_right = True
                                            enemy.at_platform_edge = True
                                            break
                                    elif enemy.direction == 1:  # Moving right
                                        if (hazard.left <= enemy.hitbox.right + hazard_check_distance and
                                            hazard.right > enemy.hitbox.right and
                                            abs(hazard.top - enemy.hitbox.bottom) < 50):
                                            # Hazard ahead! Turn around
                                            enemy.direction = -1
                                            enemy.facing_right = False
                                            enemy.at_platform_edge = True
                                            break

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

                    # Kill enemies that fall below the screen (fell in a pit)
                    if enemy.rect.top > S.WINDOW_HEIGHT + 100:
                        enemy.is_dead = True
                        # Enemy death sounds are handled by the enemy objects themselves
                        continue  # Skip rest of processing for this enemy

                    # Check collision with platforms only (enemies pass through hazards)
                    all_walkable = platforms
                    enemy_on_ground = collision.check_platform_collision_enemy(enemy, all_walkable)

                    # Check if enemy is at patrol edge - make them turn around
                    if enemy_on_ground and hasattr(enemy, 'patrol_left') and hasattr(enemy, 'patrol_right'):
                        if hasattr(enemy, 'direction'):
                            # Find which platform the enemy is on
                            for platform in all_walkable:
                                tolerance = 5
                                if (enemy.hitbox.right > platform.left and
                                    enemy.hitbox.left < platform.right and
                                    enemy.hitbox.bottom >= platform.top - tolerance and
                                    enemy.hitbox.bottom <= platform.top + tolerance):
                                    # Enemy is on this platform - check edges
                                    if enemy.direction == -1:  # Moving left
                                        if enemy.hitbox.left <= platform.left + 10:
                                            enemy.direction = 1
                                            enemy.facing_right = True
                                    elif enemy.direction == 1:  # Moving right
                                        if enemy.hitbox.right >= platform.right - 10:
                                            enemy.direction = -1
                                            enemy.facing_right = False
                                    break
            
            # Update projectiles (snowballs, iceballs, fireballs, spikes)
            projectiles.update()
            
            # Check for newly spawned projectiles that need sound (only if player is nearby)
            if ENABLE_SOUND and audio_manager.get_sound('enemy_projectile'):
                PROJECTILE_SOUND_RANGE = 400  # Only hear projectiles within this distance
                for projectile in projectiles:
                    if hasattr(projectile, 'spawn_sound') and projectile.spawn_sound:
                        # Calculate distance from player to projectile
                        distance = abs(player.hitbox.centerx - projectile.rect.centerx)
                        
                        if distance <= PROJECTILE_SOUND_RANGE:
                            # Player is close enough to hear it
                            # Optional: adjust volume based on distance
                            volume_multiplier = 1.0 - (distance / PROJECTILE_SOUND_RANGE) * 0.6
                            audio_manager.set_sound_volume('enemy_projectile', 0.2 * volume_multiplier)
                            audio_manager.play_sound('enemy_projectile')
                        
                        projectile.spawn_sound = False  # Only check once
            
            # Update coins
            coins.update()

            # Update goal NPC (if exists)
            if goal_npc:
                goal_npc.update()

            # Rebuild platforms list from static platforms each frame
            platforms = static_platforms.copy()

            # Update moving platforms and add to collision list
            for moving_platform in moving_platforms:
                moving_platform.update()
                platforms.append(moving_platform.rect)

            # Update disappearing platforms and add to collision list (if visible)
            player_on_disappearing = False
            for disappearing_platform in disappearing_platforms:
                # Check if player is standing on this platform
                on_platform = (not disappearing_platform.disappeared and
                              player.hitbox.bottom <= disappearing_platform.rect.top + 10 and
                              player.hitbox.bottom >= disappearing_platform.rect.top - 5 and
                              player.hitbox.right > disappearing_platform.rect.left and
                              player.hitbox.left < disappearing_platform.rect.right)
                disappearing_platform.update(on_platform)
                # Add disappearing platforms to regular platforms list for collision (if not disappeared)
                if not disappearing_platform.disappeared:
                    platforms.append(disappearing_platform.rect)

            # Update appearing platforms and add to collision list ONLY when solid
            for appearing_platform in appearing_platforms:
                appearing_platform.update()
                # Only add to collision when the platform is fully solid
                if appearing_platform.is_solid():
                    platforms.append(appearing_platform.rect)

            # --- COLLISION DETECTION ---
            if SHOW_ENEMIES:  # Only check enemy collisions if they're enabled
                for enemy in enemies:
                    # Skip dead enemies completely
                    if getattr(enemy, 'is_dead', False):
                        continue

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
                            # Player is spin attacking
                            if vulnerable_to.get('spin_attack', False):
                                # Enemy is vulnerable to spin attack - deal damage to enemy
                                if enemy.take_damage(1):
                                    # Optional: slight bounce for player on successful hit
                                    player.vel_y = -8
                            else:
                                # Enemy is NOT vulnerable to spin attack - player takes damage
                                if not player.invincible and not DEBUG_INVINCIBILITY:
                                    knockback_direction = 1 if player.rect.centerx < enemy.rect.centerx else -1
                                    player.take_damage(1, knockback_direction)
                                    if ENABLE_SOUND:
                                        audio_manager.play_sound('bump')
                        
                        # --- ROLL DETECTION ---
                        elif player.is_rolling:
                            # Player is rolling
                            if vulnerable_to.get('roll', False):
                                # Enemy is vulnerable to roll - deal damage to enemy
                                if enemy.take_damage(1):
                                    # Apply knockback velocity to enemy (push away from player)
                                    knockback_direction = 1 if player.rect.centerx < enemy.rect.centerx else -1
                                    enemy.knockback_velocity = knockback_direction * 20

                                    # Stop player's roll immediately and prevent re-rolling
                                    player.is_rolling = False
                                    player.roll_timer = 0.0
                                    player.roll_speed_current = player.roll_speed_initial
                                    player.roll_cooldown = 6  # 0.1 seconds at 60 fps

                                    # Reset to standing animation
                                    player.current_frame = 0
                                    player.frame_counter = 0.0

                                    # Apply dramatic knockback - push player back and up
                                    bounce_distance = 60  # Much stronger knockback
                                    player.rect.x += -knockback_direction * bounce_distance

                                    # Give player upward velocity for a small bounce
                                    player.vel_y = -6  # Small upward bounce
                                    player.on_ground = False  # Make player airborne

                                    player.update_hitbox_position()

                                    # Grant brief invincibility after successful roll hit (0.4 seconds)
                                    player.invincible = True
                                    player.invincible_timer = 24  # 0.4 seconds at 60 fps

                                    # Play land_enemy sound
                                    if ENABLE_SOUND:
                                        audio_manager.play_sound('land_enemy')

                                    # Break out of enemy loop to prevent multiple hits in one frame
                                    break
                            else:
                                # Enemy is NOT vulnerable to roll - player takes damage
                                if not player.invincible and not DEBUG_INVINCIBILITY:
                                    knockback_direction = 1 if player.rect.centerx < enemy.rect.centerx else -1
                                    player.take_damage(1, knockback_direction)
                                    if ENABLE_SOUND:
                                        audio_manager.play_sound('bump')
                        
                        # --- STOMP DETECTION ---
                        elif player.vel_y > 0 and player.hitbox.centery < enemy.hitbox.centery:
                            # Player is coming from above (falling onto enemy) - use center comparison for more reliable detection
                            # This prevents damage when landing on enemies under low platforms
                            if vulnerable_to.get('stomp', False):
                                # Enemy is vulnerable to stomp - deal damage to enemy
                                enemy.take_damage(1)
                                player.vel_y = -15  # Always bounce player up on stomp
                                
                                # Play appropriate stomp sound
                                if ENABLE_SOUND:
                                    # Check if enemy is a slime
                                    if hasattr(enemy, '__class__') and 'Slime' in enemy.__class__.__name__:
                                        if True:  # Sound handled by audio_manager
                                            audio_manager.play_sound('land_slime')
                                    else:
                                        if True:  # Sound handled by audio_manager
                                            audio_manager.play_sound('land_enemy')
                            else:
                                # Enemy is NOT vulnerable to stomp - player takes damage
                                if not player.invincible and not DEBUG_INVINCIBILITY:
                                    knockback_direction = 1 if player.rect.centerx < enemy.rect.centerx else -1
                                    player.take_damage(1, knockback_direction)
                                    if ENABLE_SOUND:
                                        audio_manager.play_sound('bump')

                        # --- NORMAL COLLISION (no special power active) ---
                        else:
                            # Regular side collision - player takes damage and knockback
                            if not player.invincible and not player.is_spinning and not DEBUG_INVINCIBILITY:
                                knockback_direction = 1 if player.rect.centerx < enemy.rect.centerx else -1
                                player.take_damage(1, knockback_direction)
                                if ENABLE_SOUND:
                                    audio_manager.play_sound('bump')
                    
                    # Check sword hitbox collision (for Swordsman enemy)
                    if hasattr(enemy, 'sword_hitbox_active') and enemy.sword_hitbox_active:
                        if player.hitbox.colliderect(enemy.sword_hitbox):
                            # Sword always damages player UNLESS player is spin attacking
                            if not player.invincible and not player.is_spinning and not DEBUG_INVINCIBILITY:
                                knockback_direction = 1 if player.rect.centerx < enemy.rect.centerx else -1
                                player.take_damage(1, knockback_direction)
                                if ENABLE_SOUND:
                                    audio_manager.play_sound('bump')

                    # Check punch hitbox collision (for Snowy enemy)
                    if hasattr(enemy, 'punch_hitbox_active') and enemy.punch_hitbox_active:
                        if player.hitbox.colliderect(enemy.punch_hitbox):
                            # Punch always damages player UNLESS player is spin attacking
                            if not player.invincible and not player.is_spinning and not DEBUG_INVINCIBILITY:
                                damage = getattr(enemy, 'punch_damage', 1)
                                knockback_direction = 1 if player.rect.centerx < enemy.rect.centerx else -1
                                player.take_damage(damage, knockback_direction)
                                if ENABLE_SOUND:
                                    audio_manager.play_sound('bump')
            
            # Check projectile hits (snowballs, iceballs, fireballs, spikes)
            if SHOW_ENEMIES:  # Only check projectiles if enemies are enabled
                for projectile in projectiles:
                    if player.hitbox.colliderect(projectile.rect):
                        # Projectiles don't damage player if they're spin attacking
                        if not player.is_spinning and not DEBUG_INVINCIBILITY:
                            # Knockback away from projectile
                            knockback_direction = 1 if player.rect.centerx < projectile.rect.centerx else -1
                            player.take_damage(1, knockback_direction)
                            if ENABLE_SOUND:
                                audio_manager.play_sound('bump')
                        # Always destroy the projectile on contact (even during spin)
                        projectile.kill()
            
            # --- COIN COLLECTION ---
            for coin in coins:
                if player.hitbox.colliderect(coin.hitbox):
                    coin.collect()
                    coins_collected += 1
                    if ENABLE_SOUND:
                        audio_manager.play_sound('coin')

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

            # Pre-render to get button rectangles (needed for mouse clicks)
            temp_surface = pygame.Surface((S.WINDOW_WIDTH, S.WINDOW_HEIGHT))
            continue_rect, menu_rect = draw_level_complete_screen(
                temp_surface,
                progression.current_level,
                coins_collected,
                level_time,
                progression.username,
                cutscene_selected_button
            )

            # Check mouse hover to update button selection
            mouse_pos = pygame.mouse.get_pos()
            scaled_mouse_x = int(mouse_pos[0] / S.DISPLAY_SCALE)
            scaled_mouse_y = int(mouse_pos[1] / S.DISPLAY_SCALE)
            scaled_mouse_pos = (scaled_mouse_x, scaled_mouse_y)

            if continue_rect.collidepoint(scaled_mouse_pos):
                cutscene_selected_button = "continue"
            elif menu_rect.collidepoint(scaled_mouse_pos):
                cutscene_selected_button = "menu"

            # Handle cutscene button navigation and selection
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        # Toggle between buttons
                        old_button = cutscene_selected_button
                        cutscene_selected_button = "menu" if cutscene_selected_button == "continue" else "continue"
                        print(f"Arrow key pressed: {old_button} -> {cutscene_selected_button}")
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        # Activate selected button
                        if cutscene_selected_button == "continue":
                            # Check if there's a next level
                            next_level = progression.current_level + 1
                            if next_level in LevelManager.LEVELS:
                                # There's a next level - advance to it
                                progression.advance_to_next_level()
                                return "NEXT_LEVEL"  # Signal to load next level
                            else:
                                # No more levels - return to title screen
                                return "LEVEL_COMPLETE"  # Return to title screen
                        else:  # menu button
                            return "MENU"  # Return to main menu
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Mouse click - detect which button was clicked
                    mouse_pos = pygame.mouse.get_pos()
                    scaled_mouse_x = int(mouse_pos[0] / S.DISPLAY_SCALE)
                    scaled_mouse_y = int(mouse_pos[1] / S.DISPLAY_SCALE)
                    scaled_mouse_pos = (scaled_mouse_x, scaled_mouse_y)

                    if continue_rect.collidepoint(scaled_mouse_pos):
                        # Clicked continue button
                        next_level = progression.current_level + 1
                        if next_level in LevelManager.LEVELS:
                            progression.advance_to_next_level()
                            return "NEXT_LEVEL"
                        else:
                            return "LEVEL_COMPLETE"
                    elif menu_rect.collidepoint(scaled_mouse_pos):
                        # Clicked menu button
                        return "MENU"
        elif game_over:
            # Still update player animation even when dead to show death animation
            # But don't pass real keys - pass empty dict to prevent movement
            player.update({})

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
            # For Level 2, draw ground with snowy texture, platforms with wooden texture
            # For other levels, draw everything with icy brick texture
            
            if world_name == "1-1":
                # LEVEL 1: Invisible ground segments (ground_1 through ground_8), visible platforms
                # Skip first 8 platforms which are ground segments at y=570
                platforms_to_draw = platforms[8:]  # Skip ground_1 through ground_8

                for platform in platforms_to_draw:
                    # Draw brick pattern for platforms (not ground)
                    draw_brick_platform(screen, platform, camera_x)

                    # Optional: Draw platform outline for hitbox debugging
                    if SHOW_HITBOXES:
                        draw_rect = pygame.Rect(platform.x - camera_x, platform.y, platform.width, platform.height)
                        pygame.draw.rect(screen, (255, 255, 0), draw_rect, 2)
            elif world_name == "1-2":
                # LEVEL 2: Snowy ground + wooden platforms
                # Level 2 has 6 ground segments at Y=400, then platforms above
                # Draw first 6 platforms as snowy ground (the main floor)
                for i, platform in enumerate(platforms):
                    if i < 6:  # First 6 are ground segments
                        draw_snowy_ground(screen, platform, camera_x)
                    else:  # Rest are wooden platforms
                        draw_wooden_platform(screen, platform, camera_x)

                    if SHOW_HITBOXES:
                        draw_rect = pygame.Rect(platform.x - camera_x, platform.y, platform.width, platform.height)
                        pygame.draw.rect(screen, (255, 255, 0), draw_rect, 2)
            elif world_name == "1-3":
                # LEVEL 3: Dark blue icy brick platforms
                # Draw all platforms (including ground) with dark blue icy bricks
                for platform in platforms:
                    draw_icy_brick_platform(screen, platform, camera_x)

                    if SHOW_HITBOXES:
                        draw_rect = pygame.Rect(platform.x - camera_x, platform.y, platform.width, platform.height)
                        pygame.draw.rect(screen, (255, 255, 0), draw_rect, 2)

                # Draw moving platforms
                for moving_platform in moving_platforms:
                    draw_icy_brick_platform(screen, moving_platform.rect, camera_x)

                    if SHOW_HITBOXES:
                        draw_rect = pygame.Rect(moving_platform.rect.x - camera_x, moving_platform.rect.y,
                                               moving_platform.rect.width, moving_platform.rect.height)
                        pygame.draw.rect(screen, (0, 255, 255), draw_rect, 2)  # Cyan for moving platforms

                # Draw disappearing platforms (same style as Level 4)
                for disappearing_platform in disappearing_platforms:
                    if not disappearing_platform.disappeared:
                        # Create a semi-transparent surface
                        platform_surface = pygame.Surface((disappearing_platform.rect.width, disappearing_platform.rect.height))
                        platform_surface.set_colorkey((0, 0, 0))

                        # Fill with semi-transparent white/blue ice color
                        ice_color = (180, 200, 220)
                        pygame.draw.rect(platform_surface, ice_color, (0, 0, disappearing_platform.rect.width, disappearing_platform.rect.height))

                        # Draw border (black/grey) to make it clear
                        border_color = (50, 50, 50) if not disappearing_platform.should_shake() else (100, 100, 100)
                        pygame.draw.rect(platform_surface, border_color, (0, 0, disappearing_platform.rect.width, disappearing_platform.rect.height), 3)

                        # Apply transparency
                        platform_surface.set_alpha(disappearing_platform.get_alpha())

                        # Apply pulse effect if warning about state change
                        pulse_offset = 0
                        if disappearing_platform.should_shake():
                            import random
                            pulse_offset = random.randint(-1, 1)

                        # Draw to screen
                        screen.blit(platform_surface,
                                   (disappearing_platform.rect.x - camera_x,
                                    disappearing_platform.rect.y + pulse_offset))

                        if SHOW_HITBOXES:
                            draw_rect = pygame.Rect(disappearing_platform.rect.x - camera_x, disappearing_platform.rect.y,
                                                   disappearing_platform.rect.width, disappearing_platform.rect.height)
                            pygame.draw.rect(screen, (255, 0, 255), draw_rect, 2)  # Magenta for disappearing platforms
            elif world_name == "1-4":
                # LEVEL 4: Glowing northern lights platforms with animated colors
                # Draw all platforms (including ground) with animated northern lights effect
                for platform in platforms:
                    draw_northern_lights_ground(screen, platform, camera_x)

                    if SHOW_HITBOXES:
                        draw_rect = pygame.Rect(platform.x - camera_x, platform.y, platform.width, platform.height)
                        pygame.draw.rect(screen, (255, 255, 0), draw_rect, 2)

                # Draw moving platforms
                for moving_platform in moving_platforms:
                    draw_northern_lights_ground(screen, moving_platform.rect, camera_x)

                    if SHOW_HITBOXES:
                        draw_rect = pygame.Rect(moving_platform.rect.x - camera_x, moving_platform.rect.y,
                                                moving_platform.rect.width, moving_platform.rect.height)
                        pygame.draw.rect(screen, (0, 255, 255), draw_rect, 2)  # Cyan for moving platforms

                # Draw disappearing platforms with same design as Level 4 appearing platforms
                for disappearing_platform in disappearing_platforms:
                    if not disappearing_platform.disappeared:
                        # Create a semi-transparent surface (matching Level 4 style)
                        platform_surface = pygame.Surface((disappearing_platform.rect.width, disappearing_platform.rect.height))
                        platform_surface.set_colorkey((0, 0, 0))

                        # Fill with semi-transparent white/blue ice color (same as Level 4)
                        ice_color = (180, 200, 220)
                        pygame.draw.rect(platform_surface, ice_color, (0, 0, disappearing_platform.rect.width, disappearing_platform.rect.height))

                        # Draw solid border (not dashed) - matching Level 4 style
                        # Use red warning color if about to disappear, otherwise black/grey
                        if disappearing_platform.should_shake():
                            border_color = (255, 50, 50)  # Red warning when shaking
                        else:
                            border_color = (50, 50, 50)  # Dark grey/black normally (matches Level 4)

                        pygame.draw.rect(platform_surface, border_color, (0, 0, disappearing_platform.rect.width, disappearing_platform.rect.height), 3)

                        # Apply alpha for fade effect
                        platform_surface.set_alpha(disappearing_platform.get_alpha())

                        # Apply pulse effect if warning (same as Level 4 appearing platforms)
                        pulse_offset = 0
                        if disappearing_platform.should_shake():
                            import random
                            pulse_offset = random.randint(-1, 1)

                        # Draw to screen
                        screen.blit(platform_surface,
                                   (disappearing_platform.rect.x - camera_x,
                                    disappearing_platform.rect.y + pulse_offset))

                        if SHOW_HITBOXES:
                            draw_rect = pygame.Rect(disappearing_platform.rect.x - camera_x, disappearing_platform.rect.y,
                                                   disappearing_platform.rect.width, disappearing_platform.rect.height)
                            pygame.draw.rect(screen, (255, 0, 255), draw_rect, 2)  # Magenta for disappearing platforms

                # Draw appearing platforms with transparency and border
                for appearing_platform in appearing_platforms:
                    if appearing_platform.get_alpha() > 0:  # Only draw if visible at all
                        # Create a semi-transparent surface
                        platform_surface = pygame.Surface((appearing_platform.rect.width, appearing_platform.rect.height))
                        platform_surface.set_colorkey((0, 0, 0))

                        # Fill with semi-transparent white/blue ice color
                        ice_color = (180, 200, 220)
                        pygame.draw.rect(platform_surface, ice_color, (0, 0, appearing_platform.rect.width, appearing_platform.rect.height))

                        # Draw border (black/grey) to make it clear
                        border_color = (50, 50, 50) if appearing_platform.is_solid() else (100, 100, 100)
                        pygame.draw.rect(platform_surface, border_color, (0, 0, appearing_platform.rect.width, appearing_platform.rect.height), 3)

                        # Apply transparency
                        platform_surface.set_alpha(appearing_platform.get_alpha())

                        # Apply pulse effect if warning about state change
                        pulse_offset = 0
                        if appearing_platform.should_pulse():
                            import random
                            pulse_offset = random.randint(-1, 1)

                        # Draw to screen
                        screen.blit(platform_surface,
                                   (appearing_platform.rect.x - camera_x,
                                    appearing_platform.rect.y + pulse_offset))

                        if SHOW_HITBOXES:
                            draw_rect = pygame.Rect(appearing_platform.rect.x - camera_x, appearing_platform.rect.y,
                                                   appearing_platform.rect.width, appearing_platform.rect.height)
                            color = (0, 255, 0) if appearing_platform.is_solid() else (128, 128, 128)
                            pygame.draw.rect(screen, color, draw_rect, 2)
            else:
                # OTHER LEVELS: Icy brick texture, skip ground
                platforms_to_draw = platforms[1:]  # Skip invisible ground

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
                # Skip drawing enemies that have completed their death animation
                if getattr(enemy, 'death_complete', False):
                    continue

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
        
        # Draw game HUD (coins, world, time, difficulty, coins remaining)
        coins_remaining = progression.get_coins_remaining(progression.current_level, coins_collected)
        draw_game_hud(screen, coins_collected, level_time, world_name, progression.difficulty, coins_remaining)
        
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
            
            # Update and draw death menu
            death_menu.update()
            death_menu.draw(screen)
        
        # --- LEVEL COMPLETE CUTSCENE ---
        if cutscene_active:
            # Draw the cutscene (button rects already calculated earlier)
            draw_level_complete_screen(
                screen,
                progression.current_level,
                coins_collected,
                level_time,
                progression.username,
                cutscene_selected_button
            )
        
        # --- PAUSE MENU OVERLAY ---
        if paused:
            pause_menu.update()
            pause_menu.draw(screen)

        # Scale render surface to display screen
        scaled_surface = pygame.transform.scale(screen, (display_width, display_height))
        display_screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    # Initialize pygame first (needed for username input)
    pygame.init()

    # Create display for username input
    display_width = int(S.WINDOW_WIDTH * S.DISPLAY_SCALE)
    display_height = int(S.WINDOW_HEIGHT * S.DISPLAY_SCALE)
    screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption(S.TITLE)

    # Initialize progression system
    progression = GameProgression()

    # Load config to check if DEBUG_UNLOCK_ALL_LEVELS is enabled
    from config_loader import get_config
    config = get_config()

    # Load saved progress and username (unless in debug mode)
    current_username = None
    if not config.get('debug.unlock_all_levels', True):
        success, username = SaveSystem.load_progress(progression)
        if success and username:
            current_username = username
            print(f"📁 Loaded progress: {username} - Level {progression.current_level}/{progression.max_level_reached}")
        else:
            print("ℹ️ No save file found.")
    else:
        # Debug mode: unlock all levels (excluding test levels like 99)
        regular_levels = [lvl for lvl in LevelManager.LEVELS.keys() if lvl < 90]
        progression.max_level_reached = max(regular_levels) if regular_levels else 1
        print(f"🔓 DEBUG: All {len(regular_levels)} levels unlocked")
        # Abilities are NOT unlocked - player must earn them by completing levels

    # If no username, prompt for one
    if current_username is None:
        from ui.username_input import show_username_input
        current_username = show_username_input(screen)
        if current_username is None:
            # User closed window during username input
            pygame.quit()
            sys.exit()
        print(f"👤 Welcome, {current_username}!")
        # Update progression with username
        progression.username = current_username
        # Save progress with new username
        SaveSystem.save_progress(progression, current_username)
    else:
        # Username was loaded from save file, update progression
        progression.username = current_username
    
    # Main game loop - keeps running until player quits
    while True:
        # Show title screen and get selection
        result = show_title_screen(progression, disable_audio=DISABLE_ALL_AUDIO)
        
        # If user closed window during title screen, exit
        if result is None:
            break
        
        # Handle menu selection
        if result == "START":
            # Start from level 1
            progression.current_level = 1
        elif result.startswith("LEVEL_"):
            # Start from selected level
            level_num = int(result.split("_")[1])
            progression.set_level(level_num)

        # Track which levels have shown their tutorial
        tutorials_shown = set()

        # Play through levels with transitions
        playing = True
        while playing:
            # Show level transition and tutorial screens for this level if not yet shown
            if progression.current_level not in tutorials_shown:
                show_level_transition(progression.current_level, disable_audio=DISABLE_ALL_AUDIO)
                tutorials_shown.add(progression.current_level)

            # Play current level
            game_result = main(progression)
            
            # Handle result
            if game_result == "QUIT":
                # Player wants to quit entirely
                pygame.quit()
                sys.exit()
            
            elif game_result == "NEXT_LEVEL":
                # Level completed - show transition screen
                show_level_transition(progression.current_level, disable_audio=DISABLE_ALL_AUDIO)
                tutorials_shown.add(progression.current_level)
                # Continue to next level (progression already advanced)
                continue
            
            elif game_result == "LEVEL_COMPLETE":
                # Final level completed or player chose to return to menu
                playing = False

            elif game_result == "MENU" or game_result == "MAIN_MENU":
                # Player chose to return to main menu from level complete screen
                playing = False
            
            elif game_result == "RESTART":
                # Player restarted level - just loop and replay current level
                continue
            
            else:
                # Unknown result - return to title screen
                playing = False