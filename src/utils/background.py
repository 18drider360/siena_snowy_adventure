import pygame
from src.utils import settings as S

class ParallaxBackground:
    def __init__(self, image_paths, level_width):
        self.layers = []
        for i, path in enumerate(image_paths):
            img = pygame.image.load(path).convert_alpha()

            # Scale to at least screen height to ensure coverage
            # Adjust scaling to be more conservative
            depth_scale = 1.0 - (i * 0.05)  # Less aggressive scaling
            
            # Ensure minimum size is screen dimensions
            target_height = max(S.WINDOW_HEIGHT, int(img.get_height() * depth_scale))
            aspect_ratio = img.get_width() / img.get_height()
            target_width = int(target_height * aspect_ratio)
            
            # Make sure width is sufficient for tiling
            target_width = max(target_width, S.WINDOW_WIDTH)
            
            img = pygame.transform.scale(img, (target_width, target_height))

            # Speed factor: distant layers move slower
            speed_factor = 0.1 + (i * 0.15)
            
            # Vertical offset - position layers based on their index
            # First 2 layers (4.png, 5.png) = sky/clouds - anchor to top
            # Last 3 layers (1.png, 2.png, 3.png) = ground/trees - anchor to bottom
            if i >= len(image_paths) - 3:  # Last 3 layers (ground and trees)
                # Anchor to bottom of screen
                vertical_offset = S.WINDOW_HEIGHT - target_height
            else:  # First 2 layers (sky and distant mountains)
                # Anchor to top
                vertical_offset = 0

            self.layers.append({
                "image": img,
                "speed": speed_factor,
                "y": vertical_offset,
                "width": target_width
            })

        self.level_width = level_width

    def draw(self, screen, camera_x):
        for layer in self.layers:
            img = layer["image"]
            speed = layer["speed"]
            y = layer["y"]
            width = layer["width"]

            # Calculate x offset for parallax (moving slower than camera)
            offset = camera_x * speed
            
            # Calculate starting position (modulo for seamless tiling)
            x_start = -(offset % width)
            
            # Draw tiles to cover the screen
            # Start one tile to the left to ensure coverage
            x = x_start - width
            tiles_drawn = 0
            max_tiles = 5  # Safety limit to prevent infinite loops
            
            while x < S.WINDOW_WIDTH and tiles_drawn < max_tiles:
                screen.blit(img, (x, y))
                x += width
                tiles_drawn += 1