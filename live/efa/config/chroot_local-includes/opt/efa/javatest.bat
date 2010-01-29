@echo off

echo Damit efa gestartet werden kann, muss auf dem Rechner die Java
echo Laufzeitumgebung installiert sein.
echo.

echo Folgende Java-Version ist installiert (mind. v1.4.0 benoetigt):
echo.
echo ============================= JAVA-VERSION =============================
java -version
echo ========================================================================
echo.
echo Sollte in der vorangehenden Zeile "Befehl oder Dateiname nicht gefunden"
echo stehen, so ist auf dem Rechner KEIN Java installiert.
echo.
echo Falls kein Java installiert ist, oder eine Version aelter als v1.4.0,
echo findest Du in der Dokumentation im Abschnitt "Download und Installation"
echo Hinweise zur Installation von Java.
goto ende

REM Folgendes funktioniert leider nicht, weil die bloeden Batchdateien sowas
REM anscheinen nicht koennen....

echo Es wird nun geprueft, ob Java installiert ist.
echo.

javaw -version
REM IF ERRORLEVEL 1 goto nojava
IF "%ERRORLEVEL" == "1" goto nojava

echo Java ist auf diesem Rechner INSTALLIERT.
echo.
echo Es wird nun geprueft, welche Version von Java installiert ist.
echo efa benoetigt mindestens die Version v1.4.0
echo.
echo Folgende Java-Version ist installiert:
java -version
echo.
echo Sollte eine zu alte Version installiert sein, findest Du in der
echo Dokumentation im Abschnitt "Download und Installation" Hinweise
echo zur Installation von Java.
goto ende

:nojava
echo Java ist auf diesem Rechner NICHT INSTALLIERT.
echo.
echo Bevor efa gestartet werden kann, muﬂ zun‰chst Java installiert
echo werden. Hilfe hierzu findest Du in der Dokumentation im Abschnitt
echo "Download und Installation".

:ende
echo.
pause
@CLS