"""Stochastic gradient ascent to find where theories fail."""

import random

import numpy as np
np.set_printoptions(precision=4)

import judicious

judicious.register("http://127.0.0.1:5000")
# judicious.register("https://imprudent.herokuapp.com")


def EV(PA1, A1, B1, PA2, A2, B2, L=1):
    """Expected value theory w/ softmax Luce choice axiom."""
    EV1 = PA1 * A1 + (1 - PA1) * B1
    EV2 = PA2 * A2 + (1 - PA2) * B2
    return (EV1**L) / (EV1**L + EV2**L)


def state2problem(s, alpha=1):
    """Convert from a real-valued state to a choice problem.

    Alpha controls the scaling of the values."""
    PA1 = 1.0/(1+np.exp(-s[0]))
    A1 = s[1] * alpha
    B1 = s[2] * alpha
    A2 = s[3] * alpha
    B2 = s[4] * alpha
    PA2 = 1.0/(1+np.exp(-s[3]))
    return np.array([PA1, A1, B1, PA2, A2, B2])


NUM_ROUNDS = 50
NOISE_LEVEL = 0.25
ALPHA = 0.95
N = 4  # Number of decision problems per round.
M = 2   # Number of participants per decision problem.

state = np.zeros((1, 6)).astype('float32')

for j in range(NUM_ROUNDS):

    print("Round {}".format(j))
    print("Seed is {}".format(state[0]))
    print("Seed problem is {}".format(state2problem(state[0])))
    print("Step size is {}".format((ALPHA ** j)/(N*NOISE_LEVEL)))

    noise = np.random.normal(scale=NOISE_LEVEL, size=(N, 6))
    problem_states = state + np.tile(noise, (M, 1))

    # Collect the data.
    results = judicious.map(
        judicious.risky_choice,
        [tuple(state2problem(problem_states[i, :])) for i in range(M*N)]
    )

    # Analyze the results.
    scores = np.mean((np.reshape(results, (M, N)) == 'A').astype('float32'), axis=0)
    z_scores = (scores - scores.mean())/scores.std()
    gradient = np.dot(noise.T, z_scores)/(N*NOISE_LEVEL)
    state = state + (ALPHA**j) * gradient.T
