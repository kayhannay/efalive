@echo off
REM efa - Elektronisches Fahrtenbuch
REM Java (mind. Java 2 JRE 1.4) muss installiert sein!

IF "%1" == "run" GOTO RUN

REM Betriebssystemtest
IF "%OS%" == "Windows_NT" GOTO WINNT
GOTO WIN9X

:WIN9X
echo Betriebssystem: Windows 9x
command.com /e:1024 /cefadirekt.bat run %1 %2 %3 %4 %5 %6 %7 %8
GOTO ENDE

:WINNT
echo Betriebssystem: Windows NT
call efadirekt.bat run %1 %2 %3 %4 %5 %6 %7 %8
GOTO ENDE

:RUN
REM Starten von efa

REM Classpath: efa
SET CP=program/efa.jar

REM Classpath: JAXP-Plugin
SET CP=%CP%;program/plugins/dom.jar
SET CP=%CP%;program/plugins/jaxp-api.jar
SET CP=%CP%;program/plugins/sax.jar
SET CP=%CP%;program/plugins/xalan.jar
SET CP=%CP%;program/plugins/xercesImpl.jar

REM Classpath: FOP-Plugin
SET CP=%CP%;program/plugins/fop.jar
SET CP=%CP%;program/plugins/batik.jar
SET CP=%CP%;program/plugins/avalon-framework-cvs-20020315.jar

REM Classpath: FTP-Plugin
SET CP=%CP%;program/plugins/ftp.jar

REM Classpath: MAIL-Plugin
SET CP=%CP%;program/plugins/mail.jar

REM Classpath: JSUNTIMES-Plugin
SET CP=%CP%;program/plugins/jsuntimes.jar

REM Java Heap
SET EFA_JAVA_HEAP=64m
SET EFA_NEW_SIZE=16m
IF EXIST javaheap.bat CALL javaheap.bat

REM JVM Options
SET JVMOPTIONS=-Xmx%EFA_JAVA_HEAP% -XX:NewSize=%EFA_NEW_SIZE% -XX:MaxNewSize=%EFA_NEW_SIZE% -XX:+PrintGCTimeStamps -XX:+PrintGCDetails -Xloggc:efadirekt.gc -verbose:gc
ECHO JVMOPTIONS=%JVMOPTIONS%

REM Java Arguments
SET EFA_JAVA_ARGUMENTS=%JVMOPTIONS% -cp %CP% de.nmichael.efa.direkt.EfaDirekt -javaRestart %2 %3 %4 %5 %6 %7 %8 %9
ECHO EFA_JAVA_ARGUMENTS=%EFA_JAVA_ARGUMENTS%

IF "%OS%" == "Windows_NT" GOTO STARTNT
GOTO START9X

:STARTNT
REM Path for Windows 7 (64 Bit)
SET PATH=%PATH%;C:\Windows\SysWOW64
echo Start: efa im Bootshaus (Windows NT)
start /b javaw %EFA_JAVA_ARGUMENTS%
GOTO ENDE

:START9X
echo Start: efa im Bootshaus (Windows 9x)
javaw %EFA_JAVA_ARGUMENTS%
GOTO ENDE

:ENDE
@CLS