import pygame
import random

class Snowy(pygame.sprite.Sprite):
    """Snowman enemy - slow, powerful melee fighter that tracks and punches the player"""
    def __init__(self, x, y, patrol_left, patrol_right):
        super().__init__()

        # --- POWER EFFECTIVENESS CONFIGURATION ---
        # Define which player powers work against this enemy
        self.vulnerable_to = {
            'stomp': True,      # Can be damaged by landing on head
            'spin_attack': True, # Can be damaged by spin attack
            'roll': False       # Roll does NOT damage (player takes damage instead)
        }
        
        # --- LOAD ANIMATIONS ---
        try:
            # Single idle frame
            self.idle_frames = self.load_sprite_sheet(
                "assets/images/1 Snowy/Snowy.png",
                frame_count=1,
                target_height=160
            )
            
            # 6 walk frames
            self.walk_frames = self.load_sprite_sheet(
                "assets/images/1 Snowy/Snowy_walk.png",
                frame_count=6,
                target_height=160
            )
            
            # 4 idle frames (standing still animation)
            self.idle_anim_frames = self.load_sprite_sheet(
                "assets/images/1 Snowy/Snowy_idle.png",
                frame_count=4,
                target_height=160
            )
            
            # 2 hurt frames
            self.hurt_frames = self.load_sprite_sheet(
                "assets/images/1 Snowy/Snowy_hurt.png",
                frame_count=2,
                target_height=160
            )
            
            # 6 death frames
            self.death_frames = self.load_sprite_sheet(
                "assets/images/1 Snowy/Snowy_death.png",
                frame_count=6,
                target_height=160
            )
            
            # 4 attack frames (punch animation)
            self.attack_frames = self.load_sprite_sheet(
                "assets/images/1 Snowy/Snowy_attack.png",
                frame_count=4,
                target_height=160
            )
        except Exception as e:
            print(f"Error loading Snowy sprites: {e}")
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
        
        # Create a smaller hitbox for body collision
        self.hitbox = pygame.Rect(0, 0, 72, 104)
        self.hitbox.midbottom = self.rect.midbottom
        
        # Punch hitbox (only active during attack frames 2, 3)
        self.punch_hitbox = pygame.Rect(0, 0, 55, 55)
        self.punch_hitbox_active = False
        
        # Hitbox offset to account for sprite centering
        self.hitbox_offset_x = -29
        
        # Sprite offset compensation
        self.sprite_offset = 16
        
        # Animation
        self.current_frame = 0
        self.frame_counter = 0.0
        self.animation_speed = 0.08  # Slow, lumbering movement
        
        # Movement - slow but powerful
        self.speed = 0.6  # Very slow movement (glacier-like)
        self.chase_speed = 1.0  # Slightly faster when chasing
        self.direction = -1  # Start moving left
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right
        
        # State
        self.state = "walk"
        self.facing_right = False
        
        # Idle behavior (stops to idle occasionally)
        self.idle_timer = 0
        self.idle_duration = 0
        self.is_idling = False
        
        # --- TRACKING BEHAVIOR ---
        self.tracking_mode = False  # Whether actively tracking player
        self.tracking_range = 500  # Large range - Snowy notices player from far away
        self.attack_range = 90  # Needs to get close to punch
        self.lose_interest_range = 800  # Very persistent - doesn't give up easily
        self.chase_determination = 0  # How determined Snowy is to reach player
        
        # Attack/Punch mechanics
        self.attack_cooldown = 0
        self.attack_cooldown_max = random.randint(80, 140)  # Moderate attack frequency
        self.is_attacking = False
        self.attack_windup_pause_frame = 1  # Pause at frame 1 (windup)
        self.attack_pause_timer = 0
        self.attack_pause_duration = 35  # Longer windup for powerful punch
        
        # Health - tanky snowman
        self.max_health = 4  # Track maximum health
        self.health = 4  # More health than most enemies
        self.is_dead = False
        self.hurt_flash_timer = 0
        self.invincible = False
        self.invincible_timer = 0
        
        # Damage - hits hard when he lands a punch
        self.punch_damage = 2  # Does 2 damage instead of 1
        
    def load_sprite_sheet(self, path, frame_count, target_height=160):
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
        surf = pygame.Surface((80, 112), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 255, 255), (0, 0, 80, 112))
        pygame.draw.circle(surf, (100, 100, 100), (40, 32), 13)
        return surf
    
    def update_hitbox_position(self):
        """Update hitbox to follow rect with directional offset"""
        self.hitbox.midbottom = self.rect.midbottom
        
        # Apply offset based on facing direction
        if self.facing_right:
            self.hitbox.x += self.hitbox_offset_x
        else:
            self.hitbox.x -= self.hitbox_offset_x
    
    def update_punch_hitbox(self):
        """Update punch hitbox position based on attack state"""
        if not self.punch_hitbox_active:
            return
        
        # Position punch hitbox in front of the character (extended arm)
        # Adjust the second value to move hitbox up (negative) or down (positive)
        if self.facing_right:
            self.punch_hitbox.midleft = (self.hitbox.right + 5, self.hitbox.centery + 10)
        else:
            self.punch_hitbox.midright = (self.hitbox.left - 5, self.hitbox.centery + 10)
    
    def check_player_distance(self, player):
        """Calculate distance to player and determine tracking behavior"""
        if not player or player.is_dead:
            return None
        
        dx = player.hitbox.centerx - self.hitbox.centerx
        distance = abs(dx)
        
        return distance, dx
    
    def update(self, player=None, projectile_group=None):
        """Update Snowy's behavior and animation"""
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
            self.update_punch_hitbox()
            return
        
        # Deactivate punch hitbox when not attacking
        self.punch_hitbox_active = False
        
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
        current_speed = self.speed
        
        if player:
            result = self.check_player_distance(player)
            if result:
                distance, dx = result
                
                # Enter tracking mode if player is within range
                if distance < self.tracking_range:
                    self.tracking_mode = True
                    self.chase_determination = 100  # Reset determination
                
                # Exit tracking mode if player is too far and determination runs out
                if distance > self.lose_interest_range:
                    self.chase_determination -= 1
                    if self.chase_determination <= 0:
                        self.tracking_mode = False
                
                # If tracking, move toward player
                if self.tracking_mode:
                    # Use faster chase speed when tracking
                    current_speed = self.chase_speed
                    
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
                        self.attack_cooldown = random.randint(80, 140)
        
        # --- WALKING STATE ---
        # Move in current direction (either patrol or tracking)
        self.rect.x += current_speed * self.direction
        
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
            if random.randint(0, 240) == 0:  # Occasionally stops to rest
                self.start_idle()
        
        # --- ATTACK COOLDOWN ---
        self.attack_cooldown -= 1
        
        # Update hitbox to follow rect
        self.update_hitbox_position()
        
        # Animate walking
        self.animate_walk()
    
    def start_idle(self):
        """Start idle animation"""
        self.is_idling = True
        self.idle_timer = random.randint(70, 130)  # Longer idle times (lumbering)
        self.idle_duration = self.idle_timer
        self.current_frame = 0
        self.frame_counter = 0.0
        self.state = "idle"
    
    def start_attack(self):
        """Start the attack animation sequence"""
        self.is_attacking = True
        self.attack_pause_timer = 0  # Reset pause timer
        self.current_frame = 0
        self.frame_counter = 0.0
        self.state = "attack"
        self.punch_hitbox_active = False
    
    def animate_idle(self):
        """Animate idle standing"""
        self.frame_counter += 0.06  # Very slow idle animation
        
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
        """Handle attack animation and punch hitbox activation"""
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
        self.frame_counter += 0.13  # Slow but powerful punch animation
        
        if self.frame_counter >= 1.0:
            self.frame_counter = 0.0
            self.current_frame += 1
            
            # Activate punch hitbox on frames 2 and 3 (0-indexed)
            # This is when the arm is extended
            if self.current_frame in [2, 3]:
                self.punch_hitbox_active = True
            else:
                self.punch_hitbox_active = False
            
            # End of attack animation
            if self.current_frame >= len(self.attack_frames):
                self.is_attacking = False
                self.state = "walk"
                self.current_frame = 0
                self.punch_hitbox_active = False
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
            # Flash red for 20 frames (~0.33 seconds)
            self.hurt_flash_timer = 20
            # Make invincible for 60 frames (1 second at 60 FPS)
            self.invincible = True
            self.invincible_timer = 60
    
    def die(self):
        """Trigger death sequence"""
        self.is_dead = True
        self.state = "death"
        self.current_frame = 0
        self.frame_counter = 0.0
        self.punch_hitbox_active = False
    
    def animate_death(self):
        """Play death animation and remove sprite"""
        self.frame_counter += 0.20  # Moderate death animation speed
        
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