import pygame
import math
import assets.scripts.particle as particle

pygame.init()

screen = pygame.display.set_mode((800, 600))

emmiter = particle.ParticleEmitter()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.mouse.get_pressed()[0]:
        for i in range(60):
            emmiter.add_particle(math.cos(math.radians(i * 6)) * math.sqrt(300**2 + 400**2) + 640, math.sin(math.radians(i * 6)) * math.sqrt(300**2 + 400**2) + 360, (170, 100, 90), 10, -math.cos(math.radians(i * 6)), -math.sin(math.radians(i * 6)), 5, 0.01)

    emmiter.update(1)

    screen.fill((255, 255,255))
    emmiter.draw(screen, [0, 0])

    pygame.display.update()

pygame.quit()
