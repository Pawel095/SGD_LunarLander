import pygame
import math
import generic.sprite
from objects.particle import LinearParticle, AngularParticle, ParticleSystem


class Lander(generic.sprite.DynamicSprite):
    def __init__(self, position, texture, world):
        texture = pygame.transform.rotozoom(texture, 0, 0.25)
        self.thrusting = False
        self._colour = (123, 123, 123)
        self._particles = ParticleSystem()
        self.landed = False
        self.exploded = False

        super().__init__(position, texture, world)

    def update(self, deltaT):
        center = (
            self._position[0] + self._size[0] / 2,
            self._position[1] + self._size[1] / 2,
        )
        # thrust vector
        thrust_x = int(math.sin(math.radians(self._angle)) * 500)
        thrust_y = int(math.cos(math.radians(self._angle)) * 500)
        # update particles
        self._particles.update(deltaT)

        if self.thrusting and not self.exploded:
            camera_transform = self._camera.get_transform(center)
            self._particles.add_particles(
                [
                    LinearParticle(
                        position=camera_transform,
                        speed=(
                            (thrust_x - 200, thrust_x + 200),
                            (thrust_y - 200, thrust_y + 200),
                        ),
                        color_range=((122, 255), (122, 217), (64, 122)),
                    )
                    for _ in range(3)
                ]
            )

        if self._world.check_if_collides(self) and not self.landed:
            self.landed = True
            center = (
                self._position[0] + self._size[0] / 2,
                self._position[1] + self._size[1] / 2,
            )
            px, py = self._world.get_normal_vector(self)
            cx = math.sin(math.radians(self._angle))
            cy = math.cos(math.radians(self._angle))

            dot = px * cx + py * cy
            c_len = math.sqrt(cx ** 2 + cy ** 2)
            p_len = math.sqrt(px ** 2 + py ** 2)
            angle = math.degrees(math.acos(dot / c_len * p_len))
            speed = math.sqrt(self._linear_v[0] ** 2 + self._linear_v[1] ** 2)
            print(f"angle: {angle}")
            print(f"Velocity: {speed}")

            # check angle of rotation and planets normal
            #   if less than 30 deg, land
            # check speed, if less than 100, land
            # else explode
            if angle <= 15 and speed <= 100:
                print("Landing succesfull")
            else:
                self.exploded = True
                camera_transform = self._camera.get_transform(center)
                x, y = self._world.get_normal_vector(self)
                angle = math.degrees(math.atan2(y, x))
                angle += 180
                print(angle)
                self._particles.add_particles(
                    [
                        AngularParticle(
                            position=camera_transform,
                            angle=(angle - 10, angle + 10),
                            speed=(100, 200),
                        )
                        for _ in range(300)
                    ]
                )

            self._linear_a = (0, 0)
            self._linear_v = (0, 0)
        elif self.landed:
            if self.thrusting:
                self._linear_v = (-thrust_x / 100, -thrust_y / 100)
                self._angular_a = 0
                super().update(deltaT)
                self.landed = False
        else:
            # space flight
            super().update(deltaT)

    def draw(self, window: pygame.Surface):
        self._particles.draw(window)
        if not self.exploded:
            # draw particles

            center = (
                self._position[0] + self._size[0] / 2,
                self._position[1] + self._size[1] / 2,
            )

            # debug info
            # linear_v vector
            x = center[0] + math.sin(math.radians(self._angle)) * 100
            y = center[1] + math.cos(math.radians(self._angle)) * 100
            center_transform = self._camera.get_transform(center)
            x, y = self._camera.get_transform((x, y))
            pygame.draw.line(window, (255, 255, 255), center_transform, (x, y))

            # acceletarion vector
            vx, vy = self._linear_v
            x = vx + center[0]
            y = vy + center[1]
            x, y = self._camera.get_transform((x, y))
            pygame.draw.line(window, (0xBE, 0xDE, 0xAD), center_transform, (x, y))
            super().draw(window)

    def main_thruster(self, accel):
        self.thrusting = True
        a = math.sin(math.radians(self._angle))
        b = math.cos(math.radians(self._angle))
        self._linear_a = (-a * accel, -b * accel)

    def disable_main_thruster(self):
        self.thrusting = False
        self._linear_a = (0, 0)

    def rcs(self, accel):
        self._angular_a = accel

    def disable_rcs(self):
        self._angular_a = 0
