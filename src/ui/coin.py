import pygame

class Coin(pygame.sprite.Sprite):
    """Collectible coin that animates and can be picked up by the player"""
    
    def __init__(self, x, y):
        super().__init__()
        
        # Load coin sprite sheet
        try:
            self.frames = self.load_sprite_sheet(
                "assets/images/objects/coin.png",
                frame_count=13,
                target_size=(40, 40)  # Adjust size as needed
            )
        except Exception as e:
            print(f"Error loading coin sprite: {e}")
            # Fallback to a simple yellow circle
            self.frames = [self.create_fallback_sprite()]
        
        # Animation setup
        self.current_frame = 0
        self.frame_counter = 0.0
        self.animation_speed = 0.15  # Adjust for animation speed
        
        # Initial image and rect
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))
        
        # Create a slightly smaller hitbox for more forgiving collection
        self.hitbox = pygame.Rect(0, 0, 30, 30)
        self.hitbox.center = self.rect.center
        
        # Coin properties
        self.collected = False
        self.value = 1  # How many coins this is worth
    
    def load_sprite_sheet(self, path, frame_count, target_size=(40, 40)):
        """Load and split a horizontal sprite sheet into frames"""
        sheet = pygame.image.load(path).convert_alpha()
        sheet_width, sheet_height = sheet.get_size()
        frame_width = sheet_width // frame_count
        
        frames = []
        for i in range(frame_count):
            # Extract frame from sheet
            frame = pygame.Surface((frame_width, sheet_height), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), (i * frame_width, 0, frame_width, sheet_height))
            
            # Scale to target size
            scaled = pygame.transform.scale(frame, target_size)
            frames.append(scaled)
        
        return frames
    
    def create_fallback_sprite(self):
        """Create a simple fallback coin sprite"""
        surf = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255, 215, 0), (20, 20), 18)  # Gold color
        pygame.draw.circle(surf, (218, 165, 32), (20, 20), 18, 3)  # Gold border
        return surf
    
    def update(self):
        """Update coin animation"""
        if self.collected:
            return
        
        # Animate through frames
        self.frame_counter += self.animation_speed
        if self.frame_counter >= 1.0:
            self.frame_counter = 0.0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
    
    def collect(self):
        """Mark coin as collected and remove it"""
        self.collected = True
        self.kill()  # Remove from sprite group
    
    def draw_hitbox(self, screen, camera_x):
        """Debug function to draw hitbox"""
        debug_hitbox = self.hitbox.copy()
        debug_hitbox.x -= camera_x
        pygame.draw.rect(screen, (255, 255, 0), debug_hitbox, 2)