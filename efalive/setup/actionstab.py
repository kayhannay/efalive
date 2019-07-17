'''
Created on 19.09.2015

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
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import logging
import subprocess
import traceback

from ..common import common
from ..common.i18n import _
from efalive.setup.setupcommon import dialogs

class ActionsTabView(Gtk.VBox):
    def __init__(self):
        super(Gtk.VBox, self).__init__()
        self._logger = logging.getLogger('ActionsTabView')
        self._init_components()

    def _init_components(self):
        self.actionsGrid=Gtk.Table(1, 3, True)
        self.pack_start(self.actionsGrid, False, False, 5)
        self.actionsGrid.set_row_spacings(2)
        self.actionsGrid.set_col_spacings(2)
        self.actionsGrid.show()

        self.shutdownButton=Gtk.Button()
        button_vbox = common.get_button_label("power.png", _("Shutdown PC"))
        self.shutdownButton.add(button_vbox)
        self.actionsGrid.attach(self.shutdownButton, 0, 1, 0, 1)
        self.shutdownButton.show()

        self.restartButton=Gtk.Button()
        button_vbox = common.get_button_label("restart.png", _("Restart PC"))
        self.restartButton.add(button_vbox)
        self.actionsGrid.attach(self.restartButton, 1, 2, 0, 1)
        self.restartButton.show()

        self.actionsDummy=Gtk.Label()
        self.actionsGrid.attach(self.actionsDummy, 2, 3, 0, 1)
        self.actionsDummy.show()

class ActionsTabController(object):
    def __init__(self):
        self._logger = logging.getLogger('ActionsTabController')
        
        self._view = ActionsTabView()
        
        self._init_events()

    def _init_events(self):
        self._view.shutdownButton.connect("clicked", self.runShutdown)
        self._view.restartButton.connect("clicked", self.runRestart)

    def get_view(self):
        return self._view

    def runShutdown(self, widget):
        do_shutdown = dialogs.show_confirm_dialog(self._view.get_toplevel(), _("Really shut down PC ?"))
        if do_shutdown == False:
            return
        try:
            subprocess.Popen(['sudo', '/sbin/shutdown', '-h', 'now'])
        except OSError as error:
            message = _("Could not run /sbin/shutdown program: %s") % error
            self._logger.error(message)
            dialogs.show_exception_dialog(self._view.get_toplevel(), message, traceback.format_exc())

    def runRestart(self, widget):
        do_reboot = dialogs.show_confirm_dialog(self._view.get_toplevel(), _("Really reboot PC ?"))
        if do_reboot == False:
            return
        try:
            subprocess.Popen(['sudo', '/sbin/shutdown', '-r', 'now'])
        except OSError as error:
            message = _("Could not run /sbin/shutdown program: %s") % error
            self._logger.error(message)
            dialogs.show_exception_dialog(self._view.get_toplevel(), message, traceback.format_exc())

