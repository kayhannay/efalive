#!/bin/bash
#
#
#VERSION=2.2

#rm -r efalive-*
#mkdir efalive-$VERSION
#cp -a content/* efalive-$VERSION
#cp -a debian efalive-$VERSION
#cd content
#tar czf ../efalive_$VERSION.orig.tar.gz *
#cd ..
#cd efalive-$VERSION
#debuild -uc -us
#cd ..

BUILD_DIR=build/efalive
PROJECT_ROOT=$(pwd)

rm -rf build
mkdir -p $BUILD_DIR
cp -r debian $BUILD_DIR

cd src/python
python setup.py sdist --dist-dir ../../build/python
cd $PROJECT_ROOT

cd $BUILD_DIR
debuild -uc -us -b

cd $PROJECT_ROOT
