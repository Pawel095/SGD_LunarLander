import generic.sprite
import pygame
import math


class Planet(generic.sprite.StaticSprite):
    def __init__(self, gravity, position, texture):
        self.gravity = gravity
        if texture is None:
            self._texture = pygame.Surface((100, 100))
            pygame.draw.circle(self._texture, (255, 255, 255), (50, 50), 50)

        super().__init__(position, texture)

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
        length = math.sqrt((px - cx) ** 2 + (py - cy) ** 2)
        nx, ny = ((px - cx) / length, (py - cy) / length)
        sx, sy = s._linear_a
        return (
            (nx * self.gravity) / length ** 2 + sx,
            (ny * self.gravity) / length ** 2 + sy,
        )

    def draw(self, window):
        super().draw(window)

    def check_if_collides(self, s: generic.sprite.DynamicSprite):
        future_s = s.get_self_on_next_iteration()
        x1, y1 = (
            self._position[0] + self._size[0] / 2,
            self._position[1] + self._size[1] / 2,
        )
        x2, y2 = (
            future_s._position[0] + future_s._size[0] / 2,
            future_s._position[1] + future_s._size[1] / 2,
        )

        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        distance -= self._collision_radius
        distance -= s._collision_radius
        return distance <= 0

    def get_normal_vector(self, outside_point):
        planet_center = (
            self._position[0] + self._size[0] / 2,
            self._position[1] + self._size[1] / 2,
        )
        px, py = planet_center
        cx, cy = outside_point
        length = math.sqrt((px - cx) ** 2 + (py - cy) ** 2)
        return ((px - cx) / length, (py - cy) / length)
