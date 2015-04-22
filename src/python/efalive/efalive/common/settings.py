#!/usr/bin/python
'''
Created on 04.03.2015

Copyright (C) 2015-2015 Kay Hannay

This file is part of efaLive.

efaLiveSetup is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
efaLiveSetup is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with efaLive.  If not, see <http://www.gnu.org/licenses/>.
'''
import logging
import os

from observable import Observable

class EfaLiveSettings(object):

    def __init__(self, confPath = os.path.join(os.path.expanduser('~'), ".efalive")):
        self._logger = logging.getLogger('efalive.common.EfaLiveSettings')
        self._checkPath(confPath)
        self.confPath=confPath
        self._logger.info("Using configuration directory '%s'" % confPath)
        self._settingsFileName = os.path.join(self.confPath, "settings.conf")
        self._backupFileName = os.path.join(self.confPath, "backup.conf")
        self.efaShutdownAction=Observable()
        self.autoUsbBackup=Observable()
        self.autoUsbBackupDialog=Observable()
        self.efaBackupPaths="/usr/lib/efa/ausgabe/layout /usr/lib/efa/daten /home/efa/efa"
        self.efaLiveBackupPaths="/home/efa/.efalive"
        self.efaPort=Observable()
        self.efaCredentialsFile="~/.efalive/.efacred"
        self.auto_backup_use_password=Observable()
        self.auto_backup_password=""

    def initSettings(self):
        self.efaShutdownAction.updateData("shutdown")
        self.efaPort.updateData(3834)
        if os.path.isfile(self._settingsFileName):
            self.settingsFile=open(self._settingsFileName, "r")
            self.parseSettingsFile(self.settingsFile)
            self.settingsFile.close()

    def _checkPath(self, path):
        if not os.path.exists(path):
            self._logger.debug("Creating directory: %s" % path)
            os.makedirs(path, 0755)

    def parseSettingsFile(self, file):
        self._logger.info("Parsing settings file")
        for line in file:
            if line.startswith("EFA_SHUTDOWN_ACTION="):
                actionStr=line[(line.index('=') + 1):].rstrip()
                self.efaShutdownAction.updateData(actionStr)
                self._logger.debug("Parsed shutdown action: " + actionStr)
            elif line.startswith("AUTO_USB_BACKUP="):
                enableStr=line[(line.index('=') + 1):].rstrip()
                if enableStr == "\"TRUE\"":
                    self.autoUsbBackup.updateData(True)
                else:
                    self.autoUsbBackup.updateData(False)
                self._logger.debug("Parsed auto USB backup setting: " + enableStr)
            elif line.startswith("AUTO_USB_BACKUP_DIALOG="):
                enableStr=line[(line.index('=') + 1):].rstrip()
                if enableStr == "\"TRUE\"":
                    self.autoUsbBackupDialog.updateData(True)
                else:
                    self.autoUsbBackupDialog.updateData(False)
                self._logger.debug("Parsed auto USB backup dialog setting: " + enableStr)
            elif line.startswith("EFA_BACKUP_PATHS="):
                backupStr=line[(line.index('=') + 1):].rstrip()
                self.efaBackupPaths = backupStr.replace("\"", "")
                self._logger.debug("Parsed efa backup paths: " + backupStr)
            elif line.startswith("EFALIVE_BACKUP_PATHS="):
                backupStr=line[(line.index('=') + 1):].rstrip()
                self.efaLiveBackupPaths = backupStr.replace("\"", "")
                self._logger.debug("Parsed efaLive backup paths: " + backupStr)
            elif line.startswith("EFA_PORT="):
                portStr=line[(line.index('=') + 1):].rstrip()
                self.efaPort.updateData(int(portStr))
                self._logger.debug("Parsed efa port: " + portStr)
            elif line.startswith("EFA_CREDENTIALS_FILE="):
                credStr=line[(line.index('=') + 1):].rstrip()
                self.efaCredentialsFile = credStr
                self._logger.debug("Parsed efa credentials file setting: " + credStr)
            elif line.startswith("AUTO_BACKUP_PASSWORD="):
                pwdStr=line[(line.index('=') + 1):].rstrip()
                self.auto_backup_password = pwdStr
                self._logger.debug("Parsed efa auto backup password setting: " + pwdStr)
            elif line.startswith("AUTO_BACKUP_USE_PASSWORD="):
                enableStr=line[(line.index('=') + 1):].rstrip()
                if enableStr == "\"TRUE\"":
                    self.auto_backup_use_password.updateData(True)
                else:
                    self.auto_backup_use_password.updateData(False)
                self._logger.debug("Parsed auto backup enable password setting: " + enableStr)

    def save(self):
        self._logger.info("Saving settings to file: %s" % (self._settingsFileName))
        try:
            settingsFile=open(self._settingsFileName, "w")
            settingsFile.write("EFA_SHUTDOWN_ACTION=%s\n" % self.efaShutdownAction.getData())
            if self.autoUsbBackup._data == True:
                settingsFile.write("AUTO_USB_BACKUP=\"TRUE\"\n")
            else:
                settingsFile.write("AUTO_USB_BACKUP=\"FALSE\"\n")
            if self.autoUsbBackupDialog._data == True:
                settingsFile.write("AUTO_USB_BACKUP_DIALOG=\"TRUE\"\n")
            else:
                settingsFile.write("AUTO_USB_BACKUP_DIALOG=\"FALSE\"\n")
            settingsFile.write("EFA_BACKUP_PATHS=\"%s\"\n" % self.efaBackupPaths)
            settingsFile.write("EFALIVE_BACKUP_PATHS=\"%s\"\n" % self.efaLiveBackupPaths)
            settingsFile.write("EFA_PORT=%d\n" % self.efaPort.getData())
            settingsFile.write("EFA_CREDENTIALS_FILE=%s\n" % self.efaCredentialsFile)
            settingsFile.write("AUTO_BACKUP_PASSWORD=%s\n" % self.auto_backup_password)
            if self.auto_backup_use_password._data == True:
                settingsFile.write("AUTO_BACKUP_USE_PASSWORD=\"TRUE\"\n")
            else:
                settingsFile.write("AUTO_BACKUP_USE_PASSWORD=\"FALSE\"\n")
            settingsFile.close()
        except IOError, exception:
            self._logger.error("Could not save files: %s" % exception)
            raise Exception("Could not save files")
