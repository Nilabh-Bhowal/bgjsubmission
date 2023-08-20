import pygame
import assets.scripts.animation as animation

class Player:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 128, 128)
        self.animation = animation.Animation("gopher")
        self.movement = [0, 0]
        self.speed = 10
        self.draw_surf = self.animation.get_image()

    def update(self, dt, tiles):
        self.rect.x += self.movement[0] * self.speed * dt
        collided_tiles = [tile for tile in tiles if self.rect.colliderect(tile[1]) and (tile[0] == "1" or (tile[0] == "3" and (tile[2] == "locked")))]
        for tile in collided_tiles:
            if self.movement[0] > 0:
                self.rect.right = tile[1].left
            elif self.movement[0] < 0:
                self.rect.left = tile[1].right

        self.rect.y += self.movement[1] * self.speed * dt
        collided_tiles = [tile for tile in tiles if self.rect.colliderect(tile[1]) and (tile[0] == "1" or (tile[0] == "3" and (tile[2] == "locked")))]
        for tile in collided_tiles:
            if self.movement[1] > 0:
                self.rect.bottom = tile[1].top
            elif self.movement[1] < 0:
                self.rect.top = tile[1].bottom

        if 1 in self.movement or -1 in self.movement:
            self.animation.change_animation("run")
        else:
            self.animation.change_animation("idle")
        self.animation.update()

    def draw(self, screen, scroll):
        if self.movement[0] == 1:
            self.draw_surf = pygame.transform.rotate(self.animation.get_image(), -90)
        elif self.movement[0] == -1:
            self.draw_surf = pygame.transform.rotate(self.animation.get_image(), 90)
        elif self.movement[1] == 1:
            self.draw_surf = pygame.transform.rotate(self.animation.get_image(), 180)
        elif self.movement[1] == -1:
            self.draw_surf = self.animation.get_image()
        screen.blit(self.draw_surf, (self.rect.x - scroll[0], self.rect.y - scroll[1]))
