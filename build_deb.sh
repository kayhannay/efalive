#!/bin/bash
#
#

BUILD_DIR=build/efalive
PROJECT_ROOT=$(pwd)

rm -rf build
mkdir -p $BUILD_DIR
cp -r debian $BUILD_DIR

./run_tests.sh
if [ $? != 0 ]
then
    echo "Build failed due to test errors!"
    exit 1
fi

python3 setup.py sdist --dist-dir build/python
cd $PROJECT_ROOT

cd $BUILD_DIR
debuild -uc -us -b

cd $PROJECT_ROOT

cp build/*.deb .

