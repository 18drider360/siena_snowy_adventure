import pygame

class LevelGoalNPC(pygame.sprite.Sprite):
    """
    NPC that appears at the end of levels to congratulate the player
    Similar to the castle/flagpole in Mario games
    """
    
    def __init__(self, x, y):
        super().__init__()
        
        # Create a simple visual representation
        # You can replace this with actual sprite art later
        self.image = pygame.Surface((40, 60), pygame.SRCALPHA)
        
        # Draw a simple penguin NPC (placeholder)
        # Body
        pygame.draw.ellipse(self.image, (50, 50, 50), (5, 15, 30, 40))  # Dark gray body
        # Belly
        pygame.draw.ellipse(self.image, (240, 240, 240), (10, 20, 20, 30))  # White belly
        # Head
        pygame.draw.circle(self.image, (50, 50, 50), (20, 15), 12)  # Head
        # Eyes
        pygame.draw.circle(self.image, (255, 255, 255), (16, 12), 3)  # Left eye
        pygame.draw.circle(self.image, (255, 255, 255), (24, 12), 3)  # Right eye
        pygame.draw.circle(self.image, (0, 0, 0), (16, 12), 1)  # Left pupil
        pygame.draw.circle(self.image, (0, 0, 0), (24, 12), 1)  # Right pupil
        # Beak
        pygame.draw.polygon(self.image, (255, 165, 0), [(20, 16), (18, 20), (22, 20)])  # Orange beak
        # Feet
        pygame.draw.ellipse(self.image, (255, 165, 0), (8, 52, 10, 6))  # Left foot
        pygame.draw.ellipse(self.image, (255, 165, 0), (22, 52, 10, 6))  # Right foot
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Collision box for detecting when player reaches NPC
        self.trigger_zone = pygame.Rect(x - 50, y - 20, 140, 80)
        
        # Animation
        self.bob_timer = 0
        self.bob_offset = 0
        self.original_y = y
    
    def update(self):
        """Simple bobbing animation"""
        self.bob_timer += 0.1
        self.bob_offset = int(pygame.math.Vector2(0, 3).rotate(self.bob_timer * 50).y)
        self.rect.y = self.original_y + self.bob_offset
        self.trigger_zone.y = self.rect.y - 20
    
    def draw_trigger_zone(self, screen, camera_x):
        """Debug: Draw the trigger zone"""
        debug_zone = self.trigger_zone.copy()
        debug_zone.x -= camera_x
        pygame.draw.rect(screen, (0, 255, 0), debug_zone, 2)