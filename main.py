import pygame
import constants
from loader import Loader, assets
from timeit import default_timer as time
from time import sleep
from generic.worlds import Moon

from objects.lander import Lander as Shuttle

pygame.init()

Loader().load()

window = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Lunar Lander")

lander = Shuttle(assets["lander"],Moon(40))
fps_target = 60

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
                lander.enable_thrust(1000)

            if event.key == pygame.K_d:
                lander.angular_a = -200
            if event.key == pygame.K_a:
                lander.angular_a = 200

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                lander.disable_thrust()

            if event.key == pygame.K_d:
                lander.angular_a = 0
            if event.key == pygame.K_a:
                lander.angular_a = 0

    # Physics
    lander.update(deltaT)

    # render
    window.fill((0, 0, 0))

    lander.draw(window)

    pygame.display.update()

    limiter_wait = True
    while limiter_wait:
        sleep(1 / 480)
        if time() - now >= 1 / fps_target:
            limiter_wait = False

    last = now
