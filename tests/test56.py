"""Markov Chain Monte Carlo with People."""
import random

import judicious

ANIMAL = {
    "foot_spread": [0, 1],
    "body_height": [0.1, 1.5],
    "body_tilt": [-15, 45],
    "tail_length": [0.05, 1.2],
    "tail_angle": [-45, 190],
    "neck_length": [0, 2.5],
    "neck_angle": [90, 180],
    "head_length": [0.05, 0.75],
    "head_angle": [5, 80],
}


def random_animal():
    animal = {}
    for key, value in ANIMAL.items():
        animal[key] = random.uniform(value[0], value[1])
    return animal


def perturb(animal, coeff):
    for key, value in ANIMAL.items():
        range = value[1] - value[0]
        animal[key] += random.gauss(0, coeff * range)
    return animal


with judicious.Person() as person:
    options = [random_animal(), random_animal()]
    for _ in range(20):
        s = person.select_the_stick_animal("dog", options[0], options[1])
        options[~s] = perturb(options[s].copy(), coeff=0.1)
        random.shuffle(options)
