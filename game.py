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

p = player.Player()

dig_particles = particle.ParticleEmitter()
dig_timer = 0

escape_timer = 3000
escaping = False

curr_level = 0
level = load_level(curr_level)

tint = pygame.Surface((1280, 720))
tint.fill((198, 80, 90))
tint.set_alpha(0)

gauntlet = pygame.Surface((1280, 720))
gauntlet.fill((198, 80, 90))
gauntlet.set_colorkey((0, 0, 0))
gauntlet_particles = particle.ParticleEmitter()

dead = False
death_timer = 60

clock = pygame.time.Clock()
dt = 1
pt = time.time()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    p.movement[0] = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    p.movement[1] = keys[pygame.K_DOWN] - keys[pygame.K_UP]

    if keys[pygame.K_d] and len(os.listdir("assets/levels")) > curr_level + 1 and any(p.rect.colliderect(tile[1]) and tile[0] == "2" for tile in level):
        dig_particles.add_burst(p.rect.centerx, p.rect.centery, (90, 38, 43), 10, 3, 0.5, 10)
        dig_timer += 1 * dt
    else:
        dig_timer = 0

    if escaping:
        escape_timer -= 1 * dt

    if keys[pygame.K_p]:
        print(p.rect.center)

    collided_tiles = [tile for tile in level if p.rect.colliderect(tile[1]) and tile[0] != 0]
    if not dead:
        p.update(dt, level)
    dig_particles.update(dt)
    gauntlet_particles.update(dt)
    if dig_timer > p.rect.width * math.sqrt(2) / 2:
        curr_level += 1
        level = load_level(curr_level)
        dig_timer = 0

    scroll[0] += ((p.rect.centerx - (1280 / 2) - scroll[0]) / 5 * dt)
    scroll[1] += ((p.rect.centery - (720 / 2) - scroll[1]) / 5 * dt)
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    if any(p.rect.colliderect(tile[1]) and tile[0] == "4" and (tile[2] == "not collected") for tile in level):
        for tile in level:
            if len(tile) == 3:
                tile.pop()
                tile[0] = "0"
                level = load_level(curr_level)

    if any(p.rect.colliderect(tile[1]) and tile[0] == "5" for tile in level):
        curr_level -= 1
        level = load_level(curr_level)

    screen.fill((120, 68, 73))
    for tile in level:
        if (len(tile) == 2 or len(tile) == 3 and tile[2] in ["locked", "not collected"]) and -32 <= tile[1].centerx - scroll[0] <= 1312 and -32 <= tile[1].centery - scroll[1] <= 752:
            screen.blit(tile_img[int(tile[0])], (tile[1].x - scroll[0], tile[1].y - scroll[1]))
    pygame.draw.circle(screen, (46, 19, 45), (p.rect.centerx - scroll[0], p.rect.centery - scroll[1]), dig_timer)
    dig_particles.draw(screen, scroll)
    tint.set_alpha(curr_level * 15)
    screen.blit(tint, (0, 0))
    if not dead:
        p.draw(screen, scroll)

    ui.title(f"{int(clock.get_fps())}", 500, 500, screen)
    ui.title(f"Layer: {curr_level + 1}", 640, 100, screen, (46, 19, 45))

    if curr_level == 0:
        ui.title("I'm a gopher", 64 - scroll[0] * 0.99, 164 - scroll[1] * 0.99, screen)
        ui.title("Arrow keys to move me", 64 - scroll[0] * 0.99, 214 - scroll[1] * 0.99, screen)
        ui.title("D for me to dig", 764 - scroll[0] * 0.99, 164 - scroll[1] * 0.99, screen)
        ui.title("in designated spots", 764 - scroll[0] * 0.99, 214 - scroll[1] * 0.99, screen)
        ui.title("(They're yellow)", 764 - scroll[0] * 0.99, 264 - scroll[1] * 0.99, screen)
        ui.title("We made it!", -6912 - scroll[0] * 0.99, 4860 - scroll[1] * 0.99, screen)
        ui.title("Thanks for playing!", -6912 - scroll[0] * 0.99, 4910 - scroll[1] * 0.99, screen)
        escaping = False
    elif curr_level == 1:
        ui.title("I must reach the", 1349 - scroll[0] * 0.99, -57 - scroll[1] * 0.99, screen)
        ui.title("center of the world", 1349 - scroll[0] * 0.99, -7 - scroll[1] * 0.99, screen)
        ui.title("Almost", -6656 - scroll[0] * 0.99, 4630 - scroll[1] * 0.99, screen)
        ui.title("there!", -6656 - scroll[0] * 0.99, 4680 - scroll[1] * 0.99, screen)
    elif curr_level == 2:
        ui.title("Keys remove all locks", 336 - scroll[0] * 0.99, 410 - scroll[1] * 0.99, screen)
        ui.title("in the layer", 336 - scroll[0] * 0.99, 450 - scroll[1] * 0.99, screen)
    elif curr_level == 3:
        ui.title("Colorful thing", -500 - scroll[0] * 0.99, 167 - scroll[1] * 0.99, screen)
        ui.title("teleports me up", -500 - scroll[0] * 0.99, 217 - scroll[1] * 0.99, screen)
        ui.title("ULDR!!", -4740 - scroll[0] * 0.99, 4896 - scroll[1] * 0.99, screen)
    elif curr_level == 4:
        ui.title("It can't", -800 - scroll[0] * 0.99, -650 - scroll[1] * 0.99, screen)
        ui.title("be that easy", -800 - scroll[0] * 0.99, -600 - scroll[1] * 0.99, screen)
        ui.title("This layer-hopping is", -1914 - scroll[0] * 0.99, -100 - scroll[1] * 0.99, screen)
        ui.title("making me dizzy", -1914 - scroll[0] * 0.99, -50 - scroll[1] * 0.99, screen)
        ui.title("Oops... Wrong spot", -1536 - scroll[0] * 0.99, 600 - scroll[1] * 0.99, screen)
    elif curr_level == 5:
        ui.title("I got the key but...", -3100 - scroll[0] * 0.99, 705 - scroll[1] * 0.99, screen)
        ui.title("I also see another", -3100 - scroll[0] * 0.99, 755 - scroll[1] * 0.99, screen)
        ui.title("path to the next layer", -3100 - scroll[0] * 0.99, 805 - scroll[1] * 0.99, screen)
        ui.title("What's over here?", -2000 - scroll[0] * 0.99, 1728 - scroll[1] * 0.99, screen)
    elif curr_level == 6:
        ui.title("There's that key!", -1408 - scroll[0] * 0.99, 2518 - scroll[1] * 0.99, screen)
        ui.title("Wrong way!", -3409 - scroll[0] * 0.99, 4800 - scroll[1] * 0.99, screen)
    elif curr_level == 7:
        ui.title("It's steamy down here", -2400 - scroll[0] * 0.99, 1470 - scroll[1] * 0.99, screen)
    elif curr_level == 8:
        ui.title("Wait... THE EARTH", -1900 - scroll[0] * 0.99, 2775 - scroll[1] * 0.99, screen)
        ui.title("HATES GOPHERS!!", -1900 - scroll[0] * 0.99, 2925 - scroll[1] * 0.99, screen)
        ui.title("The lava will get us!", -1374 - scroll[0] * 0.99, 3750 - scroll[1] * 0.99, screen)
        ui.title("This way!", -1881 - scroll[0] * 0.99, 3904 - scroll[1] * 0.99, screen)
    elif curr_level == 9:
        ui.title("RUN!!!", -1344 - scroll[0] * 0.99, 2675 - scroll[1] * 0.99, screen)
        escaping = True

    if escaping:
        gauntlet.fill((198, 80, 90))
        pygame.draw.circle(gauntlet, (0, 0, 0), (640, 360), math.sqrt(360**2 + 640**2) / 3000 * escape_timer)
        gauntlet_particles.draw(screen, [0, 0])
        screen.blit(gauntlet, (0, 0))
        if int(escape_timer) % 5 in [1, 2]:
            for i in range(120):
                gauntlet_particles.add_particle(math.cos(math.radians(i * 3)) * math.sqrt(360**2 + 640**2) / 3000 * escape_timer + 640, math.sin(math.radians(i * 3)) * math.sqrt(360**2 + 640**2) / 3000 * escape_timer + 360, (170, 100, 90), 10, -math.cos(math.radians(i * 3)), -math.sin(math.radians(i * 3)), 5, 10 / (math.sqrt(360**2 + 640**2) / 3000 * escape_timer) * 9)
    if dead:
        death_timer -= 1 * dt
    if escape_timer <= 600 and not dead:
        dead = True
        death_timer = 60
    if death_timer <= 0 and dead:
        p = player.Player(x=-1344, y=2624)
        curr_level = 9
        level = load_level(curr_level)
        escape_timer = 3000
        escaping = True
        dead = False


    pygame.display.update()

    clock.tick(60)
    now = time.time()
    dt = (now - pt) * 60
    pt = now

pygame.quit()
