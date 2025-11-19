import pygame

class RollStaminaDisplay:
    """Displays the player's roll stamina as a bar above their head"""
    
    def __init__(self):
        self.bar_width = 80
        self.bar_height = 8
        self.offset_y = -40  # How far above player to show the bar
        
        # Colors
        self.bg_color = (40, 40, 40)  # Dark gray background
        self.border_color = (255, 255, 255)  # White border
        self.stamina_color_full = (100, 200, 255)  # Light blue when full
        self.stamina_color_low = (255, 100, 100)  # Red when low
        self.stamina_color_empty = (150, 50, 50)  # Dark red when empty
        
        # Visibility settings
        self.fade_timer = 0
        self.fade_duration = 120  # Show for 2 seconds after stamina changes
        self.alpha = 0  # Current transparency (0-255)
        self.always_show_when_rolling = True  # Always visible while rolling
        
    def draw(self, screen, player, camera_x):
        """Draw the stamina bar above the player
        
        Args:
            screen: Pygame screen surface
            player: Player object with stamina attributes
            camera_x: Camera x offset for scrolling
        """
        # Only show if player is rolling, stamina not full, or fade timer active
        show_bar = (
            player.is_rolling or 
            player.roll_stamina < player.roll_stamina_max or 
            self.fade_timer > 0
        )
        
        if not show_bar:
            self.alpha = 0
            return
        
        # Update fade timer
        if player.is_rolling or player.roll_stamina < player.roll_stamina_max:
            self.fade_timer = self.fade_duration
            self.alpha = 255
        else:
            if self.fade_timer > 0:
                self.fade_timer -= 1
                # Fade out in last 30 frames
                if self.fade_timer < 30:
                    self.alpha = int((self.fade_timer / 30) * 255)
            else:
                self.alpha = 0
        
        if self.alpha == 0:
            return
        
        # Calculate bar position (centered above player, camera-adjusted)
        bar_x = player.rect.centerx - camera_x - (self.bar_width // 2)
        bar_y = player.rect.top + self.offset_y
        
        # Calculate stamina percentage
        stamina_percent = player.roll_stamina / player.roll_stamina_max
        fill_width = int(self.bar_width * stamina_percent)
        
        # Choose color based on stamina level
        if stamina_percent > 0.5:
            stamina_color = self.stamina_color_full
        elif stamina_percent > 0.2:
            # Blend between full and low color
            t = (stamina_percent - 0.2) / 0.3
            stamina_color = (
                int(self.stamina_color_low[0] + (self.stamina_color_full[0] - self.stamina_color_low[0]) * t),
                int(self.stamina_color_low[1] + (self.stamina_color_full[1] - self.stamina_color_low[1]) * t),
                int(self.stamina_color_low[2] + (self.stamina_color_full[2] - self.stamina_color_low[2]) * t)
            )
        else:
            stamina_color = self.stamina_color_low
        
        # Create surfaces with alpha support
        bar_surface = pygame.Surface((self.bar_width + 4, self.bar_height + 4), pygame.SRCALPHA)
        
        # Draw background
        pygame.draw.rect(bar_surface, (*self.bg_color, self.alpha), 
                        (2, 2, self.bar_width, self.bar_height))
        
        # Draw stamina fill
        if fill_width > 0:
            pygame.draw.rect(bar_surface, (*stamina_color, self.alpha), 
                            (2, 2, fill_width, self.bar_height))
        
        # Draw border
        pygame.draw.rect(bar_surface, (*self.border_color, self.alpha), 
                        (2, 2, self.bar_width, self.bar_height), 1)
        
        # Blit to screen
        screen.blit(bar_surface, (bar_x - 2, bar_y - 2))
        
        # Draw "EMPTY" text if stamina depleted
        if player.roll_stamina <= 0:
            font = pygame.font.Font(None, 16)
            text = font.render("EMPTY", True, (255, 100, 100))
            text.set_alpha(self.alpha)
            text_rect = text.get_rect(center=(bar_x + self.bar_width // 2, bar_y - 12))
            screen.blit(text, text_rect)