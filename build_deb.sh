#!/bin/bash
#
#

set -e

BUILD_DIR=build/efalive
PROJECT_ROOT=$(pwd)

rm -rf build
mkdir -p $BUILD_DIR
cp -r debian $BUILD_DIR

poetry install
poetry run pytest

python3 setup.py sdist --dist-dir build/python
cd $PROJECT_ROOT

cd $BUILD_DIR
debuild -uc -us -b

cd $PROJECT_ROOT

cp build/*.deb .

