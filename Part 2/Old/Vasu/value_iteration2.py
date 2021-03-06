from transition_prob import *
import numpy as np

num_h = 5
num_a = 4
num_s = 3
gamma = 0.99
delta = 0.001
step_cost = -20
non_terminal_reward = 0
terminal_reward = 10
inf = 1e17

actions = ["SHOOT", "DODGE", "RECHARGE"]

states = np.array([(health, arrows, stamina) for health in range(num_h)
                   for arrows in range(num_a)
                   for stamina in range(num_s)])


def value_iteration():
    utilities = np.zeros(shape=(num_h, num_a, num_s))

    iterations = 0

    while True:
        new_utilities = np.zeros(shape=(num_h, num_a, num_s))

        # print("iteration=", iterations)
        print("iteration={}".format(iterations))

        for health, arrows, stamina in states:

            cur_state = tuple([health, arrows, stamina])

            if health == 0:
                continue

            cur_max = -inf

            for action in actions:

                if action == "SHOOT":
                    if stamina == 0 or arrows == 0:
                        continue

                elif action == "DODGE" and stamina == 0:
                    continue

                total_reward = 0
                cur = 0

                for h, a, s in states:

                    new_state = tuple([h, a, s])

                    if h == 0:
                        total_reward += (step_cost + terminal_reward) * transition_prob[cur_state][action][new_state]

                    else:
                        total_reward += (step_cost + non_terminal_reward) * transition_prob[cur_state][action][new_state]

                    cur += gamma * transition_prob[cur_state][action][new_state] * utilities[h, a, s]

                cur += total_reward

                if cur_max < cur:
                    cur_max = cur

            new_utilities[health, arrows, stamina] = cur_max

        for health, arrows, stamina in states:

            cur_state = tuple([health, arrows, stamina])

            if health == 0:
                # print(cur_state, "-1 0")
                print("({},{},{}):{}=[{}]".format(health, arrows, stamina, -1, round(new_utilities[health, arrows, stamina], 3)))
                continue

            cur_max = -inf
            cur_action = ""

            for action in actions:

                if action == "SHOOT":
                    if stamina == 0 or arrows == 0:
                        continue

                elif action == "DODGE" and stamina == 0:
                    continue

                cur = 0

                for h, a, s in states:
                    new_state = tuple([h, a, s])

                    if h == 0:
                        total_reward += (step_cost + terminal_reward) * transition_prob[cur_state][action][new_state]
                    else:
                        total_reward += (step_cost + non_terminal_reward) * transition_prob[cur_state][action][new_state]

                    cur += gamma * transition_prob[cur_state][action][new_state] * new_utilities[h, a, s]

                if cur_max < cur:
                    cur_max = cur
                    cur_action = action

            # print(cur_state, cur_action, round(new_utilities[health, arrows, stamina], 3)
            print("({},{},{}):{}=[{}]".format(health, arrows, stamina, cur_action, round(new_utilities[health, arrows, stamina], 3)))

        converged = np.max(np.abs(new_utilities - utilities)) < delta

        if converged:
            break

        utilities = new_utilities
        iterations += 1

        print()
        print()


value_iteration()
