import pygame

class HealthDisplay:
    """Displays Siena's health as hearts in the top-left corner"""
    
    def __init__(self):
        # Load heart sprites from the sprite sheet
        try:
            sheet = pygame.image.load("assets/images/ui/Health.png").convert_alpha()
            sheet_width, sheet_height = sheet.get_size()
            heart_width = sheet_width // 3  # 3 hearts in the sheet
            
            # Extract each heart (full, half, empty)
            self.heart_full = pygame.Surface((heart_width, sheet_height), pygame.SRCALPHA)
            self.heart_full.blit(sheet, (0, 0), (0, 0, heart_width, sheet_height))
            
            self.heart_half = pygame.Surface((heart_width, sheet_height), pygame.SRCALPHA)
            self.heart_half.blit(sheet, (0, 0), (heart_width, 0, heart_width, sheet_height))
            
            self.heart_empty = pygame.Surface((heart_width, sheet_height), pygame.SRCALPHA)
            self.heart_empty.blit(sheet, (0, 0), (heart_width * 2, 0, heart_width, sheet_height))
            
            # Scale hearts to a reasonable size (adjust as needed)
            scale_size = (40, 40)
            self.heart_full = pygame.transform.scale(self.heart_full, scale_size)
            self.heart_half = pygame.transform.scale(self.heart_half, scale_size)
            self.heart_empty = pygame.transform.scale(self.heart_empty, scale_size)
            
        except Exception as e:
            print(f"Error loading health UI: {e}")
            # Fallback: create simple colored squares
            self.heart_full = self.create_fallback_heart((255, 0, 0))
            self.heart_half = self.create_fallback_heart((255, 100, 100))
            self.heart_empty = self.create_fallback_heart((100, 100, 100))
        
        # Position settings
        self.start_x = 20  # Left margin
        self.start_y = 20  # Top margin
        self.spacing = 50  # Space between hearts
    
    def create_fallback_heart(self, color):
        """Create a simple fallback heart if images fail to load"""
        surf = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.rect(surf, color, (0, 0, 40, 40))
        return surf
    
    def draw(self, screen, current_health, max_health=6):
        """
        Draw hearts based on current health
        
        Args:
            screen: pygame surface to draw on
            current_health: current health value (0-6)
            max_health: maximum health value (default 6 = 3 full hearts)
        """
        # Calculate how many full hearts, half hearts, and empty hearts
        full_hearts = current_health // 2
        half_heart = current_health % 2
        empty_hearts = (max_health // 2) - full_hearts - half_heart
        
        x = self.start_x
        y = self.start_y
        
        # Draw full hearts
        for i in range(full_hearts):
            screen.blit(self.heart_full, (x, y))
            x += self.spacing
        
        # Draw half heart if needed
        if half_heart:
            screen.blit(self.heart_half, (x, y))
            x += self.spacing
        
        # Draw empty hearts
        for i in range(empty_hearts):
            screen.blit(self.heart_empty, (x, y))
            x += self.spacing