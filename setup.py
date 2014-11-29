from distutils.core import setup
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
    py_modules=['tmhmm'],
    ext_modules=extensions,
    include_dirs=[numpy.get_include()]
)
