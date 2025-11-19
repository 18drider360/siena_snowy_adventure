import pygame

class EnemyHealthDisplay:
    """Displays health hearts above enemies"""
    def __init__(self):
        try:
            # Load the heart sprite sheet
            sheet = pygame.image.load("assets/images/ui/Health.png").convert_alpha()
            sheet_width, sheet_height = sheet.get_size()
            heart_width = sheet_width // 3  # 3 hearts in the sheet (full, half, empty)
            
            # Extract each heart frame
            self.heart_full = pygame.Surface((heart_width, sheet_height), pygame.SRCALPHA)
            self.heart_full.blit(sheet, (0, 0), (0, 0, heart_width, sheet_height))
            
            self.heart_half = pygame.Surface((heart_width, sheet_height), pygame.SRCALPHA)
            self.heart_half.blit(sheet, (0, 0), (heart_width, 0, heart_width, sheet_height))
            
            self.heart_empty = pygame.Surface((heart_width, sheet_height), pygame.SRCALPHA)
            self.heart_empty.blit(sheet, (0, 0), (heart_width * 2, 0, heart_width, sheet_height))
            
            # Scale hearts down for enemies
            scale_size = (20, 20)  # Smaller than player hearts (which are 40x40)
            self.heart_full = pygame.transform.scale(self.heart_full, scale_size)
            self.heart_empty = pygame.transform.scale(self.heart_empty, scale_size)
            
        except Exception as e:
            print(f"Error loading enemy health hearts: {e}")
            # Fallback: create simple colored squares
            self.heart_full = pygame.Surface((20, 20))
            self.heart_full.fill((255, 0, 0))  # Red
            self.heart_empty = pygame.Surface((20, 20))
            self.heart_empty.fill((100, 100, 100))  # Gray
    
    def draw(self, screen, enemy, camera_x):
        """Draw health hearts above a specific enemy
        
        Args:
            screen: pygame screen to draw on
            enemy: enemy sprite with health and max_health attributes
            camera_x: camera offset for scrolling
        """
        if enemy.is_dead:
            return  # Don't show health for dead enemies
        
        # Get enemy's max health (or default to current health if no max_health)
        max_health = getattr(enemy, 'max_health', enemy.health)
        current_health = enemy.health
        
        # Calculate position above enemy (centered)
        heart_size = 20
        heart_spacing = 4
        total_width = (max_health * heart_size) + ((max_health - 1) * heart_spacing)
        
        # Position above enemy's hitbox
        start_x = int(enemy.hitbox.centerx - (total_width / 2.0) - camera_x)
        start_y = int(enemy.hitbox.top - 28)
        
        # Draw hearts
        for i in range(max_health):
            x = int(start_x + (i * (heart_size + heart_spacing)))
            y = start_y
            
            if i < current_health:
                # Full heart
                screen.blit(self.heart_full, (x, y))
            else:
                # Empty heart
                screen.blit(self.heart_empty, (x, y))