import generic.sprite


class Moon:
    def __init__(self, gravity):
        self.gravity = gravity

    def apply_gravity(self, s: generic.sprite.Sprite):
        return (s._linear_a[0], s._linear_a[1] + 40)
