import pygame
import math
from objects.particle import Particle


class Lander:
    def __init__(self, texture):
        self._texture = pygame.transform.rotozoom(texture, 180, 0.25)

        self._size = self._texture.get_rect()[2:]

        self._position = (400, 300)
        self._linear_v = (0, 0)
        self._linear_a = (0, 0)

        self._angle = 180
        self._angular_v = 0
        self._angular_a = 0
        self._colour = (123, 123, 123)
        self._particles = []

    def update(self, deltaT):
        # Linear calculation
        px, py = self._position
        vx, vy = self._linear_v
        ax, ay = self._linear_a

        # grawitacja na księżycu
        ay += 40

        self._linear_v = (ax * deltaT + vx, ay * deltaT + vy)
        self._position = (
            px + vx * deltaT + 0.5 * ax * deltaT ** 2,
            py + vy * deltaT + 0.5 * ay * deltaT ** 2,
        )
        # angular calculation
        tetha = self._angle
        av = self._angular_v
        aa = self._angular_a

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

        # debug info
        # thrust vector
        x = center[0] + math.sin(math.radians(self._angle)) * -100
        y = center[1] + math.cos(math.radians(self._angle)) * -100
        pygame.draw.line(window, (255, 255, 255), center, (x, y))

        # linear_v vector
        pygame.draw.line(window, (255, 255, 255), center, (x, y))
        vx, vy = self._linear_v
        x = vx + center[0]
        y = vy + center[1]
        pygame.draw.line(window, (0xBE, 0xDE, 0xAD), center, (x, y))

    def apply_thrust(self, accel):
        a = math.sin(math.radians(self._angle))
        b = math.cos(math.radians(self._angle))
        self._particles = [Particle() for _ in range(30)]
        self.linear_a = (a * accel, b * accel)

    @property
    def linear_a(self):
        return self._linear_a

    @linear_a.setter
    def linear_a(self, v):
        self._linear_a = v

    @property
    def angular_a(self):
        return self._angular_a

    @angular_a.setter
    def angular_a(self, v):
        self._angular_a = v
