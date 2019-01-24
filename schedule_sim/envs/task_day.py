import yaml
import pathlib
import numpy as np
from functools import partial

import gym
from gym import spaces

from schedule_sim import BaseEnv
from schedule_sim.tools.parser import yaml_parser
from schedule_sim.tools.costs import rectified_linear_cost

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

    def __init__(self, parameters_file, reward_scale=10, max_steps=300,
                 debug=0):
        BaseEnv.__init__(self)
        self.parameters = yaml_parser(parameters_file)
        self.observation_space_shape = (self.parameters['aircrafts']['total_number']* \
        self.parameters['tasks']['total_number'],1)

        self.ntasks_per_type, self.cost_fnc_per_type = self.distribute_tasks()
        self.state_trasition_model = self.setup_state_transition_model()
        self.reward_scale = reward_scale
        self.max_steps = max_steps

        self.observation_space = spaces.Box(
            low=0, high=1, shape=self.observation_space_shape, dtype=np.float32)
        self.action_space = spaces.Discrete(
            self.parameters['tasks']['total_number'] + 1)

        # This should be made with loggers later.....
        if debug:
            self.setup_print()

    def step(self, action):

        assert self.action_space.contains(
            action), "action outside of state space!"

        self.state -= self.state_trasition_model
        #TODO: Action will actually be more complext than just 0 and 1
        #TODO: action will probably be the argamax of a Q function, action goes from 1 to N

        if not action == self.parameters['tasks']['total_number']:
            self.state[action] = 1

        reward = self.reward_model()

        if self.steps == self.max_steps:
            done = True
            if all(_ >= 0 for _ in self.state):
                print("NO WRONG ASSIGNMENTS!")
        else:
            done = False

        self.steps += 1
        return np.array(self.state), reward, done, {}

    def reset(self):
        self.steps = 0
        self.state = self.np_random.uniform(
            low=0.1, high=0.0, size=(self.observation_space.shape[0],))
        return np.array(self.state)

    def reward_model(self):
        costs = []

        i = 0
        for _ in self.cost_fnc_per_type.keys():
            costs.extend(
                list(
                    map(self.cost_fnc_per_type[_],
                        self.state[i:i + self.ntasks_per_type[_]])))
            i += self.ntasks_per_type[_]

        assert len(costs) == self.parameters["tasks"]["total_number"]

        return sum(costs) / self.reward_scale

    def setup_state_transition_model(self):
        state_transition_model = []
        for ttype in self.ntasks_per_type.keys():
            for _ in range(self.ntasks_per_type[ttype]):
                state_transition_model.append(\
                1/self.parameters['tasks']['types'][ttype]['interval'])
        assert len(state_transition_model) == self.parameters['tasks'][
            'total_number'], "transition model incorrect!"
        return state_transition_model

    def distribute_tasks(self):
        tasks_distribution = {}
        cost_func = {}
        for task_type in self.parameters['tasks']['types'].keys():
            tasks_distribution[task_type] = round(\
            self.parameters['tasks']['types'][task_type]['ratio']*\
            self.parameters['tasks']['total_number'])

            linear_cost = self.parameters['tasks']['types'][task_type][
                'linear_cost_before_due_date']

            step_cost = self.parameters['tasks']['types'][task_type][
                'step_cost_after_due_date']

            cost_func[task_type] = partial(rectified_linear_cost, linear_cost,
                                           step_cost)

        assert cost_func.keys() == tasks_distribution.keys(
        ), "task type with invalid cost input!!"
        return tasks_distribution, cost_func

    def setup_print(self):
        print("====Environment setup complete====")
        print("State Space #S: ")
        print("Action Space #A: ")
        print("Initial_state S_0: ")
        print("===Task Distribution===")
        for ttype in self.parameters['tasks']['types'].keys():
            print("Task {} total:{}".format(ttype, self.ntasks_per_type[ttype]))
        print("===State Transition Model===")
        print(self.state_trasition_model)


if __name__ == '__main__':

    parameteres_default_file = pathlib.Path(
        'config/task_day_custom.yaml').absolute()

    cart = gym.make("CartPole-v0")
    s0 = cart.reset()
    print(s0)
    print("=======")
    env = TaskDay(
        parameters_file=parameteres_default_file, reward_scale=10, debug=1)

    state = env.reset()
    print(state)
    # np.array(self.state), reward, done, {}

    env.step(0)
    for _ in range(100):
        next_state, reward, done, lul = env.step(0)
        print("=======")
        print(reward)
