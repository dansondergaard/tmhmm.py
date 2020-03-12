import argparse
import itertools
import os.path
import textwrap

from .api import predict
from .model import parse
from .utils import (
    dump_posterior_file,
    load_posterior_file,
    load_fasta_file,
)

has_matplotlib = True
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
except ImportError:
    has_matplotlib = False


DEFAULT_MODEL = os.path.join(os.path.dirname(__file__), 'TMHMM2.0.model')


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


def plot(posterior_file, outputfile):
    inside, membrane, outside = load_posterior_file(posterior_file)

    plt.figure(figsize=(16, 8))
    plt.title('Posterior probabilities')
    plt.suptitle('tmhmm.py')
    plt.plot(inside, label='inside', color='blue')
    plt.plot(membrane, label='transmembrane', color='red')
    plt.fill_between(range(len(inside)), membrane, color='red')
    plt.plot(outside, label='outside', color='black')
    plt.legend(frameon=False, bbox_to_anchor=[0.5, 0],
               loc='upper center', ncol=3, borderaxespad=1.5)
    plt.tight_layout(pad=3)
    plt.savefig(outputfile)


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', dest='sequence_file',
                        type=argparse.FileType('r'), required=True,
                        help='path to file in fasta format with sequences')
    parser.add_argument('-m', '--model', dest='model_file',
                        type=argparse.FileType('r'), default=DEFAULT_MODEL,
                        help='path to the model to use')
    if has_matplotlib:
        parser.add_argument('-p', '--plot', dest='plot_posterior',
                            action='store_true',
                            help='plot posterior probabilies')

    args = parser.parse_args()

    header, model = parse(args.model_file)
    for entry in load_fasta_file(args.sequence_file):
        path, posterior = predict(entry.sequence, header, model)

        with open(entry.id + '.summary', 'w') as summary_file:
            for start, end, state in summarize(path):
                print("{} {} {}".format(start, end, PRETTY_NAMES[state]),
                      file=summary_file)

        with open(entry.id + '.annotation', 'w') as ann_file:
            print('>', entry.id, ' ', entry.description, sep='', file=ann_file)
            for line in textwrap.wrap(path, 79):
                print(line, file=ann_file)

        plot_filename = entry.id + '.plot'
        with open(plot_filename, 'w') as plot_file:
            dump_posterior_file(plot_file, posterior)

        if hasattr(args, 'plot_posterior') and args.plot_posterior:
            with open(plot_filename, 'r') as fileobj:
                plot(fileobj, entry.id + '.pdf')
