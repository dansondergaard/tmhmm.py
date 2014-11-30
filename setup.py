from setuptools import setup
from distutils.extension import Extension

from Cython.Build import cythonize

import numpy

USE_CYTHON = ...   # command line option, try-import, ...

ext = '.pyx' if USE_CYTHON else '.c'

extensions = [Extension("viterbi", ["viterbi" + ext])]

if USE_CYTHON:
    from Cython.Build import cythonize
    extensions = cythonize(extensions)

setup(
    name='tmhmm.py',
    version='1.0',
    author='Dan Søndergaard',
    author_email='das@birc.au.dk',
    description='A transmembrane helix finder.',
    url='https://github.com/dansondergaard/tmhmm.py/',
    install_requires=['scikit-bio>=0.2', 'numpy>=1.9'],
    py_modules=['tmhmm'],
    ext_modules=extensions,
    include_dirs=[numpy.get_include()],
)
