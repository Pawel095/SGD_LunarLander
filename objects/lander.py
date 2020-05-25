import pygame
import math
import generic.sprite
from objects.particle import Particle, ParticleSystem


class Lander(generic.sprite.DynamicSprite):
    def __init__(self, texture, world):
        self._texture = pygame.transform.rotozoom(texture, 180, 0.25)
        self.thrusting = False

        self._size = self._texture.get_rect()[2:]

        self._position = (400, 300)
        self._linear_v = (0, 0)
        self._linear_a = (0, 0)

        self._angle = 180
        self._angular_v = 0
        self._angular_a = 0
        self._colour = (123, 123, 123)
        self._particles = ParticleSystem()
        super().__init__(texture, world)

    def update(self, deltaT):
        center = (
            self._position[0] + self._size[0] / 2,
            self._position[1] + self._size[1] / 2,
        )
        # thrust vector
        x = int(math.sin(math.radians(self._angle)) * -500)
        y = int(math.cos(math.radians(self._angle)) * -500)
        # update particles
        self._particles.update(deltaT)
        if self.thrusting:
            self._particles.add_particles(
                # 255, 217, 64
                # 122, 122, 122
                Particle(
                    center,
                    ((x - 200, x + 200), (y - 200, y + 200)),
                    ((122, 255), (122, 217), (64, 122)),
                )
                for _ in range(3)
            )
        center = (
            self._position[0] + self._size[0] / 2,
            self._position[1] + self._size[1] / 2,
        )

        super().update(deltaT)

    def draw(self, window: pygame.Surface):
        # draw particles
        self._particles.draw(window)

        center = (
            self._position[0] + self._size[0] / 2,
            self._position[1] + self._size[1] / 2,
        )

        # thrust vector
        x = center[0] + math.sin(math.radians(self._angle)) * -100
        y = center[1] + math.cos(math.radians(self._angle)) * -100
        pygame.draw.line(window, (255, 255, 255), center, (x, y))
        super().draw(window)

    def enable_thrust(self, accel):
        self.thrusting = True
        a = math.sin(math.radians(self._angle))
        b = math.cos(math.radians(self._angle))
        self.linear_a = (a * accel, b * accel)

    def disable_thrust(self):
        self.thrusting = False
        self._linear_a = (0, 0)

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
