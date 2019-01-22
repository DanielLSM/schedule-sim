import yaml
import pathlib
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

    def __init__(self, parameters_file):
        BaseEnv.__init__(self)
        self.parameters = yaml_parser(parameters_file)
        print(self.parameters)


if __name__ == '__main__':

    parameteres_default_file = pathlib.Path(
        'config/task_day_custom.yaml').absolute()

    env = TaskDay(parameters_file=parameteres_default_file)
