"""
Particle system for visual effects in Siena's Snowy Adventure.

Provides various particle effects for game feel:
- Snow puffs (landing, rolling)
- Sparkles (coin collection, power-ups)
- Hit sparks (enemy damage)
- Explosions (enemy defeat)
"""

import pygame
import random
import math


class Particle:
    """Base particle class with physics and rendering."""

    def __init__(self, x, y, vx, vy, lifetime, color, size=3, gravity=0.3):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.color = color
        self.size = size
        self.gravity = gravity

    def update(self):
        """Update particle position and lifetime. Returns True if still alive."""
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.vx *= 0.98  # Air resistance
        self.lifetime -= 1
        return self.lifetime > 0

    def draw(self, screen, camera_x):
        """Draw particle with fade-out effect."""
        if self.lifetime <= 0:
            return

        alpha = self.lifetime / self.max_lifetime
        current_size = max(1, int(self.size * alpha))
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y)

        # Skip off-screen particles
        if not (-current_size <= screen_x <= screen.get_width() + current_size):
            return
        if not (-current_size <= screen_y <= screen.get_height() + current_size):
            return

        # For small particles, draw directly (faster)
        if current_size <= 2:
            pygame.draw.circle(screen, self.color, (screen_x, screen_y), current_size)
        else:
            # For larger particles, use surface with alpha (cached approach)
            surf = pygame.Surface((current_size * 2, current_size * 2))
            surf.set_colorkey((0, 0, 0))
            pygame.draw.circle(surf, self.color, (current_size, current_size), current_size)
            surf.set_alpha(int(255 * alpha))
            screen.blit(surf, (screen_x - current_size, screen_y - current_size))


class SnowPuffParticle(Particle):
    """White fluffy particle for landing and rolling."""

    def __init__(self, x, y, vx, vy):
        color = (200 + random.randint(0, 55), 220 + random.randint(0, 35), 255)
        size = random.randint(2, 4)
        lifetime = random.randint(15, 30)
        super().__init__(x, y, vx, vy, lifetime, color, size, gravity=0.2)


class SparkleParticle(Particle):
    """Golden sparkle for coins and power-ups."""

    def __init__(self, x, y, vx, vy):
        color = (255, 215 + random.randint(-20, 0), random.randint(0, 50))
        size = random.randint(2, 5)
        lifetime = random.randint(20, 40)
        super().__init__(x, y, vx, vy, lifetime, color, size, gravity=0.15)


class HitSparkParticle(Particle):
    """Red/orange spark for damage effects."""

    def __init__(self, x, y, vx, vy):
        color = (255, random.randint(50, 150), random.randint(0, 50))
        size = random.randint(2, 4)
        lifetime = random.randint(10, 25)
        super().__init__(x, y, vx, vy, lifetime, color, size, gravity=0.25)


class ExplosionParticle(Particle):
    """White/blue particle for enemy defeats."""

    def __init__(self, x, y, vx, vy):
        color = (random.randint(200, 255), random.randint(220, 255), 255)
        size = random.randint(3, 6)
        lifetime = random.randint(20, 35)
        super().__init__(x, y, vx, vy, lifetime, color, size, gravity=0.2)


class ParticleManager:
    """Manages all particles in the game."""

    MAX_PARTICLES = 150  # Limit to prevent performance issues

    def __init__(self):
        self.particles = []

    def spawn_burst(self, x, y, count=8, particle_type='snow', direction=None, speed_range=(1, 3)):
        """
        Spawn a burst of particles.

        Args:
            x, y: Position to spawn particles
            count: Number of particles
            particle_type: 'snow', 'sparkle', 'hit', or 'explosion'
            direction: Angle in radians (None = all directions)
            speed_range: (min_speed, max_speed) tuple
        """
        # Limit particle count to prevent lag
        if len(self.particles) >= self.MAX_PARTICLES:
            return

        particle_class = {
            'snow': SnowPuffParticle,
            'sparkle': SparkleParticle,
            'hit': HitSparkParticle,
            'explosion': ExplosionParticle
        }.get(particle_type, SnowPuffParticle)

        # Reduce count if we're near the limit
        available_slots = self.MAX_PARTICLES - len(self.particles)
        count = min(count, available_slots)

        for _ in range(count):
            if direction is None:
                # Random full circle
                angle = random.uniform(0, 2 * math.pi)
            else:
                # Cone around direction (±45 degrees)
                angle = direction + random.uniform(-math.pi/4, math.pi/4)

            speed = random.uniform(*speed_range)
            vx = speed * math.cos(angle)
            vy = speed * math.sin(angle) - random.uniform(1, 2)  # Upward bias

            self.particles.append(particle_class(x, y, vx, vy))

    def spawn_landing_puff(self, x, y, width):
        """Spawn snow puff when player/enemy lands."""
        # Spread across landing width
        for _ in range(random.randint(3, 6)):
            spawn_x = x + random.uniform(0, width)
            vx = random.uniform(-1, 1)
            vy = random.uniform(-3, -1)
            self.particles.append(SnowPuffParticle(spawn_x, y, vx, vy))

    def spawn_coin_sparkles(self, x, y):
        """Spawn sparkle ring when coin collected."""
        for i in range(12):
            angle = (i / 12) * 2 * math.pi
            speed = random.uniform(1.5, 2.5)
            vx = speed * math.cos(angle)
            vy = speed * math.sin(angle)
            self.particles.append(SparkleParticle(x, y, vx, vy))

    def spawn_enemy_defeat(self, x, y, width, height):
        """Spawn explosion when enemy defeated."""
        # Explosion from center
        center_x = x + width / 2
        center_y = y + height / 2
        self.spawn_burst(center_x, center_y, count=15,
                        particle_type='explosion', speed_range=(2, 5))

    def spawn_hit_effect(self, x, y, knockback_direction):
        """Spawn hit sparks when damage dealt."""
        # Direction is 1 (right) or -1 (left)
        direction = 0 if knockback_direction > 0 else math.pi
        self.spawn_burst(x, y, count=8, particle_type='hit',
                        direction=direction, speed_range=(2, 4))

    def spawn_roll_trail(self, x, y):
        """Spawn small snow trail while rolling."""
        if random.random() < 0.3:  # Only spawn 30% of frames
            vx = random.uniform(-0.5, 0.5)
            vy = random.uniform(-0.5, 0)
            self.particles.append(SnowPuffParticle(x, y, vx, vy))

    def spawn_spin_ring(self, x, y, radius):
        """Spawn particle ring during spin attack."""
        for i in range(8):
            angle = (i / 8) * 2 * math.pi
            spawn_x = x + radius * math.cos(angle)
            spawn_y = y + radius * math.sin(angle)
            vx = math.cos(angle) * 2
            vy = math.sin(angle) * 2
            self.particles.append(SparkleParticle(spawn_x, spawn_y, vx, vy))

    def update(self):
        """Update all particles and remove dead ones."""
        self.particles = [p for p in self.particles if p.update()]

    def draw(self, screen, camera_x):
        """Draw all particles."""
        for particle in self.particles:
            particle.draw(screen, camera_x)

    def clear(self):
        """Remove all particles (e.g., on level transition)."""
        self.particles.clear()

    def count(self):
        """Return number of active particles (for debugging)."""
        return len(self.particles)
