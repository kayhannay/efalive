#!/usr/bin/python
'''
Created on 16.02.2015

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
import unittest
from mock import MagicMock

from efalive.common import common
from efalivedaemon import AutoBackupModule
from efalive.common.usbmonitor import UsbStorageDevice

class AutoBackupModuleTestCase(unittest.TestCase):

    def test_handle_usb_add_device(self):
        classUnderTest = AutoBackupModule()
        common.command_output = MagicMock(return_value=(0, "Test output"))

        result = classUnderTest._handle_usb_add_event(UsbStorageDevice("/dev/test1"))

        common.command_output.assert_called_once_with(["/usr/lib/efalive/bin/autobackup", "/dev/test1"])

    def test_run_autobackup__success(self):
        classUnderTest = AutoBackupModule()
        common.command_output = MagicMock(return_value=(0, "Test output"))

        result = classUnderTest._run_autobackup("/dev/test1")

        common.command_output.assert_called_once_with(['/usr/lib/efalive/bin/autobackup', '/dev/test1'])
        self.assertEqual(0, result)

    def test_run_autobackup__fail_user(self):
        classUnderTest = AutoBackupModule()
        common.command_output = MagicMock(return_value=(1, "Test error"))

        result = classUnderTest._run_autobackup("/dev/test1")

        common.command_output.assert_not_called()
        self.assertEqual(1, result)

    def test_run_autobackup__fail_other(self):
        classUnderTest = AutoBackupModule()
        common.command_output = MagicMock(return_value=(2, "Test error"))

        result = classUnderTest._run_autobackup("/dev/test1")

        common.command_output.assert_not_called()
        self.assertEqual(1, result)

    def test_run_autobackup__fail_exception(self):
        classUnderTest = AutoBackupModule()
        common.command_output = MagicMock(side_effect = OSError())

        result = classUnderTest._run_autobackup("/dev/test1")

        common.command_output.assert_not_called()
        self.assertEqual(1, result)


