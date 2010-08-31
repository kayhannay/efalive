@echo off
REM efa - Elektronisches Fahrtenbuch
REM Java (mind. Java 2 JRE 1.4) muss installiert sein!

IF "%OS%" == "Windows_NT" GOTO STARTNT
GOTO START9X

:STARTNT
REM Path for Windows 7 (64 Bit)
SET PATH=%PATH%;C:\Windows\SysWOW64
echo Start: emil (Windows NT)
start /b javaw -cp program/efa.jar de.nmichael.efa.emil.Emil %1 %2 %3 %4 %5 %6 %7 %8 %9
GOTO ENDE

:START9X
echo Start: emil (Windows 9X)
javaw -cp program/efa.jar de.nmichael.efa.emil.Emil %1 %2 %3 %4 %5 %6 %7 %8 %9
GOTO ENDE

:ENDE
@CLS