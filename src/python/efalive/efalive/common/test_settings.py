#!/usr/bin/python
'''
Created on 25.04.2015

Copyright (C) 2015 Kay Hannay

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
import os
import unittest
from mock import call, patch, MagicMock

from settings import EfaLiveSettings

class EfaLiveSettingsTestCase(unittest.TestCase):

    def test_init__path_exists(self):
        os.path.exists = MagicMock(return_value = True)

        settings = EfaLiveSettings("/test/")

        self.assertEqual("/test/", settings.confPath)
        self.assertEqual("/test/settings.conf", settings._settingsFileName)
        self.assertEqual("/test/backup.conf", settings._backupFileName)
        self.assertEqual(None, settings.efaShutdownAction.getData())
        self.assertEqual(None, settings.autoUsbBackup.getData())
        self.assertEqual(None, settings.autoUsbBackupDialog.getData())
        self.assertEqual("/home/efa/.efalive", settings.efaLiveBackupPaths)
        self.assertEqual(None, settings.efaPort.getData())
        self.assertEqual("~/.efalive/.efacred", settings.efaCredentialsFile)
        self.assertEqual(None, settings.auto_backup_use_password.getData())
        self.assertEqual("", settings.auto_backup_password)
        self.assertEqual(None, settings.mailer_host.getData())
        self.assertEqual(None, settings.mailer_port.getData())
        self.assertEqual(None, settings.mailer_use_ssl.getData())
        self.assertEqual(None, settings.mailer_use_starttls.getData())
        self.assertEqual(None, settings.mailer_user.getData())
        self.assertEqual(None, settings.mailer_password.getData())
        self.assertEqual(None, settings.backup_mail_recipient.getData())
        self.assertEqual(None, settings.hourly_tasks.getData())
        self.assertEqual(None, settings.daily_tasks.getData())
        self.assertEqual(None, settings.weekly_tasks.getData())
        self.assertEqual(None, settings.monthly_tasks.getData())

    @patch("__builtin__.open")
    def test_initSettings__no_settings(self, open_mock):
        os.path.exists = MagicMock(return_value = True)
        os.path.isfile = MagicMock(return_value = True)
        open_mock.return_value = FileStub(True)

        settings = EfaLiveSettings("/test/")
        settings.initSettings()

        self.assertEqual("shutdown", settings.efaShutdownAction.getData())
        self.assertEqual(3834, settings.efaPort.getData())
        self.assertEqual(25, settings.mailer_port.getData())
        self.assertEqual(False, settings.mailer_use_ssl.getData())
        self.assertEqual(True, settings.mailer_use_starttls.getData())

    @patch("__builtin__.open")
    def test_initSettings__settings_filled(self, open_mock):
        os.path.exists = MagicMock(return_value = True)
        os.path.isfile = MagicMock(return_value = True)
        open_mock.return_value = FileStub(False)

        settings = EfaLiveSettings("/test/")
        settings.initSettings()

        self.assertEqual("restart", settings.efaShutdownAction.getData())
        self.assertEqual(True, settings.autoUsbBackup.getData())
        self.assertEqual(True, settings.autoUsbBackupDialog.getData())
        self.assertEqual("/tmp /test", settings.efaLiveBackupPaths)
        self.assertEqual(1234, settings.efaPort.getData())
        self.assertEqual("/tmp/cred.txt", settings.efaCredentialsFile)
        self.assertEqual("secret", settings.auto_backup_password)
        self.assertEqual(True, settings.auto_backup_use_password.getData())
        self.assertEqual("smtp.testserver.local", settings.mailer_host.getData())
        self.assertEqual(465, settings.mailer_port.getData())
        self.assertEqual(True, settings.mailer_use_ssl.getData())
        self.assertEqual(False, settings.mailer_use_starttls.getData())
        self.assertEqual("testuser", settings.mailer_user.getData())
        self.assertEqual("secret", settings.mailer_password.getData())
        self.assertEqual([["SHELL", "ls /tmp0"]], settings.hourly_tasks.getData())
        self.assertEqual([["BACKUP", ""], ["SHELL", "ls /tmp1"]], settings.daily_tasks.getData())
        self.assertEqual([["SHELL", "ls /tmp2"]], settings.weekly_tasks.getData())
        self.assertEqual([["SHELL", "ls /tmp3"]], settings.monthly_tasks.getData())

    @patch("__builtin__.open")
    def test_save__settings_filled(self, open_mock):
        os.path.exists = MagicMock(return_value = True)
        file_stub = FileStub(True)
        open_mock.return_value = file_stub

        settings = EfaLiveSettings("/test/")
        settings.efaShutdownAction.updateData("test")
        settings.autoUsbBackup.updateData(True)
        settings.autoUsbBackupDialog.updateData(True)
        settings.efaLiveBackupPaths = "/tmp /test"
        settings.efaPort.updateData(1234)
        settings.efaCredentialsFile = "/tmp/cred.txt"
        settings.auto_backup_password = "secret"
        settings.auto_backup_use_password.updateData(True)
        settings.mailer_host.updateData("smtp.testserver.local")
        settings.mailer_port.updateData(465)
        settings.mailer_use_ssl.updateData(True)
        settings.mailer_use_starttls.updateData(False)
        settings.mailer_user.updateData("testuser")
        settings.mailer_password.updateData("secret")
        settings.hourly_tasks.updateData([["SHELL", "ls /tmp0"]])
        settings.daily_tasks.updateData([["BACKUP", ""], ["SHELL", "ls /tmp1"]])
        settings.weekly_tasks.updateData([["SHELL", "ls /tmp2"]])
        settings.monthly_tasks.updateData([["SHELL", "ls /tmp3"]])
        settings.save()

        self.assertEqual("EFA_SHUTDOWN_ACTION=test\n", file_stub.settings_list[0])
        self.assertEqual("AUTO_USB_BACKUP=\"TRUE\"\n", file_stub.settings_list[1])
        self.assertEqual("AUTO_USB_BACKUP_DIALOG=\"TRUE\"\n", file_stub.settings_list[2])
        self.assertEqual("EFALIVE_BACKUP_PATHS=\"/tmp /test\"\n", file_stub.settings_list[3])
        self.assertEqual("EFA_PORT=1234\n", file_stub.settings_list[4])
        self.assertEqual("EFA_CREDENTIALS_FILE=/tmp/cred.txt\n", file_stub.settings_list[5])
        self.assertEqual("AUTO_BACKUP_PASSWORD=secret\n", file_stub.settings_list[6])
        self.assertEqual("AUTO_BACKUP_USE_PASSWORD=\"TRUE\"\n", file_stub.settings_list[7])
        self.assertEqual("MAILER_HOST=smtp.testserver.local\n", file_stub.settings_list[8])
        self.assertEqual("MAILER_PORT=465\n", file_stub.settings_list[9])
        self.assertEqual("MAILER_USE_SSL=\"TRUE\"\n", file_stub.settings_list[10])
        self.assertEqual("MAILER_USE_STARTTLS=\"FALSE\"\n", file_stub.settings_list[11])
        self.assertEqual("MAILER_USER=testuser\n", file_stub.settings_list[12])
        self.assertEqual("MAILER_PASSWORD=secret\n", file_stub.settings_list[13])
        self.assertEqual("HOURLY_TASKS=[[\"SHELL\", \"ls /tmp0\"]]\n", file_stub.settings_list[14])
        self.assertEqual("DAILY_TASKS=[[\"BACKUP\", \"\"], [\"SHELL\", \"ls /tmp1\"]]\n", file_stub.settings_list[15])
        self.assertEqual("WEEKLY_TASKS=[[\"SHELL\", \"ls /tmp2\"]]\n", file_stub.settings_list[16])
        self.assertEqual("MONTHLY_TASKS=[[\"SHELL\", \"ls /tmp3\"]]\n", file_stub.settings_list[17])


class FileStub(object):

    def __init__(self, is_empty):
        if is_empty:
            self.settings_list = []
        else:
            self.settings_list = [
                    "EFA_SHUTDOWN_ACTION=restart",
                    "AUTO_USB_BACKUP=\"TRUE\"",
                    "AUTO_USB_BACKUP_DIALOG=\"TRUE\"",
                    "EFALIVE_BACKUP_PATHS=\"/tmp /test\"",
                    "EFA_PORT=1234",
                    "EFA_CREDENTIALS_FILE=/tmp/cred.txt",
                    "AUTO_BACKUP_PASSWORD=secret",
                    "AUTO_BACKUP_USE_PASSWORD=\"TRUE\"",
                    "MAILER_HOST=smtp.testserver.local",
                    "MAILER_PORT=465",
                    "MAILER_USE_STARTTLS=\"FALSE\"",
                    "MAILER_USE_SSL=\"TRUE\"",
                    "MAILER_USER=testuser",
                    "MAILER_PASSWORD=secret",
                    "HOURLY_TASKS=[[\"SHELL\",\"ls /tmp0\"]]",
                    "DAILY_TASKS=[[\"BACKUP\",\"\"],[\"SHELL\",\"ls /tmp1\"]]",
                    "WEEKLY_TASKS=[[\"SHELL\",\"ls /tmp2\"]]",
                    "MONTHLY_TASKS=[[\"SHELL\",\"ls /tmp3\"]]",
                    ]

    def close(self):
        pass

    def __iter__(self):
        return iter(self.settings_list)

    def write(self, data):
        self.settings_list.append(data)

