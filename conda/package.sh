#!/bin/bash
#
# Build and upload Conda package for tmhmm.py
#
# Make sure to run `conda activate` before running this script, so that
# conda-build is available.
#
# Usage:
#   ./package.sh
#

set -eux
set -o pipefail

echo '*** conda-build version ***'
conda-build --version

echo '*** conda-build . ***'
conda-build .

echo '*** anaconda upload ***'
for package in `conda build --output .`; do
    anaconda upload --user dansondergaard "${package}"
done
# Done? Check your script with https://www.shellcheck.net/.
