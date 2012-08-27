#!/bin/bash
#
#
VERSION=2.0

rm -r efalive-$VERSION
mkdir efalive-$VERSION
cp -a content/* efalive-$VERSION
cp -a debian efalive-$VERSION
cd content
tar czf ../efalive_$VERSION.orig.tar.gz *
cd ..
cd efalive-$VERSION
debuild -uc -us
cd ..

