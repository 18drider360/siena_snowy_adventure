"""
Game Constants (Compatibility Layer)

This file now acts as a compatibility layer that reads from config.yaml.
This allows existing code to continue using constants while we migrate to config_loader.

DEPRECATED: New code should use config_loader directly.
"""

from src.core.config_loader import get_config
from src.core.game_logging import get_logger

logger = get_logger(__name__)

# Load configuration
_config = get_config()

# === PLAYER CONSTANTS ===

# Hitbox sizes (width, height) - From config
PLAYER_HITBOX_NORMAL = tuple(_config.get('player.hitbox_normal', [40, 45]))
PLAYER_HITBOX_CROUCH = tuple(_config.get('player.hitbox_crouch', [55, 25]))
PLAYER_HITBOX_ROLL = tuple(_config.get('player.hitbox_roll', [35, 35]))

# Hitbox offsets (how far up the hitbox is from rect bottom)
# These are rendering-specific and stay as constants
PLAYER_HITBOX_OFFSET_NORMAL = 90
PLAYER_HITBOX_OFFSET_CROUCH = 70
PLAYER_HITBOX_OFFSET_ROLL = 72

# Movement - From config
PLAYER_SPEED = _config.get('player.speed', 4)
PLAYER_GRAVITY = _config.get('player.gravity', 0.6)
PLAYER_JUMP_STRENGTH = _config.get('player.jump_strength', -13)
PLAYER_DOUBLE_JUMP_MULTIPLIER = _config.get('player.double_jump_multiplier', 0.9)
PLAYER_VARIABLE_JUMP_DAMPENING = _config.get('player.variable_jump_dampening', 0.4)

# Roll mechanics - From config
PLAYER_ROLL_SPEED_INITIAL = _config.get('player.roll.speed_initial', 7)
PLAYER_ROLL_SPEED_MAX = _config.get('player.roll.speed_max', 12)
PLAYER_ROLL_SPEED_ACCELERATION = _config.get('player.roll.acceleration', 0.15)
PLAYER_ROLL_STAMINA_MAX = _config.get('player.roll.stamina_max', 120)
PLAYER_ROLL_STAMINA_RECHARGE_RATE = _config.get('player.roll.stamina_recharge_rate', 0.4)
PLAYER_ROLL_STAMINA_RECHARGE_DELAY = _config.get('player.roll.stamina_recharge_delay', 30)
PLAYER_ROLL_COOLDOWN = _config.get('player.roll.cooldown', 0)

# Spin attack - From config
PLAYER_SPIN_CHARGES_MAX = _config.get('player.spin.charges_max', 3)
PLAYER_SPIN_CHARGE_COOLDOWN = _config.get('player.spin.charge_cooldown', 180)
PLAYER_SPIN_SPEED = _config.get('player.spin.speed', 10)
PLAYER_SPIN_DURATION_FRAMES = _config.get('player.spin.duration_frames', 7)
PLAYER_SPIN_ANIMATION_FPS = _config.get('player.spin.animation_fps', 20)

# Health and damage - From config
PLAYER_MAX_HEALTH = _config.get('player.max_health', 6)
PLAYER_INVINCIBLE_DURATION = _config.get('player.invincible_duration', 35)
PLAYER_HURT_DURATION = _config.get('player.hurt_duration', 30)
PLAYER_KNOCKBACK_STRENGTH = _config.get('player.knockback_strength', 20)
PLAYER_KNOCKBACK_Y_BOOST = _config.get('player.knockback_y_boost', -5)

# Animation - These are frame-specific constants, keep as-is
PLAYER_ANIMATION_SPEED_WALK = 0.15
PLAYER_ANIMATION_SPEED_IDLE = 0.1
PLAYER_ANIMATION_SPEED_ROLL = 0.25
PLAYER_ANIMATION_SPEED_SPIN = 0.3
PLAYER_ANIMATION_SPEED_FLAP = 0.3
PLAYER_ANIMATION_SPEED_HURT = 0.2

# Sprite heights - Rendering constants
PLAYER_SPRITE_HEIGHT_NORMAL = 180
PLAYER_SPRITE_HEIGHT_CROUCH = 145
PLAYER_SPRITE_HEIGHT_ROLL = 145


# === ENEMY CONSTANTS ===

# Snowy (Snowman) enemy - From config
SNOWY_HEALTH = _config.get('enemies.snowy.health', 2)
SNOWY_SPEED = _config.get('enemies.snowy.speed', 0.6)
SNOWY_CHASE_SPEED = _config.get('enemies.snowy.chase_speed', 1.0)
SNOWY_TRACKING_RANGE = _config.get('enemies.snowy.tracking_range', 500)
SNOWY_ATTACK_RANGE = _config.get('enemies.snowy.attack_range', 90)
SNOWY_LOSE_INTEREST_RANGE = _config.get('enemies.snowy.lose_interest_range', 800)
SNOWY_PUNCH_DAMAGE = _config.get('enemies.snowy.punch_damage', 2)
SNOWY_ATTACK_COOLDOWN_MIN = _config.get('enemies.snowy.attack_cooldown_min', 80)
SNOWY_ATTACK_COOLDOWN_MAX = _config.get('enemies.snowy.attack_cooldown_max', 140)
SNOWY_ATTACK_PAUSE_DURATION = _config.get('enemies.snowy.attack_pause_duration', 35)

# Generic enemy defaults - From config
ENEMY_GRAVITY = _config.get('enemies.global.gravity', 0.6)
ENEMY_INVINCIBLE_DURATION = _config.get('enemies.global.invincible_duration', 60)
ENEMY_HURT_FLASH_DURATION = _config.get('enemies.global.hurt_flash_duration', 20)


# === COLLISION CONSTANTS ===

# Collision tolerances - From config
PLATFORM_COLLISION_TOLERANCE = _config.get('collision.platform_tolerance', 5)
STOMP_DETECTION_TOLERANCE = _config.get('collision.stomp_detection_tolerance', 15)

# Bounce - From config
STOMP_BOUNCE_VELOCITY = _config.get('collision.stomp_bounce_velocity', -10)


# === GAME MECHANICS ===

# Camera - From config
CAMERA_OFFSET_X = _config.get('level.camera_offset_x', 300)

# Death and respawn - From config
DEATH_ANIMATION_DELAY = _config.get('death.animation_delay', 90)
DEATH_FADE_SPEED = _config.get('death.fade_speed', 5)
PIT_DEATH_Y_THRESHOLD = _config.get('death.pit_y_threshold', 550)

# Projectile sounds - From config
PROJECTILE_SOUND_RANGE = _config.get('projectiles.sound_range', 400)


# === LEVEL CONSTANTS ===

# Level dimensions - From config
DEFAULT_LEVEL_HEIGHT = _config.get('level.default_height', 600)
DEFAULT_GROUND_Y = _config.get('level.default_ground_y', 570)
DEFAULT_GROUND_HEIGHT = _config.get('level.default_ground_height', 30)


# === AUDIO CONSTANTS ===

# Volume levels (0.0 to 1.0) - Hardcoded for now, could move to config
VOLUME_MUSIC_DEFAULT = 0.6
VOLUME_DEATH = 0.6
VOLUME_STAGE_CLEAR = 0.7
VOLUME_JUMP = 0.4
VOLUME_DOUBLE_JUMP = 0.4
VOLUME_COIN = 0.2
VOLUME_BUMP = 0.2
VOLUME_LAND_ENEMY = 0.3
VOLUME_LAND_SLIME = 0.3
VOLUME_ENEMY_PROJECTILE = 0.2
VOLUME_SPIN_ATTACK = 0.3


# === UI CONSTANTS ===

# Font sizes - Rendering constants
FONT_SIZE_TITLE = 48
FONT_SIZE_LARGE = 32
FONT_SIZE_MEDIUM = 24
FONT_SIZE_SMALL = 16
FONT_SIZE_TINY = 12

# HUD positioning - Rendering constants
HUD_MARGIN_TOP = 10
HUD_MARGIN_LEFT = 10
HUD_SPACING = 35


# === RENDERING CONSTANTS ===

# Platform brick dimensions - Rendering constants
BRICK_WIDTH = 32
BRICK_HEIGHT = 16

# Colors (R, G, B) - Rendering constants
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GOLD = (255, 215, 0)
COLOR_RED = (255, 50, 50)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 100, 255)

# Snowy/icy brick colors
COLOR_BRICK_ICY = (200, 220, 240)
COLOR_BRICK_HIGHLIGHT = (240, 250, 255)
COLOR_BRICK_SHADOW = (120, 140, 170)
COLOR_BRICK_OUTLINE = (100, 120, 150)

# Dark icy brick colors
COLOR_DARK_ICY_BRICK = (50, 100, 150)
COLOR_DARK_ICY_HIGHLIGHT = (70, 120, 180)
COLOR_DARK_ICY_SHADOW = (30, 70, 110)
COLOR_DARK_ICY_OUTLINE = (20, 50, 90)

# Snowy ground colors
COLOR_SNOWY_BRICK = (255, 255, 255)
COLOR_SNOWY_HIGHLIGHT = (245, 250, 255)
COLOR_SNOWY_SHADOW = (220, 230, 240)
COLOR_SNOWY_OUTLINE = (200, 210, 220)


# Log that constants have been loaded
logger.debug(f"Constants loaded from config.yaml: PLAYER_SPEED={PLAYER_SPEED}, FPS={_config.fps}")
