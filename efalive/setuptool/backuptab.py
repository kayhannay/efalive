'''
Created on 20.09.2015

Copyright (C) 2015-2024 Kay Hannay

This file is part of efaLiveTools.

efaLiveTools is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
efaLiveSetup is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with efaLiveTools.  If not, see <http://www.gnu.org/licenses/>.
'''
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import logging
import hashlib

from ..common.i18n import _

class BackupTabModel(object):
    def __init__(self, settings):
        self._logger = logging.getLogger('BackupTabModel')
        self._settings = settings

    def enableAutoUsbBackup(self, enable):
        self._settings.autoUsbBackup.updateData(enable)
        self._logger.debug("auto USB backup: %s" % enable)

    def enableAutoUsbBackupDialog(self, enable):
        self._settings.autoUsbBackupDialog.updateData(enable)
        self._logger.debug("auto USB backup dialog: %s" % enable)

    def enableAutoBackupPassword(self, enable):
        self._settings.auto_backup_use_password.updateData(enable)
        self._logger.debug("auto backup use password: %s" % enable)

    def setAutoBackupPassword(self, backupPassword):
        passwordHash = hashlib.sha512(backupPassword.encode('utf-8')).hexdigest()
        self._settings.auto_backup_password = passwordHash
        self._logger.debug("efa auto backup password: %s, hash %s" % (backupPassword, passwordHash))

    def enableAutoBackupEncryption(self, enable):
        self._settings.auto_backup_use_encryption.updateData(enable)
        self._logger.debug("auto backup use encryption: %s" % enable)

    def setAutoBackupEncryptionPassword(self, encryptionPassword):
        passwordHash = hashlib.sha512(encryptionPassword.encode('utf-8')).hexdigest()
        self._settings.auto_backup_encryption_password = passwordHash
        self._logger.debug("efa auto backup encryption password: %s, hash %s" % (encryptionPassword, passwordHash))

    def registerAutoUsbBackupCb(self, callback):
        self._settings.autoUsbBackup.registerObserverCb(callback)

    def registerAutoUsbBackupDialogCb(self, callback):
        self._settings.autoUsbBackupDialog.registerObserverCb(callback)

    def registerAutoBackupUsePasswordCb(self, callback):
        self._settings.auto_backup_use_password.registerObserverCb(callback)

    def registerAutoBackupUseEncryptionCb(self, callback):
        self._settings.auto_backup_use_encryption.registerObserverCb(callback)

class BackupTabView(Gtk.VBox):
    def __init__(self):
        super(Gtk.VBox, self).__init__()
        self._logger = logging.getLogger('BackupTabView')
        self._init_components()

    def _init_components(self):
        self._create_auto_usb_backup_components()

    def _create_auto_usb_backup_components(self):
        # automatic usb backup box
        self.usbBackupFrame=Gtk.Frame.new(_("Auto USB backup"))
        self.pack_start(self.usbBackupFrame, False, False, 5)
        self.usbBackupFrame.show()

        self.usbBackupSpaceBox=Gtk.HBox(False, 5)
        self.usbBackupFrame.add(self.usbBackupSpaceBox)
        self.usbBackupSpaceBox.show()

        self.autoUsbBackupVBox=Gtk.VBox(False, 2)
        self.usbBackupSpaceBox.pack_start(self.autoUsbBackupVBox, True, True, 2)
        self.autoUsbBackupVBox.show()

        self.autoUsbBackupHBox=Gtk.HBox(False, 2)
        self.autoUsbBackupVBox.pack_start(self.autoUsbBackupHBox, True, True, 2)
        self.autoUsbBackupHBox.show()

        self.autoUsbBackupCbox = Gtk.CheckButton(_("enable automatic USB backup"))
        self.autoUsbBackupHBox.pack_start(self.autoUsbBackupCbox, False, True, 2)
        self.autoUsbBackupCbox.show()

        self.autoUsbBackupEnabledVBox=Gtk.VBox(False, 2)
        self.autoUsbBackupVBox.pack_start(self.autoUsbBackupEnabledVBox, True, True, 2)
        self.autoUsbBackupEnabledVBox.show()

        self.autoUsbBackupDialogHBox=Gtk.HBox(False, 2)
        self.autoUsbBackupEnabledVBox.pack_start(self.autoUsbBackupDialogHBox, True, True, 2)
        self.autoUsbBackupDialogHBox.show()

        self.autoUsbBackupDialogCbox = Gtk.CheckButton(_("show dialog after automatic backup"))
        self.autoUsbBackupDialogHBox.pack_start(self.autoUsbBackupDialogCbox, False, True, 20)
        self.autoUsbBackupDialogCbox.show()

        self.autoBackupUsePasswordHBox=Gtk.HBox(False, 2)
        self.autoUsbBackupEnabledVBox.pack_start(self.autoBackupUsePasswordHBox, True, True, 2)
        self.autoBackupUsePasswordHBox.show()

        self.autoBackupUsePasswordCbox = Gtk.CheckButton(_("use password for automatic backup"))
        self.autoBackupUsePasswordHBox.pack_start(self.autoBackupUsePasswordCbox, False, True, 20)
        self.autoBackupUsePasswordCbox.show()

        self.autoBackupPasswordHBox=Gtk.HBox(False, 2)
        self.autoUsbBackupEnabledVBox.pack_start(self.autoBackupPasswordHBox, True, True, 2)
        self.autoBackupPasswordHBox.show()

        self.autoBackupPasswordLabel=Gtk.Label(_("backup password"))
        self.autoBackupPasswordHBox.pack_start(self.autoBackupPasswordLabel, False, False, 40)
        self.autoBackupPasswordLabel.show()

        self.autoBackupPasswordEntry = Gtk.Entry()
        self.autoBackupPasswordEntry.set_max_length(255)
        self.autoBackupPasswordEntry.set_visibility(False)
        self.autoBackupPasswordHBox.pack_end(self.autoBackupPasswordEntry, True, True, 2)
        self.autoBackupPasswordEntry.show()

        self.autoBackupUseEncryptionHBox=Gtk.HBox(False, 2)
        self.autoUsbBackupEnabledVBox.pack_start(self.autoBackupUseEncryptionHBox, True, True, 2)
        self.autoBackupUseEncryptionHBox.show()

        self.autoBackupUseEncryptionCbox = Gtk.CheckButton(_("use encryption for automatic backup"))
        self.autoBackupUseEncryptionHBox.pack_start(self.autoBackupUseEncryptionCbox, False, True, 20)
        self.autoBackupUseEncryptionCbox.show()

        self.autoBackupEncryptionPasswordHBox=Gtk.HBox(False, 2)
        self.autoUsbBackupEnabledVBox.pack_start(self.autoBackupEncryptionPasswordHBox, True, True, 2)
        self.autoBackupEncryptionPasswordHBox.show()

        self.autoBackupEncryptionPasswordLabel=Gtk.Label(_("encryption password"))
        self.autoBackupEncryptionPasswordHBox.pack_start(self.autoBackupEncryptionPasswordLabel, False, False, 40)
        self.autoBackupEncryptionPasswordLabel.show()

        self.autoBackupEncryptionPasswordEntry = Gtk.Entry()
        self.autoBackupEncryptionPasswordEntry.set_max_length(255)
        self.autoBackupEncryptionPasswordEntry.set_visibility(False)
        self.autoBackupEncryptionPasswordHBox.pack_end(self.autoBackupEncryptionPasswordEntry, True, True, 2)
        self.autoBackupEncryptionPasswordEntry.show()

class BackupTabController(object):
    def __init__(self, settings):
        self._logger = logging.getLogger('BackupTabController')
        
        self._view = BackupTabView()
        
        self._model = BackupTabModel(settings)
        self._view.autoUsbBackupEnabledVBox.set_sensitive(False)
        self._view.autoBackupPasswordHBox.set_sensitive(False)
        self._model.registerAutoUsbBackupCb(self.autoUsbBackupChanged)
        self._model.registerAutoUsbBackupDialogCb(self.autoUsbBackupDialogChanged)
        self._model.registerAutoBackupUsePasswordCb(self.autoBackupUsePasswordChanged)
        self._model.registerAutoBackupUseEncryptionCb(self.autoBackupUseEncryptionChanged)

        self._init_events()

    def _init_events(self):
        self._view.autoUsbBackupCbox.connect("toggled", self.setAutoUsbBackup)
        self._view.autoUsbBackupDialogCbox.connect("toggled", self.setAutoUsbBackupDialog)
        self._view.autoBackupUsePasswordCbox.connect("toggled", self.setAutoBackupUsePassword)
        self._view.autoBackupPasswordEntry.connect("changed", self.setAutoBackupPassword)
        self._view.autoBackupUseEncryptionCbox.connect("toggled", self.setAutoBackupUseEncryption)
        self._view.autoBackupEncryptionPasswordEntry.connect("changed", self.setAutoBackupEncryptionPassword)

    def get_view(self):
        return self._view

    def autoUsbBackupChanged(self, enable):
        self._view.autoUsbBackupEnabledVBox.set_sensitive(enable)
        self._view.autoUsbBackupCbox.set_active(enable)

    def autoUsbBackupDialogChanged(self, enable):
        self._view.autoUsbBackupDialogCbox.set_active(enable)

    def autoBackupUsePasswordChanged(self, enable):
        self._view.autoBackupPasswordHBox.set_sensitive(enable)
        self._view.autoBackupUsePasswordCbox.set_active(enable)

    def autoBackupPasswordChanged(self, pwd):
        self._view.autoBackupPasswordEntry.set_text(pwd)

    def autoBackupUseEncryptionChanged(self, enable):
        self._view.autoBackupPasswordHBox.set_sensitive(enable)
        self._view.autoBackupUsePasswordCbox.set_active(enable)

    def autoBackupEncryptionPasswordChanged(self, pwd):
        self._view.autoBackupPasswordEntry.set_text(pwd)

    def setAutoUsbBackup(self, widget):
        self._model.enableAutoUsbBackup(widget.get_active())

    def setAutoUsbBackupDialog(self, widget):
        self._model.enableAutoUsbBackupDialog(widget.get_active())

    def setAutoBackupUsePassword(self, widget):
        self._model.enableAutoBackupPassword(widget.get_active())

    def setAutoBackupPassword(self, widget):
        self._model.setAutoBackupPassword(widget.get_text())

    def setAutoBackupUseEncryption(self, widget):
        self._model.enableAutoBackupPassword(widget.get_active())

    def setAutoBackupEncryptionPassword(self, widget):
        self._model.setAutoBackupPassword(widget.get_text())
