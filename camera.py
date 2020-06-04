class Camera(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Creating the object")
            cls._instance = super(Camera, cls).__new__(cls)
            cls.init()
        return cls._instance

    @classmethod
    def init(cls):
        cls.position = (100, 100)

    def update(self, deltaT):
        pass

    def get_transform(self):
        return self.position
