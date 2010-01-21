#!/bin/sh

# change to efa directory
cd `dirname $0`

# efa
CP=program/efa.jar

# JAXP-Plugin
CP=$CP:program/plugins/dom.jar
CP=$CP:program/plugins/jaxp-api.jar
CP=$CP:program/plugins/sax.jar
CP=$CP:program/plugins/xalan.jar
CP=$CP:program/plugins/xercesImpl.jar

# FOP-Plugin
CP=$CP:program/plugins/fop.jar
CP=$CP:program/plugins/batik.jar
CP=$CP:program/plugins/avalon-framework-cvs-20020315.jar

# FTP-Plugin
CP=$CP:program/plugins/ftp.jar

# Mail-Plugin
CP=$CP:program/plugins/mail.jar

# JSUNTIMES-Plugin
CP=$CP:program/plugins/jsuntimes.jar

# Java Heap
if [ -f java.heap ] ; then
  . ./java.heap
fi
if [ "$EFA_JAVA_HEAP" = "" ] ; then
  EFA_JAVA_HEAP=64m
fi
if [ "$EFA_NEW_SIZE" = "" ] ; then
  EFA_NEW_SIZE=16m
fi

# JVM-Optionen
JVMOPTIONS="-Xmx$EFA_JAVA_HEAP -XX:NewSize=$EFA_NEW_SIZE -XX:MaxNewSize=$EFA_NEW_SIZE -XX:+PrintGCTimeStamps -XX:+PrintGCDetails -Xloggc:efa.gc -verbose:gc"

# Java Arguments
EFA_JAVA_ARGUMENTS="$JVMOPTIONS -cp $CP de.nmichael.efa.Efa $*"
export EFA_JAVA_ARGUMENTS

java $EFA_JAVA_ARGUMENTS
