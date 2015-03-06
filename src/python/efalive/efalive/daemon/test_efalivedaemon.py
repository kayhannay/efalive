from efalivedaemon import AutoBackupModule
import unittest
from mock import MagicMock
import pyudev
from efalive.common import common

class AutoBackupModuleTestCase(unittest.TestCase):

    def test_handle_device_event_add_usb_device(self):
        classUnderTest = AutoBackupModule()
        classUnderTest._run_autobackup = MagicMock()

        deviceStub = DeviceStub()

        classUnderTest._handle_device_event(deviceStub)

        classUnderTest._run_autobackup.assert_called_once_with('/dev/test1')

    def test_handle_device_event_add_non_usb_device(self):
        classUnderTest = AutoBackupModule()
        classUnderTest._run_autobackup = MagicMock()

        deviceStub = DeviceStub()
        deviceStub.bus_id = "ata"

        classUnderTest._handle_device_event(deviceStub)

        classUnderTest._run_autobackup.assert_not_called()

    def test_handle_device_event_remove_usb_device(self):
        classUnderTest = AutoBackupModule()
        classUnderTest._run_autobackup = MagicMock()

        deviceStub = DeviceStub()
        deviceStub.action = "remove"

        classUnderTest._handle_device_event(deviceStub)

        classUnderTest._run_autobackup.assert_not_called()

    def test_run_autobackup_success(self):
        classUnderTest = AutoBackupModule()
        common.command_output = MagicMock(return_value=(0, "Test output"))

        result = classUnderTest._run_autobackup("/dev/test1")

        common.command_output.assert_called_once_with(['/usr/lib/efalive/bin/autobackup', '/dev/test1'])
        self.assertEqual(0, result)

    def test_run_autobackup_fail_user(self):
        classUnderTest = AutoBackupModule()
        common.command_output = MagicMock(return_value=(1, "Test error"))

        result = classUnderTest._run_autobackup("/dev/test1")

        common.command_output.assert_not_called()
        self.assertEqual(1, result)

    def test_run_autobackup_fail_other(self):
        classUnderTest = AutoBackupModule()
        common.command_output = MagicMock(return_value=(2, "Test error"))

        result = classUnderTest._run_autobackup("/dev/test1")

        common.command_output.assert_not_called()
        self.assertEqual(1, result)

    def test_run_autobackup_fail_exception(self):
        classUnderTest = AutoBackupModule()
        common.command_output = MagicMock(side_effect = OSError())

        result = classUnderTest._run_autobackup("/dev/test1")

        common.command_output.assert_not_called()
        self.assertEqual(1, result)


class DeviceStub(pyudev.Device):

    subsystem = "block"
    device_type = "partition"
    sys_name = "test1"
    sys_number = "1"
    sys_path = "/sys/devices/test1"
    driver = None
    action = "add"
    device_node = "/dev/test1"
    bus_id = "usb"

    def __init__(self):
        pass

    def __del__(self):
        pass

    def __getitem__(self, key):
        return self.bus_id

