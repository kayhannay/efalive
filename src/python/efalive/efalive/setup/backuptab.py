'''
Created on 20.09.2015

Copyright (C) 2015-2016 Kay Hannay

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
import pygtk
pygtk.require('2.0')
import gtk
import logging
import gettext
import hashlib

from ..common import common

APP="BackupTab"
gettext.install(APP, common.LOCALEDIR, unicode=True)

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
        self._logger.debug("auto backup password: %s" % enable)

    def setAutoBackupPassword(self, backupPassword):
        passwordHash = hashlib.sha512(backupPassword).hexdigest()
        self._settings.auto_backup_password = passwordHash
        self._logger.debug("efa auto backup password: %s, hash %s" % (backupPassword, passwordHash))

    def registerAutoUsbBackupCb(self, callback):
        self._settings.autoUsbBackup.registerObserverCb(callback)

    def registerAutoUsbBackupDialogCb(self, callback):
        self._settings.autoUsbBackupDialog.registerObserverCb(callback)

    def registerAutoBackupUsePasswordCb(self, callback):
        self._settings.auto_backup_use_password.registerObserverCb(callback)

class BackupTabView(gtk.VBox):
    def __init__(self):
        super(gtk.VBox, self).__init__()
        self._logger = logging.getLogger('BackupTabView')
        self._init_components()

    def _init_components(self):
        self._create_auto_usb_backup_components()

    def _create_auto_usb_backup_components(self):
        # automatic usb backup box
        self.usbBackupFrame=gtk.Frame(_("Auto USB backup"))
        self.pack_start(self.usbBackupFrame, False, False, 5)
        self.usbBackupFrame.show()

        self.usbBackupSpaceBox=gtk.HBox(False, 5)
        self.usbBackupFrame.add(self.usbBackupSpaceBox)
        self.usbBackupSpaceBox.show()

        self.autoUsbBackupVBox=gtk.VBox(False, 2)
        self.usbBackupSpaceBox.pack_start(self.autoUsbBackupVBox, True, True, 2)
        self.autoUsbBackupVBox.show()

        self.autoUsbBackupHBox=gtk.HBox(False, 2)
        self.autoUsbBackupVBox.pack_start(self.autoUsbBackupHBox, True, True, 2)
        self.autoUsbBackupHBox.show()

        self.autoUsbBackupCbox = gtk.CheckButton(_("enable automatic USB backup"))
        self.autoUsbBackupHBox.pack_start(self.autoUsbBackupCbox, False, True, 2)
        self.autoUsbBackupCbox.show()

        self.autoUsbBackupEnabledVBox=gtk.VBox(False, 2)
        self.autoUsbBackupVBox.pack_start(self.autoUsbBackupEnabledVBox, True, True, 2)
        self.autoUsbBackupEnabledVBox.show()

        self.autoUsbBackupDialogHBox=gtk.HBox(False, 2)
        self.autoUsbBackupEnabledVBox.pack_start(self.autoUsbBackupDialogHBox, True, True, 2)
        self.autoUsbBackupDialogHBox.show()

        self.autoUsbBackupDialogCbox = gtk.CheckButton(_("show dialog after automatic backup"))
        self.autoUsbBackupDialogHBox.pack_start(self.autoUsbBackupDialogCbox, False, True, 20)
        self.autoUsbBackupDialogCbox.show()

        self.autoBackupUsePasswordHBox=gtk.HBox(False, 2)
        self.autoUsbBackupEnabledVBox.pack_start(self.autoBackupUsePasswordHBox, True, True, 2)
        self.autoBackupUsePasswordHBox.show()

        self.autoBackupUsePasswordCbox = gtk.CheckButton(_("use password for automatic backup"))
        self.autoBackupUsePasswordHBox.pack_start(self.autoBackupUsePasswordCbox, False, True, 20)
        self.autoBackupUsePasswordCbox.show()

        self.autoBackupPasswordHBox=gtk.HBox(False, 2)
        self.autoUsbBackupEnabledVBox.pack_start(self.autoBackupPasswordHBox, True, True, 2)
        self.autoBackupPasswordHBox.show()

        self.autoBackupPasswordLabel=gtk.Label(_("backup password"))
        self.autoBackupPasswordHBox.pack_start(self.autoBackupPasswordLabel, False, False, 40)
        self.autoBackupPasswordLabel.show()

        self.autoBackupPasswordEntry = gtk.Entry(max=255)
        self.autoBackupPasswordEntry.set_visibility(False)
        self.autoBackupPasswordHBox.pack_end(self.autoBackupPasswordEntry, True, True, 2)
        self.autoBackupPasswordEntry.show()

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
        
        self._init_events()

    def _init_events(self):
        self._view.autoUsbBackupCbox.connect("toggled", self.setAutoUsbBackup)
        self._view.autoUsbBackupDialogCbox.connect("toggled", self.setAutoUsbBackupDialog)
        self._view.autoBackupUsePasswordCbox.connect("toggled", self.setAutoBackupUsePassword)
        self._view.autoBackupPasswordEntry.connect("changed", self.setAutoBackupPassword)

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

    def setAutoUsbBackup(self, widget):
        self._model.enableAutoUsbBackup(widget.get_active())

    def setAutoUsbBackupDialog(self, widget):
        self._model.enableAutoUsbBackupDialog(widget.get_active())

    def setAutoBackupUsePassword(self, widget):
        self._model.enableAutoBackupPassword(widget.get_active())

    def setAutoBackupPassword(self, widget):
        self._model.setAutoBackupPassword(widget.get_text())

