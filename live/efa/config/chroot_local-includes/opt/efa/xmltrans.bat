@echo off
REM XMLTransformer
REM Transformieren von XML-Dokumenten mittels XSLT
REM "xmltrans -help" fuer weitere Informationen

SET CP=program/efa.jar
SET CP=%CP%;program/plugins/dom.jar
SET CP=%CP%;program/plugins/jaxp-api.jar
SET CP=%CP%;program/plugins/sax.jar
SET CP=%CP%;program/plugins/xalan.jar
SET CP=%CP%;program/plugins/xercesImpl.jar

java -cp %CP% de.nmichael.efa.XMLTransformer %1 %2 %3 %4 %5 %6
