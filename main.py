import pygame
from timeit import default_timer as time

from objects.lander import Lander as Shuttle

pygame.init()

window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Lunar Lander")

lander = Shuttle()

running = True
last = 0
while running:
    now = time()
    deltaT = now - last

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                lander.linear_A = (1000, 0)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                lander.linear_A = (0, 0)

    window.fill((0, 0, 0))

    lander.update(deltaT)
    lander.draw(window)

    pygame.display.update()

    # TODO: FPS limiter here
    
    last = now
