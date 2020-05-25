import pygame
import threading

assets = {}
loadingFinished = False


class worker(threading.Thread):
    def __init__(self, loadFunc, path, key, args=None):
        super().__init__()
        self.loadFunc = loadFunc
        self.path = path
        self.key = key
        self.args = args

    def run(self):
        if self.args is not None:
            assets[self.key] = self.loadFunc(self.path, *self.args)
        else:
            assets[self.key] = self.loadFunc(self.path)


class Loader:
    def load(self):
        threads = []
        threads.extend([
            worker(pygame.image.load,"assets/lander.png","lander"),
        ])
        [t.start() for t in threads]
        [t.join() for t in threads]
        loadingFinished = True

        if loadingFinished:
            pass

    def get(self, key):
        try:
            ret = assets[key]
        except KeyError as e:
            print(e)
        else:
            return ret
