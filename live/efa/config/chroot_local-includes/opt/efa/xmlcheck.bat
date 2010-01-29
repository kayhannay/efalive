@echo off
REM XMLChecker
REM Ueberpruefen der Gueltigkeit von XML-Dokumenten
REM "xmlcheck -help" fuer weitere Informationen

SET CP=program/efa.jar
SET CP=%CP%;program/plugins/sax.jar
SET CP=%CP%;program/plugins/xercesImpl.jar

java -cp %CP% de.nmichael.efa.XMLChecker %1 %2 %3 %4
