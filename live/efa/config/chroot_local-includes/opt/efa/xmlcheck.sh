#!/bin/sh

# XMLChecker
# Ueberpruefen der Gueltigkeit von XML-Dokumenten
# "xmlcheck -help" fuer weitere Informationen

CP=program/efa.jar
CP=$CP:program/plugins/sax.jar
CP=$CP:program/plugins/xercesImpl.jar

java -cp $CP de.nmichael.efa.XMLChecker $*
