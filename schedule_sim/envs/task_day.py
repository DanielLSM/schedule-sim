import yaml
import pathlib
import numpy as np
from gym import spaces

from schedule_sim import BaseEnv
from schedule_sim.tools.parser import yaml_parser

# A scheduling game assigning aircraft tasks per day
#
# parameteres:
# custom: parameters/task_day_custom.yaml
# default: parameters/task_day_default.yaml
#
# === State Space ===
# continuos state space
# s_nk: n (aircraft) array of kr ratios r = (r1 = days_to_due_date)/(r2 = due_data_max_interval)
#
# === Initial State ==
# s_nk: random_float(0.8,1)
#
# === Action Space ===
# discrete state space
# a_nk: n (aircraft) assign k (tasks)
#
# === Time ===
# t = day , e.g, a_nkt = n (aircraft) assign k (tasks) on t (day)
#
# === Dynamics ===
# transition dynamics of the system
# s_niki_(t+1) = 1 for a_niki_t ; else s_nk_(t+1) = s_nk_(t+1) + transition_ratio_nk)
# the increased ratios can be computed beforehand for computational performance
# transition_ratio_nk = 1/max_interval_task_nk
#
# === Reward ===
#
# r=sum(cost(s_niki))
#
#


class TaskDay(BaseEnv):

    def __init__(self, parameters_file, debug=0):
        BaseEnv.__init__(self)
        self.parameters = yaml_parser(parameters_file)
        self.state_space_shape = (self.parameters['aircrafts']['total_number']* \
        self.parameters['tasks']['total_number'],1)

        self.ntasks_per_type = self.distribute_tasks()
        # import ipdb
        # ipdb.set_trace()
        self.state_space = spaces.Box(
            low=0, high=1, shape=self.state_space_shape, dtype=np.float32)
        self.action_space = spaces.Discrete(1)

        self.step: int = 0
        self.state = None
        self.prev_reward: np.float32 = 0
        self.reward: np.float32 = 0

        # This should be made with loggers later.....
        if debug:
            self.setup_print()

    # def step(self, action):
    #     assert self.action_space.contains(
    #         action), "action outside of state space!"
    #     self.state = self.state_transition_model()
    #     self.

    def reset(self):
        self.prev_reward = 0
        self.reward = 0
        self.state = self.sample_initial_state()

    def sample_initial_state(self):
        pass

    def reward_model(self, action):
        pass

    # def setup_state_transition_model(self):
    #     self.state_transition_model =
    #     pass

    def distribute_tasks(self):
        tasks_distribution = {}
        for task_type in self.parameters['tasks']['types'].keys():
            tasks_distribution[task_type] = round(\
            self.parameters['tasks']['types'][task_type]['ratio']*\
            self.parameters['tasks']['total_number'])
        return tasks_distribution

    def setup_print(self):
        print("====Environment setup complete====")
        print("State Space #S: ")
        print("Action Space #A: ")
        print("Initial_state S_0: ")
        print("===Task Distribution===")
        for ttype in self.parameters['tasks']['types'].keys():
            print("Task {} total:{}".format(ttype, self.ntasks_per_type[ttype]))


if __name__ == '__main__':

    parameteres_default_file = pathlib.Path(
        'config/task_day_custom.yaml').absolute()

    env = TaskDay(parameters_file=parameteres_default_file, debug=1)
