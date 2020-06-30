# Introduction

This repository houses a Python 3.5+ implementation of transmembrane helix
hidden Markov model ([TMHMM](http://www.cbs.dtu.dk/services/TMHMM/)) originally
described in:

E\. L.L. Sonnhammer, G. von Heijne, and A. Krogh. **A hidden Markov model for
predicting transmembrane helices in protein sequences**. In J. Glasgow,
T. Littlejohn, F. Major, R. Lathrop, D. Sankoff, and C. Sensen, editors,
Proceedings of the Sixth International Conference on Intelligent Systems for
Molecular Biology, pages 175-182, Menlo Park, CA, 1998. AAAI Press.

# Why?

I did this for a few reasons:

- the source code is not available as part of the publication,
- the downloadable binaries are Linux-only,
- the downloadable binaries may not be redistributed, so it's not possible to
  put them in a Docker image or a VM for other people to use,
- the need to predict transmembrane helices on a large dataset, which rules
  out the web service.

This Python implementation includes a parser for the undocumented file format
used to describe the model and a pretty fast Cython implementation of the
Viterbi algorithm used to perform the annotation. The tool will output files
similar to the files produced by the original TMHMM implementation.

# Incompatibilities

* The original TMHMM implementation handles ambigious characters and gaps in an
  undocumented way. However, tmhmm.py does not attempt to handle such
  characters at all and will fail. A possible fix is to replace those
  characters with something also based on expert/domain knowledge. For details,
  see issue #9.

# Installation

This package supports Python 3.5, 3.6, and 3.7. Install with:

    $ pip install tmhmm.py

Only Linux is supported at the moment.

# Usage

    $ tmhmm -h
      usage: tmhmm [-h] -f SEQUENCE_FILE [-m MODEL_FILE] [-p]

      optional arguments:
        -h, --help            show this help message and exit
        -f SEQUENCE_FILE, --file SEQUENCE_FILE
                              path to file in fasta format with sequences
        -m MODEL_FILE, --model MODEL_FILE
                              path to the model to use
        -p, --plot            plot posterior probabilies

The `-p`/`--plot` option will only be available if `matplotlib` is installed
and importable.

Say we have the following sequence in FASTA format in a file called `test.fa`:

    >B9DFX7|1B|HMA8_ARATH Copper-transporting ATPase PAA2, chloroplastic  [Arabidopsis thaliana ]
    MASNLLRFPLPPPSSLHIRPSKFLVNRCFPRLRRSRIRRHCSRPFFLVSNSVEISTQSFESTESSIESVKSITSDTPIL
    LDVSGMMCGGCVARVKSVLMSDDRVASAVVNMLTETAAVKFKPEVEVTADTAESLAKRLTESGFEAKRRVSGMGVAENV
    KKWKEMVSKKEDLLVKSRNRVAFAWTLVALCCGSHTSHILHSLGIHIAHGGIWDLLHNSYVKGGLAVGALLGPGRELLF
    DGIKAFGKRSPNMNSLVGLGSMAAFSISLISLVNPELEWDASFFDEPVMLLGFVLLGRSLEERAKLQASTDMNELLSLI
    STQSRLVITSSDNNTPVDSVLSSDSICINVSVDDIRVGDSLLVLPGETFPVDGSVLAGRSVVDESMLTGESLPVFKEEG
    CSVSAGTINWDGPLRIKASSTGSNSTISKIVRMVEDAQGNAAPVQRLADAIAGPFVYTIMSLSAMTFAFWYYVGSHIFP
    DVLLNDIAGPDGDALALSLKLAVDVLVVSCPCALGLATPTAILIGTSLGAKRGYLIRGGDVLERLASIDCVALDKTGTL
    TEGRPVVSGVASLGYEEQEVLKMAAAVEKTATHPIAKAIVNEAESLNLKTPETRGQLTEPGFGTLAEIDGRFVAVGSLE
    WVSDRFLKKNDSSDMVKLESLLDHKLSNTSSTSRYSKTVVYVGREGEGIIGAIAISDCLRQDAEFTVARLQEKGIKTVL
    LSGDREGAVATVAKNVGIKSESTNYSLSPEKKFEFISNLQSSGHRVAMVGDGINDAPSLAQADVGIALKIEAQENAASN
    AASVILVRNKLSHVVDALSLAQATMSKVYQNLAWAIAYNVISIPIAAGVLLPQYDFAMTPSLSGGLMALSSIFVVSNSL
    LLQLHKSETSKNSL

We can then run tmhmm.py on this file using the following command:

    $ tmhmm -m TMHMM2.0.model -f test.fa

This produces a bunch of files. One is the summary:

    $ cat B9DFX7|1B|HMA8_ARATH.summary
    0-444: outside
    445-467: transmembrane helix
    468-820: inside
    821-843: transmembrane helix
    844-852: outside
    853-870: transmembrane helix
    871-882: inside

An annotation in FASTA format:

    $ cat B9DFX7|1B|HMA8_ARATH.annotation
    >B9DFX7|1B|HMA8_ARATH Copper-transporting ATPase PAA2, chloroplastic  [Arabidopsis thaliana ]
    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOMMMMMMMMMMMMMMMMMMMMMMMiiiiii
    iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
    iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
    iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
    iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
    iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiMMMMMMMMMMMMMMMMMMMMMMMoooooooooMMMMMMMMMMMMMMMM
    MMiiiiiiiiiiii

And finally a file containing the posterior probabilities for each label for
plotting.

    $ cat B9DFX7|1B|HMA8_ARATH.plot
    inside membrane outside
    0.20341044516 0.0 0.79658955484
    0.210104176071 2.77194446172e-08 0.78989579621
    0.189291062167 3.11365191554e-08 0.810708906697
    0.253334801857 7.17866017044e-07 0.746664480277
    0.126185012808 1.34197873962e-05 0.873801567405
    ...

If the `-p` flag is set a plot in PDF format will also be produced, following
the same naming scheme as the other output files.

# API

You can also use tmhmm.py as a library:

    import tmhmm
    annotation, posterior = tmhmm.predict(sequence_string)

This returns the annotation as a string and the posterior probabilities for
each label as a numpy array with shape `(len(sequence), 3)` where column 0, 1
and 2 corresponds to being inside, transmembrane and outside, respectively.

If you don't need the posterior probabilities set `compute_posterior=False`,
this will save quite a lot of computation:

    annotation, posterior = tmhmm.predict(
        sequence_string, compute_posterior=False
    )
