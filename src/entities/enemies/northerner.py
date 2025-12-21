import pygame
import random

class Pilos(pygame.sprite.Sprite):
    """Spear projectile thrown by Northerner"""
    def __init__(self, x, y, direction, speed_x=15, speed_y=-2):
        super().__init__()
        
        # Load the pilos spear image
        try:
            self.image = pygame.image.load("assets/images/6 Northerner/pilos.png").convert_alpha()
            # Scale it to a reasonable size (adjust as needed)
            self.image = pygame.transform.scale(self.image, (40, 12))
            
            # Flip if going left
            if direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)
        except Exception as e:
            print(f"Error loading pilos sprite: {e}")
            # Fallback: create a simple spear shape
            self.image = pygame.Surface((40, 12), pygame.SRCALPHA)
            pygame.draw.polygon(self.image, (139, 69, 19), [(0, 6), (30, 0), (40, 6), (30, 12)])
            pygame.draw.rect(self.image, (101, 67, 33), (0, 4, 30, 4))
            
            if direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)
        
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = speed_x  # Horizontal speed (can be customized)
        self.direction = direction  # -1 for left, 1 for right
        self.speed_y = speed_y  # Initial vertical velocity
        self.gravity = 0.4
        
    def update(self):
        """Move the spear with arc physics"""
        # Horizontal movement
        self.rect.x += self.speed_x * self.direction

        # Apply gravity for arc
        self.speed_y += self.gravity
        self.rect.y += self.speed_y

        # Remove if off screen or hits ground
        if self.rect.x < -100 or self.rect.x > 15000 or self.rect.y > 600:
            self.kill()


class Northerner(pygame.sprite.Sprite):
    """Northerner enemy - intelligent ranged warrior who throws spears"""
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
                "assets/images/6 Northerner/Northerner.png",
                frame_count=1,
                target_height=130
            )
            
            # 6 walk frames
            self.walk_frames = self.load_sprite_sheet(
                "assets/images/6 Northerner/Northerner_walk.png",
                frame_count=6,
                target_height=130
            )
            
            # 4 idle animation frames (standing still animation)
            self.idle_anim_frames = self.load_sprite_sheet(
                "assets/images/6 Northerner/Northerner_idle.png",
                frame_count=4,
                target_height=130
            )
            
            # 2 hurt frames
            self.hurt_frames = self.load_sprite_sheet(
                "assets/images/6 Northerner/Northerner_hurt.png",
                frame_count=2,
                target_height=130
            )
            
            # 6 death frames
            self.death_frames = self.load_sprite_sheet(
                "assets/images/6 Northerner/Northerner_death.png",
                frame_count=4,
                target_height=130
            )
            
            # 6 attack frames (throwing spear)
            self.attack_frames = self.load_sprite_sheet(
                "assets/images/6 Northerner/Northerner_attack.png",
                frame_count=6,
                target_height=130
            )
        except Exception as e:
            print(f"Error loading Northerner sprites: {e}")
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
        
        # Create a hitbox for collision
        self.hitbox = pygame.Rect(0, 0, 55, 90)
        self.hitbox.midbottom = self.rect.midbottom
        
        # Hitbox offset to account for sprite centering
        self.hitbox_offset_x = -30
        
        # Sprite offset compensation
        self.sprite_offset = 10
        
        # Animation
        self.current_frame = 0
        self.frame_counter = 0.0
        self.animation_speed = 0.12
        
        # Movement
        self.speed = 1.5  # Faster movement for combat positioning
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
        
        # --- INTELLIGENT TRACKING BEHAVIOR ---
        self.tracking_mode = False
        self.detection_range = 500  # Distance at which Northerner notices player
        self.optimal_attack_range_min = 180  # Minimum preferred distance
        self.optimal_attack_range_max = 320  # Maximum preferred distance
        self.retreat_range = 120  # If player closer than this, back away
        self.lose_interest_range = 700  # Distance at which gives up chase
        
        # Attack/Throw mechanics
        self.attack_cooldown = 0
        self.attack_cooldown_max = random.randint(80, 140)  # More frequent attacks
        self.is_attacking = False
        self.attack_frame_trigger = 4  # Throw spear on frame 4
        self.attack_windup_pause_frame = 2  # Pause at frame 2 (wind-up)
        self.attack_pause_timer = 0
        self.attack_pause_duration = 30
        self.has_thrown_spear = False
        
        # Lead shot calculation
        self.player_last_x = None
        self.player_velocity_x = 0
        
        # Health
        self.health = 1  # Tougher than Frost Golem
        self.max_health = 1
        self.is_dead = False
        self.death_complete = False
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
        surf = pygame.Surface((40, 90), pygame.SRCALPHA)
        pygame.draw.rect(surf, (180, 150, 120), (0, 0, 40, 90))
        pygame.draw.circle(surf, (200, 180, 160), (20, 20), 10)
        return surf
    
    def update_hitbox_position(self):
        """Update hitbox to follow rect with directional offset"""
        self.hitbox.midbottom = self.rect.midbottom
        
        # Apply offset based on facing direction
        if self.facing_right:
            self.hitbox.x += self.hitbox_offset_x
        else:
            self.hitbox.x -= self.hitbox_offset_x
    
    def check_player_distance(self, player):
        """Calculate distance to player and estimate player velocity"""
        if not player or getattr(player, 'is_dead', False):
            return None
        
        dx = player.hitbox.centerx - self.hitbox.centerx
        dy = player.hitbox.centery - self.hitbox.centery
        distance = abs(dx)
        
        # Calculate player velocity for lead shots
        if self.player_last_x is not None:
            self.player_velocity_x = player.hitbox.centerx - self.player_last_x
        self.player_last_x = player.hitbox.centerx
        
        return distance, dx, dy
    
    def update(self, player=None, projectile_group=None):
        """Update Northerner's behavior and animation"""
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
            self.animate_attack(projectile_group, player)
            self.update_hitbox_position()
            return
        
        # --- IDLING STATE ---
        if self.is_idling:
            self.idle_timer -= 1
            if self.idle_timer <= 0:
                self.is_idling = False
                self.state = "walk"
            self.animate_idle()
            self.update_hitbox_position()
            return
        
        # --- INTELLIGENT COMBAT BEHAVIOR ---
        if player:
            result = self.check_player_distance(player)
            if result:
                distance, dx, dy = result
                
                # Enter tracking mode if player detected
                if distance < self.detection_range:
                    self.tracking_mode = True
                
                # Exit tracking mode if player too far
                if distance > self.lose_interest_range:
                    self.tracking_mode = False
                
                if self.tracking_mode:
                    # Face the player
                    if dx > 0:
                        self.facing_right = True
                    else:
                        self.facing_right = False
                    
                    # TACTICAL POSITIONING
                    if distance < self.retreat_range:
                        # TOO CLOSE - RETREAT
                        # Move away from player
                        if dx > 0:
                            self.direction = -1  # Player right, move left
                        else:
                            self.direction = 1  # Player left, move right
                        
                    elif distance > self.optimal_attack_range_max:
                        # TOO FAR - ADVANCE
                        # Move toward player
                        if dx > 0:
                            self.direction = 1  # Player right, move right
                        else:
                            self.direction = -1  # Player left, move left
                        
                    elif distance < self.optimal_attack_range_min:
                        # SLIGHTLY TOO CLOSE - BACK UP SLOWLY
                        if dx > 0:
                            self.direction = -1
                        else:
                            self.direction = 1
                        
                    else:
                        # OPTIMAL RANGE - STOP AND ATTACK
                        # Stop moving to take aim
                        self.direction = 0

                        # Attack if cooldown ready
                        if self.attack_cooldown <= 0:
                            self.start_attack()
                            self.attack_cooldown = random.randint(80, 140)

                    # ALSO attack from any range if tracking and cooldown ready (more aggressive)
                    if self.attack_cooldown <= 0 and random.randint(0, 30) == 0:
                        self.start_attack()
                        self.attack_cooldown = random.randint(100, 160)
        
        # --- WALKING STATE ---
        # If at platform edge, go idle and occasionally throw spear instead of moving
        at_edge = hasattr(self, 'at_platform_edge') and self.at_platform_edge
        if at_edge:
            self.at_platform_edge = False  # Reset for next frame
            # Start idle animation if not already idling or attacking
            if not self.is_idling and not self.is_attacking and random.randint(0, 10) == 0:
                self.start_idle()
            # Occasionally throw spear even when at edge
            if player and self.attack_cooldown <= 0 and random.randint(0, 60) == 0:
                self.start_attack()
                self.attack_cooldown = random.randint(100, 180)

        if self.direction != 0 and not at_edge:
            self.rect.x += self.speed * self.direction

        # Check patrol bounds only if NOT tracking
        if not self.tracking_mode and not at_edge:
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
            
            # Random idle when patrolling
            if random.randint(0, 250) == 0:
                self.start_idle()
            
            # Random attacks when patrolling (less frequent)
            if self.attack_cooldown <= 0 and random.randint(0, 200) == 0:
                self.start_attack()
                self.attack_cooldown = random.randint(180, 300)
        
        # --- ATTACK COOLDOWN ---
        self.attack_cooldown -= 1
        
        # Update hitbox to follow rect
        self.update_hitbox_position()
        
        # Animate walking (or idle if direction is 0)
        if self.direction != 0:
            self.animate_walk()
        else:
            self.animate_idle()
    
    def start_idle(self):
        """Start idle animation"""
        self.is_idling = True
        self.idle_timer = random.randint(60, 120)
        self.idle_duration = self.idle_timer
        self.current_frame = 0
        self.frame_counter = 0.0
        self.state = "idle"
    
    def start_attack(self):
        """Start the attack animation sequence"""
        self.is_attacking = True
        self.has_thrown_spear = False
        self.attack_pause_timer = 0
        self.current_frame = 0
        self.frame_counter = 0.0
        self.state = "attack"
    
    def animate_idle(self):
        """Animate idle standing"""
        self.frame_counter += 0.10
        
        if self.frame_counter >= 1.0:
            self.frame_counter = 0.0
            self.current_frame = (self.current_frame + 1) % len(self.idle_anim_frames)
        
        # Ensure current_frame is within bounds (safety check)
        self.current_frame = self.current_frame % len(self.idle_anim_frames)
        
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
    
    def animate_attack(self, projectile_group, player):
        """Handle attack animation and spear throwing"""
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
        self.frame_counter += 0.15
        
        if self.frame_counter >= 1.0:
            self.frame_counter = 0.0
            self.current_frame += 1
            
            # Throw spear at frame 4
            if self.current_frame == self.attack_frame_trigger and not self.has_thrown_spear:
                self.throw_spear_at_player(projectile_group, player)
                self.has_thrown_spear = True
            
            # End of attack animation
            if self.current_frame >= len(self.attack_frames):
                self.is_attacking = False
                self.state = "walk"
                self.current_frame = 0
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
    
    def throw_spear_at_player(self, projectile_group, player):
        """Create and launch a spear with intelligent aiming"""
        # Don't throw if no projectile group provided
        if projectile_group is None:
            return

        offset = 40 if self.facing_right else -40
        spear_x = self.rect.centerx + offset
        spear_y = self.rect.centery - 20  # Shoulder level

        direction = 1 if self.facing_right else -1

        # INTELLIGENT AIMING
        if player and self.tracking_mode:
            # Calculate where player will be
            dx = player.hitbox.centerx - spear_x
            dy = player.hitbox.centery - spear_y

            # Lead the shot based on player velocity
            # Estimate time to reach player
            time_to_target = abs(dx) / 15.0  # 15 is base spear speed
            predicted_x = player.hitbox.centerx + (self.player_velocity_x * time_to_target)

            # Recalculate with prediction
            dx = predicted_x - spear_x
            distance = abs(dx)

            # Adjust arc based on distance
            if distance > 250:
                # Long range - higher arc
                speed_y = -4
                speed_x = 16
            elif distance > 150:
                # Medium range - medium arc
                speed_y = -2.5
                speed_x = 15
            else:
                # Close range - flat trajectory
                speed_y = -1
                speed_x = 14

            # Adjust vertical aim for height difference
            if dy < -30:  # Player is above
                speed_y -= 1.5
            elif dy > 30:  # Player is below
                speed_y += 1

            spear = Pilos(spear_x, spear_y, direction, speed_x, speed_y)
        else:
            # Default throw if no player tracking
            spear = Pilos(spear_x, spear_y, direction)

        projectile_group.add(spear)
    
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
    
    def animate_death(self):
        """Play death animation and remove sprite"""
        # Safety check: if we've already gone past the last frame, mark complete and exit
        if self.current_frame >= len(self.death_frames):
            self.death_complete = True
            self.kill()
            return

        self.frame_counter += 0.20

        if self.frame_counter >= 1.0:
            self.frame_counter = 0.0
            self.current_frame += 1

            # Remove sprite after death animation completes
            if self.current_frame >= len(self.death_frames):
                self.death_complete = True
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