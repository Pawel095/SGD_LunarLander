import generic.sprite
import pygame
import math


class Planets:
    def __init__(self, gravities, positions, textures):
        self.sprites = []
        for i, p in enumerate(positions):
            self.sprites.append(Planet(gravities[i], p, textures[i]))

    def apply_gravity(self, s: generic.sprite.DynamicSprite):
        gravity_vector = [0, 0]
        # odjąć sx*planets i sy*planets
        for p in self.sprites:
            v = p.apply_gravity(s)
            gravity_vector = [
                gravity_vector[0] + v[0] - s._linear_a[0],
                gravity_vector[1] + v[1] - s._linear_a[1],
            ]
        gravity_vector[0] += s._linear_a[0]
        gravity_vector[1] += s._linear_a[1]
        return gravity_vector

    def update(self, deltaT):
        for p in self.sprites:
            p.update(deltaT)

    def draw(self, window):
        for p in self.sprites:
            p.draw(window)

    def __get_nearest(self, s: generic.sprite.DynamicSprite):
        min_distance = (None, 999999999999999999999999999999999999999)
        for p in self.sprites:
            sx, sy = s._position
            px, py = p._position
            distance = math.sqrt((sx - px) ** 2 + (sy - py) ** 2)

            if min_distance[1] >= distance:
                min_distance = (p, distance)
        return min_distance

    def check_if_collides(self, s: generic.sprite.DynamicSprite):
        p, _ = self.__get_nearest(s)
        return p.check_if_collides(s)

    def get_normal_vector(self, s: generic.sprite.DynamicSprite):
        p, _ = self.__get_nearest(s)
        return p.get_normal_vector(s._position)


class Planet(generic.sprite.BackgroundSprite):
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
        length += 0.00000000000001
        nx, ny = ((px - cx) / length, (py - cy) / length)
        sx, sy = s._linear_a
        return (
            ((nx * self.gravity) / length ** 2) + sx,
            ((ny * self.gravity) / length ** 2) + sy,
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
