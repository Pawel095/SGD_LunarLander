import pygame
import random
import math
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


class LinearParticle:
    def __init__(
        self,
        position=(0, 0),
        speed=((-100, 100), (-100, 100)),
        color_range=((0, 255), (0, 255), (0, 255)),
        size=((5, 20), (5, 20)),
        ttl=(1, 2),
    ):
        self.position = position
        self.speed = (
            random.uniform(speed[0][0], speed[0][1]),
            random.uniform(speed[1][0], speed[1][1]),
        )
        self.size = (
            random.uniform(size[0][0], size[0][1]),
            random.uniform(size[1][0], size[1][1]),
        )
        self.color = (
            random.uniform(color_range[0][0], color_range[0][1]),
            random.uniform(color_range[1][0], color_range[1][1]),
            random.uniform(color_range[2][0], color_range[2][1]),
        )
        self.ttl = random.uniform(ttl[0], ttl[1])
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


class AngularParticle(LinearParticle):
    def __init__(
        self,
        position=(0, 0),
        angle=(0, 359),
        speed=(10, 20),
        color_range=((0, 255), (0, 255), (0, 255)),
        size=((5, 20), (5, 20)),
        ttl=(1, 2),
    ):
        # unit vector
        ux = math.sin(math.radians(random.uniform(angle[0], angle[1])))
        uy = math.cos(math.radians(random.uniform(angle[0], angle[1])))
        newSpeed = random.uniform(speed[0], speed[1])
        ux *= newSpeed
        uy *= newSpeed
        super().__init__(
            position=position,
            speed=((ux - 100, ux + 100), (uy - 100, uy + 100)),
            color_range=color_range,
            size=size,
            ttl=ttl,
        )
