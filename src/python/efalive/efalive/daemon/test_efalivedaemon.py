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
from efalivedaemon import EfaLiveDaemon,AutoBackupModule, WatchDogModule, TaskSchedulerModule
from efalive.common.usbmonitor import UsbStorageDevice
from efalive.common import settings
from efalive.common.settings import EfaLiveSettings

class EfaLiveDaemonTestCase(unittest.TestCase):

    @patch('efalive.daemon.efalivedaemon.EfaLiveSettings')
    def test_init__start(self, settingsMock):
        classUnderTest = EfaLiveDaemon(["efalivedaemon", "start"])
        settingsMock.initSettings.assert_called_once()

    @patch('efalive.daemon.efalivedaemon.EfaLiveSettings')
    def test_init__restart(self, settingsMock):
        classUnderTest = EfaLiveDaemon(["efalivedaemon", "restart"])
        settingsMock.initSettings.assert_called_once()

    @patch('efalive.daemon.efalivedaemon.EfaLiveSettings')
    def test_init__stop(self, settingsMock):
        classUnderTest = EfaLiveDaemon(["efalivedaemon", "stop"])
        settingsMock.initSettings.assert_not_called()

    def test_init__unknown(self):
        EfaLiveDaemon._print_usage_and_exit = MagicMock()
        classUnderTest = EfaLiveDaemon(["efalivedaemon", "unknown"])
        EfaLiveDaemon._print_usage_and_exit.assert_called_once()

    def test_init__no_argument(self):
        EfaLiveDaemon._print_usage_and_exit = MagicMock()
        classUnderTest = EfaLiveDaemon(["efalivedaemon"])
        EfaLiveDaemon._print_usage_and_exit.assert_called_once()

    def test_init__too_many_arguments(self):
        EfaLiveDaemon._print_usage_and_exit = MagicMock()
        classUnderTest = EfaLiveDaemon(["efalivedaemon", "start", "/tmp", "test"])
        EfaLiveDaemon._print_usage_and_exit.assert_called_once()

    @patch('efalive.daemon.efalivedaemon.EfaLiveSettings')
    def test_init__start_with_conf_path_first(self, settingsMock):
        classUnderTest = EfaLiveDaemon(["efalivedaemon", "/tmp", "start"])
        settingsMock.initSettings.assert_called_once()

    @patch('efalive.daemon.efalivedaemon.EfaLiveSettings')
    def test_init__start_with_conf_path_last(self, settingsMock):
        classUnderTest = EfaLiveDaemon(["efalivedaemon", "start", "/tmp"])
        settingsMock.initSettings.assert_called_once()

    @patch('efalive.daemon.efalivedaemon.EfaLiveSettings')
    def test_init__restart_with_conf_path_first(self, settingsMock):
        classUnderTest = EfaLiveDaemon(["efalivedaemon", "/tmp", "restart"])
        settingsMock.initSettings.assert_called_once()

    @patch('efalive.daemon.efalivedaemon.EfaLiveSettings')
    def test_init__restart_with_conf_path_last(self, settingsMock):
        classUnderTest = EfaLiveDaemon(["efalivedaemon", "restart", "/tmp"])
        settingsMock.initSettings.assert_called_once()

    @patch('efalive.daemon.efalivedaemon.EfaLiveSettings')
    def test_init__stop_with_conf_path_first(self, settingsMock):
        classUnderTest = EfaLiveDaemon(["efalivedaemon", "/tmp", "stop"])
        settingsMock.initSettings.assert_not_called()

    @patch('efalive.daemon.efalivedaemon.EfaLiveSettings')
    def test_init__stop_with_conf_path_last(self, settingsMock):
        classUnderTest = EfaLiveDaemon(["efalivedaemon", "stop", "/tmp"])
        settingsMock.initSettings.assert_not_called()

    @patch('efalive.daemon.efalivedaemon.EfaLiveSettings')
    def test_init__unknown_with_conf_path(self, settingsMock):
        EfaLiveDaemon._print_usage_and_exit = MagicMock()
        classUnderTest = EfaLiveDaemon(["efalivedaemon", "unknown"])
        EfaLiveDaemon._print_usage_and_exit.assert_called_once()


class AutoBackupModuleTestCase(unittest.TestCase):

    def test_handle_usb_add_device(self):
        classUnderTest = AutoBackupModule()
        common.command_output = MagicMock(return_value=(0, "Test output"))

        result = classUnderTest._handle_usb_add_event(UsbStorageDevice("/dev/test1"))

        self.assertEqual(call(['/usr/lib/efalive/bin/autobackup.sh', '/dev/test1']), common.command_output.call_args)
        self.assertEqual(1, common.command_output.call_count)

    def test_run_autobackup__success(self):
        classUnderTest = AutoBackupModule()
        common.command_output = MagicMock(return_value=(0, "Test output"))

        result = classUnderTest._run_autobackup("/dev/test1")

        self.assertEqual(call(['/usr/lib/efalive/bin/autobackup.sh', '/dev/test1']), common.command_output.call_args)
        self.assertEqual(1, common.command_output.call_count)
        self.assertEqual(0, result)

    def test_run_autobackup__fail_user(self):
        classUnderTest = AutoBackupModule()
        common.command_output = MagicMock(return_value=(1, "Test error"))

        result = classUnderTest._run_autobackup("/dev/test1")

        self.assertEqual(1, result)

    def test_run_autobackup__fail_other(self):
        classUnderTest = AutoBackupModule()
        common.command_output = MagicMock(return_value=(2, "Test error"))

        result = classUnderTest._run_autobackup("/dev/test1")

        self.assertEqual(1, result)

    def test_run_autobackup__fail_exception(self):
        classUnderTest = AutoBackupModule()
        common.command_output = MagicMock(side_effect = OSError())

        result = classUnderTest._run_autobackup("/dev/test1")

        self.assertEqual(1, result)


class WatchDogModuleTestCase(unittest.TestCase):

    def test_run_checks__process_found(self):
        class_under_test = WatchDogModule()
        common.command_output = MagicMock(return_value=(0, "root       792   707  2 19:03 tty7     00:01:03 openbox"))

        class_under_test.run_checks()

        self.assertEqual(1, common.command_output.call_count)
        self.assertEqual(call(["ps", "-Af"]), common.command_output.call_args)

    def test_run_checks__process_not_found(self):
        class_under_test = WatchDogModule()
        common.command_output = MagicMock(return_value=(0, "root       792   707  2 19:03 tty7     00:01:03 AnotherProcess -foo"))

        class_under_test.run_checks()
        class_under_test.run_checks()
        class_under_test.run_checks()

        expected_calls = [call(["ps", "-Af"]), call(["ps", "-Af"]), call(["ps", "-Af"]), call(["sudo", "/sbin/shutdown", "-r", "now"])]
        self.assertEquals(expected_calls, common.command_output.call_args_list)


class TaskSchedulerModuleTestCase(unittest.TestCase):

    @patch("efalive.daemon.efalivedaemon.EfaLiveSettings")
    @patch("__builtin__.open")
    def test_run_tasks(self, open_mock, settings_mock):
        common.command_output = MagicMock(return_value = (0, "testfile.txt"))
        fileStub = FileStub()
        open_mock.return_value = fileStub
        settings_mock.hourly_tasks.getData.return_value = [["SHELL", "ls /tmp1"]]
        settings_mock.daily_tasks.getData.return_value = [["SHELL", "ls /tmp2"]]
        settings_mock.weekly_tasks.getData.return_value = [["SHELL", "ls /tmp3"]]
        settings_mock.monthly_tasks.getData.return_value = [["SHELL", "ls /tmp4"]]
        settings_mock.confPath = "/test"

        class_under_test = TaskSchedulerModule()
        class_under_test.load_tasks(settings_mock)
        class_under_test.run_tasks()

        self.assertEqual(4, common.command_output.call_count)
        self.assertEqual(call(["ls", "/tmp1"]), common.command_output.call_args_list[0])
        self.assertEqual(call(["ls", "/tmp2"]), common.command_output.call_args_list[1])
        self.assertEqual(call(["ls", "/tmp3"]), common.command_output.call_args_list[2])
        self.assertEqual(call(["ls", "/tmp4"]), common.command_output.call_args_list[3])
        self.assertEqual(1, len(class_under_test._hourly_markers))
        self.assertEqual(1, len(class_under_test._daily_markers))
        self.assertEqual(1, len(class_under_test._weekly_markers))
        self.assertEqual(1, len(class_under_test._monthly_markers))
        self.assertEqual(4, len(fileStub.data))

    @patch("efalive.daemon.efalivedaemon.EfaLiveSettings")
    @patch("__builtin__.open")
    def test_run_tasks__already_executed(self, open_mock, settings_mock):
        common.command_output = MagicMock(return_value = (0, "testfile.txt"))
        fileStub = FileStub()
        open_mock.return_value = fileStub
        settings_mock.hourly_tasks.getData.return_value = [["SHELL", "ls /tmp1"]]
        settings_mock.daily_tasks.getData.return_value = []
        settings_mock.weekly_tasks.getData.return_value = []
        settings_mock.monthly_tasks.getData.return_value = []
        settings_mock.confPath = "/test"

        class_under_test = TaskSchedulerModule()
        class_under_test.load_tasks(settings_mock)
        class_under_test.run_tasks()

        self.assertEqual(1, common.command_output.call_count)
        self.assertEqual(call(["ls", "/tmp1"]), common.command_output.call_args_list[0])
        self.assertEqual(1, len(class_under_test._hourly_markers))
        self.assertEqual(0, len(class_under_test._daily_markers))
        self.assertEqual(0, len(class_under_test._weekly_markers))
        self.assertEqual(0, len(class_under_test._monthly_markers))
        self.assertEqual(1, len(fileStub.data))

        class_under_test.run_tasks()

        self.assertEqual(1, common.command_output.call_count)
        self.assertEqual(call(["ls", "/tmp1"]), common.command_output.call_args_list[0])
        self.assertEqual(1, len(class_under_test._hourly_markers))
        self.assertEqual(0, len(class_under_test._daily_markers))
        self.assertEqual(0, len(class_under_test._weekly_markers))
        self.assertEqual(0, len(class_under_test._monthly_markers))
        self.assertEqual(1, len(fileStub.data))

    @patch("efalive.daemon.efalivedaemon.EfaLiveSettings")
    @patch("__builtin__.open")
    def test_run_tasks__new_task(self, open_mock, settings_mock):
        common.command_output = MagicMock(return_value = (0, "testfile.txt"))
        fileStub = FileStub()
        open_mock.return_value = fileStub
        settings_mock.hourly_tasks.getData.return_value = [["SHELL", "ls /tmp1"]]
        settings_mock.daily_tasks.getData.return_value = []
        settings_mock.weekly_tasks.getData.return_value = []
        settings_mock.monthly_tasks.getData.return_value = []
        settings_mock.confPath = "/test"

        class_under_test = TaskSchedulerModule()
        class_under_test.load_tasks(settings_mock)
        class_under_test.run_tasks()

        self.assertEqual(1, common.command_output.call_count)
        self.assertEqual(call(["ls", "/tmp1"]), common.command_output.call_args_list[0])
        self.assertEqual(1, len(class_under_test._hourly_markers))
        self.assertEqual(0, len(class_under_test._daily_markers))
        self.assertEqual(0, len(class_under_test._weekly_markers))
        self.assertEqual(0, len(class_under_test._monthly_markers))
        self.assertEqual(1, len(fileStub.data))

        settings_mock.daily_tasks.getData.return_value = [["SHELL", "ls /tmp2"]]

        class_under_test.load_tasks(settings_mock)
        class_under_test.run_tasks()

        self.assertEqual(2, common.command_output.call_count)
        self.assertEqual(call(["ls", "/tmp1"]), common.command_output.call_args_list[0])
        self.assertEqual(call(["ls", "/tmp2"]), common.command_output.call_args_list[1])
        self.assertEqual(1, len(class_under_test._hourly_markers))
        self.assertEqual(1, len(class_under_test._daily_markers))
        self.assertEqual(0, len(class_under_test._weekly_markers))
        self.assertEqual(0, len(class_under_test._monthly_markers))
        self.assertEqual(2, len(fileStub.data))


class FileStub(object):

    def __init__(self):
        self.data = []

    def close(self):
        pass

    def __iter__(self):
        return iter(self.data)

    def write(self, d):
        self.data.append(d)


