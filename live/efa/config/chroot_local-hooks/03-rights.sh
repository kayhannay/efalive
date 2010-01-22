#!/bin/bash

chown -R 1000:1000 /opt/efa/*
chown 1000:1000 /home/efa/.xinitrc
chmod 644 /etc/ivman/IvmConfigActions.xml

