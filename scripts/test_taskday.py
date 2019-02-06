from schedule_sim.envs import parameteres_default_file, render_file, ENVS_DIR
from schedule_sim.envs.task_day import TaskDay

if __name__ == '__main__':

    print("=======")
    env = TaskDay(
        parameters_file=parameteres_default_file,
        reward_scale=10,
        debug=1,
        rendering=True,
        render_file=render_file)

    state = env.reset()
    total_reward = 0
    for _ in range(100):
        action = env.action_space.sample()
        next_state, reward, done, lul = env.step(action)
        total_reward += reward
        env.render()
        print("=======")
        print("Action: ", action)
        print("=======")
        print("Reward: {0:0.3f} /// Total Reward: {0:0.3f}".format(
            reward, total_reward))
        print("=======")
        print("State:")
        print(next_state)
    env.close()
