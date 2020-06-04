from pygame import Rect
from constants import WIDTH, HEIGHT


class Camera(object):
    _instance = None

    def __new__(cls, camera_func, width, height):
        if cls._instance is None:
            print("Creating new camera")
            cls._instance = super(Camera, cls).__new__(cls)
            cls.init(camera_func, width, height)
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls._instance

    @classmethod
    def init(cls, camera_func, width, height):
        cls.camera_func = camera_func
        cls.state = Rect(0, 0, width, height)

    def get_transform(self, position):
        # move to postition in rect
        return (
            position[0] + self.state[0],
            position[1] + self.state[1],
        )

    def update(self, target):
        self.state = self.camera_func(
            self.state, Rect((target._position, target._size))
        )


def simple_follow(self, camera, target_rect):
    px, py, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-px + WIDTH / 2, -py + HEIGHT / 2, w, h)
