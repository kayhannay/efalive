#!/usr/bin/python
'''
Created on 27.04.2015

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
from mock import call, patch, MagicMock, Mock
from email.mime.multipart import MIMEMultipart

from tasks import ShellTask, BackupMailTask
from efalive.common import common
from efalive.common.mailer import Mailer
from efalive.common.observable import Observable
from efalive.common.settings import EfaLiveSettings

class ShellTaskTestCase(unittest.TestCase):

    def test_run(self):
        common.command_output = MagicMock(return_value = (0, "testfile.txt"))

        class_under_test = ShellTask("123def", "ls /tmp")
        class_under_test.run()

        self.assertEqual(1, common.command_output.call_count)
        self.assertEqual(call(["ls", "/tmp"]), common.command_output.call_args)

class BackupMailTaskTestCase(unittest.TestCase):

    def test_run(self):
        common.command_output = MagicMock(return_value = (0, ""))
        os.path.exists = MagicMock(return_value = False)
        os.makedirs = MagicMock()
        os.listdir = MagicMock()
        os.rmdir = MagicMock()
        Mailer.create_mail = MagicMock(return_value = MIMEMultipart())
        Mailer.send_mail = MagicMock()

        settings_mock = Mock(spec=EfaLiveSettings)
        settings_mock.mailer_host = Observable()
        settings_mock.mailer_host.updateData("localhost")
        settings_mock.mailer_port = Observable()
        settings_mock.mailer_use_starttls = Observable()
        settings_mock.mailer_use_ssl = Observable()
        settings_mock.mailer_user = Observable()
        settings_mock.mailer_password = Observable()
        settings_mock.mailer_sender = Observable()

        class_under_test = BackupMailTask("123def", ["user@test.local"], settings_mock)
        mailer_mock = Mock(spec=Mailer)
        class_under_test.run(mailer=mailer_mock)

        self.assertEqual(1, os.makedirs.call_count)
        self.assertEqual(1, common.command_output.call_count)
        self.assertEqual(call(["/usr/bin/efalive-backup", "/tmp/efalive_backup_mail"]), common.command_output.call_args)
        self.assertEqual(1, mailer_mock.create_mail.call_count)
        self.assertEqual(1, mailer_mock.send_mail.call_count)

