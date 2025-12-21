"""
Unit tests for collision_physics module
Tests all collision detection and physics calculation functions
"""

import pytest
import pygame
import sys
import os

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core import collision_physics as collision
from src.core import constants as C


# Mock classes for testing
class MockPlayer:
    """Mock player object for testing"""
    def __init__(self, x, y, width=40, height=45):
        self.rect = pygame.Rect(x, y, width, height)
        self.hitbox = pygame.Rect(x, y, width, height)
        self.vel_y = 0
        self.on_ground = False
        self.has_double_jump = True
        self.is_spinning = False
        self.is_rolling = False
        self.health = 3

    def update_hitbox_position(self):
        """Mock hitbox update"""
        pass

    def take_damage(self, amount, knockback_direction=0):
        """Mock take damage"""
        self.health -= amount


class MockEnemy:
    """Mock enemy object for testing"""
    def __init__(self, x, y, width=50, height=50):
        self.rect = pygame.Rect(x, y, width, height)
        self.hitbox = pygame.Rect(x, y, width, height)
        self.vel_y = 0

    def update_hitbox_position(self):
        """Mock hitbox update"""
        pass


class MockProjectile:
    """Mock projectile object for testing"""
    def __init__(self, x, y, width=10, height=10):
        self.rect = pygame.Rect(x, y, width, height)
        self.direction = 1


class MockCoin:
    """Mock coin object for testing"""
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)


class MockAudioManager:
    """Mock audio manager for testing"""
    def __init__(self):
        self.sounds_played = []
        self.volume_changes = []

    def play_sound(self, sound_name):
        self.sounds_played.append(sound_name)
        return True

    def set_sound_volume(self, sound_name, volume):
        self.volume_changes.append((sound_name, volume))


# Initialize pygame for tests
pygame.init()


class TestPlatformCollisionPlayer:
    """Tests for player-platform collision detection"""

    def test_player_on_platform(self):
        """Test player standing on a platform"""
        player = MockPlayer(x=100, y=100)
        player.vel_y = 5  # Falling
        platform = pygame.Rect(80, 145, 100, 30)  # Platform below player

        on_ground = collision.check_platform_collision_player(player, [platform])

        assert on_ground == True
        assert player.vel_y == 0
        assert player.has_double_jump == False

    def test_player_not_touching_platform(self):
        """Test player not touching any platform"""
        player = MockPlayer(x=100, y=100)
        player.vel_y = 5
        platform = pygame.Rect(300, 145, 100, 30)  # Platform far away

        on_ground = collision.check_platform_collision_player(player, [platform])

        assert on_ground == False
        assert player.vel_y == 5  # Velocity unchanged

    def test_player_landing_on_platform(self):
        """Test player landing on platform from above"""
        player = MockPlayer(x=100, y=140)
        player.vel_y = 10  # Falling fast
        player.hitbox.bottom = 145
        platform = pygame.Rect(80, 145, 100, 30)

        on_ground = collision.check_platform_collision_player(player, [platform])

        assert on_ground == True
        assert player.vel_y == 0  # Velocity stopped

    def test_player_hitting_platform_from_below(self):
        """Test player jumping into platform from below"""
        player = MockPlayer(x=100, y=180)
        player.vel_y = -10  # Moving up
        # Position player mostly below platform, with minimal top overlap
        player.hitbox.top = 173  # Just overlapping with platform bottom (175)
        player.hitbox.bottom = 218  # 173 + 45 (height)
        platform = pygame.Rect(80, 145, 100, 30)  # Platform bottom is at 175

        collision.check_platform_collision_player(player, [platform])

        # Player should stop moving up
        assert player.vel_y == 0

    def test_multiple_platforms(self):
        """Test collision with multiple platforms"""
        player = MockPlayer(x=100, y=100)
        player.vel_y = 5
        platforms = [
            pygame.Rect(300, 145, 100, 30),  # Far away
            pygame.Rect(80, 145, 100, 30),   # Under player
            pygame.Rect(400, 145, 100, 30),  # Also far away
        ]

        on_ground = collision.check_platform_collision_player(player, platforms)

        assert on_ground == True


class TestPlatformCollisionEnemy:
    """Tests for enemy-platform collision detection"""

    def test_enemy_on_platform(self):
        """Test enemy standing on a platform"""
        enemy = MockEnemy(x=100, y=100)
        enemy.vel_y = 3
        platform = pygame.Rect(75, 150, 100, 30)

        on_ground = collision.check_platform_collision_enemy(enemy, [platform])

        assert on_ground == True
        assert enemy.vel_y == 0

    def test_enemy_falling(self):
        """Test enemy falling with no platform"""
        enemy = MockEnemy(x=100, y=100)
        enemy.vel_y = 3
        platforms = []

        on_ground = collision.check_platform_collision_enemy(enemy, platforms)

        assert on_ground == False
        assert enemy.vel_y == 3

    def test_enemy_rect_positioning_after_collision(self):
        """
        Test that enemy rect is correctly positioned after platform collision.
        Regression test for bug where enemies fell through platforms due to
        incorrect rect.bottom calculation.
        """
        enemy = MockEnemy(x=100, y=100)
        enemy.vel_y = 5  # Falling

        # Set up enemy above platform
        platform = pygame.Rect(80, 200, 100, 30)
        enemy.hitbox.bottom = 198  # Just above platform
        enemy.rect.bottom = enemy.hitbox.bottom  # Midbottom alignment

        # Store initial alignment (rect and hitbox should share same bottom)
        initial_alignment = enemy.rect.bottom == enemy.hitbox.bottom

        # Collision occurs
        on_ground = collision.check_platform_collision_enemy(enemy, [platform])

        # Verify collision was detected
        assert on_ground == True

        # CRITICAL: Verify rect and hitbox maintain same bottom position
        # This prevents enemies from falling through platforms
        assert enemy.rect.bottom == enemy.hitbox.bottom, \
            f"Enemy rect.bottom ({enemy.rect.bottom}) != hitbox.bottom ({enemy.hitbox.bottom}). " \
            f"This causes enemies to fall through platforms!"

        # Verify enemy is placed ON the platform (not below it)
        assert enemy.hitbox.bottom == platform.top, \
            f"Enemy hitbox.bottom ({enemy.hitbox.bottom}) should equal platform.top ({platform.top})"

        # Verify velocity was stopped
        assert enemy.vel_y == 0


class TestHazardCollision:
    """Tests for hazard collision detection"""

    def test_player_hits_hazard(self):
        """Test player colliding with hazard"""
        player = MockPlayer(x=100, y=100)
        hazard = pygame.Rect(100, 100, 50, 30)

        hit = collision.check_hazard_collision(player, [hazard])

        assert hit == True

    def test_player_misses_hazard(self):
        """Test player not touching hazard"""
        player = MockPlayer(x=100, y=100)
        hazard = pygame.Rect(200, 100, 50, 30)

        hit = collision.check_hazard_collision(player, [hazard])

        assert hit == False

    def test_invincibility_ignores_hazard(self):
        """Test that invincibility prevents hazard damage"""
        player = MockPlayer(x=100, y=100)
        hazard = pygame.Rect(100, 100, 50, 30)

        hit = collision.check_hazard_collision(player, [hazard], debug_invincibility=True)

        assert hit == False


class TestPitDeath:
    """Tests for pit death detection"""

    def test_player_falls_in_pit(self):
        """Test player falling below screen"""
        player = MockPlayer(x=100, y=600)

        fell = collision.check_pit_death(player, screen_height=600)

        assert fell == True

    def test_player_safe_on_screen(self):
        """Test player safely on screen"""
        player = MockPlayer(x=100, y=300)

        fell = collision.check_pit_death(player, screen_height=600)

        assert fell == False

    def test_invincibility_prevents_pit_death(self):
        """Test that invincibility prevents pit death"""
        player = MockPlayer(x=100, y=700)

        fell = collision.check_pit_death(player, screen_height=600, debug_invincibility=True)

        assert fell == False


class TestPlayerEnemyCollision:
    """Tests for player-enemy collision interactions"""

    def test_player_stomps_enemy(self):
        """Test player jumping on enemy's head"""
        player = MockPlayer(x=100, y=90)
        player.vel_y = 10  # Falling
        player.hitbox.bottom = 105  # Slightly overlapping with enemy top (100)

        enemy = MockEnemy(x=95, y=100)
        enemy.hitbox.top = 100
        enemy.vulnerable_to = {'stomp': True, 'spin_attack': True, 'roll': True}
        enemy.health = 2

        def take_damage(amount):
            enemy.health -= amount
        enemy.take_damage = take_damage

        audio = MockAudioManager()

        result = collision.check_player_enemy_collision(player, enemy, audio, enable_sound=True)

        assert result == 'stomp'
        assert player.vel_y == -10  # Player bounces
        assert enemy.health == 1
        assert 'land_enemy' in audio.sounds_played or 'land_slime' in audio.sounds_played

    def test_player_touches_enemy_from_side(self):
        """Test player touching enemy from the side"""
        player = MockPlayer(x=100, y=100)
        player.health = 3

        enemy = MockEnemy(x=120, y=100)  # Closer so they actually collide
        enemy.vulnerable_to = {'stomp': True, 'spin_attack': True, 'roll': True}

        audio = MockAudioManager()

        result = collision.check_player_enemy_collision(player, enemy, audio, enable_sound=True)

        assert result == 'hit_player'
        assert player.health == 2
        assert 'bump' in audio.sounds_played

    def test_spin_attack_hits_enemy(self):
        """Test player's spin attack hitting enemy"""
        player = MockPlayer(x=100, y=100)
        player.is_spinning = True

        enemy = MockEnemy(x=110, y=100)
        enemy.vulnerable_to = {'stomp': True, 'spin_attack': True, 'roll': True}
        enemy.health = 2

        def take_damage(amount):
            enemy.health -= amount
        enemy.take_damage = take_damage

        audio = MockAudioManager()

        result = collision.check_player_enemy_collision(player, enemy, audio, enable_sound=True)

        assert result == 'spin'
        assert enemy.health == 1
        assert 'bump' in audio.sounds_played

    def test_roll_attack_hits_enemy(self):
        """Test player rolling into enemy"""
        player = MockPlayer(x=100, y=100)
        player.is_rolling = True
        player.is_spinning = False  # Make sure not spinning

        enemy = MockEnemy(x=110, y=100)
        enemy.vulnerable_to = {'stomp': True, 'spin_attack': True, 'roll': True}
        enemy.health = 2

        def take_damage(amount):
            enemy.health -= amount
        enemy.take_damage = take_damage

        audio = MockAudioManager()

        result = collision.check_player_enemy_collision(player, enemy, audio, enable_sound=True)

        assert result == 'roll'
        assert enemy.health == 1

    def test_player_stomps_enemy_poking_through_platform(self):
        """
        Test player stomping enemy that is poking through a platform.
        Regression test for bug where player takes damage instead of stomping
        when enemy sprite extends through platform.
        """
        player = MockPlayer(x=100, y=90)
        player.vel_y = 8  # Falling downward
        # Player's center is at y=90+22.5=112.5
        player.hitbox.centery = 112

        # Enemy is below but poking through platform
        enemy = MockEnemy(x=95, y=130)
        # Enemy's center is at y=130+25=155
        enemy.hitbox.centery = 155
        enemy.vulnerable_to = {'stomp': True, 'spin_attack': True, 'roll': True}
        enemy.health = 2

        # Make hitboxes collide (player landing on enemy from above)
        enemy.hitbox.top = 105
        player.hitbox.bottom = 110

        def take_damage(amount):
            enemy.health -= amount
        enemy.take_damage = take_damage

        audio = MockAudioManager()

        result = collision.check_player_enemy_collision(player, enemy, audio, enable_sound=True)

        # CRITICAL: Should be stomp, NOT hit_player
        assert result == 'stomp', \
            f"Player falling from above should stomp enemy, but got '{result}'. " \
            f"Player center: {player.hitbox.centery}, Enemy center: {enemy.hitbox.centery}"

        # Verify stomp effects
        assert player.vel_y == -10, "Player should bounce after stomp"
        assert enemy.health == 1, "Enemy should take damage"
        assert ('land_enemy' in audio.sounds_played or 'land_slime' in audio.sounds_played), \
            "Stomp sound should play"


class TestProjectileCollision:
    """Tests for projectile collision detection"""

    def test_projectile_hits_player(self):
        """Test projectile hitting player"""
        player = MockPlayer(x=100, y=100)
        player.health = 3

        def take_damage(amount, knockback_direction=0):
            player.health -= amount
        player.take_damage = take_damage

        projectile = MockProjectile(x=100, y=100)
        audio = MockAudioManager()

        hit = collision.check_projectile_player_collision(player, projectile, audio, enable_sound=True)

        assert hit == True
        assert player.health == 2
        assert 'bump' in audio.sounds_played

    def test_projectile_misses_player(self):
        """Test projectile missing player"""
        player = MockPlayer(x=100, y=100)
        projectile = MockProjectile(x=300, y=100)
        audio = MockAudioManager()

        hit = collision.check_projectile_player_collision(player, projectile, audio, enable_sound=False)

        assert hit == False


class TestCoinCollection:
    """Tests for coin collection"""

    def test_player_collects_coin(self):
        """Test player touching coin"""
        player = MockPlayer(x=100, y=100)
        coin = MockCoin(x=105, y=105)

        collected = collision.check_coin_collection(player, coin)

        assert collected == True

    def test_player_misses_coin(self):
        """Test player not touching coin"""
        player = MockPlayer(x=100, y=100)
        coin = MockCoin(x=300, y=300)

        collected = collision.check_coin_collection(player, coin)

        assert collected == False


class TestGravity:
    """Tests for gravity application"""

    def test_gravity_applied(self):
        """Test gravity increases velocity"""
        entity = MockPlayer(x=100, y=100)
        entity.vel_y = 0

        collision.apply_gravity(entity, gravity=0.6)

        assert entity.vel_y == 0.6
        assert entity.rect.y == pytest.approx(100.6, rel=0.1)  # Allow floating point tolerance

    def test_gravity_accumulates(self):
        """Test gravity accumulates over time"""
        entity = MockPlayer(x=100, y=100)
        entity.vel_y = 5

        collision.apply_gravity(entity, gravity=0.6)

        assert entity.vel_y == 5.6


class TestLevelBoundary:
    """Tests for level boundary enforcement"""

    def test_left_boundary(self):
        """Test player can't go past left edge"""
        player = MockPlayer(x=-10, y=100)

        collision.check_level_boundary(player, level_width=1000)

        assert player.rect.left == 0

    def test_right_boundary(self):
        """Test player can't go past right edge"""
        player = MockPlayer(x=1010, y=100)
        player.rect.width = 40

        collision.check_level_boundary(player, level_width=1000)

        assert player.rect.right == 1000

    def test_within_boundaries(self):
        """Test player within boundaries is not affected"""
        player = MockPlayer(x=500, y=100)
        original_x = player.rect.x

        collision.check_level_boundary(player, level_width=1000)

        assert player.rect.x == original_x


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
