import pygame
import os
import math
import time
import json

import assets.scripts.player as player
import assets.scripts.ui as ui
import assets.scripts.particle as particle

pygame.init()
screen = pygame.display.set_mode((1280, 720))

all_levels = []

def load_level(num):
    global all_levels
    if len(all_levels) - 1 >= num:
        return(all_levels[num])
    with open(f'assets/levels/{num}.json', 'r') as f:
        data = json.load(f)
    level = []
    for tile in data:
        if tile[0] == "3":
            level.append([tile[0], pygame.Rect(tile[1], tile[2], 64, 64), "locked"])
        elif tile[0] == "4":
            level.append([tile[0], pygame.Rect(tile[1], tile[2], 64, 64), "not collected"])
        else:
            level.append([tile[0], pygame.Rect(tile[1], tile[2], 64, 64)])
    all_levels.append(level)
    return level

tile_img = [
    pygame.transform.scale2x(pygame.image.load(f"assets/images/tiles/{tile}"))
    for tile in os.listdir("assets/images/tiles")
]
scroll = [0, -200]

player = player.Player()

dig_particles = particle.ParticleEmitter()
dig_timer = 0
alphabet = "abcdefghijklmnopqrstuvwxyz"

curr_level = 0
level = load_level(curr_level)

clock = pygame.time.Clock()
dt = 1
pt = time.time()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    player.movement[0] = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    player.movement[1] = keys[pygame.K_DOWN] - keys[pygame.K_UP]

    if keys[pygame.K_d] and len(os.listdir("assets/levels")) > curr_level + 1 and any(player.rect.colliderect(tile[1]) and tile[0] == "2" for tile in level):
        dig_particles.add_burst(player.rect.centerx, player.rect.centery, (90, 38, 43), 10, 3, 0.5, 10)
        dig_timer += 1 * dt
    else:
        dig_timer = 0

    if keys[pygame.K_a] and curr_level > 0:
        curr_level -= 1
        level = load_level(curr_level)

    collided_tiles = [tile for tile in level if player.rect.colliderect(tile[1]) and tile[0] != 0]
    player.update(dt, level)
    dig_particles.update(dt)
    if dig_timer > player.rect.width * math.sqrt(2) / 2:
        curr_level += 1
        level = load_level(curr_level)
        dig_timer = 0

    scroll[0] += ((player.rect.centerx - (1280 / 2) - scroll[0]) / 10 * dt)
    scroll[1] += ((player.rect.centery - (720 / 2) - scroll[1]) / 10 * dt)
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    if any(player.rect.colliderect(tile[1]) and tile[0] == "4" and (tile[2] == "not collected") for tile in level):
        for tile in level:
            if len(tile) == 3:
                tile.pop()
                tile[0] = "0"
                level = load_level(curr_level)

    if any(player.rect.colliderect(tile[1]) and tile[0] == "5" for tile in level):
        curr_level -= 1
        level = load_level(curr_level)

    screen.fill((120, 68, 73))
    for tile in level:
        if len(tile) == 2 or len(tile) == 3 and tile[2] in ["locked", "not collected"]:
            screen.blit(tile_img[int(tile[0])], (tile[1].x - scroll[0], tile[1].y - scroll[1]))
    pygame.draw.circle(screen, (46, 19, 45), (player.rect.centerx - scroll[0], player.rect.centery - scroll[1]), dig_timer)
    dig_particles.draw(screen, scroll)
    player.draw(screen, scroll)

    ui.title(f"{int(clock.get_fps())}", 500, 500, screen)

    pygame.display.update()

    clock.tick(60)
    now = time.time()
    dt = (now - pt) * 60
    pt = now

pygame.quit()
