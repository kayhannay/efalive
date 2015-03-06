'''
Created on 26.08.2010

Copyright (C) 2010-2014 Kay Hannay

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
import sys
import os
import subprocess
import traceback
import logging
import hashlib

from setupcommon import dialogs
from devicemanager.devicemanager import DeviceManagerController as DeviceManager
from screen.screensetup import ScreenSetupController as ScreenSetup
from dttime.datetime import DateTimeController as DateTime
#from datetime.dttime import DateTimeController
from backup.backup import BackupController as Backup
from ..common import common
from ..common.settings import EfaLiveSettings

import locale
import gettext
APP="efaLiveSetup"
gettext.install(APP, common.LOCALEDIR, unicode=True)

class SetupModel(object):
    def __init__(self, confPath):
        self._logger = logging.getLogger('efalivesetup.maingui.SetupModel')
        self._settings = EfaLiveSettings(confPath)

    def initModel(self):
        self._settings.initSettings()

    def save(self):
        self._settings.save()

    def setEfaShutdownAction(self, action):
        self._settings.efaShutdownAction.updateData(action)
        self._logger.debug("efa shutdown action: %s" % action)

    def enableAutoUsbBackup(self, enable):
        self._settings.autoUsbBackup.updateData(enable)
        self._logger.debug("auto USB backup: %s" % enable)

    def enableAutoUsbBackupDialog(self, enable):
        self._settings.autoUsbBackupDialog.updateData(enable)
        self._logger.debug("auto USB backup dialog: %s" % enable)

    def getConfigPath(self):
        return self._settings.confPath

    def setEfaVersion(self, version):
        self._settings.efaVersion.updateData(version)
        self._logger.debug("efa version: %d" % version)

    def setEfaPort(self, port):
        self._settings.efaPort.updateData(port)
        self._logger.debug("efa port: %d" % port)

    def create_log_package(self, path):
        return common.command_output(["/usr/lib/efalive/bin/create_log_package.sh", path])

    def enableAutoBackupPassword(self, enable):
        self._settings.auto_backup_use_password.updateData(enable)
        self._logger.debug("auto backup password: %s" % enable)

    def setAutoBackupPassword(self, pwd):
        hash = hashlib.sha512(pwd).hexdigest()
        self._settings.auto_backup_password = hash
        self._logger.debug("efa auto backup password: %s, hash %s" % (pwd,hash))

    def registerEfaShutdownActionCb(self, callback):
        self._settings.efaShutdownAction.registerObserverCb(callback)

    def registerAutoUsbBackupCb(self, callback):
        self._settings.autoUsbBackup.registerObserverCb(callback)

    def registerAutoUsbBackupDialogCb(self, callback):
        self._settings.autoUsbBackupDialog.registerObserverCb(callback)

    def registerAutoBackupUsePasswordCb(self, callback):
        self._settings.auto_backup_use_password.registerObserverCb(callback)

    def registerEfaPortCb(self, callback):
        self._settings.efaPort.registerObserverCb(callback)

class SetupView(gtk.Window):
    def __init__(self, type):
        self._logger = logging.getLogger('efalivesetup.maingui.SetupView')
        gtk.Window.__init__(self, type)
        self.set_title(_("efaLive setup"))
        self.set_border_width(5)

        self.initComponents()

    def initComponents(self):
        self.mainBox=gtk.VBox(False, 2)
        self.add(self.mainBox)
        self.mainBox.show()

        # settings box
        self.settingsFrame=gtk.Frame(_("efaLive settings"))
        self.mainBox.pack_start(self.settingsFrame, True, True, 2)
        self.settingsFrame.show()

        self.settingsSpaceBox=gtk.HBox(False, 5)
        self.settingsFrame.add(self.settingsSpaceBox)
        self.settingsSpaceBox.show()

        self.settingsVBox=gtk.VBox(False, 0)
        self.settingsSpaceBox.pack_start(self.settingsVBox, True, True, 2)
        self.settingsVBox.show()

        # efa port field
        self.portVBox=gtk.VBox(False, 0)
        self.settingsVBox.pack_start(self.portVBox, True, True, 2)
        self.portVBox.show()

        self.portHBox=gtk.HBox(False, 5)
        self.portVBox.pack_start(self.portHBox, True, True, 2)
        self.portHBox.show()

        self.portLabel=gtk.Label(_("efa network port"))
        self.portHBox.pack_start(self.portLabel, False, False, 5)
        self.portLabel.show()

        self.port_adjustment = gtk.Adjustment(0, 0, 65565, 1, 1000)
        self.port_button = gtk.SpinButton(self.port_adjustment)
        self.port_button.set_wrap(True)
        self.portHBox.pack_end(self.port_button, False, False, 2)
        self.port_button.show()

        # shutdown box
        self.shutdownVBox=gtk.VBox(False, 0)
        self.settingsVBox.pack_start(self.shutdownVBox, True, True, 2)
        self.shutdownVBox.show()

        self.shutdownHBox=gtk.HBox(False, 5)
        self.shutdownVBox.pack_start(self.shutdownHBox, True, True, 2)
        self.shutdownHBox.show()

        self.shutdownLabel=gtk.Label(_("efa shutdown action"))
        self.shutdownHBox.pack_start(self.shutdownLabel, False, False, 5)
        self.shutdownLabel.show()

        self.shutdownCombo=gtk.combo_box_new_text()
        self.shutdownHBox.pack_end(self.shutdownCombo, False, False, 2)
        self.shutdownCombo.show()

        # automatic usb backup box
        self.autoUsbBackupVBox=gtk.VBox(False, 2)
        self.settingsVBox.pack_start(self.autoUsbBackupVBox, True, True, 2)
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

        # tools box
        self.toolsFrame=gtk.Frame(_("Tools"))
        self.mainBox.pack_start(self.toolsFrame, True, False, 2)
        self.toolsFrame.show()

        self.toolsSpaceVBox=gtk.VBox(False, 10)
        self.toolsFrame.add(self.toolsSpaceVBox)
        self.toolsSpaceVBox.show()

        self.toolsSpaceBox=gtk.HBox(False, 10)
        self.toolsSpaceVBox.pack_start(self.toolsSpaceBox, True, True, 5)
        self.toolsSpaceBox.show()

        self.toolsGrid=gtk.Table(2, 3, True)
        self.toolsSpaceBox.pack_start(self.toolsGrid, True, True, 5)
        self.toolsGrid.set_row_spacings(2)
        self.toolsGrid.set_col_spacings(2)
        self.toolsGrid.show()

        self.terminalButton=gtk.Button(_("Terminal"))
        self.toolsGrid.attach(self.terminalButton, 0, 1, 0, 1)
        self.terminalButton.show()

        self.fileManagerButton=gtk.Button(_("File manager"))
        self.toolsGrid.attach(self.fileManagerButton, 1, 2, 0, 1)
        self.fileManagerButton.show()

        self.deviceButton=gtk.Button(_("Devices"))
        self.toolsGrid.attach(self.deviceButton, 2, 3, 0, 1)
        self.deviceButton.show()

        self.editorButton=gtk.Button(_("Editor"))
        self.toolsGrid.attach(self.editorButton, 0, 1, 1, 2)
        self.editorButton.show()

        self.backupButton=gtk.Button(_("Backup"))
        self.toolsGrid.attach(self.backupButton, 1, 2, 1, 2)
        self.backupButton.show()

        self.log_button=gtk.Button(_("Logs"))
        self.toolsGrid.attach(self.log_button, 2, 3, 1, 2)
        self.log_button.show()

        # system box
        self.systemFrame=gtk.Frame(_("System"))
        self.mainBox.pack_start(self.systemFrame, True, False, 2)
        self.systemFrame.show()

        self.systemSpaceVBox=gtk.VBox(False, 10)
        self.systemFrame.add(self.systemSpaceVBox)
        self.systemSpaceVBox.show()

        self.systemSpaceBox=gtk.HBox(False, 10)
        self.systemSpaceVBox.pack_start(self.systemSpaceBox, True, True, 5)
        self.systemSpaceBox.show()

        self.systemGrid=gtk.Table(2, 3, True)
        self.systemSpaceBox.pack_start(self.systemGrid, True, True, 5)
        self.systemGrid.set_row_spacings(2)
        self.systemGrid.set_col_spacings(2)
        self.systemGrid.show()

        self.screenButton=gtk.Button(_("Screen"))
        self.systemGrid.attach(self.screenButton, 0, 1, 0, 1)
        self.screenButton.show()

        self.networkButton=gtk.Button(_("Network"))
        self.systemGrid.attach(self.networkButton, 1, 2, 0, 1)
        self.networkButton.show()

        self.dyndnsButton=gtk.Button(_("Hostname"))
        self.systemGrid.attach(self.dyndnsButton, 2, 3, 0, 1)
        self.dyndnsButton.show()

        self.screensaverButton=gtk.Button(_("Screensaver"))
        self.systemGrid.attach(self.screensaverButton, 0, 1, 1, 2)
        self.screensaverButton.show()

        self.datetimeButton=gtk.Button(_("Date & time"))
        self.systemGrid.attach(self.datetimeButton, 1, 2, 1, 2)
        self.datetimeButton.show()

        self.keyboardButton=gtk.Button(_("Keyboard"))
        self.systemGrid.attach(self.keyboardButton, 2, 3, 1, 2)
        self.keyboardButton.show()


        # actions box
        self.actionsFrame=gtk.Frame(_("Actions"))
        self.mainBox.pack_start(self.actionsFrame, True, False, 2)
        self.actionsFrame.show()

        self.actionsSpaceVBox=gtk.VBox(False, 10)
        self.actionsFrame.add(self.actionsSpaceVBox)
        self.actionsSpaceVBox.show()

        self.actionsSpaceBox=gtk.HBox(False, 10)
        self.actionsSpaceVBox.pack_start(self.actionsSpaceBox, True, True, 5)
        self.actionsSpaceBox.show()

        self.actionsGrid=gtk.Table(1, 3, True)
        self.actionsSpaceBox.pack_start(self.actionsGrid, True, True, 5)
        self.actionsGrid.set_row_spacings(2)
        self.actionsGrid.set_col_spacings(2)
        self.actionsGrid.show()

        self.shutdownButton=gtk.Button(_("Shutdown PC"))
        self.actionsGrid.attach(self.shutdownButton, 0, 1, 0, 1)
        self.shutdownButton.show()

        self.restartButton=gtk.Button(_("Restart PC"))
        self.actionsGrid.attach(self.restartButton, 1, 2, 0, 1)
        self.restartButton.show()

        self.actionsDummy=gtk.Label()
        self.actionsGrid.attach(self.actionsDummy, 2, 3, 0, 1)
        self.actionsDummy.show()


        # button box
        self.buttonBox=gtk.HBox(False, 0)
        self.mainBox.pack_start(self.buttonBox, False, False, 2)
        self.buttonBox.show()

        self.okButton=gtk.Button(_("Ok"))
        self.buttonBox.pack_end(self.okButton, False, False, 2)
        self.okButton.show()

        self.closeButton=gtk.Button(_("Cancel"))
        self.buttonBox.pack_end(self.closeButton, False, False, 2)
        self.closeButton.show()


class SetupController(object):
    def __init__(self, argv, model=None, view=None):
        self._logger = logging.getLogger('efalivesetup.maingui.SetupController')
        if(len(argv) < 2):
            raise(BaseException("No arguments given"))
        ask_for_password = False
        if(len(argv) == 2):
            confPath=argv[1]
        elif(len(argv) == 3):
            if argv[1] != '-p':
                raise(BaseException("Two parameters given, but first one is not -p"))
            ask_for_password = True
            confPath=argv[2]
        if(model==None):
            self._model=SetupModel(confPath)
        else:
            self._model=model
        if(view==None):
            self._view=SetupView(gtk.WINDOW_TOPLEVEL)
        else:
            self._view=view
        if ask_for_password == True:
            pwok = dialogs.show_password_dialog(self._view, 'efa')
            if pwok == False:
                exit()
        self.initEvents()
        self._view.connect("destroy", self.destroy)
        self._view.show()

        self._view.shutdownCombo.append_text(_("shutdown pc"))
        self._view.shutdownCombo.append_text(_("restart pc"))
        self._view.shutdownCombo.append_text(_("restart efa"))
        self._view.shutdownCombo.append_text(_("stop efa"))

        self._view.autoUsbBackupEnabledVBox.set_sensitive(False)
        self._view.autoBackupPasswordHBox.set_sensitive(False)

        self._model.registerEfaShutdownActionCb(self.efaShutdownActionChanged)
        self._model.registerAutoUsbBackupCb(self.autoUsbBackupChanged)
        self._model.registerAutoUsbBackupDialogCb(self.autoUsbBackupDialogChanged)
        self._model.registerAutoBackupUsePasswordCb(self.autoBackupUsePasswordChanged)
        self._model.registerEfaPortCb(self.efaPortChanged)
        self._model.initModel()

    def efaShutdownActionChanged(self, action):
        index=0
        if(action=="\"shutdown\""):
            index=0
        elif(action=="\"restart\""):
            index=1
        elif(action=="\"start_efa\""):
            index=2
        elif(action=="\"stop_efa\""):
            index=3
        self._view.shutdownCombo.set_active(index)

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

    def efaPortChanged(self, port):
        self._view.port_button.set_value(port)

    def destroy(self, widget):
        gtk.main_quit()

    def initEvents(self):
        self._logger.debug("Initialize events")
        self._view.closeButton.connect("clicked", self.destroy)
        self._view.okButton.connect("clicked", self.save)
        self._view.shutdownCombo.connect("changed", self.setEfaShutdownAction)
        self._view.autoUsbBackupCbox.connect("toggled", self.setAutoUsbBackup)
        self._view.autoUsbBackupDialogCbox.connect("toggled", self.setAutoUsbBackupDialog)
        self._view.autoBackupUsePasswordCbox.connect("toggled", self.setAutoBackupUsePassword)
        self._view.autoBackupPasswordEntry.connect("changed", self.setAutoBackupPassword)
        self._view.terminalButton.connect("clicked", self.runTerminal)
        self._view.screenButton.connect("clicked", self.runScreenSetup)
        self._view.deviceButton.connect("clicked", self.runDeviceManager)
        self._view.networkButton.connect("clicked", self.runNetworkSettings)
        self._view.fileManagerButton.connect("clicked", self.runFileManager)
        self._view.shutdownButton.connect("clicked", self.runShutdown)
        self._view.restartButton.connect("clicked", self.runRestart)
        self._view.keyboardButton.connect("clicked", self.runKeyboardSetup)
        self._view.dyndnsButton.connect("clicked", self.runDyndnsSetup)
        self._view.screensaverButton.connect("clicked", self.runScreensaverSetup)
        self._view.datetimeButton.connect("clicked", self.runDateTimeSetup)
        self._view.editorButton.connect("clicked", self.runEditor)
        self._view.backupButton.connect("clicked", self.runBackup)
        self._view.log_button.connect("clicked", self.run_create_log)
        self._view.port_adjustment.connect("value_changed", self.setEfaPort)

    def runTerminal(self, widget):
        try:
            subprocess.Popen(['xterm'])
        except OSError as error:
            message = _("Could not open xterm program: %s") % error
            self._logger.error(message)
            dialogs.show_exception_dialog(self._view, message, traceback.format_exc())

    def runNetworkSettings(self, widget):
        try:
            subprocess.Popen(['sudo', '/usr/bin/nm-connection-editor'])
        except OSError as error:
            message = _("Could not open nm-connection-editor program: %s") % error
            self._logger.error(message)
            dialogs.show_exception_dialog(self._view, message, traceback.format_exc())

    def runFileManager(self, widget):
        try:
            subprocess.Popen(['thunar'])
        except OSError as error:
            message = _("Could not open thunar program: %s") % error
            self._logger.error(message)
            dialogs.show_exception_dialog(self._view, message, traceback.format_exc())

    def runShutdown(self, widget):
        do_shutdown = dialogs.show_confirm_dialog(self._view, _("Really shut down PC ?"))
        if do_shutdown == False:
            return
        try:
            subprocess.Popen(['sudo', '/sbin/shutdown', '-h', 'now'])
        except OSError as error:
            message = _("Could not run /sbin/shutdown program: %s") % error
            self._logger.error(message)
            dialogs.show_exception_dialog(self._view, message, traceback.format_exc())

    def runRestart(self, widget):
        do_reboot = dialogs.show_confirm_dialog(self._view, _("Really reboot PC ?"))
        if do_reboot == False:
            return
        try:
            subprocess.Popen(['sudo', '/sbin/shutdown', '-r', 'now'])
        except OSError as error:
            message = _("Could not run /sbin/shutdown program: %s") % error
            self._logger.error(message)
            dialogs.show_exception_dialog(self._view, message, traceback.format_exc())

    def runScreenSetup(self, widget):
        ScreenSetup(None, confPath=self._model.getConfigPath(), standalone=False)

    def runDeviceManager(self, widget):
        DeviceManager(None, standalone=False)

    def runKeyboardSetup(self, widget):
        try:
            subprocess.Popen(['sudo', 'dpkg-reconfigure', '-fgnome', 'keyboard-configuration'])
        except OSError as error:
            message = _("Could not run keyboard setup: %s") % error
            self._logger.error(message)
            dialogs.show_exception_dialog(self._view, message, traceback.format_exc())

    def runDyndnsSetup(self, widget):
        try:
            subprocess.Popen(['sudo', 'dpkg-reconfigure', '-fgnome', 'ddclient'])
        except OSError as error:
            message = _("Could not run dynamic hostname setup: %s") % error
            self._logger.error(message)
            dialogs.show_exception_dialog(self._view, message, traceback.format_exc())

    def runScreensaverSetup(self, widget):
        try:
            subprocess.Popen(['xscreensaver-demo'])
        except OSError as error:
            message = _("Could not open xscreensaver-demo program: %s") % error
            self._logger.error(message)
            dialogs.show_exception_dialog(self._view, message, traceback.format_exc())

    def runDateTimeSetup(self, widget):
        DateTime(None, standalone=False)

    def runEditor(self, widget):
        try:
            subprocess.Popen(['leafpad'])
        except OSError as error:
            message = _("Could not open leafpad program: %s") % error
            self._logger.error(message)
            dialogs.show_exception_dialog(self._view, message, traceback.format_exc())

    def runBackup(self, widget):
        Backup(None, standalone=False)

    def run_create_log(self, widget):
        try:
            file_chooser = gtk.FileChooserDialog(_("Select directory to store log files"), 
                                                 self._view, 
                                                 gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, 
                                                 (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
            result = file_chooser.run()
            if result == gtk.RESPONSE_OK:
                file_chooser.hide()
                directory = file_chooser.get_filename()
                (returncode, output) = self._model.create_log_package(directory)
                if returncode != 0:
                    message = _("Could not create log file package in %s !") % directory
                    self._logger.error(message)
                    self._logger.debug(output)
                    dialogs.show_exception_dialog(self._view, message, output)
                else:
                    message = _("Created log file package in %s .") % directory
                    self._logger.info(message)
                    self._logger.debug(output)
                    dialogs.show_output_dialog(self._view, message, output)

        except OSError as error:
            message = "Could not create log file package: %s" % error
            dialogs.show_exception_dialog(self._view, message, traceback.format_exc())
        finally:
            file_chooser.destroy()

    def setEfaShutdownAction(self, widget):
        action_string = ""
        action = widget.get_active()
        if action == 0:
            action_string = "\"shutdown\""
        elif action == 1:
            action_string = "\"restart\""
        elif action == 2:
            action_string = "\"start_efa\""
        elif action == 3:
            action_string = "\"stop_efa\""
        self._model.setEfaShutdownAction(action_string)

    def setAutoUsbBackup(self, widget):
        self._model.enableAutoUsbBackup(widget.get_active())

    def setAutoUsbBackupDialog(self, widget):
        self._model.enableAutoUsbBackupDialog(widget.get_active())

    def setAutoBackupUsePassword(self, widget):
        self._model.enableAutoBackupPassword(widget.get_active())

    def setAutoBackupPassword(self, widget):
        self._model.setAutoBackupPassword(widget.get_text())

    def setEfaPort(self, widget):
        self._model.setEfaPort(widget.get_value())

    def save(self, widget):
        try:
            self._model.save()
            self.destroy(widget)
        except:
            message = _("Could not save files!\n\n") \
                    + _("Please check the path you provided for ") \
                    + _("user rights and existance.")
            self._logger.error(message)
            dialogs.show_exception_dialog(self._view, message, traceback.format_exc())

