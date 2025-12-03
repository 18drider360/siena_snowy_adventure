import pygame
import random

class Spike(pygame.sprite.Sprite):
    """Spike projectile shot by Spiked Slime"""
    def __init__(self, x, y, direction):
        super().__init__()
        
        try:
            spike_sheet = pygame.image.load("assets/images/4 Spiked_slime/Spikes.png").convert_alpha()
            self.image = spike_sheet
            self.image = pygame.transform.scale(self.image, (35, 35))
        except Exception as e:
            print(f"Error loading spike sprite: {e}")
            self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.polygon(self.image, (150, 150, 150), [(10, 0), (20, 20), (0, 20)])
        
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = 5
        self.direction = direction
        self.speed_y = -8
        self.gravity = 0.5
        self.ground_y = 570
        
    def update(self):
        """Move the spike in an arc"""
        self.rect.x += self.speed_x * self.direction
        self.speed_y += self.gravity
        self.rect.y += self.speed_y
        
        if self.rect.bottom >= self.ground_y or self.rect.x < -100 or self.rect.x > 10000:
            self.kill()


class SpikedSlime(pygame.sprite.Sprite):
    """Spiked Slime - aggressive melee-focused enemy that stays on platform"""
    def __init__(self, x, y, patrol_left, patrol_right):
        super().__init__()

        # --- POWER EFFECTIVENESS CONFIGURATION ---
        self.vulnerable_to = {
            'stomp': True,
            'spin_attack': False,
            'roll': True
        }
        
        # --- LOAD ANIMATIONS ---
        try:
            self.idle_frames = self.load_sprite_sheet(
                "assets/images/4 Spiked_slime/Spiked_slime.png",
                frame_count=1,
                target_height=80
            )
            self.walk_frames = self.load_sprite_sheet(
                "assets/images/4 Spiked_slime/Spiked_slime_walk.png",
                frame_count=4,
                target_height=80
            )
            self.idle_anim_frames = self.load_sprite_sheet(
                "assets/images/4 Spiked_slime/Spiked_slime_idle.png",
                frame_count=4,
                target_height=80
            )
            self.hurt_frames = self.load_sprite_sheet(
                "assets/images/4 Spiked_slime/Spiked_slime_hurt.png",
                frame_count=2,
                target_height=80
            )
            self.death_frames = self.load_sprite_sheet(
                "assets/images/4 Spiked_slime/Spiked_slime_death.png",
                frame_count=4,
                target_height=80
            )
            self.attack_frames = self.load_sprite_sheet(
                "assets/images/4 Spiked_slime/Spiked_slime_attack.png",
                frame_count=4,
                target_height=80
            )
        except Exception as e:
            print(f"Error loading Spiked Slime sprites: {e}")
            self.idle_frames = [self.create_fallback_sprite()]
            self.walk_frames = [self.create_fallback_sprite()]
            self.idle_anim_frames = [self.create_fallback_sprite()]
            self.hurt_frames = [self.create_fallback_sprite()]
            self.death_frames = [self.create_fallback_sprite()]
            self.attack_frames = [self.create_fallback_sprite()]
        
        # --- INITIAL STATE ---
        self.image = self.walk_frames[0]
        self.rect = self.image.get_rect(midbottom=(x, y))
        
        self.hitbox = pygame.Rect(0, 0, 45, 35)
        self.hitbox.midbottom = self.rect.midbottom
        self.hitbox_offset_x = -5
        self.sprite_offset = 8
        
        # Animation
        self.current_frame = 0
        self.frame_counter = 0.0
        self.animation_speed = 0.12
        
        # --- PLATFORM BOUNDARY ENFORCEMENT ---
        self.platform_left = patrol_left
        self.platform_right = patrol_right
        self.enforce_boundaries = False  # Let them chase off platform!
        self.home_platform_left = patrol_left  # Remember home for patrol
        self.home_platform_right = patrol_right
        
        # Movement - Melee focused
        self.base_speed = 1.5  # Moderate speed
        self.speed = self.base_speed + random.uniform(-0.15, 0.15)  # Slight variation
        self.chase_speed = 2.2  # Faster when chasing
        self.direction = random.choice([-1, 1])
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right
        
        # State
        self.state = "walk"
        self.facing_right = self.direction == 1
        
        # --- MELEE-FOCUSED BEHAVIOR ---
        self.tracking_mode = False
        self.detection_range = 500  # Notice player from farther away
        self.melee_preference_range = 450  # Almost always prefers melee
        self.spike_range_max = 350  # Only shoots if really far
        
        # Movement personality - add variety
        self.aggression_level = random.uniform(0.8, 1.2)  # Some are more aggressive
        self.zigzag_enabled = random.choice([True, False])  # Some zigzag when chasing
        self.zigzag_timer = 0
        self.zigzag_offset = 0
        
        # Attack mechanics - Very rare spikes, strongly prefers melee
        self.attack_cooldown = random.randint(200, 300)  # Much longer cooldown
        self.attack_cooldown_min = 240  # Very infrequent
        self.attack_cooldown_max = 360  # Up to 6 seconds between spikes
        self.is_attacking = False
        self.attack_frame_trigger = 2
        self.attack_windup_pause_frame = 1
        self.attack_pause_timer = 0
        self.attack_pause_duration = 30
        self.has_shot_spikes = False
        
        # Idle behavior
        self.idle_timer = 0
        self.is_idling = False
        
        # Health
        self.health = 1  # One-hit enemy
        self.max_health = 1
        self.is_dead = False
        self.death_complete = False  # Flag for when death animation finishes
        self.hurt_flash_timer = 0
        self.invincible = False
        self.invincible_timer = 0

        # Gravity
        self.vel_y = 0
        self.gravity = 0.6

        # Knockback
        self.knockback_velocity = 0
        self.knockback_decay = 0.85

        # Load attack sound
        try:
            self.attack_sound = pygame.mixer.Sound("assets/sounds/enemy_projectile.ogg")
            self.attack_sound.set_volume(0.3)
        except Exception as e:
            # Silently fail if mixer not initialized
            self.attack_sound = None
        
    def load_sprite_sheet(self, path, frame_count, target_height=80):
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
        surf = pygame.Surface((40, 56), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (100, 200, 150), (0, 20, 40, 36))
        pygame.draw.circle(surf, (80, 80, 80), (15, 30), 3)
        pygame.draw.circle(surf, (80, 80, 80), (25, 30), 3)
        return surf
    
    def update_hitbox_position(self):
        self.hitbox.midbottom = self.rect.midbottom
        if self.facing_right:
            self.hitbox.x += self.hitbox_offset_x
        else:
            self.hitbox.x -= self.hitbox_offset_x
    
    def update(self, player=None, projectile_group=None):
        """Update Spiked Slime's behavior and animation"""
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

        # Apply knockback
        if self.knockback_velocity != 0:
            self.rect.x += self.knockback_velocity
            self.knockback_velocity *= self.knockback_decay
            if abs(self.knockback_velocity) < 0.5:
                self.knockback_velocity = 0

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
            self.current_frame = self.current_frame % len(self.idle_anim_frames)
            self.animate_idle()
            self.update_hitbox_position()
            return
        
        # --- MELEE-FOCUSED AI ---
        current_speed = self.speed
        should_move = True
        move_direction = self.direction
        
        if player and not player.is_dead:
            dx = player.hitbox.centerx - self.hitbox.centerx
            distance = abs(dx)
            
            # Detect player
            if distance < self.detection_range:
                self.tracking_mode = True
                self.facing_right = dx > 0
                
                # AGGRESSIVE MELEE CHASE - This is the primary behavior
                if distance < self.melee_preference_range:
                    # RUSH IN for melee contact!
                    current_speed = self.chase_speed * self.aggression_level
                    move_direction = 1 if dx > 0 else -1
                    
                    # Add zigzag movement for variety (some slimes do this)
                    if self.zigzag_enabled:
                        self.zigzag_timer += 1
                        if self.zigzag_timer > 30:  # Change direction every 0.5 seconds
                            self.zigzag_timer = 0
                            self.zigzag_offset = random.choice([-1, 0, 1])
                        
                        # Occasionally move perpendicular briefly
                        if self.zigzag_offset != 0 and random.randint(0, 10) == 0:
                            move_direction = self.zigzag_offset
                    
                    # EXTREMELY RARE spike throw while chasing (only 1% chance)
                    if self.attack_cooldown <= 0 and random.randint(0, 99) == 0:
                        self.start_attack()
                        self.attack_cooldown = random.randint(240, 360)
                
                else:
                    # Too far for effective melee - move toward player first
                    current_speed = self.speed * 1.1
                    move_direction = 1 if dx > 0 else -1
                    
                    # Only shoot spikes if REALLY far (10% chance when far)
                    if distance > self.spike_range_max and self.attack_cooldown <= 0:
                        if random.randint(0, 9) == 0:  # 10% chance
                            self.start_attack()
                            self.attack_cooldown = random.randint(self.attack_cooldown_min, self.attack_cooldown_max)
            else:
                self.tracking_mode = False
        
        # --- MOVEMENT WITH SMART BOUNDARIES ---
        if should_move and move_direction != 0:
            new_x = self.rect.x + (current_speed * move_direction)
            
            # Only enforce boundaries when NOT tracking (i.e., when patrolling)
            if not self.tracking_mode and self.enforce_boundaries:
                future_hitbox_center = new_x + (self.rect.width // 2) + (self.hitbox_offset_x if not self.facing_right else -self.hitbox_offset_x)
                
                if self.platform_left <= future_hitbox_center <= self.platform_right:
                    self.rect.x = new_x
                    self.direction = move_direction
                else:
                    # Hit patrol boundary while patrolling - turn around
                    self.direction *= -1
                    self.facing_right = not self.facing_right
            else:
                # Tracking player OR no boundary enforcement - move freely!
                self.rect.x = new_x
                self.direction = move_direction
        
        # --- PATROL BOUNDS (only when NOT tracking) ---
        if not self.tracking_mode and not self.enforce_boundaries:
            # Use home platform for patrol boundaries
            if self.direction == -1 and self.rect.left <= self.home_platform_left:
                self.direction = 1
                self.facing_right = True
            elif self.direction == 1 and self.rect.right >= self.home_platform_right:
                self.direction = -1
                self.facing_right = False
            
            # Rare idle when patrolling
            if random.randint(0, 300) == 0:
                self.start_idle()
        
        # Count down attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        self.update_hitbox_position()
        self.animate_walk()
    
    def start_idle(self):
        """Start idle animation"""
        self.is_idling = True
        self.idle_timer = random.randint(40, 80)
        self.idle_duration = self.idle_timer
        self.current_frame = 0
        self.frame_counter = 0.0
        self.state = "idle"
    
    def start_attack(self):
        """Start the attack animation sequence"""
        self.is_attacking = True
        self.has_shot_spikes = False
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
        
        self.current_frame = self.current_frame % len(self.idle_anim_frames)
        
        old_bottom = self.rect.bottom
        old_centerx = self.rect.centerx
        
        base_image = self.hurt_frames[0] if self.hurt_flash_timer > 0 else self.idle_anim_frames[self.current_frame]
        self.image = pygame.transform.flip(base_image, True, False) if self.facing_right else base_image
        
        self.rect = self.image.get_rect(centerx=old_centerx, bottom=old_bottom)
        self.update_hitbox_position()
    
    def animate_attack(self, projectile_group, player=None):
        """Handle attack animation and spike shooting"""
        # Pause at windup
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
        self.frame_counter += 0.18
        
        if self.frame_counter >= 1.0:
            self.frame_counter = 0.0
            self.current_frame += 1
            
            # Shoot spikes
            if self.current_frame == self.attack_frame_trigger and not self.has_shot_spikes:
                self.shoot_spikes(projectile_group, player)
                self.has_shot_spikes = True
            
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
    
    def shoot_spikes(self, projectile_group, player=None):
        """Shoot 2 spikes in a spread pattern (reduced from 3)"""
        spike_x = self.rect.centerx
        spike_y = self.rect.centery - 10

        direction = 1 if self.facing_right else -1

        # Create 2 spikes with different trajectories
        for i in range(2):
            spike = Spike(spike_x, spike_y, direction)
            spike.speed_y = -8 - (i * 3)  # -8, -11
            spike.speed_x = 5 + (i * 0.5)
            projectile_group.add(spike)

        # Play attack sound only if player is nearby (within 600 pixels)
        if self.attack_sound and player:
            distance = abs(player.hitbox.centerx - self.hitbox.centerx)
            if distance < 600:
                self.attack_sound.play()
    
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
        self.frame_counter += 0.20

        if self.frame_counter >= 1.0:
            self.frame_counter = 0.0
            self.current_frame += 1

            if self.current_frame >= len(self.death_frames):
                self.death_complete = True
                self.kill()
                return

        # Safety check: ensure current_frame is within bounds
        if self.current_frame >= len(self.death_frames):
            self.death_complete = True
            self.kill()
            return

        old_bottom = self.rect.bottom
        old_centerx = self.rect.centerx

        base_image = self.death_frames[self.current_frame]
        self.image = pygame.transform.flip(base_image, True, False) if self.facing_right else base_image
        
        self.rect = self.image.get_rect(centerx=old_centerx, bottom=old_bottom)
        self.update_hitbox_position()