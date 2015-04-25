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
                    "EFA_CREDENTIALS_FILE=/tmp/cred.txt"
                    ]

    def close(self):
        pass

    def __iter__(self):
        return iter(self.settings_list)

"""
    class __metaclass__(type):
        def __iter__(self):
            for attr in dir(FileStub):
                if not attr.startswith("__"):
                    yield attr
"""

