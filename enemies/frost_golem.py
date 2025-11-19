import pygame
import random

class Fireball(pygame.sprite.Sprite):
    """Projectile shot by Frost Golem - bounces 3 times"""
    def __init__(self, x, y, direction):
        super().__init__()
        
        # Create a fireball (orange/red circle with glow effect)
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 150, 50), (10, 10), 10)
        pygame.draw.circle(self.image, (255, 80, 0), (10, 10), 7)
        pygame.draw.circle(self.image, (255, 200, 100), (10, 10), 4)
        
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = 6  # Horizontal speed
        self.direction = direction  # -1 for left, 1 for right
        self.speed_y = 2  # Start with downward velocity
        self.gravity = 0.6
        
        # Bounce mechanics
        self.bounce_count = 0
        self.max_bounces = 3
        self.bounce_dampening = 0.7  # Reduces bounce height each time
        self.ground_y = 570  # Ground level
        
    def update(self):
        """Move the fireball with bouncing physics"""
        # Horizontal movement
        self.rect.x += self.speed_x * self.direction
        
        # Apply gravity
        self.speed_y += self.gravity
        self.rect.y += self.speed_y
        
        # Check for ground collision (bounce)
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.bounce_count += 1
            
            # Check if we've bounced enough times
            if self.bounce_count >= self.max_bounces:
                self.kill()
                return
            
            # Bounce back up with reduced velocity
            self.speed_y = -abs(self.speed_y) * self.bounce_dampening
        
        # Remove if off screen
        if self.rect.x < -100 or self.rect.x > 3000:
            self.kill()


class FrostGolem(pygame.sprite.Sprite):
    """Frost Golem enemy - fast, agile, and uses hit-and-run tactics"""
    def __init__(self, x, y, patrol_left, patrol_right):
        super().__init__()
        
        # --- POWER EFFECTIVENESS CONFIGURATION ---
        # Define which player powers work against this enemy
        self.vulnerable_to = {
            'stomp': False,      # Can be damaged by landing on head
            'spin_attack': False, # Can be damaged by spin attack
            'roll': True      # Roll does NOT damage (player takes damage instead)
        }

        # --- LOAD ANIMATIONS ---
        try:
            # Single idle frame
            self.idle_frames = self.load_sprite_sheet(
                "assets/images/3 Frost_golem/Frost_golem.png",
                frame_count=1,
                target_height=80
            )
            
            # 4 walk frames
            self.walk_frames = self.load_sprite_sheet(
                "assets/images/3 Frost_golem/Frost_golem_walk.png",
                frame_count=4,
                target_height=80
            )
            
            # 4 idle animation frames (standing still animation)
            self.idle_anim_frames = self.load_sprite_sheet(
                "assets/images/3 Frost_golem/Frost_golem_idle.png",
                frame_count=4,
                target_height=80
            )
            
            # 2 hurt frames
            self.hurt_frames = self.load_sprite_sheet(
                "assets/images/3 Frost_golem/Frost_golem_hurt.png",
                frame_count=2,
                target_height=80
            )
            
            # 6 death frames
            self.death_frames = self.load_sprite_sheet(
                "assets/images/3 Frost_golem/Frost_golem_death.png",
                frame_count=6,
                target_height=80
            )
            
            # 4 attack frames
            self.attack_frames = self.load_sprite_sheet(
                "assets/images/3 Frost_golem/Frost_golem_attack.png",
                frame_count=4,
                target_height=80
            )
        except Exception as e:
            print(f"Error loading Frost Golem sprites: {e}")
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
        
        # Create a smaller hitbox for more accurate collision
        self.hitbox = pygame.Rect(0, 0, 28, 50)
        self.hitbox.midbottom = self.rect.midbottom
        
        # Hitbox offset to account for sprite centering
        self.hitbox_offset_x = -18
        
        # Sprite offset compensation
        self.sprite_offset = 8
        
        # Animation
        self.current_frame = 0
        self.frame_counter = 0.0
        self.animation_speed = 0.15  # Faster animation
        
        # Movement - Enhanced for agility
        self.base_speed = 2.2  # Faster base speed
        self.speed = self.base_speed
        self.direction = -1  # Start moving left
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right
        
        # State
        self.state = "walk"
        self.facing_right = False
        
        # Idle behavior (rarely idles - stays aggressive)
        self.idle_timer = 0
        self.idle_duration = 0
        self.is_idling = False
        
        # --- INTELLIGENT BEHAVIOR ---
        self.tracking_mode = False
        self.detection_range = 400  # Detects player from medium distance
        self.optimal_range_min = 140  # Preferred minimum distance
        self.optimal_range_max = 220  # Preferred maximum distance
        self.danger_zone = 100  # If player closer, panic and retreat
        self.lose_interest_range = 600
        
        # Hit-and-run tactics
        self.aggro_mode = False  # When true, rushes at player
        self.retreat_mode = False  # When true, runs away from player
        self.strafe_mode = False  # When true, moves laterally
        self.strafe_direction = 1
        self.tactic_timer = 0
        self.tactic_duration = 0
        
        # Evasion behavior
        self.dodge_timer = 0
        self.is_dodging = False
        self.dodge_direction = 1
        
        # Attack/Shoot mechanics
        self.attack_cooldown = 0
        self.attack_cooldown_max = random.randint(60, 100)  # Fast attacks
        self.is_attacking = False
        self.attack_frame_trigger = 3  # Shoot on frame 3
        self.attack_windup_pause_frame = 1  # Pause at frame 1
        self.attack_pause_timer = 0
        self.attack_pause_duration = 25  # Quick attack
        self.has_shot_fireball = False
        
        # Quick-fire mode (shoots multiple times rapidly)
        self.burst_fire_mode = False
        self.burst_shots_remaining = 0
        self.burst_shot_cooldown = 0
        
        # Health
        self.health = 2
        self.max_health = 2
        self.is_dead = False
        self.hurt_flash_timer = 0
        self.invincible = False
        self.invincible_timer = 0
        
    def load_sprite_sheet(self, path, frame_count, target_height=80):
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
        surf = pygame.Surface((40, 56), pygame.SRCALPHA)
        pygame.draw.rect(surf, (150, 150, 200), (0, 0, 40, 56))
        pygame.draw.circle(surf, (255, 100, 50), (20, 20), 8)
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
        """Calculate distance to player"""
        if not player or getattr(player, 'is_dead', False):
            return None
        
        dx = player.hitbox.centerx - self.hitbox.centerx
        dy = player.hitbox.centery - self.hitbox.centery
        distance = abs(dx)
        
        return distance, dx, dy
    
    def decide_tactic(self, distance, dx):
        """Decide which combat tactic to use based on distance"""
        # If in danger zone, always retreat
        if distance < self.danger_zone:
            self.aggro_mode = False
            self.retreat_mode = True
            self.strafe_mode = False
            self.tactic_timer = random.randint(40, 70)
            return
        
        # If too far, chase player
        if distance > self.optimal_range_max + 50:
            self.aggro_mode = True
            self.retreat_mode = False
            self.strafe_mode = False
            self.tactic_timer = random.randint(50, 90)
            return
        
        # In optimal range - randomly choose between strafe and shoot
        if distance >= self.optimal_range_min and distance <= self.optimal_range_max:
            choice = random.randint(0, 2)
            if choice == 0:
                # Strafe
                self.strafe_mode = True
                self.aggro_mode = False
                self.retreat_mode = False
                self.strafe_direction = random.choice([-1, 1])
                self.tactic_timer = random.randint(30, 60)
            else:
                # Stop and shoot
                self.strafe_mode = False
                self.aggro_mode = False
                self.retreat_mode = False
                self.tactic_timer = random.randint(20, 40)
                
                # Occasionally do burst fire
                if random.randint(0, 3) == 0:
                    self.burst_fire_mode = True
                    self.burst_shots_remaining = 2
    
    def update(self, player=None, projectile_group=None):
        """Update Frost Golem's behavior and animation"""
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
        
        # Count down dodge timer
        if self.dodge_timer > 0:
            self.dodge_timer -= 1
            if self.dodge_timer == 0:
                self.is_dodging = False
        
        # --- ATTACKING STATE ---
        if self.is_attacking:
            self.animate_attack(projectile_group)
            self.update_hitbox_position()
            return
        
        # --- BURST FIRE MODE ---
        if self.burst_fire_mode:
            self.burst_shot_cooldown -= 1
            if self.burst_shot_cooldown <= 0 and self.burst_shots_remaining > 0:
                self.start_attack()
                self.burst_shots_remaining -= 1
                self.burst_shot_cooldown = 15  # Quick succession
                if self.burst_shots_remaining == 0:
                    self.burst_fire_mode = False
        
        # --- IDLING STATE (rarely happens) ---
        if self.is_idling:
            self.idle_timer -= 1
            if self.idle_timer <= 0:
                self.is_idling = False
                self.state = "walk"
            self.animate_idle()
            self.update_hitbox_position()
            return
        
        # --- INTELLIGENT COMBAT AI ---
        if player:
            result = self.check_player_distance(player)
            if result:
                distance, dx, dy = result
                
                # Enter tracking mode if player detected
                if distance < self.detection_range:
                    self.tracking_mode = True
                
                # Exit tracking mode if too far
                if distance > self.lose_interest_range:
                    self.tracking_mode = False
                    self.aggro_mode = False
                    self.retreat_mode = False
                    self.strafe_mode = False
                
                if self.tracking_mode:
                    # Always face the player
                    self.facing_right = dx > 0
                    
                    # Decide new tactic when timer runs out
                    if self.tactic_timer <= 0:
                        self.decide_tactic(distance, dx)
                    else:
                        self.tactic_timer -= 1
                    
                    # Execute current tactic
                    if self.retreat_mode:
                        # RUN AWAY - speed boost when panicking
                        self.speed = self.base_speed * 1.4
                        if dx > 0:
                            self.direction = -1
                        else:
                            self.direction = 1
                    
                    elif self.aggro_mode:
                        # CHASE PLAYER - normal speed
                        self.speed = self.base_speed * 1.1
                        if dx > 0:
                            self.direction = 1
                        else:
                            self.direction = -1
                    
                    elif self.strafe_mode:
                        # STRAFE - move perpendicular to player
                        self.speed = self.base_speed * 0.8
                        self.direction = self.strafe_direction
                        
                        # Don't strafe outside patrol bounds
                        if (self.direction == -1 and self.rect.left <= self.patrol_left + 50) or \
                           (self.direction == 1 and self.rect.right >= self.patrol_right - 50):
                            self.strafe_direction *= -1
                            self.direction = self.strafe_direction
                    
                    else:
                        # STAND AND SHOOT
                        self.direction = 0
                        self.speed = 0
                    
                    # Attack when in optimal range and cooldown ready
                    if self.optimal_range_min <= distance <= self.optimal_range_max + 30:
                        if self.attack_cooldown <= 0 and not self.retreat_mode:
                            self.start_attack()
                            self.attack_cooldown = random.randint(50, 90)
                    
                    # Random dodge when player is close (evasive maneuver)
                    if distance < 180 and not self.is_dodging and random.randint(0, 60) == 0:
                        self.is_dodging = True
                        self.dodge_timer = 20
                        self.dodge_direction = random.choice([-1, 1])
                        self.speed = self.base_speed * 2.5  # FAST dodge
        
        # Apply dodge movement
        if self.is_dodging:
            self.direction = self.dodge_direction
        
        # --- WALKING STATE ---
        if self.direction != 0:
            self.rect.x += self.speed * self.direction
        
        # Check patrol bounds only if NOT tracking
        if not self.tracking_mode:
            self.speed = self.base_speed  # Reset to normal speed
            
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
            
            # Rarely idle when patrolling
            if random.randint(0, 300) == 0:
                self.start_idle()
            
            # Occasional random attacks when patrolling
            if self.attack_cooldown <= 0 and random.randint(0, 150) == 0:
                self.start_attack()
                self.attack_cooldown = random.randint(120, 240)
        
        # --- ATTACK COOLDOWN ---
        self.attack_cooldown -= 1
        
        # Update hitbox to follow rect
        self.update_hitbox_position()
        
        # Animate walking or idle
        if self.direction != 0:
            self.animate_walk()
        else:
            # Ensure current_frame is within bounds before calling animate_idle
            self.current_frame = self.current_frame % len(self.idle_anim_frames)
            self.animate_idle()
    
    def start_idle(self):
        """Start idle animation"""
        self.is_idling = True
        self.idle_timer = random.randint(30, 60)  # Short idle
        self.idle_duration = self.idle_timer
        self.current_frame = 0
        self.frame_counter = 0.0
        self.state = "idle"
    
    def start_attack(self):
        """Start the attack animation sequence"""
        self.is_attacking = True
        self.has_shot_fireball = False
        self.attack_pause_timer = 0
        self.current_frame = 0
        self.frame_counter = 0.0
        self.state = "attack"
    
    def animate_idle(self):
        """Animate idle standing"""
        self.frame_counter += 0.12
        
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
    
    def animate_attack(self, projectile_group):
        """Handle attack animation and fireball shooting"""
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
        self.frame_counter += 0.18
        
        if self.frame_counter >= 1.0:
            self.frame_counter = 0.0
            self.current_frame += 1
            
            # Shoot fireball at frame 3 (when mouth opens)
            if self.current_frame == self.attack_frame_trigger and not self.has_shot_fireball:
                self.shoot_fireball(projectile_group)
                self.has_shot_fireball = True
            
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
    
    def shoot_fireball(self, projectile_group):
        """Create and launch a fireball from the mouth"""
        offset = 30 if self.facing_right else -30
        fireball_x = self.rect.centerx + offset
        fireball_y = self.rect.centery + 5
        
        direction = 1 if self.facing_right else -1
        fireball = Fireball(fireball_x, fireball_y, direction)
        projectile_group.add(fireball)
    
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
            
            # PANIC RESPONSE - immediately retreat when hit
            self.retreat_mode = True
            self.aggro_mode = False
            self.strafe_mode = False
            self.tactic_timer = random.randint(50, 80)
    
    def die(self):
        """Trigger death sequence"""
        self.is_dead = True
        self.state = "death"
        self.current_frame = 0
        self.frame_counter = 0.0
    
    def animate_death(self):
        """Play death animation and remove sprite"""
        self.frame_counter += 0.25
        
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