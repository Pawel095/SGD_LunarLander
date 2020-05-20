import pygame


class Lander:
    def __init__(self):
        self._position = (100, 100)
        self._acceleration = (0, 0)
        self._speed = (0, 0)
        self._angle = 30

    def update(self, deltaT):
        # Linear calculation
        px, py = self._position
        vx, vy = self._speed
        ax, ay = self._acceleration

        self._speed = (ax * deltaT + vx, ay * deltaT + vy)
        self._position = (
            px + vx * deltaT + 0.5 * ax * deltaT ** 2,
            py + vy * deltaT + 0.5 * ay * deltaT ** 2,
        )

        # angular calculation
        self._angle += 1

    def draw(self, window: pygame.Surface):
        srf = pygame.Surface((100,50))
        srf.set_colorkey((0, 0, 0))
        srf.fill((50, 50, 50))
        pygame.draw.rect(srf, (123, 123, 123), ((0, 0), (100, 50)))
        srf = pygame.transform.rotate(srf, self._angle)
        window.blit(srf, self._position)

    @property
    def linear_A(self):
        return self._acceleration

    @linear_A.setter
    def linear_A(self, v):
        self._acceleration = v
