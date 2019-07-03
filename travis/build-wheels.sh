#!/bin/bash
set -e -x

PYVERSIONS=cp35-cp35m cp36-cp36m cp37-cp37m

# Compile wheels
for PYVER in $PYVERSIONS; do
    PYBIN="/opt/python/$PYVER/bin"
    "${PYBIN}/pip" install -r /io/requirements-build.txt
    "${PYBIN}/pip" wheel /io/ -w wheelhouse/
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
    auditwheel repair "$whl" --plat $PLAT -w /io/wheelhouse/
done

# Install packages
for PYBIN in $PYVERSIONS; do
    PYBIN="/opt/python/$PYVER/bin"
    "${PYBIN}/pip" install tmhmm.py --user --no-index -f /io/wheelhouse
    (cp /io/test.fa $HOME/; cd $HOME; /root/.local/bin/tmhmm -f test.fa -p)
done
