#!/bin/bash

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    brew install pyenv pyenv-virtualenv
    pyenv local 3.4.0 3.5.0 3.6.0
    case "${PYTHON_VERSION}" in
        py34)
            pyenv install 3.4.0
            pyenv local 3.4.0
            ;;
        py35)
            pyenv install 3.5.0
            pyenv local 3.5.0
            ;;
        py36)
            pyenv install 3.6.0
            pyenv local 3.6.0
            ;;
    esac
fi

pip install --upgrade pip
pip install .
