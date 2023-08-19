import pygame
import math
import random

import assets.scripts.dungeon as dungeon

class Entity:
    def __init__(self, x, y, width, height, speed, health, img):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.movement = [0, 0]
        self.img = pygame.image.load(f"assets/images/entity/{img}").convert_alpha()
        self.knockback_angle = 0
        self.angle = 0
        self.state = "idle"
        self.max_health = health
        self.health = self.max_health
        self.alive = True
        self.immune = False
        self.immune_timer = 15

    def stun(self, knockback_angle):
        self.state = "stunned"
        self.knockback_angle = knockback_angle
        self.immune = True
        self.immune_timer = 15

    def move(self, dt, rooms):
        self.rect.x += self.speed * self.movement[0] * dt
        self.rect.y += self.speed * self.movement[1] * dt
        if self.state == "stunned":
            self.movement = [0, 0]
            dx = math.cos(math.radians(self.knockback_angle - 90))
            dy = -math.sin(math.radians(self.knockback_angle - 90))
            self.rect.x += dx * self.immune_timer * dt
            self.rect.y += dy * self.immune_timer * dt
        dungeon.collide(self, rooms, dt)

    def draw(self, screen, scroll):
        if (self.rect.left - scroll[0] <= 1280 and self.rect.right - scroll[0] >= 0) and (self.rect.top - scroll[1] <= 720 and self.rect.bottom - scroll[1] >= 0):
            draw_surf = pygame.transform.rotate(self.img, self.angle)
            screen.blit(draw_surf, ((self.rect.centerx - scroll[0]) - (draw_surf.get_width() / 2), (self.rect.centery - scroll[1]) - (draw_surf.get_height() / 2)))
