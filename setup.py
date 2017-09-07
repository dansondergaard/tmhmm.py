from setuptools import setup
from Cython.Build import cythonize

import numpy

setup(
    name='tmhmm.py',
    version='1.1',
    author='Dan Søndergaard',
    author_email='das@birc.au.dk',
    description='A transmembrane helix finder.',
    url='https://github.com/dansondergaard/tmhmm.py/',
    entry_points={
        'console_scripts': ['tmhmm=tmhmm.cli:cli'],
    },
    install_requires=['numpy>=1.9', 'scikit-bio>=0.5'],
    packages=['tmhmm'],
    ext_modules=cythonize('tmhmm/hmm.pyx', include_path=[numpy.get_include()]),
    include_dirs=[numpy.get_include()],
    data_files=[('', ['TMHMM2.0.model'])]
)
