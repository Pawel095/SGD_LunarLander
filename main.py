import pygame
import constants
from loader import Loader, assets
from timeit import default_timer as time
from time import sleep
from camera import Camera
from generic.worlds import Planet
from objects.lander import Lander as Shuttle

pygame.init()

Loader().load()

window = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Lunar Lander")

camera = Camera()

moon = Planet(1000000, (300, 300), None)

lander = Shuttle((100, 100 + 26), assets["lander"], moon)
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
                lander.main_thruster(1000)

            if event.key == pygame.K_d:
                lander.rcs(-200)
            if event.key == pygame.K_a:
                lander.rcs(200)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                lander.disable_main_thruster()

            if event.key == pygame.K_d:
                lander.disable_rcs()
            if event.key == pygame.K_a:
                lander.disable_rcs()

    # Physics
    lander.update(deltaT)
    moon.update(deltaT)

    # render
    window.fill((0, 0, 0))
    moon.draw(window)
    lander.draw(window)

    pygame.display.update()

    limiter_wait = True
    while limiter_wait:
        sleep(1 / 480)
        if time() - now >= 1 / fps_target:
            limiter_wait = False

    last = now
