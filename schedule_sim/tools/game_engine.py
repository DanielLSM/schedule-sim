#for more info check https://github.com/openai/gym/blob/master/gym/envs/classic_control/rendering.py

from gym.envs.classic_control.rendering import *


class UnrealPython(Viewer):

    def __init__(self, width, height, display=None):
        Viewer.__init__(self)


if __name__ == "__main__":

    UP = UnrealPython(100, 100)
