#!/bin/sh

# change to efa directory
cd `dirname $0`

# get parameters
if [ $# -eq 0 ] ; then
  echo "usage: $0 <mainclass> [arguments]"
  exit 1
fi


# ##########################################
# Classpath                                #
# ##########################################

# efa
CP=program/efa.jar:program/efahelp.jar:program

# OnlineHelp-Plugin
CP=$CP:program/plugins/jh.jar

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


# ##########################################
# JVM Settings                             #
# ##########################################

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
JVMOPTIONS="-Xmx$EFA_JAVA_HEAP -XX:NewSize=$EFA_NEW_SIZE -XX:MaxNewSize=$EFA_NEW_SIZE"


# ##########################################
# Run Program                              #
# ##########################################

# Java Arguments
EFA_JAVA_ARGUMENTS="$JVMOPTIONS -cp $CP $*"

# Run Program
RC=99
while [ $RC -eq 99 ]
do
  echo "$0: starting $1 ..."
  java $EFA_JAVA_ARGUMENTS
  RC=$?
  echo "$0: efa exit code: $RC"
done
