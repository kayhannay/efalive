#!/bin/bash

chown -R 1000:1000 /opt/efa/*
chown -R 1000:1000 /opt/efa/.ivman
chown -R 1000:1000 /opt/efa/.config
chown 1000:1000 /home/efa/.xinitrc
#chmod 644 /etc/ivman/IvmConfigActions.xml
chmod 440 /etc/sudoers

