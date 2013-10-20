#!/usr/bin/python
'''
Created on 10.01.2012

Copyright (C) 2012-2013 Kay Hannay

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
import gtk
import os
import sys 
import subprocess
import traceback

import dialogs
import common

import locale
import gettext
APP="backup"
LOCALEDIR=os.path.join(os.path.dirname(sys.argv[0]), "locale")
DIR=os.path.realpath(LOCALEDIR)
gettext.install(APP, DIR, unicode=True)

import logging

class BackupModel(object):
    def __init__(self):
        self._logger = logging.getLogger('backup.BackupModel')

    def create_backup(self, path):
        return common.command_output(["/usr/bin/efalive-backup", path])

    def restore_backup(self, file):
        return common.command_output(["/usr/bin/efalive-restore", file])


class BackupView(gtk.Window):
    def __init__(self, type, controller=None):
        self._logger = logging.getLogger('backup.BackupView')
        gtk.Window.__init__(self, type)
        self.set_title(_("Backup & Restore"))
        self.set_border_width(5)
        self._controller = controller

        self.initComponents()

    def initComponents(self):
        main_box=gtk.VBox(False, 2)
        self.add(main_box)
        main_box.show()

        backup_button = gtk.Button(_("Backup"))
        backup_button.set_size_request(150, -1)
        backup_icon = gtk.image_new_from_file(common.get_icon_path("backup.png"))
        backup_button.set_image(backup_icon)
        main_box.pack_start(backup_button, False, False, 2)
        backup_button.show()
        backup_icon.show()
        backup_button.connect("clicked", self._controller.start_backup)

        restore_button = gtk.Button(_("Restore"))
        restore_button.set_size_request(150, -1)
        restore_icon = gtk.image_new_from_file(common.get_icon_path("restore.png"))
        restore_button.set_image(restore_icon)
        main_box.pack_start(restore_button, False, False, 2)
        restore_button.show()
        restore_icon.show()
        restore_button.connect("clicked", self._controller.start_restore)

        button_box = gtk.HBox(False, 2)
        main_box.pack_end(button_box, False, False)
        button_box.show()

        close_button = gtk.Button(_("Close"))
        button_box.pack_end(close_button, False, False, 2)
        close_button.show()
        close_button.connect("clicked", self._controller.close)

class BackupController(object):
    def __init__(self, argv, model=None, view=None, standalone=True, confPath=None):
        self._logger = logging.getLogger('backup.BackupController')
        if argv and (len(argv) > 1):
            confPath=argv[1]
        self._confPath = confPath
        if(model==None):
            self._model=BackupModel()
        else:
            self._model=model
        if(view==None):
            self._view=BackupView(gtk.WINDOW_TOPLEVEL, self)
        else:
            self._view=view
        self.init_events(standalone)
        self._view.show()
        
    def init_events(self, standalone):
        if standalone:
            self._view.connect('destroy', gtk.main_quit)

    def start_backup(self, widget):
        try:
            file_chooser = gtk.FileChooserDialog(_("Select directory"), 
                                                 self._view, 
                                                 gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, 
                                                 (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
            result = file_chooser.run()
            if result == gtk.RESPONSE_OK:
                file_chooser.hide()
                directory = file_chooser.get_filename()
                (returncode, output) = self._model.create_backup(directory)
                if returncode != 0:
                    if returncode == 1 or returncode == 5:
                        message = _("Backup failed! Please check that the efalive user is configured correctly in efa.")
                        self._logger.error(message)
                        self._logger.debug(output)
                        dialogs.show_exception_dialog(self._view, message, output)
                    else:
                        message = _("Backup to %s failed!") % directory
                        self._logger.error(message)
                        self._logger.debug(output)
                        dialogs.show_exception_dialog(self._view, message, output)
                else:
                    message = _("Backup to %s finished.") % directory
                    self._logger.info(message)
                    self._logger.debug(output)
                    dialogs.show_output_dialog(self._view, message, output)

        except OSError as error:
            message = "Could not create backup: %s" % error
            dialogs.show_exception_dialog(self._view, message, traceback.format_exc())
        finally:
            file_chooser.destroy()

    def start_restore(self, widget):
        try:
            file_chooser = gtk.FileChooserDialog(_("Select backup"), 
                                                 self._view, 
                                                 gtk.FILE_CHOOSER_ACTION_OPEN, 
                                                 (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
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
        except OSError as error:
            message = "Could not restore backup: %s" % error
            self._logger.error(message)
            dialogs.show_exception_dialog(self._view, message, traceback.format_exc())
        finally:
            file_chooser.destroy()


    def close(self, widget):
        self._view.destroy()

if __name__ == '__main__':
    logging.basicConfig(filename='screenSetup.log',level=logging.INFO)
    controller = BackupController(sys.argv)
    gtk.main();

    

