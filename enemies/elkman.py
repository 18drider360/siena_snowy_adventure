import pygame
import random

class Snowball(pygame.sprite.Sprite):
    """Projectile thrown by Elkman"""
    def __init__(self, x, y, direction):
        super().__init__()
        
        try:
            # Load and scale snowball image
            original = pygame.image.load("assets/images/2 Elkman/Snowball.png").convert_alpha()
            self.image = pygame.transform.scale(original, (30, 30))
        except:
            # Fallback white circle
            self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 255, 255), (15, 15), 15)
        
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = 6  # Horizontal speed
        self.speed_y = -2  # Slight upward velocity for natural arc
        self.gravity = 0.3  # Gravity pulls it down
        self.direction = direction  # -1 for left, 1 for right
        
    def update(self):
        """Move the snowball with gravity"""
        # Horizontal movement
        self.rect.x += self.speed_x * self.direction
        
        # Vertical movement with gravity
        self.speed_y += self.gravity
        self.rect.y += self.speed_y
        
        # Remove if off screen or hits ground (y > 600)
        if self.rect.x < -100 or self.rect.x > 10000 or self.rect.y > 600:
            self.kill()


class Elkman(pygame.sprite.Sprite):
    """Elk enemy - aggressive ranged attacker that stays on platform"""
    def __init__(self, x, y, patrol_left, patrol_right):
        super().__init__()
        
        # --- POWER EFFECTIVENESS CONFIGURATION ---
        self.vulnerable_to = {
            'stomp': True,
            'spin_attack': True,
            'roll': False
        }
        
        # --- LOAD ANIMATIONS ---
        try:
            self.idle_frames = self.load_sprite_sheet(
                "assets/images/2 Elkman/Elkman_idle.png",
                frame_count=4,
                target_height=120
            )
            self.walk_frames = self.load_sprite_sheet(
                "assets/images/2 Elkman/Elkman_walk.png",
                frame_count=4,
                target_height=120
            )
            self.attack_frames = self.load_sprite_sheet(
                "assets/images/2 Elkman/Elkman_attack.png",
                frame_count=6,
                target_height=120
            )
            self.hurt_frames = self.load_sprite_sheet(
                "assets/images/2 Elkman/Elkman_hurt.png",
                frame_count=2,  
                target_height=120
            )
            self.death_frames = self.load_sprite_sheet(
                "assets/images/2 Elkman/Elkman_death.png",
                frame_count=4,
                target_height=120
            )
        except Exception as e:
            print(f"Error loading Elkman sprites: {e}")
            self.idle_frames = [self.create_fallback_sprite()]
            self.walk_frames = [self.create_fallback_sprite()]
            self.attack_frames = [self.create_fallback_sprite()]
            self.hurt_frames = [self.create_fallback_sprite()]
            self.death_frames = [self.create_fallback_sprite()]
        
        # --- INITIAL STATE ---
        self.image = self.walk_frames[0]
        self.rect = self.image.get_rect(midbottom=(x, y))
        
        self.hitbox = pygame.Rect(0, 0, 50, 80)
        self.hitbox.midbottom = self.rect.midbottom
        self.hitbox_offset_x = -30
        self.sprite_offset = 20
        
        # Animation
        self.current_frame = 0
        self.frame_counter = 0.0
        self.animation_speed = 0.18
        
        # --- PLATFORM BOUNDARY ENFORCEMENT ---
        self.platform_left = patrol_left
        self.platform_right = patrol_right
        self.enforce_boundaries = True  # Keep on platform
        
        # Movement - More aggressive, less retreat
        self.base_speed = 1.8  # Slower base speed for more controlled movement
        self.speed = self.base_speed + random.uniform(-0.2, 0.2)  # Slight variation to prevent grouping
        self.direction = random.choice([-1, 1])  # Random starting direction
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right
        
        # State
        self.state = "walk"
        self.facing_right = self.direction == 1
        
        # --- IMPROVED BEHAVIOR ---
        self.tracking_mode = False
        self.detection_range = 500  # When to notice player
        self.attack_range_min = 100  # Minimum attack range
        self.attack_range_max = 400  # Maximum attack range
        self.optimal_range = 250  # Preferred distance
        self.personal_space = 80  # Only retreat if closer than this
        
        # Attack mechanics - MUCH more aggressive
        self.attack_cooldown = random.randint(30, 60)  # Start with varied cooldown
        self.attack_cooldown_min = 80  # Less frequent attacks
        self.attack_cooldown_max = 140
        self.is_attacking = False
        self.attack_frame_trigger = 3
        self.attack_windup_pause_frame = 2
        self.attack_pause_timer = 0
        self.attack_pause_duration = 15  # Shorter windup
        self.has_thrown_snowball = False
        
        # Health
        self.health = 1  # One-hit enemy
        self.max_health = 1
        self.is_dead = False
        self.hurt_flash_timer = 0
        self.invincible = False
        self.invincible_timer = 0
        
        # Gravity for physics
        self.vel_y = 0
        self.gravity = 0.6
        
    def load_sprite_sheet(self, path, frame_count, target_height=120):
        sheet = pygame.image.load(path).convert_alpha()
        sheet_width, sheet_height = sheet.get_size()
        frame_width = sheet_width // frame_count
        
        frames = []
        for i in range(frame_count):
            frame = pygame.Surface((frame_width, sheet_height), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), (i * frame_width, 0, frame_width, sheet_height))
            aspect = frame_width / sheet_height
            scaled = pygame.transform.scale(frame, (int(target_height * aspect), target_height))
            frames.append(scaled)
        return frames
    
    def create_fallback_sprite(self):
        surf = pygame.Surface((60, 80), pygame.SRCALPHA)
        pygame.draw.rect(surf, (100, 150, 200), (0, 0, 60, 80))
        return surf
    
    def update_hitbox_position(self):
        self.hitbox.midbottom = self.rect.midbottom
        if self.facing_right:
            self.hitbox.x += self.hitbox_offset_x
        else:
            self.hitbox.x -= self.hitbox_offset_x
    
    def update(self, player=None, projectile_group=None):
        """Update Elkman's behavior and animation"""
        if self.is_dead:
            self.animate_death()
            return
        
        # Count down timers
        if self.hurt_flash_timer > 0:
            self.hurt_flash_timer -= 1
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
            if self.invincible_timer == 0:
                self.invincible = False
        
        # --- ATTACKING STATE ---
        if self.is_attacking:
            self.animate_attack(projectile_group)
            self.update_hitbox_position()
            return
        
        # --- BEHAVIOR AI ---
        should_move = True
        move_direction = self.direction
        
        if player and not player.is_dead:
            dx = player.hitbox.centerx - self.hitbox.centerx
            distance = abs(dx)
            
            # Detect player
            if distance < self.detection_range:
                self.tracking_mode = True
                
                # Face player
                self.facing_right = dx > 0
                
                # Determine action based on distance
                if distance < self.personal_space:
                    # TOO CLOSE - back up slightly but still attack
                    move_direction = -1 if dx > 0 else 1
                    # Attack while backing up (aggressive!)
                    if self.attack_cooldown <= 0:
                        self.start_attack()
                        self.attack_cooldown = random.randint(self.attack_cooldown_min, self.attack_cooldown_max)
                
                elif distance < self.attack_range_max:
                    # IN RANGE - Stop moving and attack frequently
                    should_move = False
                    
                    # Attack much more frequently
                    if self.attack_cooldown <= 0:
                        self.start_attack()
                        self.attack_cooldown = random.randint(self.attack_cooldown_min, self.attack_cooldown_max)
                
                else:
                    # TOO FAR - Move toward player
                    move_direction = 1 if dx > 0 else -1
            else:
                # Out of range - patrol
                self.tracking_mode = False
        
        # --- MOVEMENT WITH PLATFORM BOUNDARIES ---
        if should_move:
            new_x = self.rect.x + (self.speed * move_direction)
            
            # Check platform boundaries before moving
            if self.enforce_boundaries:
                # Keep hitbox center within platform bounds
                future_hitbox_center = new_x + (self.rect.width // 2) + (self.hitbox_offset_x if not self.facing_right else -self.hitbox_offset_x)
                
                                    # Only move if staying within boundaries
                if self.platform_left <= future_hitbox_center <= self.platform_right:
                    self.rect.x = new_x
                    self.direction = move_direction
                else:
                    # Hit boundary - turn around if patrolling
                    if not self.tracking_mode:
                        self.direction *= -1
                        self.facing_right = not self.facing_right
                    # If tracking but at edge, stop and shoot (less frequently)
                    elif self.attack_cooldown <= 0 and random.randint(0, 2) == 0:  # 33% chance
                        self.start_attack()
                        self.attack_cooldown = random.randint(100, 160)
            else:
                self.rect.x = new_x
                self.direction = move_direction
        
        # --- PATROL BOUNDS (when not enforcing platform boundaries) ---
        if not self.tracking_mode and not self.enforce_boundaries:
            if self.direction == -1 and self.rect.left <= self.patrol_left:
                self.direction = 1
                self.facing_right = True
            elif self.direction == 1 and self.rect.right >= self.patrol_right:
                self.direction = -1
                self.facing_right = False
        
        # Count down attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # Random attacks while patrolling (very rare)
        if not self.tracking_mode and self.attack_cooldown <= 0 and random.randint(0, 300) == 0:
            self.start_attack()
            self.attack_cooldown = random.randint(180, 280)
        
        self.update_hitbox_position()
        self.animate_walk()
    
    def start_attack(self):
        """Start the attack animation sequence"""
        self.is_attacking = True
        self.has_thrown_snowball = False
        self.attack_pause_timer = 0
        self.current_frame = 0
        self.frame_counter = 0.0
        self.state = "attack"
    
    def animate_attack(self, snowball_group):
        """Handle attack animation and snowball throwing"""
        # Pause at windup frame
        if self.current_frame == self.attack_windup_pause_frame and self.attack_pause_timer < self.attack_pause_duration:
            self.attack_pause_timer += 1
            old_bottom = self.rect.bottom
            old_centerx = self.rect.centerx
            
            base_image = self.hurt_frames[0] if self.hurt_flash_timer > 0 else self.attack_frames[self.current_frame]
            self.image = pygame.transform.flip(base_image, True, False) if self.facing_right else base_image
            
            self.rect = self.image.get_rect(centerx=old_centerx, bottom=old_bottom)
            self.update_hitbox_position()
            return
        
        # Continue animation
        self.frame_counter += 0.25  # Faster attack animation
        
        if self.frame_counter >= 1.0:
            self.frame_counter = 0.0
            self.current_frame += 1
            
            # Throw snowball at trigger frame
            if self.current_frame == self.attack_frame_trigger and not self.has_thrown_snowball:
                self.throw_snowball(snowball_group)
                self.has_thrown_snowball = True
            
            # End attack
            if self.current_frame >= len(self.attack_frames):
                self.is_attacking = False
                self.state = "walk"
                self.current_frame = 0
                return
        
        old_bottom = self.rect.bottom
        old_centerx = self.rect.centerx
        
        base_image = self.hurt_frames[0] if self.hurt_flash_timer > 0 else self.attack_frames[self.current_frame]
        self.image = pygame.transform.flip(base_image, True, False) if self.facing_right else base_image
        
        self.rect = self.image.get_rect(centerx=old_centerx, bottom=old_bottom)
        self.update_hitbox_position()
    
    def throw_snowball(self, snowball_group):
        """Create and launch a snowball"""
        offset = 50 if self.facing_right else -50
        snowball_x = self.rect.centerx + offset
        snowball_y = self.rect.centery - 30
        
        direction = 1 if self.facing_right else -1
        snowball = Snowball(snowball_x, snowball_y, direction)
        
        # Store sound reference on snowball for main.py to play
        snowball.spawn_sound = True
        
        snowball_group.add(snowball)
    
    def animate_walk(self):
        """Animate walking"""
        self.frame_counter += self.animation_speed
        
        if self.frame_counter >= 1.0:
            self.frame_counter = 0.0
            self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
        
        old_bottom = self.rect.bottom
        old_centerx = self.rect.centerx
        
        base_image = self.hurt_frames[0] if self.hurt_flash_timer > 0 else self.walk_frames[self.current_frame]
        self.image = pygame.transform.flip(base_image, True, False) if self.facing_right else base_image
        
        self.rect = self.image.get_rect(centerx=old_centerx, bottom=old_bottom)
        self.update_hitbox_position()
    
    def take_damage(self, damage=1):
        """Handle taking damage"""
        if self.is_dead or self.invincible:
            return False
        
        self.health -= damage
        
        if self.health <= 0:
            self.die()
        else:
            self.hurt_flash_timer = 20
            self.invincible = True
            self.invincible_timer = 60
        
        return True
    
    def die(self):
        """Trigger death sequence"""
        self.is_dead = True
        self.state = "death"
        self.current_frame = 0
        self.frame_counter = 0.0
    
    def animate_death(self):
        """Play death animation and remove sprite"""
        self.frame_counter += 0.18
        
        if self.frame_counter >= 1.0:
            self.frame_counter = 0.0
            self.current_frame += 1
            
            if self.current_frame >= len(self.death_frames):
                self.kill()
                return
        
        old_bottom = self.rect.bottom
        old_centerx = self.rect.centerx
        
        base_image = self.death_frames[self.current_frame]
        self.image = pygame.transform.flip(base_image, True, False) if self.facing_right else base_image
        
        self.rect = self.image.get_rect(centerx=old_centerx, bottom=old_bottom)
        self.update_hitbox_position()