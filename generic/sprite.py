import pygame
import math
import generic.worlds
from objects.particle import Particle, ParticleSystem


class DynamicSprite:
    def __init__(self, texture: pygame.Surface, world):
        self._world = world
        self.thrusting = False

        self._size = self._texture.get_rect()[2:]

        self._position = (400, 300)
        self._linear_v = (0, 0)
        self._linear_a = (0, 0)

        self._angle = 180
        self._angular_v = 0
        self._angular_a = 0

    def update(self, deltaT):
        px, py = self._position
        vx, vy = self._linear_v
        ax, ay = self._world.apply_gravity(self)

        tetha = self._angle
        av = self._angular_v
        aa = self._angular_a

        # Linear calculation
        self._linear_v = (ax * deltaT + vx, ay * deltaT + vy)
        self._position = (
            px + vx * deltaT + 0.5 * ax * deltaT ** 2,
            py + vy * deltaT + 0.5 * ay * deltaT ** 2,
        )

        # angular calculation
        self._angular_v = av + aa * deltaT

        self._angle = self._angle + av * deltaT + 0.5 * aa * deltaT ** 2

        if self._angle < 0:
            self._angle = 360

        if self._angle > 360:
            self._angle %= 360

    def draw(self, window: pygame.Surface):
        srf = pygame.Surface(self._size)
        srf.set_colorkey((0, 0, 0))
        srf.blit(self._texture, (0, 0))

        center = (
            self._position[0] + self._size[0] / 2,
            self._position[1] + self._size[1] / 2,
        )

        # rotate and calculate correction for position
        srf = pygame.transform.rotate(srf, self._angle)
        _, _, w, h, = srf.get_rect()
        dx = int(w / 2) - int(self._size[0] / 2)
        dy = int(h / 2) - int(self._size[1] / 2)

        # corrected position
        px = self._position[0] - dx
        py = self._position[1] - dy
        # draw on window surface
        window.blit(srf, (px, py))

        # debug info

        # linear_v vector
        x = center[0] + math.sin(math.radians(self._angle)) * -100
        y = center[1] + math.cos(math.radians(self._angle)) * -100
        pygame.draw.line(window, (255, 255, 255), center, (x, y))
        vx, vy = self._linear_v
        x = vx + center[0]
        y = vy + center[1]
        pygame.draw.line(window, (0xBE, 0xDE, 0xAD), center, (x, y))


class StaticSprite:
    def __init__(self, texture: pygame.Surface):
        self.thrusting = False

        self._size = self._texture.get_rect()[2:]

        self._position = (400, 300)

        self._angle = 180
        self._angular_v = 0
        self._angular_a = 0

    def update(self, deltaT):
        px, py = self._position

        tetha = self._angle
        av = self._angular_v
        aa = self._angular_a

        # angular calculation
        self._angular_v = av + aa * deltaT

        self._angle = self._angle + av * deltaT + 0.5 * aa * deltaT ** 2

        if self._angle < 0:
            self._angle = 360

        if self._angle > 360:
            self._angle %= 360

    def draw(self, window: pygame.Surface):
        srf = pygame.Surface(self._size)
        srf.set_colorkey((0, 0, 0))
        srf.blit(self._texture, (0, 0))
        # pygame.draw.rect(srf, self._colour, ((0, 0), self._size))

        center = (
            self._position[0] + self._size[0] / 2,
            self._position[1] + self._size[1] / 2,
        )

        # rotate and calculate correction for position
        srf = pygame.transform.rotate(srf, self._angle)
        _, _, w, h, = srf.get_rect()
        dx = int(w / 2) - int(self._size[0] / 2)
        dy = int(h / 2) - int(self._size[1] / 2)

        # corrected position
        px = self._position[0] - dx
        py = self._position[1] - dy
        # draw on window surface
        window.blit(srf, (px, py))
