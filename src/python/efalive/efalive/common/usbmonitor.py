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
import logging
from pyudev import Context, Monitor, MonitorObserver as UdevObserver
from pyudev.glib import MonitorObserver as UdevGuiObserver

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

    def __init__(self, add_callback, remove_callback = None, change_callback = None, for_gui = False):
        self._logger = logging.getLogger('efalive.UsbStorageMonitor')

        self._external_add_callback = add_callback
        self._external_remove_callback = remove_callback
        self._external_change_callback = change_callback

        self._udev_context = Context()
        self._udev_monitor = Monitor.from_netlink(self._udev_context)
        self._udev_monitor.filter_by('block', device_type='partition')
        self._for_gui = for_gui
        if for_gui:
            self._udev_observer = UdevGuiObserver(self._udev_monitor)
            self._udev_observer.connect('device-event', self._handle_gui_device_event)
        else:
            self._udev_observer = UdevObserver(self._udev_monitor, callback=self._handle_device_event, name='monitor-observer')

    def start(self):
        if self._for_gui:
            self._udev_monitor.start()
        else:
            self._udev_observer.start()

    def stop(self):
        if self._for_gui:
            self._udev_monitor.stop()
        else:
            self._udev_observer.stop()

    def _handle_gui_device_event(self, observer, device):
        self._handle_device_event(device)

    def _handle_device_event(self, device):
        self._debug_device(device)
        if (device.get("ID_BUS") != "usb"):
            return
        self._logger.info("Action %s for device %s" % (device.action, device.device_node))
        if device.action == "add":
            wrapped_device = self._wrap_device(device)
            self._external_add_callback(wrapped_device)
        elif device.action == "remove" and self._external_remove_callback != None:
            wrapped_device = self._wrap_device(device)
            self._external_remove_callback(wrapped_device)
        elif device.action == "change" and self._external_change_callback != None:
            wrapped_device = self._wrap_device(device)
            self._external_change_callback(wrapped_device)
        else:
            self._logger.info("Unhandled action: %s" % device.action)

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
        ##self._logger.debug("\tID_VENDOR: %s" % device.get("ID_VENDOR"))
        self._logger.debug("\tID_SERIAL: %s" % device.properties.get("ID_SERIAL"))
        self._logger.debug("\tID_MODEL: %s" % device.get("ID_MODEL"))
        self._logger.debug("\tID_TYPE: %s" % device.get("ID_TYPE"))
        self._logger.debug("\tID_BUS: %s" % device.get("ID_BUS"))
        self._logger.debug("\tID_FS_LABEL: %s" % device.get("ID_FS_LABEL"))
        self._logger.debug("\tID_FS_TYPE: %s" % device.get("ID_FS_TYPE"))
        self._logger.debug("\tID_PART_ENTRY_SIZE: %s" % device.get("ID_PART_ENTRY_SIZE"))
        #self._logger.debug("All attributes:")
        #for attrName in device.__iter__():
        #    self._logger.debug(attrName)

    def _wrap_device(self, device):
        """ Convert a PyUdev device to an efaLive device
        """
        if device is None:
            return None
        wrapped_device = UsbStorageDevice(device.device_node)
        if device.get("ID_VENDOR"):
            wrapped_device.vendor = device.get("ID_VENDOR")
        if device.get("ID_MODEL"):
            wrapped_device.model = device.get("ID_MODEL")
        if device.get("ID_PART_ENTRY_SIZE"):
            byte_size = float(device.get("ID_PART_ENTRY_SIZE"))
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
        if device.get("ID_FS_TYPE"):
            wrapped_device.fs_type = device.get("ID_FS_TYPE")
        if device.get("ID_FS_LABEL"):
            wrapped_device.label = device.get("ID_FS_LABEL")
        if device.get("ID_VENDOR_ID") and device.get("ID_MODEL_ID"):
            wrapped_device.bus_id = "%s:%s" % (device.get("ID_VENDOR_ID"), device.get("ID_MODEL_ID"))
        return wrapped_device

    def search_for_usb_block_devices(self):
        for usb_device in self._udev_context.list_devices(subsystem='block', DEVTYPE='partition'):
            if (usb_device.get("ID_BUS") != "usb"):
                continue
            wrapped_device = self._wrap_device(usb_device)
            self._external_add_callback(wrapped_device)
