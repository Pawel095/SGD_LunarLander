import pygame
from constants import WIDTH, HEIGHT
import random
from timeit import default_timer as time


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def add_particles(self, particles):
        self.particles.extend(particles)

    def update(self, deltaT):
        for p in self.particles:
            p.update(deltaT)
            if p.check_ttl():
                self.particles.remove(p)

    def draw(self, window: pygame.Surface):
        [p.draw(window) for p in self.particles]

    def __getitem__(self, item):
        return self.particles[item]


class Particle:
    def __init__(
        self,
        position=(0, 0),
        speed=((-100, 100), (-100, 100)),
        color_range=((0, 255), (0, 255), (0, 255)),
        size=((5, 20), (5, 20)),
        ttl=1,
    ):
        self.position = position
        self.speed = (
            random.randrange(speed[0][0], speed[0][1]),
            random.randrange(speed[1][0], speed[1][1]),
        )
        self.size = (
            random.randrange(size[0][0], size[0][1]),
            random.randrange(size[1][0], size[1][1]),
        )
        self.color = (
            random.randrange(color_range[0][0], color_range[0][1]),
            random.randrange(color_range[1][0], color_range[1][1]),
            random.randrange(color_range[2][0], color_range[2][1]),
        )
        self.ttl = ttl
        self.start = time()

    def update(self, deltaT):
        px, py = self.position
        vx, vy = self.speed
        self.position = (px + vx * deltaT, py + vy * deltaT)

    def check_ttl(self):
        if time() - self.start > self.ttl:
            return True
        else:
            return False

    def draw(self, window: pygame.Surface):
        pygame.draw.rect(window, self.color, (self.position, self.size))
