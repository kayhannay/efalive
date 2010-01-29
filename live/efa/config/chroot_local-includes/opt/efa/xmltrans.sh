#!/bin/sh

# XMLTransformer
# Transformieren von XML-Dokumenten mittels XSLT
# "xmltrans -help" fuer weitere Informationen

CP=program/efa.jar
CP=$CP:program/plugins/dom.jar
CP=$CP:program/plugins/jaxp-api.jar
CP=$CP:program/plugins/sax.jar
CP=$CP:program/plugins/xalan.jar
CP=$CP:program/plugins/xercesImpl.jar

java -cp $CP de.nmichael.efa.XMLTransformer $*
