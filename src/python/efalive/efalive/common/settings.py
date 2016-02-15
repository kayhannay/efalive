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
import json
import base64

from observable import Observable
import md5

class EfaLiveSettings(object):

    def __init__(self, confPath = os.path.join(os.path.expanduser('~'), ".efalive")):
        self._logger = logging.getLogger('efalive.common.EfaLiveSettings')
        self._checkPath(confPath)
        self.confPath = confPath
        self._logger.info("Using configuration directory '%s'" % confPath)
        self._settingsFileName = os.path.join(self.confPath, "settings.conf")
        self._backupFileName = os.path.join(self.confPath, "backup.conf")
        self.efaShutdownAction = Observable()
        self.autoUsbBackup = Observable()
        self.autoUsbBackupDialog = Observable()
        self.efaLiveBackupPaths = "/home/efa/.efalive"
        self.efaPort = Observable()
        self.efaCredentialsFile = "~/.efalive/.efacred"
        self.auto_backup_use_password = Observable()
        self.auto_backup_password = ""
        self.mailer_host = Observable()
        self.mailer_port = Observable()
        self.mailer_use_ssl = Observable()
        self.mailer_use_starttls = Observable()
        self.mailer_user = Observable()
        self.mailer_password = Observable()
        self.backup_mail_recipient = Observable()
        self.hourly_tasks = Observable()
        self.daily_tasks = Observable()
        self.weekly_tasks = Observable()
        self.monthly_tasks = Observable()

    def initSettings(self):
        self.efaShutdownAction.updateData("shutdown")
        self.efaPort.updateData(3834)
        self.mailer_port.updateData(25)
        self.mailer_use_ssl.updateData(False)
        self.mailer_use_starttls.updateData(True)

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
                self.autoUsbBackup.updateData(enableStr == "\"TRUE\"")
                self._logger.debug("Parsed auto USB backup setting: " + enableStr)
            elif line.startswith("AUTO_USB_BACKUP_DIALOG="):
                enableStr=line[(line.index('=') + 1):].rstrip()
                self.autoUsbBackupDialog.updateData(enableStr == "\"TRUE\"")
                self._logger.debug("Parsed auto USB backup dialog setting: " + enableStr)
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
                self.auto_backup_use_password.updateData(enableStr == "\"TRUE\"")
                self._logger.debug("Parsed auto backup enable password setting: " + enableStr)
            elif line.startswith("MAILER_HOST="):
                hostStr=line[(line.index('=') + 1):].rstrip()
                self.mailer_host.updateData(hostStr)
                self._logger.debug("Parsed efa mailer host setting: " + hostStr)
            elif line.startswith("MAILER_PORT="):
                portStr=line[(line.index('=') + 1):].rstrip()
                self.mailer_port.updateData(int(portStr))
                self._logger.debug("Parsed efa mailer port setting: " + portStr)
            elif line.startswith("MAILER_USE_SSL="):
                enableStr=line[(line.index('=') + 1):].rstrip()
                self.mailer_use_ssl.updateData(enableStr == "\"TRUE\"")
                self._logger.debug("Parsed efa mailer use SSL setting: " + enableStr)
            elif line.startswith("MAILER_USE_STARTTLS="):
                enableStr=line[(line.index('=') + 1):].rstrip()
                self.mailer_use_starttls.updateData(enableStr == "\"TRUE\"")
                self._logger.debug("Parsed efa mailer use StartTLS setting: " + enableStr)
            elif line.startswith("MAILER_USER="):
                userStr=line[(line.index('=') + 1):].rstrip()
                self.mailer_user.updateData(userStr)
                self._logger.debug("Parsed efa mailer user setting: " + userStr)
            elif line.startswith("MAILER_PASSWORD="):
                passStr=line[(line.index('=') + 1):].rstrip()
                self.mailer_password.updateData(base64.b64decode(passStr))
                self._logger.debug("Parsed efa mailer password setting: " + passStr)
            elif line.startswith("HOURLY_TASKS="):
                valueStr=line[(line.index('=') + 1):].rstrip()
                tasks = json.loads(valueStr)
                if tasks != None:
                    task_map = {}
                    for task in tasks:
                        task_id = self._create_id(task)
                        task_map[task_id] = task
                    self.hourly_tasks.updateData(task_map)
                self._logger.debug("Parsed hourly tasks setting: " + valueStr)
            elif line.startswith("DAILY_TASKS="):
                valueStr=line[(line.index('=') + 1):].rstrip()
                tasks = json.loads(valueStr)
                if tasks != None:
                    task_map = {}
                    for task in tasks:
                        task_id = self._create_id(task)
                        task_map[task_id] = task
                    self.daily_tasks.updateData(task_map)
                self._logger.debug("Parsed daily tasks setting: " + valueStr)
            elif line.startswith("WEEKLY_TASKS="):
                valueStr=line[(line.index('=') + 1):].rstrip()
                tasks = json.loads(valueStr)
                if tasks != None:
                    task_map = {}
                    for task in tasks:
                        task_id = self._create_id(task)
                        task_map[task_id] = task
                    self.weekly_tasks.updateData(task_map)
                self._logger.debug("Parsed weekly tasks setting: " + valueStr)
            elif line.startswith("MONTHLY_TASKS="):
                valueStr=line[(line.index('=') + 1):].rstrip()
                tasks = json.loads(valueStr)
                if tasks != None:
                    task_map = {}
                    for task in tasks:
                        task_id = self._create_id(task)
                        task_map[task_id] = task
                    self.monthly_tasks.updateData(task_map)
                self._logger.debug("Parsed monthly tasks setting: " + valueStr)

    def _create_id(self, task):
        hasher = md5.new()
        hasher.update(task[0])
        hasher.update(str(task[1]))
        return hasher.hexdigest()

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
            settingsFile.write("EFALIVE_BACKUP_PATHS=\"%s\"\n" % self.efaLiveBackupPaths)
            settingsFile.write("EFA_PORT=%d\n" % self.efaPort.getData())
            settingsFile.write("EFA_CREDENTIALS_FILE=%s\n" % self.efaCredentialsFile)
            settingsFile.write("AUTO_BACKUP_PASSWORD=%s\n" % self.auto_backup_password)
            if self.auto_backup_use_password._data == True:
                settingsFile.write("AUTO_BACKUP_USE_PASSWORD=\"TRUE\"\n")
            else:
                settingsFile.write("AUTO_BACKUP_USE_PASSWORD=\"FALSE\"\n")
            settingsFile.write("MAILER_HOST=%s\n" % self.mailer_host.getData())
            settingsFile.write("MAILER_PORT=%d\n" % self.mailer_port.getData())
            if self.mailer_use_ssl.getData() == True:
                settingsFile.write("MAILER_USE_SSL=\"TRUE\"\n")
            else:
                settingsFile.write("MAILER_USE_SSL=\"FALSE\"\n")
            if self.mailer_use_starttls.getData() == True:
                settingsFile.write("MAILER_USE_STARTTLS=\"TRUE\"\n")
            else:
                settingsFile.write("MAILER_USE_STARTTLS=\"FALSE\"\n")
            settingsFile.write("MAILER_USER=%s\n" % self.mailer_user.getData())
            settingsFile.write("MAILER_PASSWORD=%s\n" % base64.b64encode(self.mailer_password.getData()))
            settingsFile.write("HOURLY_TASKS=%s\n" % json.dumps(self._get_tasks(self.hourly_tasks)))
            settingsFile.write("DAILY_TASKS=%s\n" % json.dumps(self._get_tasks(self.daily_tasks)))
            settingsFile.write("WEEKLY_TASKS=%s\n" % json.dumps(self._get_tasks(self.weekly_tasks)))
            settingsFile.write("MONTHLY_TASKS=%s\n" % json.dumps(self._get_tasks(self.monthly_tasks)))
            settingsFile.close()
        except IOError, exception:
            self._logger.error("Could not save files: %s" % exception)
            raise Exception("Could not save files")

    def _get_tasks(self, tasks_data):
        tasks = tasks_data.getData()
        if tasks == None:
            return None
        else:
            return tasks.values()

    def delete_task(self, task_id):
        tasks = self.hourly_tasks.getData()
        if tasks != None and task_id in tasks:
            del tasks[task_id]
            self.hourly_tasks.updateData(tasks)
        tasks = self.daily_tasks.getData()
        if tasks != None and task_id in tasks:
            del tasks[task_id]
            self.daily_tasks.updateData(tasks)
        tasks = self.weekly_tasks.getData()
        if tasks != None and task_id in tasks:
            del tasks[task_id]
            self.weekly_tasks.updateData(tasks)
        tasks = self.monthly_tasks.getData()
        if tasks != None and task_id in tasks:
            del tasks[task_id]
            self.monthly_tasks.updateData(tasks)

    def add_task(self, task_type, task_data, task_interval):
        task = [task_type, task_data]
        if (task_interval == "HOURLY"):
            tasks = self.hourly_tasks.getData()
            if tasks == None:
                tasks = {}
            tasks[self._create_id(task)] = task
            self.hourly_tasks.updateData(tasks)
        elif (task_interval == "DAILY"):
            tasks = self.daily_tasks.getData()
            if tasks == None:
                tasks = {}
            tasks[self._create_id(task)] = task
            self.daily_tasks.updateData(tasks)
        elif (task_interval == "WEEKLY"):
            tasks = self.weekly_tasks.getData()
            if tasks == None:
                tasks = {}
            tasks[self._create_id(task)] = task
            self.weekly_tasks.updateData(tasks)
        elif (task_interval == "MONTHLY"):
            tasks = self.monthly_tasks.getData()
            if tasks == None:
                tasks = {}
            tasks[self._create_id(task)] = task
            self.monthly_tasks.updateData(tasks)

    def get_task(self, task_id):
        tasks = self.hourly_tasks.getData()
        if tasks != None and task_id in tasks:
            return "HOURLY", tasks[task_id]
        tasks = self.daily_tasks.getData()
        if tasks != None and task_id in tasks:
            return "DAILY", tasks[task_id]
        tasks = self.weekly_tasks.getData()
        if tasks != None and task_id in tasks:
            return "WEEKLY", tasks[task_id]
        tasks = self.monthly_tasks.getData()
        if tasks != None and task_id in tasks:
            return "MONTHLY", tasks[task_id]

