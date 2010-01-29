#!/bin/sh
# ...
DEBIAN_FRONTEND="dialog" apt-get install --yes sun-java6-bin
#sun-java6-demo \
#sun-java6-fonts \
#sun-java6-jdk \
#sun-java6-jre \
#sun-java6-plugin \
#sun-java6-source
# Installation von sun-java6-doc schlägt fehl
# und verhindert die Erstellung des Images.
# die Rechte auf /tmp ändern daran auch nichts
# Ensure that /tmp has the right permissions;
# apparently sun-java5-doc tampers with it
chmod 1777 /tmp
