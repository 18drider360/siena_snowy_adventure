"""
Level Data Structure
Defines the dataclass for level data to replace the 14-item tuple
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import pygame
from src.core.game_logging import get_logger

logger = get_logger(__name__)


@dataclass
class LevelData:
    """
    Contains all data needed to run a game level

    This replaces the previous 14-item tuple return from load_level()
    with a more maintainable and self-documenting structure.
    """

    # Visual
    bg_color: Tuple[int, int, int]
    world_name: str
    background_layers: List

    # Geometry
    platforms: List[pygame.Rect]
    hazards: List[pygame.Rect]
    level_width: int

    # Entities
    player: any  # Siena instance
    enemies: pygame.sprite.Group
    projectiles: pygame.sprite.Group
    coins: pygame.sprite.Group

    # Special platforms
    moving_platforms: List = field(default_factory=list)
    disappearing_platforms: List = field(default_factory=list)
    appearing_platforms: List = field(default_factory=list)

    # Level goal
    goal_npc: Optional[any] = None  # NPC instance

    def __post_init__(self):
        """Validate level data after initialization"""
        # Ensure required fields are not None
        if self.bg_color is None:
            raise ValueError("bg_color cannot be None")
        if self.platforms is None:
            raise ValueError("platforms cannot be None")
        if self.player is None:
            raise ValueError("player cannot be None")

        logger.debug(f"LevelData created: {self.world_name}, "
                    f"{len(self.platforms)} platforms, "
                    f"{len(self.enemies)} enemies, "
                    f"{len(self.coins)} coins")

    @property
    def static_platforms(self):
        """Get list of static platforms (excludes dynamic platforms)"""
        return self.platforms.copy()

    @property
    def all_platforms(self):
        """
        Get list of ALL platforms including dynamic ones

        This rebuilds the platform list each time it's called to include
        current positions of moving platforms and visibility of disappearing platforms.
        """
        platforms = self.static_platforms

        # Add moving platforms
        for moving_platform in self.moving_platforms:
            platforms.append(moving_platform.rect)

        # Add disappearing platforms (if visible)
        for disappearing_platform in self.disappearing_platforms:
            if not disappearing_platform.disappeared:
                platforms.append(disappearing_platform.rect)

        # Add appearing platforms (if solid)
        for appearing_platform in self.appearing_platforms:
            if appearing_platform.is_solid():
                platforms.append(appearing_platform.rect)

        return platforms

    def update_dynamic_platforms(self, player_hitbox):
        """
        Update all dynamic platforms

        Args:
            player_hitbox: Player's hitbox rect for collision detection
        """
        # Update moving platforms
        for moving_platform in self.moving_platforms:
            moving_platform.update()

        # Update disappearing platforms
        for disappearing_platform in self.disappearing_platforms:
            # Check if player is standing on this platform
            on_platform = (
                not disappearing_platform.disappeared and
                player_hitbox.bottom <= disappearing_platform.rect.top + 10 and
                player_hitbox.bottom >= disappearing_platform.rect.top - 5 and
                player_hitbox.right > disappearing_platform.rect.left and
                player_hitbox.left < disappearing_platform.rect.right
            )
            disappearing_platform.update(on_platform)

        # Update appearing platforms
        for appearing_platform in self.appearing_platforms:
            appearing_platform.update()

    def __repr__(self):
        """String representation for debugging"""
        return (f"LevelData(world='{self.world_name}', "
                f"platforms={len(self.platforms)}, "
                f"enemies={len(self.enemies)}, "
                f"coins={len(self.coins)})")
