#!/bin/bash

plymouthd
plymouth --show-splash
while [ 1 ]
do 
    plymouth --update=test
    sleep 1
done
plymouth quit

