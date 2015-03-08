#!/usr/bin/python
'''
Created on 08.03.2015

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
import logging
from pyudev import Context, Monitor, MonitorObserver

class UsbStorageDevice(object):
    """ Simple USB device inforamtion class

    This is a simple data class for information about an USB storage device as
    it is used in efaLive.
    """

    def __init__(self, device_file, vendor=None, model=None, size=0, fs_type=None, label=None, bus_id=None):
        self.device_file = device_file
        self.vendor = vendor
        self.model = model
        self.size = size
        self.fs_type = fs_type
        self.label = label
        self.bus_id = bus_id


class UsbStorageMonitor(object):
    """ USB storage device add monitor

    This monitor is listening to UDEV for USB storage device 'add' events. The callback 
    that is provided to the constructor is called for every USB storage device that is
    added to the system.
    """

    def __init__(self, callback):
        self._logger = logging.getLogger('efalive.UsbStorageMonitor')

        self._external_callback = callback

        udev_context = Context()
        self._udev_monitor = Monitor.from_netlink(udev_context)
        self._udev_monitor.filter_by('block', device_type='partition')

    def start(self):
        self._udev_observer = MonitorObserver(self._udev_monitor, callback=self._handle_device_event, name='monitor-observer')
        self._udev_observer.start()

    def stop(self):
        self._udev_observer.stop()

    def _handle_device_event(self, device):
        self._debug_device(device)
        if (device.__getitem__("ID_BUS") != "usb"):
            return
        self._logger.info("Action %s for device %s" % (device.action, device.device_node))
        if device.action == "add":
            self._logger.info("Calling external callback now.")
            wrapped_device = self._wrap_device(device)
            self._external_callback(wrapped_device)
        else:
            self._logger.warn("Unhandled action: %s" % device.action)

    def _debug_device(self, device):
        self._logger.debug("Device:")
        self._logger.debug("\tSubsystem: %s" % device.subsystem)
        self._logger.debug("\tType: %s" % device.device_type)
        self._logger.debug("\tName: %s" % device.sys_name)
        self._logger.debug("\tNumber: %s" % device.sys_number)
        self._logger.debug("\tSYS-fs path: %s" % device.sys_path)
        self._logger.debug("\tDriver: %s" % device.driver)
        self._logger.debug("\tAction: %s" % device.action)
        self._logger.debug("\tFile: %s" % device.device_node)
        #self._logger.debug("\tLinks: %s" % device.get_device_file_symlinks())
        #self._logger.debug("\tProperties: %s" % device.get_property_keys())
        #self._logger.debug("\tSYBSYSTEM: %s" % device.get_property("SUBSYSTEM"))
        #self._logger.debug("\tDEVTYPE: %s" % device.get_property("DEVTYPE"))
        ##self._logger.debug("\tID_VENDOR: %s" % device.__getitem__("ID_VENDOR"))
        self._logger.debug("\tID_MODEL: %s" % device.__getitem__("ID_MODEL"))
        self._logger.debug("\tID_TYPE: %s" % device.__getitem__("ID_TYPE"))
        self._logger.debug("\tID_BUS: %s" % device.__getitem__("ID_BUS"))
        self._logger.debug("\tID_FS_LABEL: %s" % device.__getitem__("ID_FS_LABEL"))
        self._logger.debug("\tID_FS_TYPE: %s" % device.__getitem__("ID_FS_TYPE"))
        self._logger.debug("\tUDISKS_PARTITION_SIZE: %s" % device.__getitem__("UDISKS_PARTITION_SIZE"))

    def _wrap_device(self, device):
        """ Convert a PyUdev device to an efaLive device
        """
        if device is None:
            return None
        wrapped_device = UsbStorageDevice(device.device_node)
        if device.__getitem__("ID_VENDOR"):
            wrapped_device.vendor = device.__getitem__("ID_VENDOR")
        if device.__getitem__("ID_MODEL"):
            wrapped_device.model = device.__getitem__("ID_MODEL")
        if device.__getitem__("UDISKS_PARTITION_SIZE"):
            byte_size = float(device.__getitem__("UDISKS_PARTITION_SIZE"))
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
        if device.__getitem__("ID_FS_TYPE"):
            wrapped_device.fs_type = device.__getitem__("ID_FS_TYPE")
        if device.__getitem__("ID_FS_LABEL"):
            wrapped_device.label = device.__getitem__("ID_FS_LABEL")
        if device.__getitem__("ID_VENDOR_ID") and device.__getitem__("ID_MODEL_ID"):
            wrapped_device.bus_id = "%s:%s" % (device.__getitem__("ID_VENDOR_ID"), device.__getitem__("ID_MODEL_ID"))
        return wrapped_device

