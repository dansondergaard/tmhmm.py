#!/bin/bash

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    brew update
    brew install openssl readline
    brew install pyenv pyenv-virtualenv

    pyenv install ${PYTHON_VERSION}

    export PYENV_VERSION=${PYTHON_VERSION}
    export PATH="/Users/travis/.pyenv/shims:${PATH}"
    pyenv virtualenv venv
fi

pip install --upgrade pip setuptools

python --version
pip --version

pip install -r requirements-build.txt
pip install .
