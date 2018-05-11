from collections import Counter, defaultdict

import numpy as np

from tmhmm.model import parse
from tmhmm.hmm import viterbi, forward, backward


__all__  = ['predict']


GROUP_NAMES = ('i', 'm', 'o')

NON_AMINOACID_CHARS = {
    'B': 'D',
    'X': 'A',
    'Z': 'E',
    '-': '',
}


def predict(sequence, header, model_or_filelike, compute_posterior=True):
    if isinstance(model_or_filelike, tuple):
        model = model_or_filelike
    else:
        _, model = parse(open(model_or_filelike))

    _, path = viterbi(sequence, *model)
    if compute_posterior:
        forward_table, constants = forward(sequence, *model)
        backward_table = backward(sequence, constants, *model)

        posterior = forward_table * backward_table
        _, _, _, char_map, label_map, name_map = model

        observations = len(sequence)
        states = len(name_map)

        # just counts how many states there are per label
        group_counts = Counter(label_map.values())

        table = np.zeros(shape=(observations, 3))
        for i in range(observations):
            group_probs = defaultdict(float)
            for j in range(states):
                group = label_map[j].lower()
                group_probs[group] += posterior[i, j]

            for k, group in enumerate(GROUP_NAMES):
                table[i, k] = group_probs[group]
        return path, table/table.sum(axis=1, keepdims=True)
    return path


def normalize_sequence(sequence, alphabet):
    """Normalize a sequence.
    
    This removes gaps and replaces ambiguous amino acid characters with hard-
    coded amino acids. Unknown characters are replaced with X.
    """
    return ''.join(
        NON_AMINOACID_CHARS.get(c, 'X')
        if c not in alphabet else c 
        for c in sequence
    )