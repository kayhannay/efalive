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
from screen.screensetup import ScreenSetupController as ScreenSetup
from dttime.datetime import DateTimeController as DateTime

APP="SystemTab"
gettext.install(APP, common.LOCALEDIR, unicode=True)

class SystemTabModel(object):
    def __init__(self, settings):
        self._logger = logging.getLogger('SystemTabModel')
        self._settings = settings

    def getConfigPath(self):
        return self._settings.confPath

class SystemTabView(gtk.VBox):
    def __init__(self):
        super(gtk.VBox, self).__init__()
        self._logger = logging.getLogger('SystemTabView')
        self._init_components()

    def _init_components(self):
        self.systemGrid=gtk.Table(3, 3, True)
        self.pack_start(self.systemGrid, False, False, 5)
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

        self.powerManagerButton=gtk.Button(_("Power manager"))
        self.systemGrid.attach(self.powerManagerButton, 1, 2, 1, 2)
        self.powerManagerButton.show()

        self.datetimeButton=gtk.Button(_("Date & time"))
        self.systemGrid.attach(self.datetimeButton, 2, 3, 1, 2)
        self.datetimeButton.show()

        self.keyboardButton=gtk.Button(_("Keyboard"))
        self.systemGrid.attach(self.keyboardButton, 0, 1, 2, 3)
        self.keyboardButton.show()

class SystemTabController(object):
    def __init__(self, settings):
        self._logger = logging.getLogger('SystemTabController')
        
        self._view = SystemTabView()
        
        self._model = SystemTabModel(settings)
        self._init_events()

    def _init_events(self):
        self._view.screenButton.connect("clicked", self.runScreenSetup)
        self._view.networkButton.connect("clicked", self.runNetworkSettings)
        self._view.keyboardButton.connect("clicked", self.runKeyboardSetup)
        self._view.dyndnsButton.connect("clicked", self.runDyndnsSetup)
        self._view.screensaverButton.connect("clicked", self.runScreensaverSetup)
        self._view.powerManagerButton.connect("clicked", self.runPowerManagerSetup)
        self._view.datetimeButton.connect("clicked", self.runDateTimeSetup)

    def get_view(self):
        return self._view

    def runNetworkSettings(self, widget):
        try:
            subprocess.Popen(['sudo', '/usr/bin/nm-connection-editor'])
        except OSError as error:
            message = _("Could not open nm-connection-editor program: %s") % error
            self._logger.error(message)
            dialogs.show_exception_dialog(self._view.get_toplevel(), message, traceback.format_exc())

    def runScreenSetup(self, widget):
        ScreenSetup(None, confPath=self._model.getConfigPath(), standalone=False)

    def runKeyboardSetup(self, widget):
        try:
            subprocess.Popen(['sudo', 'dpkg-reconfigure', '-fgnome', 'keyboard-configuration'])
        except OSError as error:
            message = _("Could not run keyboard setup: %s") % error
            self._logger.error(message)
            dialogs.show_exception_dialog(self._view.get_toplevel(), message, traceback.format_exc())

    def runDyndnsSetup(self, widget):
        try:
            subprocess.Popen(['sudo', 'dpkg-reconfigure', '-fgnome', 'ddclient'])
        except OSError as error:
            message = _("Could not run dynamic hostname setup: %s") % error
            self._logger.error(message)
            dialogs.show_exception_dialog(self._view.get_toplevel(), message, traceback.format_exc())

    def runScreensaverSetup(self, widget):
        try:
            subprocess.Popen(['xscreensaver-demo'])
        except OSError as error:
            message = _("Could not open xscreensaver-demo program: %s") % error
            self._logger.error(message)
            dialogs.show_exception_dialog(self._view.get_toplevel(), message, traceback.format_exc())

    def runPowerManagerSetup(self, widget):
        try:
            subprocess.Popen(['xfce4-power-manager-settings'])
        except OSError as error:
            message = _("Could not open xfce4-power-manager-settings program: %s") % error
            self._logger.error(message)
            dialogs.show_exception_dialog(self._view.get_toplevel(), message, traceback.format_exc())

    def runDateTimeSetup(self, widget):
        DateTime(None, standalone=False)

