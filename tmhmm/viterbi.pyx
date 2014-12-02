import numpy as np

cimport numpy as np
cimport cython

DTYPE = np.double
ctypedef np.double_t DTYPE_t


@cython.boundscheck(False)
def viterbi(sequence,
            np.ndarray[DTYPE_t, ndim=1] initial,
            np.ndarray[DTYPE_t, ndim=2] transitions,
            np.ndarray[DTYPE_t, ndim=2] emissions,
            char_map, label_map, name_map):
    """
    Compute the most probable path through the model given the sequence.

    This function implements Viterbi's algorithm in log-space.

    :param sequence str: a string over the alphabet specified by the model.
    :rtype: tuple(matrix, optimal_path)
    :return: a tuple consisting of the dynamic programming table and the
             optimal path.
    """

    cdef int no_observations = len(sequence)
    cdef int no_states = len(initial)

    cdef float neginf = -np.inf

    # work in log space
    initial = np.log(initial)
    transitions = np.log(transitions)
    emissions = np.log(emissions)

    cdef np.ndarray[DTYPE_t, ndim=2] M = \
        np.zeros([2, no_states],dtype=DTYPE)
    cdef np.ndarray[np.int_t, ndim=2] P = \
        np.zeros([no_observations, no_states], dtype=np.int)

    cdef unsigned int i, j, k, max_state, next_state, observation
    cdef double max_state_prob, prob

    observation = char_map[sequence[0]]
    for i in range(no_states):
        M[0, i] = initial[i] + emissions[i, observation]

    for i in range(1, no_observations):
        observation = char_map[sequence[i]]
        for j in range(no_states):
            max_state = 0
            max_state_prob = neginf
            for k in range(no_states):
                prob = M[(i - 1) % 2, k] + transitions[k, j]
                if prob > max_state_prob:
                    max_state, max_state_prob = k, prob
            M[i % 2, j] = max_state_prob + emissions[j, observation]
            P[i, j] = max_state

    # TODO: figure out why stuff doesn't work when using cython without turning
    #       the range generator into a list first.
    # TODO: stuff crashes if one uses reversed(range(no_observations)), why?

    backtracked = []
    next_state = np.argmax(M[no_observations % 2,], axis=0)
    for i in list(range(no_observations - 1, -1, -1)):
        backtracked.append(label_map[next_state])
        next_state = P[i, next_state]

    return M, ''.join(reversed(backtracked))
