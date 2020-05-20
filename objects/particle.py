from constants import WIDTH, HEIGHT
import random
from timeit import default_timer as time


class Particle:
    def __init__(
        self,
        position=(0, 0),
        speed=((0, 1), (0, 1)),
        color_range=((0, 255), (0, 255), (0, 255)),
        ttl=1,
    ):
        self.position = position
        self.speed = (
            random.randrange(speed[0][0], speed[0][1]),
            random.randrange(speed[1][0], speed[1][1]),
        )
        self.color = (
            random.randrange(color_range[0][0], color_range[0][1]),
            random.randrange(color_range[1][0], color_range[1][1]),
            random.randrange(color_range[2][0], color_range[2][1]),
        )
        self.ttl = ttl
        self.start = time()

    def update(self):
        pass

    def draw(self):
        pass
