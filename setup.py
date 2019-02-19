from setuptools import setup, Extension

import numpy

setup(
    name='tmhmm.py',
    version='1.1.1',
    author='Dan Søndergaard',
    author_email='das@birc.au.dk',
    description='A transmembrane helix finder.',
    url='https://github.com/dansondergaard/tmhmm.py/',
    packages=['tmhmm'],
    package_data={'tmhmm': ['TMHMM2.0.model']},
    zip_safe=False,

    setup_requires=['setuptools>=18.0', 'numpy>=1.9', 'cython'],
    install_requires=['numpy>=1.9', 'scikit-bio>=0.5'],
    extras_require={
        'plotting':  ['matplotlib', 'pandas'],
    },

    entry_points={
        'console_scripts': ['tmhmm=tmhmm.cli:cli'],
    },

    ext_modules=[
        Extension(
            'tmhmm.hmm',
            sources=['tmhmm/hmm.pyx'],
            include_dirs=[numpy.get_include()],
        ),
    ],
)
