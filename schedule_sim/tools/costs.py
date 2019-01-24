import math
import numpy as np


# Cost should decrease from -1 to 0, then from
def rectified_linear_cost(linear_cost, max_cost, state):
    if state < 0:
        return max_cost
    elif 0 <= state <= 0:
        return 0
    elif 0.1 <= state <= 1:
        return state * linear_cost
    else:
        raise ("STATE IS INVALID!!!")


if __name__ == '__main__':
    from functools import partial

    p = partial(rectified_linear_cost, -1, -10)

    print(p(0.999))