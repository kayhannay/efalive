@echo off
REM elwiz - efa Layout Wizard
REM Java (mind. Java 2 JRE 1.4) muss installiert sein!

IF "%1" == "run" GOTO RUN

REM Betriebssystemtest
IF "%OS%" == "Windows_NT" GOTO WINNT
GOTO WIN9X

:WIN9X
echo Betriebssystem: Windows 9x
command.com /e:1024 /celwiz.bat run %1 %2 %3 %4 %5 %6 %7 %8
GOTO ENDE

:WINNT
echo Betriebssystem: Windows NT
call elwiz.bat run %1 %2 %3 %4 %5 %6 %7 %8
GOTO ENDE

:RUN
REM Starten von elwiz

REM Classpath: elwiz
SET CP=program/efa.jar

REM Classpath: JAXP-Plugin
SET CP=%CP%;program/plugins/dom.jar
SET CP=%CP%;program/plugins/jaxp-api.jar
SET CP=%CP%;program/plugins/sax.jar
SET CP=%CP%;program/plugins/xalan.jar
SET CP=%CP%;program/plugins/xercesImpl.jar

REM Classpath
ECHO CLASSPATH=%CP%

IF "%OS%" == "Windows_NT" GOTO STARTNT
GOTO START9X

:STARTNT
REM Path for Windows 7 (64 Bit)
SET PATH=%PATH%;C:\Windows\SysWOW64
echo Start: elwiz (Windows NT)
start /b javaw -cp %CP% de.nmichael.efa.elwiz.Elwiz %2 %3 %4 %5 %6 %7 %8 %9
GOTO ENDE

:START9X
echo Start: elwiz (Windows 9X)
javaw -cp %CP% de.nmichael.efa.elwiz.Elwiz %2 %3 %4 %5 %6 %7 %8 %9
GOTO ENDE

:ENDE
@CLS