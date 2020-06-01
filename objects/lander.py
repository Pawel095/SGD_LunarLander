import pygame
import math
import generic.sprite
from objects.particle import Particle, ParticleSystem


class Lander(generic.sprite.DynamicSprite):
    def __init__(self, position, texture, world):
        texture = pygame.transform.rotozoom(texture, 0, 0.25)
        self.thrusting = False
        self._colour = (123, 123, 123)
        self._particles = ParticleSystem()
        self.landed = False

        super().__init__(position, texture, world)

    def update(self, deltaT, window):
        center = (
            self._position[0] + self._size[0] / 2,
            self._position[1] + self._size[1] / 2,
        )
        # thrust vector
        thrust_x = int(math.sin(math.radians(self._angle)) * 500)
        thrust_y = int(math.cos(math.radians(self._angle)) * 500)
        # update particles
        self._particles.update(deltaT)
        if self.thrusting:
            self._particles.add_particles(
                Particle(
                    position=center,
                    speed=(
                        (thrust_x - 200, thrust_x + 200),
                        (thrust_y - 200, thrust_y + 200),
                    ),
                    color_range=((122, 255), (122, 217), (64, 122)),
                )
                for _ in range(3)
            )

        if self._world.check_if_collides(self):
            # check angle of rotation and planets normal
            #   if less than 30 deg, land
            center = (
                self._position[0] + self._size[0] / 2,
                self._position[1] + self._size[1] / 2,
            )
            px, py = self._world.get_normal_vector(center, window)
            cx = math.sin(math.radians(self._angle))
            cy = math.cos(math.radians(self._angle))

            dot = px * cx + py * cy
            c_len = math.sqrt(cx ** 2 + cy ** 2)
            p_len = math.sqrt(px ** 2 + py ** 2)
            angle = math.degrees(math.acos(dot / c_len * p_len))
            print(f"angle: {angle}")

            # check speed, if less than 100, land
            # else explode
            pass
        else:
            super().update(deltaT)
            pass

    def draw(self, window: pygame.Surface):
        # draw particles
        self._particles.draw(window)

        center = (
            self._position[0] + self._size[0] / 2,
            self._position[1] + self._size[1] / 2,
        )

        # debug info

        # linear_v vector
        x = center[0] + math.sin(math.radians(self._angle)) * 100
        y = center[1] + math.cos(math.radians(self._angle)) * 100
        pygame.draw.line(window, (255, 255, 255), center, (x, y))
        vx, vy = self._linear_v
        x = vx + center[0]
        y = vy + center[1]
        pygame.draw.line(window, (0xBE, 0xDE, 0xAD), center, (x, y))
        super().draw(window)

    def enable_thrust(self, accel):
        self.thrusting = True
        a = math.sin(math.radians(self._angle))
        b = math.cos(math.radians(self._angle))
        self.linear_a = (-a * accel, -b * accel)

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
