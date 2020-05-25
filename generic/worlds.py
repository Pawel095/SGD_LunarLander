import generic.sprite
import pygame
import math


class Moon(generic.sprite.StaticSprite):
    def __init__(self, gravity, position, texture):
        self.gravity = gravity
        self._position = position
        if texture is None:
            self._texture = pygame.Surface((100, 100))
            pygame.draw.circle(self._texture, (255, 255, 255), (50, 50), 50)

        super().__init__(texture)

    def apply_gravity(self, s: generic.sprite.DynamicSprite):
        sprite_center = (
            s._position[0] + s._size[0] / 2,
            s._position[1] + s._size[1] / 2,
        )
        planet_center = (
            self._position[0] + self._size[0] / 2,
            self._position[1] + self._size[1] / 2,
        )
        cx, cy = sprite_center
        px, py = planet_center
        sx, sy = s._linear_a
        return (px - cx) * self.gravity + sx, (py - cy) * self.gravity + sy
