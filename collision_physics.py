"""
Collision & Physics Module
Handles all collision detection and physics calculations for the game
"""

import pygame
from utils import settings as S


def check_platform_collision_player(player, platforms, tolerance=5):
    """
    Check and handle player collision with platforms (full collision detection)

    Args:
        player: The player object
        platforms: List of platform rectangles
        tolerance: Pixel tolerance for collision detection

    Returns:
        bool: True if player is on ground, False otherwise
    """
    on_ground = False

    for platform in platforms:
        # First check: Simple touching from top (most common case)
        touching_from_top = (
            player.hitbox.right > platform.left and
            player.hitbox.left < platform.right and
            player.hitbox.bottom >= platform.top - tolerance and
            player.hitbox.bottom <= platform.top + tolerance and
            player.vel_y >= 0
        )

        if touching_from_top:
            # Player is on top of platform - adjust RECT based on where hitbox should be
            hitbox_offset = player.rect.bottom - player.hitbox.bottom
            player.rect.bottom = platform.top + hitbox_offset

            player.vel_y = 0
            on_ground = True
            player.has_double_jump = False
            player.update_hitbox_position()

        elif player.hitbox.colliderect(platform):
            # More complex collision - calculate overlap on each axis
            overlap_left = player.hitbox.right - platform.left
            overlap_right = platform.right - player.hitbox.left
            overlap_top = player.hitbox.bottom - platform.top
            overlap_bottom = platform.bottom - player.hitbox.top

            # Find the smallest overlap (this is the side we collided from)
            min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

            # Landing on platform from above
            if min_overlap == overlap_top and player.vel_y >= 0:
                hitbox_offset = player.rect.bottom - player.hitbox.bottom
                player.rect.bottom = platform.top + hitbox_offset

                player.vel_y = 0
                on_ground = True
                player.has_double_jump = False
                player.update_hitbox_position()

            # Hitting platform from below
            elif min_overlap == overlap_bottom and player.vel_y < 0:
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

    return on_ground


def check_platform_collision_enemy(enemy, platforms, tolerance=20):
    """
    Check and handle enemy collision with platforms

    Args:
        enemy: The enemy object
        platforms: List of platform rectangles
        tolerance: Pixel tolerance for collision detection (increased to 20 to catch fast-falling enemies from tall drops)

    Returns:
        bool: True if enemy is on ground, False otherwise
    """
    enemy_on_ground = False

    for platform in platforms:
        # Check collision from top
        touching_from_top = (
            enemy.hitbox.right > platform.left and
            enemy.hitbox.left < platform.right and
            enemy.hitbox.bottom >= platform.top - tolerance and
            enemy.hitbox.bottom <= platform.top + tolerance and
            enemy.vel_y >= 0
        )

        if touching_from_top:
            # Enemy lands on platform
            # Enemies use midbottom alignment, so rect.bottom = hitbox.bottom
            enemy.hitbox.bottom = platform.top
            enemy.rect.bottom = enemy.hitbox.bottom
            enemy.vel_y = 0
            enemy_on_ground = True
            enemy.update_hitbox_position()
            break

    return enemy_on_ground


def check_hazard_collision(player, hazards, debug_invincibility=False):
    """
    Check if player collides with any hazards

    Args:
        player: The player object
        hazards: List of hazard rectangles
        debug_invincibility: If True, player is invincible

    Returns:
        bool: True if player hit a hazard and died, False otherwise
    """
    if debug_invincibility:
        return False

    for hazard in hazards:
        if player.hitbox.colliderect(hazard):
            return True

    return False


def check_pit_death(player, screen_height=600, debug_invincibility=False):
    """
    Check if player has fallen off the map

    Args:
        player: The player object
        screen_height: Height of the screen
        debug_invincibility: If True, player is invincible

    Returns:
        bool: True if player fell in pit, False otherwise
    """
    if debug_invincibility:
        return False

    # Player has fallen below the screen (pit death threshold)
    return player.rect.y > screen_height - 50


def check_player_enemy_collision(player, enemy, audio_manager, enable_sound=True):
    """
    Handle collision between player and enemy

    Args:
        player: The player object
        enemy: The enemy object
        audio_manager: Audio manager for playing sounds
        enable_sound: Whether sounds are enabled

    Returns:
        str: Collision type ('stomp', 'spin', 'roll', 'hit_player', 'none')
    """
    # Check if player's spin attack hit the enemy
    if player.is_spinning and player.hitbox.colliderect(enemy.hitbox):
        if enemy.vulnerable_to.get('spin_attack', True):
            enemy.take_damage(1)
            if enable_sound:
                audio_manager.play_sound('bump')
            return 'spin'
        else:
            # Enemy not vulnerable to spin - player takes damage
            knockback_dir = 1 if player.rect.centerx < enemy.rect.centerx else -1
            player.take_damage(1, knockback_direction=knockback_dir)
            if enable_sound:
                audio_manager.play_sound('bump')
            return 'hit_player'

    # Check if player is rolling and hits enemy
    if player.is_rolling and player.hitbox.colliderect(enemy.hitbox):
        if enemy.vulnerable_to.get('roll', True):
            enemy.take_damage(1)
            if enable_sound:
                audio_manager.play_sound('bump')
            return 'roll'
        else:
            # Enemy not vulnerable to roll - player takes damage
            knockback_dir = 1 if player.rect.centerx < enemy.rect.centerx else -1
            player.take_damage(1, knockback_direction=knockback_dir)
            if enable_sound:
                audio_manager.play_sound('bump')
            return 'hit_player'

    # Check if player stomps on enemy
    # Stomp is valid if:
    # 1. Player is falling (vel_y > 0)
    # 2. Player's center is above enemy's center (player is generally above enemy)
    # 3. Hitboxes collide
    # This handles cases where enemies poke through platforms
    if player.hitbox.colliderect(enemy.hitbox):
        player_center_y = player.hitbox.centery
        enemy_center_y = enemy.hitbox.centery

        # If player is falling AND their center is above enemy's center, it's a stomp
        if player.vel_y > 0 and player_center_y < enemy_center_y:
            if enemy.vulnerable_to.get('stomp', True):
                # Player stomps enemy
                enemy.take_damage(1)
                player.vel_y = -10  # Bounce
                if enable_sound:
                    # Check enemy type for sound
                    if hasattr(enemy, '__class__') and 'Slime' in enemy.__class__.__name__:
                        audio_manager.play_sound('land_slime')
                    else:
                        audio_manager.play_sound('land_enemy')
                return 'stomp'
            else:
                # Can't stomp this enemy - player takes damage
                knockback_dir = 1 if player.rect.centerx < enemy.rect.centerx else -1
                player.take_damage(1, knockback_direction=knockback_dir)
                if enable_sound:
                    audio_manager.play_sound('bump')
                return 'hit_player'

    # Regular collision (player touches enemy from side/bottom)
    if player.hitbox.colliderect(enemy.hitbox):
        knockback_dir = 1 if player.rect.centerx < enemy.rect.centerx else -1
        player.take_damage(1, knockback_direction=knockback_dir)
        if enable_sound:
            audio_manager.play_sound('bump')
        return 'hit_player'

    # Check punch hitbox (if enemy has one)
    if hasattr(enemy, 'punch_hitbox_active') and enemy.punch_hitbox_active:
        if player.hitbox.colliderect(enemy.punch_hitbox):
            knockback_dir = 1 if player.rect.centerx < enemy.rect.centerx else -1
            damage = getattr(enemy, 'punch_damage', 1)
            player.take_damage(damage, knockback_direction=knockback_dir)
            if enable_sound:
                audio_manager.play_sound('bump')
            return 'hit_player'

    return 'none'


def check_projectile_player_collision(player, projectile, audio_manager, enable_sound=True):
    """
    Check collision between player and projectile

    Args:
        player: The player object
        projectile: The projectile object
        audio_manager: Audio manager for playing sounds
        enable_sound: Whether sounds are enabled

    Returns:
        bool: True if collision occurred and projectile should be removed
    """
    if player.hitbox.colliderect(projectile.rect):
        # Determine knockback direction based on projectile direction
        knockback_dir = 1 if projectile.direction > 0 else -1
        player.take_damage(1, knockback_direction=knockback_dir)
        if enable_sound:
            audio_manager.play_sound('bump')
        return True

    return False


def check_coin_collection(player, coin):
    """
    Check if player collected a coin

    Args:
        player: The player object
        coin: The coin object

    Returns:
        bool: True if coin was collected
    """
    return player.hitbox.colliderect(coin.rect)


def apply_gravity(entity, gravity=0.6):
    """
    Apply gravity to an entity

    Args:
        entity: The entity object (must have vel_y attribute)
        gravity: Gravity strength
    """
    entity.vel_y += gravity
    entity.rect.y += entity.vel_y


def check_level_boundary(player, level_width):
    """
    Keep player within level boundaries

    Args:
        player: The player object
        level_width: Width of the level
    """
    # Left boundary
    if player.rect.left < 0:
        player.rect.left = 0
        player.update_hitbox_position()

    # Right boundary
    if player.rect.right > level_width:
        player.rect.right = level_width
        player.update_hitbox_position()
