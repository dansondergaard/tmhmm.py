#!/bin/bash

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    brew update
    brew install openssl readline
    brew install pyenv pyenv-virtualenv

    pyenv install ${PYTHON_VERSION}
    pyenv virtualenv ${PYTHON_VERSION} venv

    export PYENV_VERSION=${PYTHON_VERSION}
    export PATH="/Users/travis/.pyenv/shims:${PATH}"
    pyenv-virtualenv venv
    source venv/bin/activate
fi

pip install --upgrade pip

python --version
pip --version

pip install -r requirements-build.txt
pip install .
