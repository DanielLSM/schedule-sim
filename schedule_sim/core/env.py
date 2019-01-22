#### code based on https://github.com/openai/gym/
import numpy as np

import gym

from gym.utils import seeding, EzPickle


class BaseEnv(gym.Env, EzPickle):

    def __init__(self):
        EzPickle.__init__(self)
        self.seed()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]
