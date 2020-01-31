
from random import random, gauss
from copy import deepcopy
import numpy as np

from hurd.decision_model import ExpectedUtilityModel, ExpectedValueModel
from hurd.optimizers import (
    EvolutionaryGradientDescentOptimizer,
    GridSearchOptimizer
)

from hurd.dataset import Dataset
from hurd.utils import load_choices13k, float2str

import judicious

# judicious.seed("af842bad-f2d8-ee0f-6e52-a47296c1cb0e")
judicious.seed("f5be38d7-36eb-c209-6631-e437efffc0f0")

def unshuffle(l, order):
    """ unshuffles list given shuffled index """
    l_out = [0] * len(l)
    for i, j in enumerate(order):
        l_out[j] = l[i]
    return l_out


def sliding_avg(array, n):
    """Take a sliding average of non-overlapping n-sized chunks of an array."""
    array = np.array(array)
    out = []
    for i in range(0, len(array), n):
        out.append(np.mean(array[i: i + n]))
    return np.array(out)


def params2dataset(params):
    """ annoying and completely uninteresting helper function """
    D_dict = {
        "0": {  # one problem
            "A": [[params["pA1"], params["A1"]], [1 - params["pA1"], params["A2"]],],
            "B": [[params["pB1"], params["B1"]], [1 - params["pB1"], params["B2"]],],
        }
    }
    D = Dataset(dataset_id="single_problem")
    D.from_dict(D_dict)
    return D


def clip_params(params, perturbation=None):
    """ also not super intersting """
    for key in ["pA1", "pB1"]:
        if params[key] > 1.0:
            if perturbation is not None:
                perturbation[key] = params[key] - perturbation[key]
            params[key] = 1.0
        if params[key] < 0.0:
            if perturbation is not None:
                perturbation[key] = perturbation[key] - params[key]
            params[key] = 0.0
    if perturbation is None:
        return params
    else:
        return params, perturbation


# load a big human dataset for use once below
hgambles, hproblems, htargets = load_choices13k(include_amb=False)
human_dataset = Dataset(dataset_id="choices13k_noAmb")
human_dataset.from_dict(hgambles, hproblems)


class Human():
    """Actual homo sapiens."""

    def __init__(self, arg=None):
        super(Human, self).__init__()
        self.arg = arg

    def fit(self, dataset=None, targets=None):
        pass

    def predict(self, Ds=None):
        problems = []
        for D in Ds:
            d = list(D)[0].as_dict()
            PA1 = d['A']['probs'][0]
            A1 = d['A']['outcomes'][0]
            A2 = d['A']['outcomes'][1]
            PB1 = d['B']['probs'][0]
            B1 = d['B']['outcomes'][0]
            B2 = d['B']['outcomes'][1]
            problems.append((PA1, A1, A2, PB1, B1, B2))

        print(problems)
        rs = judicious.map(judicious.risky_choice, problems)
        ps = [1.0 * (r == 'A') for r in rs]
        ps2 = [[[p, 1-p]] for p in ps]
        return ps2


human_or_proxy = Human()

# # instantiate an EU model
# human_or_proxy = ExpectedUtilityModel(
#     util_func="PowerLossAverseUtil",  # use something else here?
#     # optimizer=EvolutionaryGradientDescentOptimizer(), # better but slow
#     optimizer=GridSearchOptimizer(grid_vals=[-0.3, 0.3]),
# )

# fit the EU model on the human dataset
# this helps make it a decent proxy for people
human_or_proxy.fit(dataset=human_dataset, targets=htargets)

# instantiate an EV model to break
model_to_break = ExpectedValueModel()

# params are probs and outcomes for each gamble (A and B)
params = {"pA1": 0.5, "A1": 1, "A2": 1, "pB1": 0.5, "B1": 1, "B2": 1}

n_gradient_updates = 20  # how many gradient updates
n_perturbations = 10  # how many perturbations to use to estimate gradient
# size of the param state perturbations, for each param type
noise_level_probs = 0.03
noise_level_outcomes = 0.4
lr = 1.0  # for gradient ascent; fixed for now

# number of subject ratings or predictions for each perturbation
# when a proxy model is used, this value has no effect since
# predictions are deterministic
n_choices_per_state = 15

for grad_i in range(n_gradient_updates):

    # first get all perturbations and perturbed states for this iteration
    perturbations = []
    perturbed_states = []
    for sample_i in range(n_perturbations):

        # add gaussian noise to the params
        perturbed_state = {}  # saves perturbed state
        perturbation = {}  # saves the noise components alone
        for k, v in params.items():
            if 'p' in k:
                noise = gauss(0, noise_level_probs)
            else:
                noise = gauss(0, noise_level_outcomes)
            perturbed_state[k] = v + noise
            perturbation[k] = noise

        # clip the input space to avoid non-probabitilies
        perturbed_state, perturbation = clip_params(
            deepcopy(perturbed_state), perturbation=deepcopy(perturbation)
        )

        perturbations.append(deepcopy(perturbation))
        perturbed_states.append(deepcopy(perturbed_state))

    # this should only be true when using real people, but works either way
    if n_choices_per_state > 1:

        # duplicate entries, e.g., [s1, s2] --> [s1, s1, s2, s2] when n = 2
        # this creates trials where multiple subjects provide judgments for each problem
        perturbed_states = [[ps] * n_choices_per_state for ps in perturbed_states]
        perturbed_states = np.array(perturbed_states).flatten()

        # shuffle indices so we know how to unshuffle perturbed_states later
        order = np.arange(len(perturbed_states))
        np.random.shuffle(order)
        perturbed_states = perturbed_states[order]

    # then get all predictions for the model_to_break
    model_preds = [
        model_to_break.predict(params2dataset(ps))[0][0] for ps in perturbed_states
    ]

    # get all predictions from the human / human proxy
    proxy_preds = human_or_proxy.predict([params2dataset(ps) for ps in perturbed_states])

    # if using real people, average per-subject results
    # the same is done for the model for consistency in the script
    if n_choices_per_state > 1:

        # unshuffle both
        model_preds = unshuffle(model_preds, order)
        proxy_preds = unshuffle(proxy_preds, order)

        # average results, e.g, [s1, s1, s2, s2] --> [s1, s2]
        model_preds = sliding_avg(model_preds, n_choices_per_state)
        proxy_preds = sliding_avg(proxy_preds, n_choices_per_state)

    # rewards are proportional to the disagreement between the models
    # here we use MSE but we could also use crossentropy
    rewards = (np.array(model_preds) - np.array(proxy_preds)) ** 2
    # the mean error here also approximates how well our last update was
    # this actually prints at the end of the print(dict2str(params) line below
    if grad_i:
        print("LOSS:", np.mean(rewards))
    # normalize rewards so they can be used to weight noise vectors
    rewards = (rewards - np.mean(rewards)) / np.std(rewards)

    # weight noise parts by rewards to get gradient
    grad = {k: 0.0 for k, v in params.items()}
    for i, perturbation in enumerate(perturbations):
        for key in perturbation.keys():
            grad[key] += perturbation[key] * rewards[i]

    # use the current gradient to update the problem state
    for key in params.keys():
        params[key] += lr * grad[key]

    # clip the new param state before the next gradient update round
    params = clip_params(deepcopy(params))

    print(
        "A: {} p({}) / {} p({})    |    B: {} p({}) / {} p({})   ---   ".format(
            *[
                float2str(_)
                for _ in [
                    params["A1"],
                    params["pA1"],
                    params["A2"],
                    1 - params["pA1"],
                    params["B1"],
                    params["pB1"],
                    params["B2"],
                    1 - params["pB1"],
                ]
            ]
        ),
        end="",
    )
