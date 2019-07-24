#!/usr/bin/python
'''
Created on 08.03.2015

Copyright (C) 2015-2019 Kay Hannay

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
import gi
gi.require_version("GUdev", "1.0")
from gi.repository import GUdev
from gi.repository import GLib

import logging
import threading
import time


class UsbStorageDevice(object):
    """ Simple USB device inforamtion class

    This is a simple data class for information about an USB storage device as
    it is used in efaLive.
    """

    def __init__(self, device_file: str, vendor: str=None, model: str=None, size: str=0, fs_type: str=None, label: str=None, bus_id: str=None, serial: str=None):
        self.device_file: str = device_file
        self.vendor: str = vendor
        self.model: str = model
        self.size: str = size
        self.fs_type: str = fs_type
        self.label: str = label
        self.bus_id: str = bus_id
        self.serial: str = serial


class UsbStorageMonitor(object):
    """ USB storage device add monitor

    This monitor is listening to UDEV for USB storage device 'add' events. The callback 
    that is provided to the constructor is called for every USB storage device that is
    added to the system.
    """

    DEFAULT_SECTOR_SIZE = 512

    def __init__(self, add_callback: callable, remove_callback: callable = None, change_callback: callable = None, for_gui: bool = False):
        self._logger = logging.getLogger('efalive.UsbStorageMonitor')

        self._external_add_callback = add_callback
        self._external_remove_callback = remove_callback
        self._external_change_callback = change_callback
        self._for_gui = for_gui

        self._gudev: GUdev.Client = GUdev.Client.new(["block/partition"])
        self._gudev.connect("uevent", self._handle_device_event)
        if not self._for_gui:
            self._event_loop = GLib.MainLoop()

    def start(self):
        if not self._for_gui:
            event_loop_thread = threading.Thread(target=self._event_loop.run, name="GLib main loop")
            event_loop_thread.start()

    def stop(self):
        if not self._for_gui:
            self._event_loop.quit()

    def _handle_device_event(self, _, action: str, device: GUdev.Device):
        if self._logger.isEnabledFor(logging.DEBUG):
            self._debug_device(device)
        if device.get_property("ID_BUS") != "usb":
            return
        self._logger.info("Action %s for device %s" % (action, device.get_device_file()))
        if action == "add":
            wrapped_device = self._wrap_device(device)
            self._external_add_callback(wrapped_device)
        elif action == "remove" and self._external_remove_callback != None:
            wrapped_device = self._wrap_device(device)
            self._external_remove_callback(wrapped_device)
        elif action == "change" and self._external_change_callback != None:
            wrapped_device = self._wrap_device(device)
            self._external_change_callback(wrapped_device)
        else:
            self._logger.info("Unhandled action: %s" % action)

    def _debug_device(self, device: GUdev.Device):
        self._logger.debug("Device:")
        self._logger.debug("\tSubsystem: %s" % device.get_subsystem())
        self._logger.debug("\tType: %s" % device.get_property("DEVTYPE"))
        self._logger.debug("\tName: %s" % device.get_name())
        self._logger.debug("\tNumber: %s" % device.get_number())
        self._logger.debug("\tSYS-fs path: %s" % device.get_sysfs_path())
        self._logger.debug("\tDriver: %s" % device.get_driver())
        self._logger.debug("\tFile: %s" % device.get_device_file())
        #self._logger.debug("\tLinks: %s" % device.get_device_file_symlinks())
        #self._logger.debug("\tProperties: %s" % device.get_property_keys())
        #self._logger.debug("\tSYBSYSTEM: %s" % device.get_property("SUBSYSTEM"))
        #self._logger.debug("\tDEVTYPE: %s" % device.get_property("DEVTYPE"))
        ##self._logger.debug("\tID_VENDOR: %s" % device.get("ID_VENDOR"))
        self._logger.debug("\tID_SERIAL: %s" % device.get_property("ID_SERIAL"))
        self._logger.debug("\tID_MODEL: %s" % device.get_property("ID_MODEL"))
        self._logger.debug("\tID_TYPE: %s" % device.get_property("ID_TYPE"))
        self._logger.debug("\tID_BUS: %s" % device.get_property("ID_BUS"))
        self._logger.debug("\tID_FS_LABEL: %s" % device.get_property("ID_FS_LABEL"))
        self._logger.debug("\tID_FS_TYPE: %s" % device.get_property("ID_FS_TYPE"))
        self._logger.debug("\tID_PART_ENTRY_SIZE: %s" % device.get_property("ID_PART_ENTRY_SIZE"))

        #self._logger.debug("All properties:")
        #for propName in device.get_property_keys():
        #    self._logger.debug("\t{name}: {value}".format(name=propName, value=device.get_property(propName)))
        #self._logger.debug("All SYSFS attributes:")
        #for attrName in device.get_sysfs_attr_keys():
        #    self._logger.debug("\t{name}: {value}".format(name=attrName, value=device.get_sysfs_attr(attrName)))

    @staticmethod
    def _wrap_device(device: GUdev.Device):
        """ Convert a GUdev device to an efaLive device
        """
        if device is None:
            return None
        wrapped_device = UsbStorageDevice(device.get_device_file())
        if device.get_property("ID_VENDOR"):
            wrapped_device.vendor = device.get_property("ID_VENDOR")
        if device.get_property("ID_MODEL"):
            wrapped_device.model = device.get_property("ID_MODEL")
        if device.get_property("ID_PART_ENTRY_SIZE"):
            byte_size = float(device.get_property("ID_PART_ENTRY_SIZE")) * UsbStorageMonitor.DEFAULT_SECTOR_SIZE
            size = byte_size / 1024
            unit = "KB"
            if (size > 1024):
                size = size / 1024
                unit = "MB"
            if (size > 1024):
                size = size / 1024
                unit = "GB"
            if (size > 1024):
                size = size / 1024
                unit = "TB"
            wrapped_device.size = "%.1f %s" % (size, unit)
        if device.get_property("ID_FS_TYPE"):
            wrapped_device.fs_type = device.get_property("ID_FS_TYPE")
        if device.get_property("ID_FS_LABEL"):
            wrapped_device.label = device.get_property("ID_FS_LABEL")
        if device.get_property("ID_VENDOR_ID") and device.get_property("ID_MODEL_ID"):
            wrapped_device.bus_id = "%s:%s" % (device.get_property("ID_VENDOR_ID"), device.get_property("ID_MODEL_ID"))
        if device.get_property("ID_SERIAL"):
            wrapped_device.serial = device.get_property("ID_SERIAL")
        return wrapped_device

    def search_for_usb_block_devices(self):
        for usb_device in self._gudev.query_by_subsystem("block/partition"):
            if (usb_device.get_property("ID_BUS") != "usb"):
                continue
            wrapped_device = self._wrap_device(usb_device)
            self._external_add_callback(wrapped_device)


def add_callback(device: UsbStorageDevice):
    print("Device added: {0}\n".format(device))


def remove_callback(device: UsbStorageDevice):
    print("Device removed: {0}\n".format(device))


def change_callback(device: UsbStorageDevice):
    print("Device changed: {0}\n".format(device))


if __name__ == "__main__":
    logging.basicConfig(filename="usbmonitor.log", level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s: %(message)s')

    monitor = UsbStorageMonitor(add_callback, remove_callback, change_callback)
    monitor.start()
    print("Monitor started.")
    for i in range(1, 10):
        time.sleep(10)
        print("Running active {}".format(i))
    monitor.stop()
    for i in range(1, 10):
        time.sleep(10)
        print("Running stopped {}".format(i))
    monitor.start()
    print("Monitor started.")
    for i in range(1, 10):
        time.sleep(10)
        print("Running active {}".format(i))
    monitor.stop()
