#!/usr/bin/python
'''
Created on 08.03.2015

Copyright (C) 2015-2016 Kay Hannay

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
import pyudev

from .usbmonitor import UsbStorageMonitor, UsbStorageDevice

DEVICE_FILE = "/dev/test1"
DEVICE_VENDOR = "Vendor"
DEVICE_MODEL = "Model"
DEVICE_FS_TYPE = "vfat"
DEVICE_FS_LABEL = "FsLabel"
DEVICE_VENDOR_ID = "VID"
DEVICE_MODEL_ID = "MID"
DEVICE_SERIAL = "serial123"

class UsbStorageMonitorTestCase(unittest.TestCase):

    def setUp(self):
        self._callback_device = None
        self._udev_device_stub = UdevDeviceStub()

    def test_handle_device_event__usb_storage_add(self):
        #given
        self._class_under_test = UsbStorageMonitor(self._callback_stub)

        #when
        self._class_under_test._handle_device_event(self._udev_device_stub)

        #then
        self.assertIsNotNone(self._callback_device)
        self.assertEqual("/dev/test1", self._callback_device.device_file)

    def test_handle_device_event__usb_storage_remove(self):
        #given
        self._class_under_test = UsbStorageMonitor(self._callback_stub)
        self._udev_device_stub.action = "remove"

        #when
        self._class_under_test._handle_device_event(self._udev_device_stub)

        #then
        self.assertIsNone(self._callback_device)

    def test_handle_device_event__non_usb(self):
        #given
        self._class_under_test = UsbStorageMonitor(self._callback_stub)
        self._udev_device_stub.bus_id = "scsi"

        #when
        self._class_under_test._handle_device_event(self._udev_device_stub)

        #then
        self.assertIsNone(self._callback_device)

    def _callback_stub(self, device):
        self._callback_device = device

    def test_wrap_device__none_device(self):
        #given
        self._class_under_test = UsbStorageMonitor(self._callback_stub)

        #when
        wrapped_device = self._class_under_test._wrap_device(None)

        #then
        self.assertIsNone(wrapped_device)

    def test_wrap_device__null_size(self):
        #given
        self._class_under_test = UsbStorageMonitor(self._callback_stub)

        #when
        wrapped_device = self._class_under_test._wrap_device(self._udev_device_stub)

        #then
        self.assertIsNotNone(wrapped_device)
        self.assertEquals(DEVICE_FILE, wrapped_device.device_file)
        self.assertEquals(DEVICE_VENDOR, wrapped_device.vendor)
        self.assertEquals(DEVICE_MODEL, wrapped_device.model)
        self.assertEquals(0, wrapped_device.size)
        self.assertEquals(DEVICE_FS_TYPE, wrapped_device.fs_type)
        self.assertEquals(DEVICE_FS_LABEL, wrapped_device.label)
        self.assertEquals(DEVICE_VENDOR_ID + ":" + DEVICE_MODEL_ID, wrapped_device.bus_id)
        self.assertEquals(DEVICE_SERIAL, wrapped_device.serial)

    def test_wrap_device__1kb_size(self):
        #given
        self._class_under_test = UsbStorageMonitor(self._callback_stub)
        self._udev_device_stub.size = 1024

        #when
        wrapped_device = self._class_under_test._wrap_device(self._udev_device_stub)

        #then
        self.assertIsNotNone(wrapped_device)
        self.assertEquals(DEVICE_FILE, wrapped_device.device_file)
        self.assertEquals(DEVICE_VENDOR, wrapped_device.vendor)
        self.assertEquals(DEVICE_MODEL, wrapped_device.model)
        self.assertEquals("1.0 KB", wrapped_device.size)
        self.assertEquals(DEVICE_FS_TYPE, wrapped_device.fs_type)
        self.assertEquals(DEVICE_FS_LABEL, wrapped_device.label)
        self.assertEquals(DEVICE_VENDOR_ID + ":" + DEVICE_MODEL_ID, wrapped_device.bus_id)

    def test_wrap_device__3_1_mb_size(self):
        #given
        self._class_under_test = UsbStorageMonitor(self._callback_stub)
        self._udev_device_stub.size = 1024 * 1024 * 3.1

        #when
        wrapped_device = self._class_under_test._wrap_device(self._udev_device_stub)

        #then
        self.assertIsNotNone(wrapped_device)
        self.assertEquals(DEVICE_FILE, wrapped_device.device_file)
        self.assertEquals(DEVICE_VENDOR, wrapped_device.vendor)
        self.assertEquals(DEVICE_MODEL, wrapped_device.model)
        self.assertEquals("3.1 MB", wrapped_device.size)
        self.assertEquals(DEVICE_FS_TYPE, wrapped_device.fs_type)
        self.assertEquals(DEVICE_FS_LABEL, wrapped_device.label)
        self.assertEquals(DEVICE_VENDOR_ID + ":" + DEVICE_MODEL_ID, wrapped_device.bus_id)

    def test_wrap_device__2_3_gb_size(self):
        #given
        self._class_under_test = UsbStorageMonitor(self._callback_stub)
        self._udev_device_stub.size = 1024 * 1024 * 1024 * 2.3

        #when
        wrapped_device = self._class_under_test._wrap_device(self._udev_device_stub)

        #then
        self.assertIsNotNone(wrapped_device)
        self.assertEquals(DEVICE_FILE, wrapped_device.device_file)
        self.assertEquals(DEVICE_VENDOR, wrapped_device.vendor)
        self.assertEquals(DEVICE_MODEL, wrapped_device.model)
        self.assertEquals("2.3 GB", wrapped_device.size)
        self.assertEquals(DEVICE_FS_TYPE, wrapped_device.fs_type)
        self.assertEquals(DEVICE_FS_LABEL, wrapped_device.label)
        self.assertEquals(DEVICE_VENDOR_ID + ":" + DEVICE_MODEL_ID, wrapped_device.bus_id)

    def test_wrap_device__7_8_tb_size(self):
        #given
        self._class_under_test = UsbStorageMonitor(self._callback_stub)
        self._udev_device_stub.size = 1024 * 1024 * 1024 * 1024 * 7.8

        #when
        wrapped_device = self._class_under_test._wrap_device(self._udev_device_stub)

        #then
        self.assertIsNotNone(wrapped_device)
        self.assertEquals(DEVICE_FILE, wrapped_device.device_file)
        self.assertEquals(DEVICE_VENDOR, wrapped_device.vendor)
        self.assertEquals(DEVICE_MODEL, wrapped_device.model)
        self.assertEquals("7.8 TB", wrapped_device.size)
        self.assertEquals(DEVICE_FS_TYPE, wrapped_device.fs_type)
        self.assertEquals(DEVICE_FS_LABEL, wrapped_device.label)
        self.assertEquals(DEVICE_VENDOR_ID + ":" + DEVICE_MODEL_ID, wrapped_device.bus_id)

    def test_wrap_device__2018_tb_size(self):
        #given
        self._class_under_test = UsbStorageMonitor(self._callback_stub)
        self._udev_device_stub.size = 1024 * 1024 * 1024 * 1024 * 2048

        #when
        wrapped_device = self._class_under_test._wrap_device(self._udev_device_stub)

        #then
        self.assertIsNotNone(wrapped_device)
        self.assertEquals(DEVICE_FILE, wrapped_device.device_file)
        self.assertEquals(DEVICE_VENDOR, wrapped_device.vendor)
        self.assertEquals(DEVICE_MODEL, wrapped_device.model)
        self.assertEquals("2048.0 TB", wrapped_device.size)
        self.assertEquals(DEVICE_FS_TYPE, wrapped_device.fs_type)
        self.assertEquals(DEVICE_FS_LABEL, wrapped_device.label)
        self.assertEquals(DEVICE_VENDOR_ID + ":" + DEVICE_MODEL_ID, wrapped_device.bus_id)


class UdevDeviceStub(pyudev.Device):

    subsystem = "block"
    device_type = "partition"
    sys_name = "test1"
    sys_number = "1"
    sys_path = "/sys/devices/test1"
    driver = None
    action = "add"
    device_node = DEVICE_FILE

    bus_id = "usb"
    size = 0

    class LibUdev(object):
        def udev_device_get_property_value(self, foo, bar):
            return DEVICE_SERIAL

    def __init__(self):
        self._libudev = self.LibUdev()

    def __del__(self):
        pass

    def get(self, key):
        return {
                "ID_PART_ENTRY_SIZE": self.size,
                "ID_VENDOR": DEVICE_VENDOR,
                "ID_MODEL": DEVICE_MODEL,
                "ID_FS_TYPE": DEVICE_FS_TYPE,
                "ID_FS_LABEL": DEVICE_FS_LABEL,
                "ID_VENDOR_ID": DEVICE_VENDOR_ID,
                "ID_MODEL_ID": DEVICE_MODEL_ID,
                "ID_TYPE": "Type",
                "ID_BUS": self.bus_id,
        }[key]

