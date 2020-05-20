import pygame


class Lander:
    def __init__(self):
        self._position = (100, 100)
        self._linear_A = (0, 0)
        self._speed = (0, 0)
        self._angle = 30
        self._size = (100, 50)
        self._colour = (123, 123, 123)

    def update(self, deltaT):
        # Linear calculation
        px, py = self._position
        vx, vy = self._speed
        ax, ay = self._linear_A

        self._speed = (ax * deltaT + vx, ay * deltaT + vy)
        self._position = (
            px + vx * deltaT + 0.5 * ax * deltaT ** 2,
            py + vy * deltaT + 0.5 * ay * deltaT ** 2,
        )

        # angular calculation
        self._angle += 1

    def draw(self, window: pygame.Surface):
        srf = pygame.Surface(self._size)
        srf.set_colorkey((0,0,0))
        pygame.draw.rect(srf, self._colour, ((0, 0), self._size))

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

    @property
    def linear_A(self):
        return self._linear_A

    @linear_A.setter
    def linear_A(self, v):
        self._linear_A = v
