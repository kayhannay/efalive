#!/bin/bash
#
#

set -ex

BUILD_DIR=build/efalive
PROJECT_ROOT=$(pwd)

rm -rf build
mkdir -p $BUILD_DIR
cp -r debian $BUILD_DIR

/usr/bin/python3 -m pytest
/usr/bin/python3 build_translations.py
/usr/bin/python3 -m build --sdist --outdir build/python

cd $BUILD_DIR
debuild -uc -us -b

cd $PROJECT_ROOT

cp build/*.deb .
