@echo off
echo Start: efa (Windows 95)
javaw -cp program/efa.jar;program/plugins/dom.jar;program/plugins/jaxp-api.jar;program/plugins/sax.jar;program/plugins/xalan.jar;program/plugins/xercesImpl.jar;program/plugins/fop.jar;program/plugins/batik.jar;program/plugins/avalon-framework-cvs-20020315.jar;program/plugins/ftp.jar;program/plugins/mail.jar;program/plugins/jsuntimes.jar de.nmichael.efa.direkt.EfaDirekt -javaRestart %2 %3 %4 %5 %6 %7 %8 %9
@CLS