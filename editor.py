import time
import pygame
import os
import json

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1280, 720))

def save(num, level):
    with open(f'assets/levels/{num}.json', 'w') as f:
        json.dump(level, f)

def load(num):
    with open(f'assets/levels/{num}.json', 'r') as f:
        data = json.load(f)
    return data

scroll = [0, 0]
cam_movement = [0, 0]

tile_img = [
    pygame.transform.scale2x(pygame.image.load(f"assets/images/tiles/{tile}"))
    for tile in os.listdir("assets/images/tiles")
]

level_num = 0
level = []

pressed = False

clock = pygame.time.Clock()

current_item = 0

pt = time.time()
dt = 1

s = None

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                cam_movement[0] = 1
            if event.key == pygame.K_LEFT:
                cam_movement[0] = -1
            if event.key == pygame.K_DOWN:
                cam_movement[1] = 1
            if event.key == pygame.K_UP:
                cam_movement[1] = -1

            if event.key == pygame.K_s:
                save(level_num, level)
            if event.key == pygame.K_l:
                level = load(level_num)
            if event.key == pygame.K_c:
                level = []
                scroll = [0, 0]
            if event.key == pygame.K_r:
                scroll = [-640, -360]

            if event.key == pygame.K_0:
                level_num = 0
                level = []
            elif event.key == pygame.K_1:
                level_num = 1
                level = []
            elif event.key == pygame.K_2:
                level_num = 2
                level = []
            elif event.key == pygame.K_3:
                level_num = 3
                level = []
            elif event.key == pygame.K_4:
                level_num = 4
                level = []
            elif event.key == pygame.K_5:
                level_num = 5
                level = []
            elif event.key == pygame.K_6:
                level_num = 6
                level = []
            elif event.key == pygame.K_7:
                level_num = 7
                level = []
            elif event.key == pygame.K_8:
                level_num = 8
                level = []
            elif event.key == pygame.K_9:
                level_num = 9
                level = []

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                cam_movement[0] = 0
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                cam_movement[1] = 0

        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                if current_item == 5:
                    current_item = 0
                else:
                    current_item += 1
            else:
                if current_item == 0:
                    current_item = 5
                else:
                    current_item -= 1

    if pygame.mouse.get_pos()[0] <= 980:
        if pygame.mouse.get_pressed()[0]:
            s = None
            level.append([str(current_item), round((pygame.mouse.get_pos()[0] + scroll[0] - 32) / 64) * 64, round((pygame.mouse.get_pos()[1] + scroll[1] - 32) / 64) * 64])
        else:
            s = pygame.Surface((64, 64))
            s.blit(tile_img[current_item], (0, 0))
            s.set_alpha(128)


    if not pygame.mouse.get_pressed()[0]:
        pressed = False

    if pygame.mouse.get_pos()[0] <= 980 and pygame.mouse.get_pressed()[2]:
        for tile in level:
            if pygame.Rect(tile[1], tile[2], 64, 64).collidepoint((pygame.mouse.get_pos()[0] + scroll[0], pygame.mouse.get_pos()[1] + scroll[1])):
                level.remove(tile)

    seen_tiles = set()
    level = [tile for tile in level if not (tile[1], tile[2]) in seen_tiles and not seen_tiles.add((tile[1], tile[2]))]



    scroll[0] += cam_movement[0] * 100
    scroll[1] += cam_movement[1] * 100

    screen.fill((117, 201, 151))

    for tile in level:
        if -32 <= tile[1] - scroll[0] <= 1312 and -32 <= tile[2] - scroll[1] <= 752:
            screen.blit(tile_img[int(tile[0])], ((tile[1] - scroll[0], tile[2] - scroll[1])))


    if isinstance(s, pygame.surface.Surface):
        width = s.get_rect().width
        height = s.get_rect().height
        grid_x = round((pygame.mouse.get_pos()[0] + scroll[0]) / 64) * 64
        grid_y = round((pygame.mouse.get_pos()[1] + scroll[1]) / 64) * 64
        surface_x = grid_x - scroll[0] - width // 2
        surface_y = grid_y - scroll[1] - height // 2
        screen.blit(s, (surface_x, surface_y))
    pygame.draw.rect(screen, (0, 0, 0),
                     (-scroll[0], -scroll[1], 32, 32))
    for i in range(34):
        pygame.draw.line(screen, (0, 0, 0), (i * 64 -
                         scroll[0] % 64, 0), (i * 64 - scroll[0] % 64, 720))
    for i in range(26):
        pygame.draw.line(screen, (0, 0, 0), (0, i * 64 -
                         scroll[1] % 64), (980, i * 64 - scroll[1] % 64))
    pygame.draw.rect(screen, (0, 0, 0), (980, 0, 300, 720))

    pygame.display.update()
    clock.tick(60)
    now = time.time()
    dt = (now - pt) * 60
    pt = now

pygame.quit()
