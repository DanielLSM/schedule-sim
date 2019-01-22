import yaml
from schedule_sim import BaseEnv

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
# === Action Space ===
# discrete state space
# a_nk: n (aircraft) assign k (tasks) (discrete action space)
#
# === Time ===
# t = day , e.g, a_t = n (aircraft) assign k (tasks) on t (day)
#
# === Dynamics ===
#
# s_(t+1) = s_t + (1/)
#


class TaskDay(BaseEnv):

    def __init__(self):
        BaseEnv.__init__(self)
