import pygame
import math
import random

class Particle:
    def __init__(self, x, y, color, size, dx, dy, speed, shrink):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.shrink = shrink

    def update(self, dt):
        self.x += self.dx * self.speed * dt
        self.y += self.dy * self.speed * dt
        self.size -= self.shrink * dt

    def draw(self, screen, scroll):
        pygame.draw.circle(screen, self.color, (self.x - scroll[0], self.y - scroll[1]), self.size)


class ParticleEmitter:
    def __init__(self):
        self.particles = []

    def add_particle(self, x, y, color, size, dx, dy, speed, shrink):
        self.particles.append(Particle(x, y, color, size, dx, dy, speed, shrink))

    def add_burst(self, x, y, color, size, speed, shrink, amount):
        for _ in range(amount):
            angle = random.uniform(0, 2 * math.pi)
            dx = math.cos(angle)
            dy = math.sin(angle)
            draw_x = x + random.randint(-16, 16)
            draw_y = y + random.randint(-16, 16)
            self.particles.append(Particle(draw_x, draw_y, color, size, dx, dy, speed, shrink))

    def update(self, dt):
        particles_to_remove = []
        for i, particle in enumerate(self.particles):
            particle.update(dt)
            if particle.size <= 0:
                particles_to_remove.append(i)

        for i in reversed(particles_to_remove):
            self.particles.pop(i)

    def draw(self, screen, scroll):
        for particle in self.particles:
            particle.draw(screen, scroll)
