import pygame
from utils import settings as S
import constants as C

class Siena(pygame.sprite.Sprite):
    def __init__(self, x=100, y=500, abilities=None, max_health=6):
        super().__init__()
        
        # --- ABILITY SYSTEM ---
        # Default: all abilities unlocked
        default_abilities = {
            'walk': True,
            'crouch': True,
            'jump': True,
            'double_jump': True,
            'roll': True,
            'spin': True
        }
        
        # If abilities dict provided, merge with defaults
        if abilities is not None:
            self.abilities = {**default_abilities, **abilities}
        else:
            self.abilities = default_abilities

        try:
            # --- WALK FRAMES ---
            self.walk_frames = self.load_sprite_sheet(
                "assets/images/siena/Walk.png",
                frame_count=6,
                target_height=180
            )

            # --- IDLE FRAMES (2 frames) ---
            self.idle_frames = self.load_sprite_sheet(
                "assets/images/siena/Idle.png",
                frame_count=2,
                target_height=180
            )

            # --- JUMP FRAMES (2 total: rising + falling) ---
            self.jump_frames = self.load_sprite_sheet(
                "assets/images/siena/Jump.png",
                frame_count=2,
                target_height=180
            )

            # --- ROLL FRAMES (4 total) ---
            self.roll_frames = self.load_sprite_sheet(
                "assets/images/siena/Roll.png",
                frame_count=4,
                target_height=145
            )

            self.crouch_frames = self.load_sprite_sheet(
                "assets/images/siena/Crouch.png",
                frame_count=1,
                target_height=145
            )

            # --- FLAP FRAMES (2 total for double jump) ---
            self.flap_frames = self.load_sprite_sheet(
                "assets/images/siena/Flap.png",
                frame_count=2,
                target_height=180
            )

            # --- SPIN ATTACK FRAMES (7 frames) ---
            self.spin_frames = self.load_sprite_sheet(
                "assets/images/siena/Spin Attack.png",
                frame_count=7,
                target_height=180
            )

            # --- HURT FRAMES (4 total) ---
            self.hurt_frames = self.load_sprite_sheet(
                "assets/images/siena/Hurt.png",
                frame_count=4,
                target_height=180
            )

            # --- DEATH FRAME (1 image) ---
            self.death_frames = self.load_sprite_sheet(
                "assets/images/siena/Death.png",
                frame_count=1,
                target_height=180
            )

        except Exception as e:
            self.walk_frames = [self.create_fallback_sprite()]
            self.idle_frames = [self.create_fallback_sprite(), self.create_fallback_sprite()]
            self.jump_frames = [self.create_fallback_sprite(), self.create_fallback_sprite()]
            self.roll_frames = [self.create_fallback_sprite()]
            self.crouch_frames = [self.create_fallback_sprite()]
            self.flap_frames = [self.create_fallback_sprite()]
            self.spin_frames = [self.create_fallback_sprite()]
            self.hurt_frames = [self.create_fallback_sprite()]
            self.death_frames = [self.create_fallback_sprite()]

        # --- INITIAL STATE ---
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect(midbottom=(x, y))

        # Create a tight hitbox that fits the penguin closely
        self.hitbox = pygame.Rect(0, 0, *C.PLAYER_HITBOX_NORMAL)
        self.hitbox.midbottom = self.rect.midbottom

        # Define hitbox sizes for different states
        self.hitbox_normal = C.PLAYER_HITBOX_NORMAL
        self.hitbox_crouch = C.PLAYER_HITBOX_CROUCH
        self.hitbox_roll = C.PLAYER_HITBOX_ROLL

        self.current_frame = 0
        self.frame_counter = 0.0
        self.animation_speed = 0.15

        # Movement
        self.speed = C.PLAYER_SPEED
        self.gravity = C.PLAYER_GRAVITY
        self.jump_strength = C.PLAYER_JUMP_STRENGTH
        self.vel_y = 0

        # State
        self.facing_right = True
        self.is_moving = False
        self.on_ground = True  # Start on ground to prevent initial fall
        self.is_rolling = False
        self.is_crouching = False
        self.is_flapping = False
        self.has_double_jump = False
        self.jump_held = False
        self.flap_timer = 0.0
        self.flap_duration = 0.3
        self.roll_timer = 0.0
        self.roll_offset_y = -10
        self.roll_duration = len(self.roll_frames) / 10.0
        self.roll_cooldown = 0  # Cooldown timer in frames (60 fps)
        
        # --- ROLL SPEED SETTINGS ---
        self.roll_speed_initial = C.PLAYER_ROLL_SPEED_INITIAL
        self.roll_speed_max = 12
        self.roll_speed_current = self.roll_speed_initial
        self.roll_acceleration = 0.15
        
        # --- ROLL STAMINA SETTINGS ---
        self.roll_stamina_max = C.PLAYER_ROLL_STAMINA_MAX
        self.roll_stamina = self.roll_stamina_max
        self.roll_stamina_recharge_rate = 0.4
        self.roll_stamina_recharge_delay = C.PLAYER_ROLL_STAMINA_RECHARGE_DELAY
        self.roll_stamina_delay_timer = 0

        # --- SPIN ATTACK STATE ---
        self.is_spinning = False
        self.spin_timer = 0.0
        self.spin_duration = len(self.spin_frames) / 20.0
        self.spin_speed = C.PLAYER_SPIN_SPEED
        self.has_used_spin = False
        
        # --- SPIN CHARGE SYSTEM ---
        self.spin_charges_max = 3
        self.spin_charges = 3
        self.spin_charge_cooldown = C.PLAYER_SPIN_CHARGE_COOLDOWN
        self.spin_charge_timers = []

        # --- HEALTH SYSTEM ---
        self.max_health = max_health
        self.health = max_health
        self.is_hurt = False
        self.hurt_timer = 0
        self.hurt_duration = C.PLAYER_HURT_DURATION
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = C.PLAYER_INVINCIBLE_DURATION
        self.is_dead = False

        # --- KNOCKBACK ---
        self.knockback_velocity = 0
        self.knockback_strength = C.PLAYER_KNOCKBACK_STRENGTH
        self.knockback_y_boost = -5

    # ------------------------------------------------------------------
    def load_sprite_sheet(self, path, frame_count, target_height=160):
        """Splits a horizontal sprite sheet into individual frames."""
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

    # ------------------------------------------------------------------
    def create_fallback_sprite(self):
        """Fallback simple ellipse sprite."""
        surf = pygame.Surface((80, 100), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (0, 0, 0), (0, 0, 80, 100))
        return surf

    # ------------------------------------------------------------------
    def update_hitbox_position(self):
        """Update hitbox to follow rect with state-based sizing"""
        if self.is_rolling:
            self.hitbox.width, self.hitbox.height = self.hitbox_roll
        elif self.is_crouching:
            self.hitbox.width, self.hitbox.height = self.hitbox_crouch
        else:
            self.hitbox.width, self.hitbox.height = self.hitbox_normal
        
        # Position hitbox at the bottom center of the sprite
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.bottom = self.rect.bottom
        
        # Adjust offsets so penguin sits lower in the hitbox
        if self.is_rolling:
            self.hitbox.y -= 72  # Offset for rolling
        elif self.is_crouching:
            self.hitbox.y -= 70  # Offset for crouching
        else:
            self.hitbox.y -= 90  # Move hitbox up so penguin fits tightly

    # ------------------------------------------------------------------
    def take_damage(self, damage=1, knockback_direction=0):
        """Handle taking damage with knockback
        
        Args:
            damage: Amount of damage to take
            knockback_direction: -1 for left, 1 for right, 0 for no knockback
        """
        if self.invincible or self.is_dead:
            return False
        
        self.health -= damage
        
        if self.health <= 0:
            self.health = 0
            self.die()
        else:
            self.start_hurt(knockback_direction)
        
        return True

    # ------------------------------------------------------------------
    def start_hurt(self, knockback_direction=0):
        """Start hurt animation, invincibility, and knockback
        
        Args:
            knockback_direction: -1 for left, 1 for right, 0 for no knockback
        """
        self.is_hurt = True
        self.hurt_timer = self.hurt_duration
        self.invincible = True
        self.invincible_timer = self.invincible_duration
        self.current_frame = 0
        self.frame_counter = 0.0
        
        # Apply knockback
        if knockback_direction != 0:
            self.knockback_velocity = -knockback_direction * self.knockback_strength
            self.vel_y = self.knockback_y_boost

    # ------------------------------------------------------------------
    def die(self):
        """Trigger death"""
        self.is_dead = True
        self.current_frame = 0
        self.frame_counter = 0.0
        self.vel_y = 0

    # ------------------------------------------------------------------
    def spin_attack(self, sound=None):
        """Trigger spin attack if in the air and charges available"""
        # Check if spin ability is unlocked
        if not self.abilities.get('spin', False):
            return

        if self.is_dead or self.is_hurt or self.on_ground or self.is_spinning:
            return

        # Check if we have charges available
        if self.spin_charges <= 0:
            return

        # Consume one charge
        self.spin_charges -= 1

        # Add a new recharge timer to the queue
        self.spin_charge_timers.append(self.spin_charge_cooldown)

        self.is_spinning = True
        self.spin_timer = 0.0
        self.current_frame = 0
        self.frame_counter = 0.0
        self.is_flapping = False

        # Play spin attack sound
        if sound:
            sound.play()

    # ------------------------------------------------------------------
    def ground_pound(self):
        """Trigger ground pound"""
        self.is_ground_pounding = True
        self.current_frame = 0
        self.frame_counter = 0.0
        self.vel_y = self.ground_pound_speed
        self.is_spinning = False
        self.is_flapping = False

    # ------------------------------------------------------------------
    def update(self, keys_pressed):
        """Handles movement, jumping, rolling, crouching, and animation."""
        
        if self.is_dead:
            self.animate_death()
            self.update_hitbox_position()
            return

        if self.is_hurt:
            self.hurt_timer -= 1
            if self.hurt_timer <= 0:
                self.is_hurt = False
                self.knockback_velocity = 0
            
            # Apply knockback movement
            if self.knockback_velocity != 0:
                self.rect.x += self.knockback_velocity
                # Gradually reduce knockback
                self.knockback_velocity *= 0.85
                if abs(self.knockback_velocity) < 0.5:
                    self.knockback_velocity = 0
            
            # Apply gravity during hurt
            self.vel_y += self.gravity
            self.rect.y += self.vel_y
            
            self.animate_hurt()
            self.update_hitbox_position()
            return

        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

        self.is_moving = False

        # --- SPIN ATTACK STATE ---
        if self.is_spinning:
            self.spin_timer += 1 / 60
            
            direction = 1 if self.facing_right else -1
            if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
                direction = -1
            elif keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
                direction = 1
            
            self.rect.x += self.spin_speed * direction
            
            if self.spin_timer >= self.spin_duration:
                self.is_spinning = False
                self.spin_timer = 0.0
                self.current_frame = 0
                self.frame_counter = 0.0
            
            if self.is_spinning:
                self.animate()
                self.update_hitbox_position()
                return

        # --- ROLLING STATE ---
        if self.is_rolling:
            # Consume stamina while rolling
            self.roll_stamina -= 1
            self.roll_stamina_delay_timer = self.roll_stamina_recharge_delay
            
            # Stop rolling if stamina depleted
            if self.roll_stamina <= 0:
                self.roll_stamina = 0
                self.is_rolling = False
                self.roll_timer = 0.0
                self.roll_speed_current = self.roll_speed_initial
            
            # Continue rolling even when airborne (removed on_ground check)
            if self.is_rolling:
                # Accelerate roll speed up to maximum
                if self.roll_speed_current < self.roll_speed_max:
                    self.roll_speed_current += self.roll_acceleration
                    if self.roll_speed_current > self.roll_speed_max:
                        self.roll_speed_current = self.roll_speed_max

                # Check if player still wants to roll (holding down + direction)
                still_holding_roll = (
                    (keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s])
                    and (keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]
                        or keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d])
                )
                
                # Stop rolling if keys released OR landed on ground without holding roll keys
                if not still_holding_roll:
                    self.is_rolling = False
                    self.roll_speed_current = self.roll_speed_initial
                    
                    if self.on_ground and (keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]) and self.abilities.get('crouch', False):
                        self.is_crouching = True
                        self.current_frame = 0
                        self.frame_counter = 0.0
                        self.update_hitbox_position()
                        self.animate()
                        return
                    else:
                        # Exiting roll to normal - adjust Y position for height difference
                        if self.on_ground:
                            # Store the hitbox bottom position (actual ground contact)
                            ground_position = self.hitbox.bottom
                            self.animate()
                            # Calculate how much the sprite grew and adjust Y to compensate
                            height_diff = 180 - 145  # normal height - roll height
                            self.rect.y += height_diff
                            self.update_hitbox_position()
                            return

                if self.is_rolling:
                    # Apply horizontal movement
                    self.rect.x += self.roll_speed_current * (1 if self.facing_right else -1)
                    
                    # Apply gravity while rolling (so player falls off platforms)
                    if not self.on_ground:
                        self.vel_y += self.gravity
                        self.rect.y += self.vel_y
                    
                    self.animate()
                    self.update_hitbox_position()
                    return

        # --- FLAPPING STATE (double jump) ---
        if self.is_flapping:
            self.flap_timer += 1 / 60
            
            if self.flap_timer >= self.flap_duration:
                self.is_flapping = False
                self.flap_timer = 0.0
            
            self.animate()

        # --- VARIABLE JUMP HEIGHT ---
        jump_keys_pressed = (
            keys_pressed[pygame.K_SPACE] or 
            keys_pressed[pygame.K_UP] or 
            keys_pressed[pygame.K_w]
        )

        if not jump_keys_pressed and self.jump_held and self.vel_y < 0:
            self.vel_y *= 0.4

        self.jump_held = jump_keys_pressed

        # Count down roll cooldown
        if self.roll_cooldown > 0:
            self.roll_cooldown -= 1

        # --- ROLL START ---
        if (
            self.on_ground
            and (keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s])
            and (keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]
                or keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d])
            and self.roll_stamina > 0
            and self.roll_cooldown == 0  # Check roll cooldown
            and self.abilities.get('roll', False)  # Check roll ability
        ):
            if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
                self.facing_right = True
            elif keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
                self.facing_right = False

            self.is_rolling = True
            self.roll_speed_current = self.roll_speed_initial
            self.current_frame = 0
            self.frame_counter = 0.0
            return

        # --- CROUCH ---
        if (
            self.on_ground
            and not self.is_moving
            and not self.is_rolling
            and (keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s])
            and self.abilities.get('crouch', False)  # Check crouch ability
        ):
            if not self.is_crouching:
                self.is_crouching = True
                self.current_frame = 0
                self.frame_counter = 0.0
                base_image = self.crouch_frames[0]
                if self.facing_right:
                    self.image = pygame.transform.flip(base_image, True, False)
                else:
                    self.image = base_image
                old_bottom = self.rect.bottom
                old_centerx = self.rect.centerx
                self.rect = self.image.get_rect(centerx=old_centerx, bottom=old_bottom)
            self.update_hitbox_position()
            return
        else:
            # Exiting crouch to normal - adjust Y position for height difference
            if self.is_crouching and self.on_ground:
                self.is_crouching = False
                # Calculate height difference and adjust Y to keep feet on ground
                height_diff = 180 - 145  # normal height - crouch height
                self.rect.y += height_diff
                self.animate()
                self.update_hitbox_position()
                return
            self.is_crouching = False

        # --- HORIZONTAL MOVEMENT ---
        if self.abilities.get('walk', False):  # Check walk ability
            if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
                self.rect.x -= self.speed
                self.facing_right = False
                self.is_moving = True

            if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
                self.rect.x += self.speed
                self.facing_right = True
                self.is_moving = True

        # --- GRAVITY (only apply when not on ground) ---
        if not self.on_ground:
            self.vel_y += self.gravity
            self.rect.y += self.vel_y

        # --- STAMINA RECHARGE ---
        if not self.is_rolling:
            if self.roll_stamina_delay_timer > 0:
                self.roll_stamina_delay_timer -= 1
            elif self.roll_stamina < self.roll_stamina_max:
                self.roll_stamina += self.roll_stamina_recharge_rate
                if self.roll_stamina > self.roll_stamina_max:
                    self.roll_stamina = self.roll_stamina_max
        
        # --- SPIN CHARGE RECHARGE ---
        if self.abilities.get('spin', False):  # Only recharge if ability unlocked
            for i in range(len(self.spin_charge_timers) - 1, -1, -1):
                self.spin_charge_timers[i] -= 1
                if self.spin_charge_timers[i] <= 0:
                    self.spin_charges += 1
                    self.spin_charge_timers.pop(i)

        self.animate()
        self.update_hitbox_position()

    # ------------------------------------------------------------------
    def jump(self, jump_sound=None, double_jump_sound=None):
        """Trigger jump if on the ground, or double jump if in air."""
        if self.is_dead or self.is_hurt:
            return
        
        # Check jump ability
        if not self.abilities.get('jump', False):
            return
            
        if self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False
            self.has_double_jump = True if self.abilities.get('double_jump', False) else False
            self.jump_held = True
            if self.is_rolling:
                self.is_rolling = False
                self.roll_timer = 0.0
                self.roll_speed_current = self.roll_speed_initial
            
            # Play jump sound
            if jump_sound:
                jump_sound.play()
                
        elif self.has_double_jump and not self.is_flapping and self.abilities.get('double_jump', False):
            self.vel_y = self.jump_strength * 0.9
            self.has_double_jump = False
            self.is_flapping = True
            self.jump_held = True
            self.flap_timer = 0.0
            self.current_frame = 0
            self.frame_counter = 0.0
            
            # Play double jump sound
            if double_jump_sound:
                double_jump_sound.play()

    # ------------------------------------------------------------------
    def animate_hurt(self):
        """Animate hurt state"""
        self.frame_counter += 0.2
        if self.frame_counter >= 1.0:
            self.frame_counter = 0.0
            self.current_frame = (self.current_frame + 1) % len(self.hurt_frames)

        old_bottom = self.rect.bottom
        old_centerx = self.rect.centerx

        base_image = self.hurt_frames[self.current_frame]
        if self.facing_right:
            self.image = pygame.transform.flip(base_image, True, False)
        else:
            self.image = base_image

        self.rect = self.image.get_rect(centerx=old_centerx, bottom=old_bottom)

    # ------------------------------------------------------------------
    def animate_death(self):
        """Show death animation"""
        old_bottom = self.rect.bottom
        old_centerx = self.rect.centerx

        base_image = self.death_frames[0]
        if self.facing_right:
            self.image = pygame.transform.flip(base_image, True, False)
        else:
            self.image = base_image

        self.rect = self.image.get_rect(centerx=old_centerx, bottom=old_bottom)

    # ------------------------------------------------------------------
    def animate(self):
        """Update sprite image based on current state."""
        # Store the actual ground level (bottom of hitbox/rect)
        # Use hitbox bottom if on ground to maintain consistent ground position
        if self.on_ground:
            ground_level = self.rect.bottom
        else:
            ground_level = None
            
        old_bottom = self.rect.bottom
        old_centerx = self.rect.centerx

        # -------------------------------------------------
        # 1. SPINNING
        # -------------------------------------------------
        if self.is_spinning:
            self.frame_counter += 0.3
            if self.frame_counter >= 1.0:
                self.frame_counter = 0.0
                self.current_frame = (self.current_frame + 1) % len(self.spin_frames)

            base_image = self.spin_frames[self.current_frame]

            if self.facing_right:
                self.image = pygame.transform.flip(base_image, True, False)
            else:
                self.image = base_image

            self.rect = self.image.get_rect(centerx=old_centerx, bottom=old_bottom)
            return

        # -------------------------------------------------
        # 2. ROLLING
        # -------------------------------------------------
        if self.is_rolling:
            self.frame_counter += 0.25
            if self.frame_counter >= 1.0:
                self.frame_counter = 0.0
                self.current_frame = (self.current_frame + 1) % len(self.roll_frames)

            base_image = self.roll_frames[self.current_frame]

            if self.facing_right:
                self.image = pygame.transform.flip(base_image, True, False)
            else:
                self.image = base_image

            if ground_level is not None:
                self.rect = self.image.get_rect(centerx=old_centerx, bottom=ground_level)
            else:
                self.rect = self.image.get_rect(centerx=old_centerx, bottom=old_bottom)
            return

        # -------------------------------------------------
        # 3. FLAPPING (double jump)
        # -------------------------------------------------
        if self.is_flapping:
            self.frame_counter += 0.3
            if self.frame_counter >= 1.0:
                self.frame_counter = 0.0
                self.current_frame = (self.current_frame + 1) % len(self.flap_frames)
            
            self.current_frame = min(self.current_frame, len(self.flap_frames) - 1)
            
            base_image = self.flap_frames[self.current_frame]
            
            if self.facing_right:
                self.image = pygame.transform.flip(base_image, True, False)
            else:
                self.image = base_image
            
            self.rect = self.image.get_rect(centerx=old_centerx, bottom=old_bottom)
            return

        # -------------------------------------------------
        # 4. CROUCHING
        # -------------------------------------------------
        if self.is_crouching:
            base_image = self.crouch_frames[0]

            if self.facing_right:
                self.image = pygame.transform.flip(base_image, True, False)
            else:
                self.image = base_image

            if ground_level is not None:
                self.rect = self.image.get_rect(centerx=old_centerx, bottom=ground_level)
            else:
                self.rect = self.image.get_rect(centerx=old_centerx, bottom=old_bottom)
            return

        # -------------------------------------------------
        # 5. JUMPING / FALLING
        # -------------------------------------------------
        if not self.on_ground:
            if self.vel_y < 0:
                base_image = self.jump_frames[0]
            else:
                base_image = self.jump_frames[1]

        # -------------------------------------------------
        # 6. WALKING
        # -------------------------------------------------
        elif self.is_moving:
            if self.current_frame >= len(self.walk_frames):
                self.current_frame = 0
                self.frame_counter = 0.0
            
            self.frame_counter += self.animation_speed
            if self.frame_counter >= 1.0:
                self.frame_counter = 0.0
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
            base_image = self.walk_frames[self.current_frame]

        # -------------------------------------------------
        # 7. IDLE
        # -------------------------------------------------
        else:
            if self.current_frame >= len(self.idle_frames):
                self.current_frame = 0
                self.frame_counter = 0.0
            
            self.frame_counter += 0.1
            if self.frame_counter >= 1.0:
                self.frame_counter = 0.0
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            base_image = self.idle_frames[self.current_frame]

        # -------------------------------------------------
        # FINAL APPLY
        # -------------------------------------------------
        if self.facing_right:
            self.image = pygame.transform.flip(base_image, True, False)
        else:
            self.image = base_image

        # When on ground, always use ground_level to prevent pop-up
        if ground_level is not None:
            self.rect = self.image.get_rect(centerx=old_centerx, bottom=ground_level)
        else:
            self.rect = self.image.get_rect(centerx=old_centerx, bottom=old_bottom)