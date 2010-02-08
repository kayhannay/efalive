#!/bin/sh

sed -i -e 's/XKBLAYOUT="us"/XKBLAYOUT="de"/' /etc/default/console-setup
sed -i -e 's/XKBMODEL=""/XKBMODEL="pc105"/' /etc/default/console-setup
sed -i -e 's/XKBVARIANT=""/XKBVARIANT="nodeadkeys"/' /etc/default/console-setup
sed -i -e 's/CODESET="Uni1"/CODESET="Lat15"/' /etc/default/console-setup

