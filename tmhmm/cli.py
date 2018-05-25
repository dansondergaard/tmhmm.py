import argparse
import itertools
import os.path
import textwrap
import multiprocessing as mp

import skbio as sk

import tmhmm

from tmhmm.model import parse
from tmhmm import predict


APP_DIR = os.path.dirname(tmhmm.__path__[0])
DEFAULT_MODEL = os.path.join(APP_DIR, 'TMHMM2.0.model')


PRETTY_NAMES = {
    'i': 'inside',
    'M': 'transmembrane helix',
    'o': 'outside',
    'O': 'outside'
}


def summarize(path):
    """
    Summarize a path as a list of (start, end, state) triples.
    """
    for state, group in itertools.groupby(enumerate(path), key=lambda x: x[1]):
        group = list(group)
        start = min(group, key=lambda x: x[0])[0]
        end = max(group, key=lambda x: x[0])[0]
        yield start, end, state


def plot(datafile, outputfile):
    try:
        import pandas as pd
        import matplotlib.pyplot as plt
    except ImportError:
        print('Error: Packages pandas and matplotlib are required', end='')
        print('for plotting, but could not be found. Exiting.')
    else:
        data = pd.read_csv(datafile, sep=' ', index_col=False)

        plt.figure(figsize=(16, 8))
        plt.title('Posterior probabilities')
        plt.suptitle('tmhmm.py')
        plt.plot(data.inside, label='inside', color='blue')
        plt.plot(data.membrane, label='transmembrane', color='red')
        plt.fill_between(range(len(data)), data.membrane, color='red')
        plt.plot(data.outside, label='outside', color='black')
        plt.legend(frameon=False, bbox_to_anchor=[0.5, 0],
                   loc='upper center', ncol=3, borderaxespad=1.5)
        plt.tight_layout(pad=3)
        plt.savefig(outputfile)

def process_record(record):
    path, posterior = predict(str(record), model)

    with open(record.metadata['id'] + '.summary', 'w') as summary_file:
        for start, end, state in summarize(path):
            print("{} {} {}".format(start, end, PRETTY_NAMES[state]),
                  file=summary_file)

    with open(record.metadata['id'] + '.annotation', 'w') as ann_file:
        print('>', record.metadata['id'], ' ', record.metadata['description'], sep='', file=ann_file)
        for line in textwrap.wrap(path, 79):
            print(line, file=ann_file)

    plot_filename = record.metadata['id'] + '.plot'
    with open(plot_filename, 'w') as plot_file:
        print('inside', 'membrane', 'outside', file=plot_file)
        for i in range(len(str(record))):
            print('{} {} {}'.format(posterior[i, 0],
                                    posterior[i, 1],
                                    posterior[i, 2]), file=plot_file)

    if args.plot_posterior:
        plot(plot_filename, record.metadata['id'] + '.pdf')


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', dest='sequence_file',
                        type=argparse.FileType('r'), required=True,
                        help='path to file in fasta format with sequences')
    parser.add_argument('-m', '--model', dest='model_file',
                        type=argparse.FileType('r'), default=DEFAULT_MODEL,
                        help='path to the model to use')
    parser.add_argument('-p', '--plot', dest='plot_posterior', action='store_true',
                        help='plot posterior probabilies')

    global args, header, model
    args = parser.parse_args()
    print("parsing %s\n" % args.model_file)
    header, model = parse(args.model_file)


    records = list(sk.io.read(args.sequence_file, format='fasta'))

    # process records in parallel
    p = mp.Pool(processes = mp.cpu_count())
    p.map(process_record, records)
    p.close()
    p.join()
