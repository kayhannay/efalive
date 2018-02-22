#!/usr/bin/python
'''
Created on 11.01.2011

Copyright (C) 2011-2016 Kay Hannay

This file is part of efaLiveSetup.

efaLiveSetup is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
efaLiveSetup is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with efaLiveSetup.  If not, see <http://www.gnu.org/licenses/>.
'''
import pygtk
pygtk.require('2.0')
import gtk
import os
import sys
import re
import traceback
import logging
import locale
import gettext

from ..setupcommon import dialogs
from efalive.common import common
from efalive.common.usbmonitor import UsbStorageDevice, UsbStorageMonitor

APP="deviceManager"
gettext.install(APP, common.LOCALEDIR, unicode=True)

class DeviceWidget(gtk.VBox):
    def __init__(self, device, homogeneous=False, spacing=2):
        super(DeviceWidget, self).__init__(homogeneous, spacing)
        self.device = device
        separator = gtk.HSeparator()
        self.add(separator)
        separator.show()

        hBox = gtk.HBox(False, 5)
        self.add(hBox)
        hBox.show()

        label_text = "Unknown"
        if self.device.label:
            label_text = self.device.label
        elif self.device.model:
            label_text = self.device.model
        self.label = gtk.Label(label_text)
        hBox.pack_start(self.label, True, True)
        self.label.show()

        self.restore_button = gtk.Button()
        restore_icon = gtk.image_new_from_file(common.get_icon_path("restore.png"))
        self.restore_button.set_image(restore_icon)
        self.restore_button.set_tooltip_text(_("Restore backup from device"))
        hBox.pack_end(self.restore_button, False, False)
        self.restore_button.show()

        self.backup_button = gtk.Button()
        backup_icon = gtk.image_new_from_file(common.get_icon_path("backup.png"))
        self.backup_button.set_image(backup_icon)
        self.backup_button.set_tooltip_text(_("Create backup on device"))
        hBox.pack_end(self.backup_button, False, False)
        self.backup_button.show()

        self.mount_button = gtk.ToggleButton()
        hBox.pack_end(self.mount_button, False, False)
        self.mount_button.show()


class Device(UsbStorageDevice):
    def __init__(self, usb_device, mounted=False):
        super(Device, self).__init__(usb_device.device_file, usb_device.vendor, usb_device.model, usb_device.size, usb_device.fs_type, usb_device.label, usb_device.bus_id)
        self.mounted = mounted

class DeviceManagerModel(object):
    def __init__(self):
        self._logger = logging.getLogger('devicemanager.DeviceManagerModel')
        self._add_device_observers = []
        self._remove_device_observers = []
        self._change_device_observers = []
        self._device_monitor = UsbStorageMonitor(self._device_add_event_callback, self._device_remove_event_callback, self._device_change_event_callback, for_gui=True)
        self._device_monitor.start()

    def _device_add_event_callback(self, usb_device):
        mounted = self.check_mounted(usb_device)
        device = Device(usb_device, mounted)
        self._notify_add_observers(device)

    def _device_remove_event_callback(self, usb_device):
        mounted = self.check_mounted(usb_device)
        device = Device(usb_device, mounted)
        self._notify_remove_observers(device)

    def _device_change_event_callback(self, usb_device):
        mounted = self.check_mounted(usb_device)
        device = Device(usb_device, mounted)
        self._notify_change_observers(device)

    def register_add_observer(self, observer_cb):
        self._add_device_observers.append(observer_cb)

    def remove_add_observer(self, observer_cb):
        self._add_device_observers.remove(observer_cb)

    def _notify_add_observers(self, device):
        for observer_cb in self._add_device_observers:
            observer_cb(device)

    def register_remove_observer(self, observer_cb):
        self._remove_device_observers.append(observer_cb)

    def remove_remove_observer(self, observer_cb):
        self._remove_device_observers.remove(observer_cb)

    def _notify_remove_observers(self, device):
        for observer_cb in self._remove_device_observers:
            observer_cb(device)

    def register_change_observer(self, observer_cb):
        self._change_device_observers.append(observer_cb)

    def remove_change_observer(self, observer_cb):
        self._change_device_observers.remove(observer_cb)

    def _notify_change_observers(self, device):
        for observer_cb in self._change_device_observers:
            observer_cb(device)

    def check_mounted(self, device):
        self._logger.debug("Check if %s is mounted" % device.device_file)
        try:
            (returncode, mount_output) = common.command_output(["mount"])
        except OSError as (errno, strerror):
            self._logger.error("Could not execute mount command to check mount status: %s" % strerror)
            raise
        mounted = re.search(device.device_file, mount_output)
        if mounted:
            return True
        else:
            return False

    def search_devices(self):
        self._logger.info("Search for devices")
        self._device_monitor.search_for_usb_block_devices()

    def get_label(self, device):
        label_text = "Unknown"
        if device.label:
            label_text = device.label
        elif device.model:
            label_text = device.model
        return label_text

    def toggle_mount(self, device, mount):
        if mount:
            label_text = self.get_label(device)
            self._logger.info("Mounting device %s to %s" % (device.device_file, label_text))
            common.command_output(["pmount", device.device_file, label_text])
        else:
            self._logger.info("Unmounting device %s" % device.device_file)
            common.command_output(["pumount", device.device_file])

    def create_backup(self, path):
        self._logger.info("Create a backup to %s" % path)
        return common.command_output(["/usr/bin/efalive-backup", path])

    def restore_backup(self, file):
        self._logger.info("Restore backup from %s" % file)
        return common.command_output(["/usr/bin/efalive-restore", file])


class DeviceManagerView(gtk.Window):
    def __init__(self, type, controller=None):
        self._logger = logging.getLogger('devicemanager.DeviceManagerView')
        gtk.Window.__init__(self, type)
        self.set_title(_("Device Manager"))
        self.set_border_width(5)
        self._controller = controller

        self._init_components()

    def _init_components(self):
        self.main_box=gtk.VBox(False, 2)
        self.add(self.main_box)
        self.main_box.show()

        self.info_label = gtk.Label(_("USB storage devices"))
        self.main_box.add(self.info_label)
        self.info_label.show()

        self.no_device_label = gtk.Label(_("no devices found"))
        self.main_box.add(self.no_device_label)
        self.no_device_label.show()

        self._device_entries = {}

    def add_device(self, device):
        device_entry = self.create_device_entry(device)
        self.main_box.add(device_entry)
        self.no_device_label.hide()
        device_entry.show()
        self._device_entries[device.device_file] = device_entry

    def remove_device(self, device):
        device_entry = self._device_entries[device.device_file]
        del self._device_entries[device.device_file]
        device_entry.destroy()
        if len(self._device_entries) == 0:
            self.no_device_label.show()
        self.queue_resize()

    def create_device_entry(self, device):
        device_entry = DeviceWidget(device)
        self.set_device_mounted(device_entry)

        device_entry.mount_button.connect("toggled", self._controller.toggle_mount, device_entry)
        device_entry.backup_button.connect("clicked", self._controller.create_backup, device)
        device_entry.restore_button.connect("clicked", self._controller.restore_backup, device)

        return device_entry

    def set_device_mounted(self, device_entry):
        if device_entry.device.mounted:
            unmount_icon = gtk.image_new_from_file(common.get_icon_path("unmount.png"))
            device_entry.mount_button.set_image(unmount_icon)
            device_entry.mount_button.set_active(True)
            device_entry.mount_button.set_tooltip_text(_("Unmount USB device"))
            device_entry.label.set_tooltip_text(_("Vendor: %s") % device_entry.device.vendor + "\n" +
                _("Model: %s") % device_entry.device.model + "\n" +
                _("Device: %s") % device_entry.device.device_file + "\n" +
                _("Size: %s") % device_entry.device.size + "\n" +
                _("Filesystem: %s") % device_entry.device.fs_type + "\n" +
                _("USB-Id: %s") % device_entry.device.bus_id + "\n" +
                _("Mouned to: %s") % "/media/" + device_entry.label.get_text())
        else:
            mount_icon = gtk.image_new_from_file(common.get_icon_path("mount.png"))
            device_entry.mount_button.set_image(mount_icon)
            device_entry.mount_button.set_active(False)
            device_entry.mount_button.set_tooltip_text(_("Mount USB device"))
            device_entry.label.set_tooltip_text(_("Vendor: %s") % device_entry.device.vendor + "\n" +
                _("Model: %s") % device_entry.device.model + "\n" +
                _("Device: %s") % device_entry.device.device_file + "\n" +
                _("Size: %s") % device_entry.device.size + "\n" +
                _("Filesystem: %s") % device_entry.device.fs_type + "\n" +
                _("USB-Id: %s") % device_entry.device.bus_id)


class DeviceManagerController(object):
    def __init__(self, argv, standalone=False, model=None, view=None):
        self._logger = logging.getLogger('devicemanager.DeviceManagerController')
        if(model==None):
            self._model=DeviceManagerModel()
        else:
            self._model=model
        if(view==None):
            self._view=DeviceManagerView(gtk.WINDOW_TOPLEVEL, self)
        else:
            self._view=view
        self._init_events(standalone)
        self._view.show()
        self._model.search_devices()

    def _init_events(self, standalone):
        if standalone:
            self._view.connect("destroy", self._destroy)
        self._model.register_add_observer(self.on_device_add)
        self._model.register_remove_observer(self.on_device_remove)
        self._model.register_change_observer(self.on_device_change)

    def _destroy(self, widget):
        gtk.main_quit()

    def toggle_mount(self, button, device_entry):
        if button.get_active():
            try:
                self._model.toggle_mount(device_entry.device, True)
                device_entry.device.mounted = True
                self._view.set_device_mounted(device_entry)
            except OSError as error:
                message = _("Could not mount device: %s") % error
                self._logger.error(message)
                dialogs.show_exception_dialog(self._view, message, traceback.format_exc())
        else:
            try:
                self._model.toggle_mount(device_entry.device, False)
                device_entry.device.mounted = False
                self._view.set_device_mounted(device_entry)
            except OSError as error:
                message = _("Could not unmount device: %s") % error
                self._logger.error(message)
                dialogs.show_exception_dialog(self._view, message, traceback.format_exc())

    def create_backup(self, widget, device):
        try:
            was_mounted = self._model.check_mounted(device)
            if not was_mounted:
                self._model.toggle_mount(device, True)
            path = os.path.join("/media", self._model.get_label(device))
            (returncode, output) = self._model.create_backup(path)
            if returncode != 0:
                if returncode == 1 or returncode == 5:
                    message = _("Backup failed! Please check that the efalive user is configured correctly in efa.")
                    self._logger.error(message)
                    self._logger.debug(output)
                    dialogs.show_exception_dialog(self._view, message, output)
                else:
                    message = _("Backup to %s failed!") % path
                    self._logger.error(message)
                    self._logger.debug(output)
                    dialogs.show_exception_dialog(self._view, message, output)
            else:
                message = _("Backup to %s finished.") % path
                self._logger.info(message)
                self._logger.debug(output)
                dialogs.show_output_dialog(self._view, message, output)
            if not was_mounted:
                self._model.toggle_mount(device, False)
        except OSError as error:
            message = _("Could not create backup: %s") % error
            dialogs.show_exception_dialog(self._view, message, traceback.format_exc())

    def restore_backup(self, widget, device):
        try:
            was_mounted = self._model.check_mounted(device)
            if not was_mounted:
                self._model.toggle_mount(device, True)
            file_chooser = gtk.FileChooserDialog(_("Select backup"), 
                                                 self._view, 
                                                 gtk.FILE_CHOOSER_ACTION_OPEN, 
                                                 (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
            path = os.path.join("/media", self._model.get_label(device))
            file_chooser.set_current_folder(path)
            result = file_chooser.run()
            if result == gtk.RESPONSE_OK:
                file_chooser.hide()
                filename = file_chooser.get_filename()
                (returncode, output) = self._model.restore_backup(filename)
                if returncode != 0:
                    if returncode == 1 or returncode == 5:
                        message = _("Restore failed! Please check that the efalive user is configured correctly in efa.")
                        self._logger.error(message)
                        self._logger.debug(output)
                        dialogs.show_exception_dialog(self._view, message, output)
                    elif returncode == 1004:
                        message = _("Restore of backup finished, but only restored efaLive backup.") % filename
                        self._logger.warning(message)
                        self._logger.debug(output)
                        dialogs.show_warning_dialog(self._view, message, output)
                    elif returncode == 1005:
                        message = _("Restore of backup finished, but only restored efa backup.") % filename
                        self._logger.warning(message)
                        self._logger.debug(output)
                        dialogs.show_warning_dialog(self._view, message, output)
                    else:
                        message = _("Restore of backup %s failed!") % filename
                        self._logger.error(message)
                        self._logger.debug(output)
                        dialogs.show_exception_dialog(self._view, message, output)
                else:
                    message = _("Restore of backup %s finished.") % filename
                    self._logger.info(message)
                    self._logger.debug(output)
                    dialogs.show_output_dialog(self._view, message, output)
            if not was_mounted:
                self._model.toggle_mount(device, False)
        except OSError as error:
            message = _("Could not restore backup: %s") % error
            dialogs.show_exception_dialog(self._view, message, traceback.format_exc())
        finally:
            file_chooser.destroy()

    def on_device_add(self, device):
        self._view.add_device(device)

    def on_device_remove(self, device):
        self._view.remove_device(device)

    def on_device_change(self, device):
        pass


if __name__ == '__main__':
    logging.basicConfig(filename='deviceManager.log',level=logging.INFO)
    controller = DeviceManagerController(sys.argv, True)
    gtk.main()
