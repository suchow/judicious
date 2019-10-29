from random import shuffle, sample, random
from copy import deepcopy


def trial_sequences(
    n_stimuli, n_ratings, n_trials, n_retests, attributes=["trustworthy", "attractive"]
):
    """New sequence generation with repeats and indexes built in."""
    # crucial tests
    assert n_stimuli % n_trials == 0
    assert n_retests <= n_trials

    # unique stimulus IDs
    stimuli = list(range(1, n_stimuli + 1))

    # create lists of lists of trials
    sequences = {"faces": [], "repeats": [], "trial_indexes": [], "attributes": []}
    for attribute in attributes:
        for _ in range(n_ratings):

            # for each rating batch, shuffle stimuli
            shuffle(stimuli)
            stimuli_perm = deepcopy(stimuli)

            # partition the stimuli into n_trial chunks
            for i in range(0, n_stimuli, n_trials):
                faces = stimuli_perm[i : i + n_trials]
                retests = sample(faces, n_retests)
                shuffle(retests)                
                non_repeats = [False for s in range(len(faces))]
                seq_repeats = [True for s in range(len(retests))]
                repeats = non_repeats + seq_repeats
                faces += retests

                trial_indexes = [s for s in range(len(faces))]
                attributes = [attribute for s in range(len(faces))]

                sequences["faces"] += [faces]
                sequences["repeats"] += [repeats]
                sequences["trial_indexes"] += [trial_indexes]
                sequences["attributes"] += [attributes]

    return sequences


sequences = trial_sequences(n_stimuli=1000, n_ratings=30, n_trials=50, n_retests=10)
print(sequences)
