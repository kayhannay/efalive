#!/bin/sh

# change to efa directory
cd `dirname $0`

# elwiz
CP=program/efa.jar

# JAXP-Plugin
CP=$CP:program/plugins/dom.jar
CP=$CP:program/plugins/jaxp-api.jar
CP=$CP:program/plugins/sax.jar
CP=$CP:program/plugins/xalan.jar
CP=$CP:program/plugins/xercesImpl.jar

java -cp $CP de.nmichael.efa.elwiz.Elwiz $*
