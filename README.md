# Introduction

This repository houses a Python 3 implementation of transmembrane helix hidden Markov model ([TMHMM](http://www.cbs.dtu.dk/services/TMHMM/)) originally described in:

E\. L.L. Sonnhammer, G. von Heijne, and A. Krogh. **A hidden Markov model for predicting transmembrane helices in protein sequences**. In J. Glasgow, T. Littlejohn, F. Major, R. Lathrop, D. Sankoff, and C. Sensen, editors, Proceedings of the Sixth International Conference on Intelligent Systems for Molecular Biology, pages 175-182, Menlo Park, CA, 1998. AAAI Press.

# Why?

I did this for a few reasons:

- the source code is not available as part of the publication,
- the downloadable binaries are Linux-only,
- the downloadable binaries may not be redistributed, so it's not possible to
  put them in a Docker image or a VM for other people to use,
- the need to predict transmembrane helices on a large dataset, which rules
  out the web service.

This Python implementation includes a parser for the undocumented file format
used to describe the model and a pretty fast Cython implementation of the Viterbi algorithm used to perform the annotation.

# Installation

The package is not available at PyPI yet, but installation is pretty trivial:

    git clone https://github.com/dansondergaard/tmhmm.py.git
    python setup.py install

# Usage

    $ tmhmm -h
    usage: tmhmm.py [-h] -f SEQUENCE_FILE [-m MODEL_FILE]

    optional arguments:
      -h, --help            show this help message and exit
      -f SEQUENCE_FILE, --file SEQUENCE_FILE
                            path to file in fasta format with sequences
      -m MODEL_FILE, --model MODEL_FILE
                            path to the model to use

    $ tmhmm -m TMHMM2.0.model -f test.fa
    0-444: outside
    445-467: transmembrane helix
    468-820: inside
    821-843: transmembrane helix
    844-852: outside
    853-870: transmembrane helix
    871-882: inside

    >Some protein
    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOMMMMM
    MMMMMMMMMMMMMMMMMMiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
    iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
    iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
    iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
    iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiMMMM
    MMMMMMMMMMMMMMMMMMMoooooooooMMMMMMMMMMMMMMMMMMiiiiiiiiiiii


# Dependencies

* scikit-bio
* numpy
