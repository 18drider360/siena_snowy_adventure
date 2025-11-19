import pygame
import math

class SpinChargeDisplay:
    """Displays the player's spin attack charges as glowing dots above their head"""
    
    def __init__(self):
        self.dot_radius = 6
        self.dot_spacing = 18  # Space between dot centers
        self.offset_y = -55  # How far above player to show the dots
        
        # Colors
        self.dot_color_available = (100, 200, 255)  # Light blue when available
        self.dot_color_empty = (60, 60, 70)  # Gray when empty/recharging
        self.glow_color = (150, 220, 255)  # Lighter blue for glow
        
        # Animation
        self.pulse_timer = 0
        self.pulse_speed = 0.1
        
        # Visibility settings
        self.fade_timer = 0
        self.fade_duration = 120  # Show for 2 seconds after using a spin
        self.alpha = 0  # Current transparency (0-255)
        
    def draw(self, screen, player, camera_x):
        """Draw the spin charge dots above the player
        
        Args:
            screen: Pygame screen surface
            player: Player object with spin charge attributes
            camera_x: Camera x offset for scrolling
        """
        # Only show if player has less than max charges, recently used a spin, or fade timer active
        show_dots = (
            player.spin_charges < player.spin_charges_max or 
            self.fade_timer > 0
        )
        
        if not show_dots:
            self.alpha = 0
            return
        
        # Update fade timer
        if player.spin_charges < player.spin_charges_max:
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
        
        # Update pulse animation
        self.pulse_timer += self.pulse_speed
        pulse = abs(math.sin(self.pulse_timer))
        
        # Calculate center position for all dots
        total_width = (player.spin_charges_max - 1) * self.dot_spacing
        start_x = player.rect.centerx - camera_x - (total_width // 2)
        dot_y = player.rect.top + self.offset_y
        
        # Calculate which dots should be filled based on charges and timers
        # We want to fill from left to right in order
        charges_display = self._calculate_charge_display(player)
        
        # Draw each dot
        for i in range(player.spin_charges_max):
            dot_x = start_x + (i * self.dot_spacing)
            
            if charges_display[i]['filled']:
                # Dot is available - draw with glow
                self._draw_available_dot(screen, dot_x, dot_y, pulse)
            else:
                # Dot is empty or recharging
                self._draw_recharging_dot(screen, dot_x, dot_y, charges_display[i]['progress'])
    
    def _calculate_charge_display(self, player):
        """Calculate which dots should be filled and their progress
        
        Returns a list of dicts with 'filled' and 'progress' keys
        """
        display = []
        
        # First, add all available (filled) charges from left to right
        for i in range(player.spin_charges):
            display.append({'filled': True, 'progress': 1.0})
        
        # Then add recharging charges from left to right, sorted by progress
        # Sort timers so the one closest to completion is shown first (leftmost)
        sorted_timers = sorted(player.spin_charge_timers, reverse=False)  # Smallest (closest to done) first
        
        for timer in sorted_timers:
            progress = 1.0 - (timer / player.spin_charge_cooldown)
            display.append({'filled': False, 'progress': progress})
        
        # Fill remaining slots with empty dots
        while len(display) < player.spin_charges_max:
            display.append({'filled': False, 'progress': 0.0})
        
        return display
    
    def _draw_available_dot(self, screen, x, y, pulse):
        """Draw an available charge dot with glow effect"""
        # Create surface for this dot with alpha
        dot_surface = pygame.Surface((self.dot_radius * 4, self.dot_radius * 4), pygame.SRCALPHA)
        center = (self.dot_radius * 2, self.dot_radius * 2)
        
        # Draw outer glow (pulsing)
        glow_radius = int(self.dot_radius * (1.5 + pulse * 0.3))
        glow_alpha = int(100 * (1 - pulse * 0.3) * (self.alpha / 255))
        
        for r in range(glow_radius, self.dot_radius, -1):
            alpha = int(glow_alpha * (glow_radius - r) / (glow_radius - self.dot_radius))
            color = (*self.glow_color, alpha)
            pygame.draw.circle(dot_surface, color, center, r)
        
        # Draw main dot
        pygame.draw.circle(dot_surface, (*self.dot_color_available, self.alpha), 
                          center, self.dot_radius)
        
        # Draw bright center highlight
        highlight_color = (200, 240, 255, self.alpha)
        pygame.draw.circle(dot_surface, highlight_color, center, self.dot_radius // 2)
        
        # Blit to screen
        screen.blit(dot_surface, (x - self.dot_radius * 2, y - self.dot_radius * 2))
    
    def _draw_recharging_dot(self, screen, x, y, progress):
        """Draw a recharging/empty dot (always gray, no progress indicator)
        
        Args:
            progress: 0.0 to 1.0, how much recharged (not used, kept for compatibility)
        """
        # Create surface for this dot with alpha
        dot_surface = pygame.Surface((self.dot_radius * 4, self.dot_radius * 4), pygame.SRCALPHA)
        center = (self.dot_radius * 2, self.dot_radius * 2)
        
        # Always draw as gray/empty (no progress indicator)
        pygame.draw.circle(dot_surface, (*self.dot_color_empty, self.alpha), 
                          center, self.dot_radius)
        
        # Draw outer ring
        pygame.draw.circle(dot_surface, (80, 80, 100, self.alpha), 
                          center, self.dot_radius, 1)
        
        # Blit to screen
        screen.blit(dot_surface, (x - self.dot_radius * 2, y - self.dot_radius * 2))