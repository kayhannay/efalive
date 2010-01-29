#!/bin/sh

# change to efa directory
cd `dirname $0`

# efa
CP=program/efa.jar

java -cp $CP de.nmichael.efa.emil.Emil $*
