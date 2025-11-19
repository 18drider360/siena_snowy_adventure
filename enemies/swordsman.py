import pygame
import random

class Swordsman(pygame.sprite.Sprite):
    """Swordsman enemy - melee attacker with sword hitbox extension and player tracking"""
    def __init__(self, x, y, patrol_left, patrol_right):
        super().__init__()

        # --- POWER EFFECTIVENESS CONFIGURATION ---
        # Define which player powers work against this enemy
        self.vulnerable_to = {
            'stomp': True,      # Can be damaged by landing on head
            'spin_attack': False, # Can be damaged by spin attack
            'roll': True      # Roll does NOT damage (player takes damage instead)
        }
        
        # --- LOAD ANIMATIONS ---
        try:
            # Single idle frame
            self.idle_frames = self.load_sprite_sheet(
                "assets/images/5 Swordsman/Swordsman.png",
                frame_count=1,
                target_height=130
            )
            
            # 6 walk frames
            self.walk_frames = self.load_sprite_sheet(
                "assets/images/5 Swordsman/Swordsman_walk.png",
                frame_count=6,
                target_height=130
            )
            
            # 4 idle animation frames
            self.idle_anim_frames = self.load_sprite_sheet(
                "assets/images/5 Swordsman/Swordsman_idle.png",
                frame_count=4,
                target_height=130
            )
            
            # 2 hurt frames
            self.hurt_frames = self.load_sprite_sheet(
                "assets/images/5 Swordsman/Swordsman_hurt.png",
                frame_count=2,
                target_height=130
            )
            
            # 4 death frames
            self.death_frames = self.load_sprite_sheet(
                "assets/images/5 Swordsman/Swordsman_death.png",
                frame_count=4,
                target_height=130
            )
            
            # 6 attack frames
            self.attack_frames = self.load_sprite_sheet(
                "assets/images/5 Swordsman/Swordsman_attack.png",
                frame_count=6,
                target_height=130
            )
        except Exception as e:
            print(f"Error loading Swordsman sprites: {e}")
            # Fallback sprites
            self.idle_frames = [self.create_fallback_sprite()]
            self.walk_frames = [self.create_fallback_sprite()]
            self.idle_anim_frames = [self.create_fallback_sprite()]
            self.hurt_frames = [self.create_fallback_sprite()]
            self.death_frames = [self.create_fallback_sprite()]
            self.attack_frames = [self.create_fallback_sprite()]
        
        # --- INITIAL STATE ---
        self.image = self.walk_frames[0]
        self.rect = self.image.get_rect(midbottom=(x, y))
        
        # Create a hitbox for body collision
        self.hitbox = pygame.Rect(0, 0, 58, 90)
        self.hitbox.midbottom = self.rect.midbottom
        
        # Sword hitbox (only active during attack frames 4, 5, 6)
        self.sword_hitbox = pygame.Rect(0, 0, 40, 70)
        self.sword_hitbox_active = False
        
        # Hitbox offset to account for sprite centering
        self.hitbox_offset_x = -23
        
        # Sprite offset compensation
        self.sprite_offset = 13
        
        # Animation
        self.current_frame = 0
        self.frame_counter = 0.0
        self.animation_speed = 0.12
        
        # Movement
        self.speed = 1.8  # Increased from 1.2 for more aggressive pursuit
        self.direction = -1  # Start moving left
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right
        
        # State
        self.state = "walk"
        self.facing_right = False
        
        # Idle behavior
        self.idle_timer = 0
        self.idle_duration = 0
        self.is_idling = False
        
        # --- TRACKING BEHAVIOR ---
        self.tracking_mode = False  # Whether actively tracking player
        self.tracking_range = 400  # Distance at which swordsman notices player
        self.attack_range = 80  # Distance at which swordsman attacks
        self.lose_interest_range = 600  # Distance at which swordsman gives up chase
        
        # Attack mechanics (melee only - no projectiles)
        self.attack_cooldown = 0
        self.attack_cooldown_max = random.randint(60, 120)  # Reduced from 100-180 for more frequent attacks
        self.is_attacking = False
        self.attack_windup_pause_frame = 2  # Pause at frame 2 (windup)
        self.attack_pause_timer = 0
        self.attack_pause_duration = 20  # Short pause
        
        # Health
        self.health = 3
        self.max_health = 3  # More health since melee fighter
        self.is_dead = False
        self.hurt_flash_timer = 0
        self.invincible = False
        self.invincible_timer = 0
        
    def load_sprite_sheet(self, path, frame_count, target_height=130):
        """Load and split a sprite sheet into frames"""
        sheet = pygame.image.load(path).convert_alpha()
        sheet_width, sheet_height = sheet.get_size()
        frame_width = sheet_width // frame_count
        
        frames = []
        for i in range(frame_count):
            frame = pygame.Surface((frame_width, sheet_height), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), (i * frame_width, 0, frame_width, sheet_height))
            
            # Scale keeping aspect ratio
            aspect = frame_width / sheet_height
            scaled = pygame.transform.scale(frame, (int(target_height * aspect), target_height))
            frames.append(scaled)
        return frames
    
    def create_fallback_sprite(self):
        """Fallback rectangle if sprites fail to load"""
        surf = pygame.Surface((65, 91), pygame.SRCALPHA)
        pygame.draw.rect(surf, (120, 80, 60), (20, 13, 26, 39))  # Body
        pygame.draw.circle(surf, (200, 150, 100), (33, 20), 10)  # Head
        pygame.draw.rect(surf, (150, 150, 150), (46, 33, 20, 5))  # Sword
        return surf
    
    def update_hitbox_position(self):
        """Update hitbox to follow rect with directional offset"""
        self.hitbox.midbottom = self.rect.midbottom
        
        # Apply offset based on facing direction
        if self.facing_right:
            self.hitbox.x += self.hitbox_offset_x
        else:
            self.hitbox.x -= self.hitbox_offset_x
    
    def update_sword_hitbox(self):
        """Update sword hitbox position based on attack state"""
        if not self.sword_hitbox_active:
            return
        
        # Position sword hitbox in front of the character
        if self.facing_right:
            self.sword_hitbox.midleft = (self.hitbox.right, self.hitbox.centery - 10)
        else:
            self.sword_hitbox.midright = (self.hitbox.left, self.hitbox.centery - 10)
    
    def check_player_distance(self, player):
        """Calculate distance to player and determine tracking behavior"""
        if not player or player.is_dead:
            return None
        
        dx = player.hitbox.centerx - self.hitbox.centerx
        distance = abs(dx)
        
        return distance, dx
    
    def update(self, player=None, projectile_group=None):
        """Update Swordsman's behavior and animation"""
        if self.is_dead:
            self.animate_death()
            return
        
        # Count down hurt flash timer
        if self.hurt_flash_timer > 0:
            self.hurt_flash_timer -= 1
        
        # Count down invincibility timer
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
            if self.invincible_timer == 0:
                self.invincible = False
        
        # --- ATTACKING STATE ---
        if self.is_attacking:
            self.animate_attack()
            self.update_hitbox_position()
            self.update_sword_hitbox()
            return
        
        # Deactivate sword hitbox when not attacking
        self.sword_hitbox_active = False
        
        # --- IDLING STATE ---
        if self.is_idling:
            self.idle_timer -= 1
            if self.idle_timer <= 0:
                self.is_idling = False
                self.state = "walk"
            self.animate_idle()
            self.update_hitbox_position()
            return
        
        # --- TRACKING BEHAVIOR ---
        if player:
            result = self.check_player_distance(player)
            if result:
                distance, dx = result
                
                # Enter tracking mode if player is within range
                if distance < self.tracking_range:
                    self.tracking_mode = True
                
                # Exit tracking mode if player is too far
                if distance > self.lose_interest_range:
                    self.tracking_mode = False
                
                # If tracking, move toward player
                if self.tracking_mode:
                    # Determine direction to player
                    if dx > 0:  # Player is to the right
                        self.direction = 1
                        self.facing_right = True
                    else:  # Player is to the left
                        self.direction = -1
                        self.facing_right = False
                    
                    # Attack if player is within attack range
                    if distance < self.attack_range and self.attack_cooldown <= 0:
                        self.start_attack()
                        self.attack_cooldown = random.randint(60, 120)
        
        # --- WALKING STATE ---
        # Move in current direction (either patrol or tracking)
        self.rect.x += self.speed * self.direction
        
        # Check patrol bounds only if NOT tracking
        if not self.tracking_mode:
            if self.direction == -1 and self.rect.left <= self.patrol_left:
                old_centerx = self.rect.centerx
                self.direction = 1
                self.facing_right = True
                self.rect.centerx = old_centerx + (self.sprite_offset * 2)
            elif self.direction == 1 and self.rect.right >= self.patrol_right:
                old_centerx = self.rect.centerx
                self.direction = -1
                self.facing_right = False
                self.rect.centerx = old_centerx - (self.sprite_offset * 2)
            
            # --- RANDOM IDLE TRIGGER (only when not tracking) ---
            if random.randint(0, 200) == 0:
                self.start_idle()
        
        # --- ATTACK COOLDOWN ---
        self.attack_cooldown -= 1
        
        # Random attacks only when not tracking
        if not self.tracking_mode and self.attack_cooldown <= 0:
            if random.randint(0, 100) == 0:  # Less frequent random attacks
                self.start_attack()
                self.attack_cooldown = random.randint(100, 180)
        
        # Update hitbox to follow rect
        self.update_hitbox_position()
        
        # Animate walking
        self.animate_walk()
    
    def start_idle(self):
        """Start idle animation"""
        self.is_idling = True
        self.idle_timer = random.randint(50, 100)
        self.idle_duration = self.idle_timer
        self.current_frame = 0
        self.frame_counter = 0.0
        self.state = "idle"
    
    def start_attack(self):
        """Start the attack animation sequence"""
        self.is_attacking = True
        self.attack_pause_timer = 0
        self.current_frame = 0
        self.frame_counter = 0.0
        self.state = "attack"
        self.sword_hitbox_active = False
    
    def animate_idle(self):
        """Animate idle standing"""
        self.frame_counter += 0.10
        
        if self.frame_counter >= 1.0:
            self.frame_counter = 0.0
            self.current_frame = (self.current_frame + 1) % len(self.idle_anim_frames)
        
        old_bottom = self.rect.bottom
        old_centerx = self.rect.centerx
        
        # Use hurt frame if recently hit, otherwise idle frame
        if self.hurt_flash_timer > 0:
            base_image = self.hurt_frames[0]
        else:
            base_image = self.idle_anim_frames[self.current_frame]
        
        if self.facing_right:
            self.image = pygame.transform.flip(base_image, True, False)
        else:
            self.image = base_image
        
        self.rect = self.image.get_rect()
        self.rect.centerx = old_centerx
        self.rect.bottom = old_bottom
        
        self.update_hitbox_position()
    
    def animate_attack(self):
        """Handle attack animation and sword hitbox activation"""
        # Check if we're at the pause frame (windup)
        if self.current_frame == self.attack_windup_pause_frame and self.attack_pause_timer < self.attack_pause_duration:
            self.attack_pause_timer += 1
            old_bottom = self.rect.bottom
            old_centerx = self.rect.centerx
            
            # Use hurt frame if recently hit, otherwise attack frame
            if self.hurt_flash_timer > 0:
                base_image = self.hurt_frames[0]
            else:
                base_image = self.attack_frames[self.current_frame]
            
            if self.facing_right:
                self.image = pygame.transform.flip(base_image, True, False)
            else:
                self.image = base_image
            
            self.rect = self.image.get_rect()
            self.rect.centerx = old_centerx
            self.rect.bottom = old_bottom
            self.update_hitbox_position()
            return
        
        # Continue with normal animation after pause
        self.frame_counter += 0.16
        
        if self.frame_counter >= 1.0:
            self.frame_counter = 0.0
            self.current_frame += 1
            
            # Activate sword hitbox on frames 3, 4, 5 (0-indexed: frames 3, 4, 5)
            # Based on description: frames 4, 5, 6 (1-indexed)
            if self.current_frame in [3, 4, 5]:
                self.sword_hitbox_active = True
            else:
                self.sword_hitbox_active = False
            
            # End of attack animation
            if self.current_frame >= len(self.attack_frames):
                self.is_attacking = False
                self.state = "walk"
                self.current_frame = 0
                self.sword_hitbox_active = False
                return
        
        # Display attack frame
        old_bottom = self.rect.bottom
        old_centerx = self.rect.centerx
        
        # Use hurt frame if recently hit, otherwise attack frame
        if self.hurt_flash_timer > 0:
            base_image = self.hurt_frames[0]
        else:
            base_image = self.attack_frames[self.current_frame]
        
        if self.facing_right:
            self.image = pygame.transform.flip(base_image, True, False)
        else:
            self.image = base_image
        
        self.rect = self.image.get_rect()
        self.rect.centerx = old_centerx
        self.rect.bottom = old_bottom
        
        self.update_hitbox_position()
    
    def animate_walk(self):
        """Animate walking"""
        self.frame_counter += self.animation_speed
        
        if self.frame_counter >= 1.0:
            self.frame_counter = 0.0
            self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
        
        old_bottom = self.rect.bottom
        old_centerx = self.rect.centerx
        
        # Use hurt frame if recently hit, otherwise walk frame
        if self.hurt_flash_timer > 0:
            base_image = self.hurt_frames[0]
        else:
            base_image = self.walk_frames[self.current_frame]
        
        if self.facing_right:
            self.image = pygame.transform.flip(base_image, True, False)
        else:
            self.image = base_image
        
        self.rect = self.image.get_rect()
        self.rect.centerx = old_centerx
        self.rect.bottom = old_bottom
        
        self.update_hitbox_position()
    
    def take_damage(self, damage=1):
        """Handle taking damage"""
        if self.is_dead or self.invincible:
            return
        
        self.health -= damage
        
        if self.health <= 0:
            self.die()
        else:
            # Flash red for 20 frames
            self.hurt_flash_timer = 20
            # Make invincible for 60 frames (1 second)
            self.invincible = True
            self.invincible_timer = 60
    
    def die(self):
        """Trigger death sequence"""
        self.is_dead = True
        self.state = "death"
        self.current_frame = 0
        self.frame_counter = 0.0
        self.sword_hitbox_active = False
    
    def animate_death(self):
        """Play death animation and remove sprite"""
        self.frame_counter += 0.20
        
        if self.frame_counter >= 1.0:
            self.frame_counter = 0.0
            self.current_frame += 1
            
            # Remove sprite after death animation completes
            if self.current_frame >= len(self.death_frames):
                self.kill()
                return
        
        old_bottom = self.rect.bottom
        old_centerx = self.rect.centerx
        
        base_image = self.death_frames[self.current_frame]
        if self.facing_right:
            self.image = pygame.transform.flip(base_image, True, False)
        else:
            self.image = base_image
        
        self.rect = self.image.get_rect()
        self.rect.centerx = old_centerx
        self.rect.bottom = old_bottom
        
        self.update_hitbox_position()