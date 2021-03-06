import pygame
import constants
from loader import Loader, assets
from timeit import default_timer as time
from time import sleep
from camera import Camera, simple_follow
from generic.worlds import Planet, Planets
from objects.lander import Lander as Shuttle

pygame.init()

Loader().load()

window = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Lunar Lander")

camera = Camera(simple_follow, 5000, 5000)

moon = Planet(1000000, (300, 300), None)
planets = Planets([1000000, 1000000], ((100, 100), (300, 100)), [None, None])

lander = Shuttle((10, 10), assets["lander"], planets)

planets.apply_gravity(lander)

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
    planets.update(deltaT)
    # moon.update(deltaT)

    # camera
    camera.update(lander)

    # render
    window.fill((0, 0, 0))
    # moon.draw(window)
    planets.draw(window)
    lander.draw(window)

    pygame.display.update()

    limiter_wait = True
    while limiter_wait:
        sleep(1 / 480)
        if time() - now >= 1 / fps_target:
            limiter_wait = False

    last = now
