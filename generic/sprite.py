import pygame
import math
import copy


def _linear_update(self, deltaT):
    px, py = self._position
    vx, vy = self._linear_v
    ax, ay = self._world.apply_gravity(self)

    # Linear calculation
    self._linear_v = (ax * deltaT + vx, ay * deltaT + vy)
    self._position = (
        px + vx * deltaT + 0.5 * ax * deltaT ** 2,
        py + vy * deltaT + 0.5 * ay * deltaT ** 2,
    )


def _angular_update(self, deltaT):
    av = self._angular_v
    aa = self._angular_a
    # angular calculation
    self._angular_v = av + aa * deltaT

    self._angle = self._angle + av * deltaT + 0.5 * aa * deltaT ** 2

    if self._angle < 0:
        self._angle = 360

    if self._angle > 360:
        self._angle %= 360


class DynamicSprite:
    def __init__(self, position, texture: pygame.Surface, world):
        self._world = world
        self.thrusting = False
        self._texture=texture

        self._size = self._texture.get_rect()[2:]
        self._collision_radius = max(self._size) / 2

        self._position = position
        self._linear_v = (0, 0)
        self._linear_a = (0, 0)

        self._angle = 0
        self._angular_v = 0
        self._angular_a = 0
        self._lastDeltaT = 1

    def update(self, deltaT):
        self._lastDeltaT = deltaT
        _linear_update(self, deltaT)
        _angular_update(self, deltaT)

    def get_self_on_next_iteration(self):
        future_self = copy.copy(self)
        deltaT = self._lastDeltaT
        _linear_update(future_self, deltaT)
        _angular_update(future_self, deltaT)

        return future_self

    def draw(self, window: pygame.Surface):
        srf = pygame.Surface(self._size)
        srf.set_colorkey((0, 0, 0))
        srf.blit(self._texture, (0, 0))

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


class StaticSprite:
    def __init__(self, position, texture: pygame.Surface):
        self.thrusting = False

        self._size = self._texture.get_rect()[2:]
        self._collision_radius = (max(self._size) / 2)*0.75
        self._position = position
        self._angle = 180
        self._angular_v = 0
        self._angular_a = 0

    def update(self, deltaT):
        px, py = self._position

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
