'''
Created on 20.09.2015

Copyright (C) 2015-2015 Kay Hannay

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
import subprocess
import traceback

from ..common import common
from setupcommon import dialogs
from devicemanager.devicemanager import DeviceManagerController as DeviceManager
from backup.backup import BackupController as Backup

APP="ToolsTab"
gettext.install(APP, common.LOCALEDIR, unicode=True)

class ToolsTabModel(object):
    def __init__(self):
        self._logger = logging.getLogger('ToolsTabModel')

    def create_log_package(self, path):
        return common.command_output(["/usr/lib/efalive/bin/create_log_package.sh", path])

class ToolsTabView(gtk.VBox):
    def __init__(self):
        super(gtk.VBox, self).__init__()
        self._logger = logging.getLogger('ToolsTabView')
        self._init_components()

    def _init_components(self):
        self.toolsGrid=gtk.Table(2, 3, True)
        self.pack_start(self.toolsGrid, False, False, 5)
        self.toolsGrid.set_row_spacings(2)
        self.toolsGrid.set_col_spacings(2)
        self.toolsGrid.show()

        self.terminalButton=gtk.Button()
        button_vbox = common.get_button_label("terminal.png", _("Terminal"))
        self.terminalButton.add(button_vbox)
        self.toolsGrid.attach(self.terminalButton, 0, 1, 0, 1)
        self.terminalButton.show()

        self.fileManagerButton=gtk.Button()
        button_vbox = common.get_button_label("file-manager.png", _("File manager"))
        self.fileManagerButton.add(button_vbox)
        self.toolsGrid.attach(self.fileManagerButton, 1, 2, 0, 1)
        self.fileManagerButton.show()

        self.deviceButton=gtk.Button()
        button_vbox = common.get_button_label("devices.png", _("Devices"))
        self.deviceButton.add(button_vbox)
        self.toolsGrid.attach(self.deviceButton, 2, 3, 0, 1)
        self.deviceButton.show()

        self.editorButton=gtk.Button()
        button_vbox = common.get_button_label("editor.png", _("Editor"))
        self.editorButton.add(button_vbox)
        self.toolsGrid.attach(self.editorButton, 0, 1, 1, 2)
        self.editorButton.show()

        self.backupButton=gtk.Button()
        button_vbox = common.get_button_label("backup_tape.png", _("Backup"))
        self.backupButton.add(button_vbox)
        self.toolsGrid.attach(self.backupButton, 1, 2, 1, 2)
        self.backupButton.show()

        self.log_button=gtk.Button()
        button_vbox = common.get_button_label("logfiles.png", _("Logs"))
        self.log_button.add(button_vbox)
        self.toolsGrid.attach(self.log_button, 2, 3, 1, 2)
        self.log_button.show()

class ToolsTabController(object):
    def __init__(self):
        self._logger = logging.getLogger('ToolsTabController')
        
        self._view = ToolsTabView()
        
        self._model = ToolsTabModel()
        self._init_events()

    def _init_events(self):
        self._view.terminalButton.connect("clicked", self.runTerminal)
        self._view.deviceButton.connect("clicked", self.runDeviceManager)
        self._view.fileManagerButton.connect("clicked", self.runFileManager)
        self._view.editorButton.connect("clicked", self.runEditor)
        self._view.backupButton.connect("clicked", self.runBackup)
        self._view.log_button.connect("clicked", self.run_create_log)

    def get_view(self):
        return self._view

    def runTerminal(self, widget):
        try:
            subprocess.Popen(['xterm'])
        except OSError as error:
            message = _("Could not open xterm program: %s") % error
            self._logger.error(message)
            dialogs.show_exception_dialog(self._view.get_toplevel(), message, traceback.format_exc())

    def runFileManager(self, widget):
        try:
            subprocess.Popen(['thunar'])
        except OSError as error:
            message = _("Could not open thunar program: %s") % error
            self._logger.error(message)
            dialogs.show_exception_dialog(self._view.get_toplevel(), message, traceback.format_exc())

    def runDeviceManager(self, widget):
        DeviceManager(None, standalone=False)

    def runEditor(self, widget):
        try:
            subprocess.Popen(['leafpad'])
        except OSError as error:
            message = _("Could not open leafpad program: %s") % error
            self._logger.error(message)
            dialogs.show_exception_dialog(self._view.get_toplevel(), message, traceback.format_exc())

    def runBackup(self, widget):
        Backup(None, standalone=False)

    def run_create_log(self, widget):
        try:
            file_chooser = gtk.FileChooserDialog(_("Select directory to store log files"), 
                                                 self._view.get_toplevel(), 
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
                    dialogs.show_exception_dialog(self._view.get_toplevel(), message, output)
                else:
                    message = _("Created log file package in %s .") % directory
                    self._logger.info(message)
                    self._logger.debug(output)
                    dialogs.show_output_dialog(self._view.get_toplevel(), message, output)

        except OSError as error:
            message = "Could not create log file package: %s" % error
            dialogs.show_exception_dialog(self._view.get_toplevel(), message, traceback.format_exc())
        finally:
            file_chooser.destroy()

