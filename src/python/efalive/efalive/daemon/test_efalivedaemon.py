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
from mock import call, patch, MagicMock

from efalive.common import common
from efalivedaemon import EfaLiveDaemon,AutoBackupModule, WatchDogModule
from efalive.common.usbmonitor import UsbStorageDevice
from efalive.common import settings
from efalive.common.settings import EfaLiveSettings

class EfaLiveDaemonTestCase(unittest.TestCase):

    @patch('efalive.daemon.efalivedaemon.EfaLiveSettings', autospec=True)
    def test_init__start(self, settingsMock):
        classUnderTest = EfaLiveDaemon(["efalivedaemon", "start"])
        assert settingsMock.return_value.initSettings.call_count == 1

    @patch('efalive.daemon.efalivedaemon.EfaLiveSettings', autospec=True)
    def test_init__restart(self, settingsMock):
        classUnderTest = EfaLiveDaemon(["efalivedaemon", "restart"])
        assert settingsMock.return_value.initSettings.call_count == 1

    @patch('efalive.daemon.efalivedaemon.EfaLiveSettings', autospec=True)
    def test_init__stop(self, settingsMock):
        classUnderTest = EfaLiveDaemon(["efalivedaemon", "stop"])
        assert settingsMock.return_value.initSettings.call_count == 0

    def test_init__unknown(self):
        EfaLiveDaemon._print_usage_and_exit = MagicMock()
        classUnderTest = EfaLiveDaemon(["efalivedaemon", "unknown"])
        assert EfaLiveDaemon._print_usage_and_exit.call_count == 1

    def test_init__no_argument(self):
        EfaLiveDaemon._print_usage_and_exit = MagicMock()
        classUnderTest = EfaLiveDaemon(["efalivedaemon"])
        assert EfaLiveDaemon._print_usage_and_exit.call_count == 1

    def test_init__too_many_arguments(self):
        EfaLiveDaemon._print_usage_and_exit = MagicMock()
        classUnderTest = EfaLiveDaemon(["efalivedaemon", "start", "/tmp", "test"])
        assert EfaLiveDaemon._print_usage_and_exit.call_count == 1

    @patch('efalive.daemon.efalivedaemon.EfaLiveSettings', autospec=True)
    def test_init__start_with_conf_path_first(self, settingsMock):
        classUnderTest = EfaLiveDaemon(["efalivedaemon", "/tmp", "start"])
        assert settingsMock.return_value.initSettings.call_count == 1

    @patch('efalive.daemon.efalivedaemon.EfaLiveSettings', autospec=True)
    def test_init__start_with_conf_path_last(self, settingsMock):
        classUnderTest = EfaLiveDaemon(["efalivedaemon", "start", "/tmp"])
        assert settingsMock.return_value.initSettings.call_count == 1

    @patch('efalive.daemon.efalivedaemon.EfaLiveSettings', autospec=True)
    def test_init__restart_with_conf_path_first(self, settingsMock):
        classUnderTest = EfaLiveDaemon(["efalivedaemon", "/tmp", "restart"])
        assert settingsMock.return_value.initSettings.call_count == 1

    @patch('efalive.daemon.efalivedaemon.EfaLiveSettings', autospec=True)
    def test_init__restart_with_conf_path_last(self, settingsMock):
        classUnderTest = EfaLiveDaemon(["efalivedaemon", "restart", "/tmp"])
        assert settingsMock.return_value.initSettings.call_count == 1

    @patch('efalive.daemon.efalivedaemon.EfaLiveSettings', autoepec=True)
    def test_init__stop_with_conf_path_first(self, settingsMock):
        classUnderTest = EfaLiveDaemon(["efalivedaemon", "/tmp", "stop"])
        assert settingsMock.return_value.initSettings.call_count == 0

    @patch('efalive.daemon.efalivedaemon.EfaLiveSettings', autospec=True)
    def test_init__stop_with_conf_path_last(self, settingsMock):
        classUnderTest = EfaLiveDaemon(["efalivedaemon", "stop", "/tmp"])
        assert settingsMock.return_value.initSettings.call_count == 0

    @patch('efalive.daemon.efalivedaemon.EfaLiveSettings', autospec=True)
    def test_init__unknown_with_conf_path(self, settingsMock):
        EfaLiveDaemon._print_usage_and_exit = MagicMock()
        classUnderTest = EfaLiveDaemon(["efalivedaemon", "unknown"])
        assert EfaLiveDaemon._print_usage_and_exit.call_count == 1


class AutoBackupModuleTestCase(unittest.TestCase):

    def test_handle_usb_add_device(self):
        classUnderTest = AutoBackupModule()
        common.command_output = MagicMock(return_value=(0, "Test output"))

        result = classUnderTest._handle_usb_add_event(UsbStorageDevice("/dev/test1"))

        common.command_output.assert_called_once_with(["/usr/lib/efalive/bin/autobackup.sh", "/dev/test1"])

    def test_run_autobackup__success(self):
        classUnderTest = AutoBackupModule()
        common.command_output = MagicMock(return_value=(0, "Test output"))

        result = classUnderTest._run_autobackup("/dev/test1")

        common.command_output.assert_called_once_with(['/usr/lib/efalive/bin/autobackup.sh', '/dev/test1'])
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


class WatchDogModuleTestCase(unittest.TestCase):

    def test_run_checks__process_found(self):
        class_under_test = WatchDogModule()
        common.command_output = MagicMock(return_value=(0, "root       792   707  2 19:03 tty7     00:01:03 openbox"))

        class_under_test.run_checks()

        common.command_output.assert_called_once_with(["ps", "-Af"])

    def test_run_checks__process_not_found(self):
        class_under_test = WatchDogModule()
        common.command_output = MagicMock(return_value=(0, "root       792   707  2 19:03 tty7     00:01:03 AnotherProcess -foo"))

        class_under_test.run_checks()
        class_under_test.run_checks()
        class_under_test.run_checks()

        expected_calls = [call(["ps", "-Af"]), call(["ps", "-Af"]), call(["ps", "-Af"]), call(["sudo", "/sbin/shutdown", "-r", "now"])]
        self.assertEquals(expected_calls, common.command_output.call_args_list)

