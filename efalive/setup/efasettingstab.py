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
import gettext

from efalive.common import common

APP="EfaSettingsTab"
gettext.install(APP, common.LOCALEDIR)

class EfaSettingsTabModel(object):
    def __init__(self, settings):
        self._logger = logging.getLogger('EfaSettingsTabModel')
        self._settings = settings

    def setEfaShutdownAction(self, action):
        self._settings.efaShutdownAction.updateData(action)
        self._logger.debug("efa shutdown action: %s" % action)

    def setEfaPort(self, port):
        self._settings.efaPort.updateData(port)
        self._logger.debug("efa port: %d" % port)

    def registerEfaShutdownActionCb(self, callback):
        self._settings.efaShutdownAction.registerObserverCb(callback)

    def registerEfaPortCb(self, callback):
        self._settings.efaPort.registerObserverCb(callback)

class EfaSettingsTabView(Gtk.VBox):
    def __init__(self):
        super(Gtk.VBox, self).__init__()
        self._logger = logging.getLogger('EfaSettingsTabView')
        self._init_components()

    def _init_components(self):
        # efa port field
        self.portVBox=Gtk.VBox(False, 0)
        self.pack_start(self.portVBox, False, False, 5)
        self.portVBox.show()

        self.portHBox=Gtk.HBox(False, 5)
        self.portVBox.pack_start(self.portHBox, True, True, 2)
        self.portHBox.show()

        self.portLabel=Gtk.Label(_("efa network port"))
        self.portHBox.pack_start(self.portLabel, False, False, 5)
        self.portLabel.show()

        self.port_adjustment = Gtk.Adjustment(0, 0, 65565, 1, 1000)
        self.port_button = Gtk.SpinButton()
        self.port_button.set_adjustment(self.port_adjustment)
        self.port_button.set_wrap(True)
        self.portHBox.pack_end(self.port_button, False, False, 2)
        self.port_button.show()

        # shutdown box
        self.shutdownVBox=Gtk.VBox(False, 0)
        self.pack_start(self.shutdownVBox, False, False, 2)
        self.shutdownVBox.show()

        self.shutdownHBox=Gtk.HBox(False, 5)
        self.shutdownVBox.pack_start(self.shutdownHBox, True, True, 2)
        self.shutdownHBox.show()

        self.shutdownLabel=Gtk.Label(_("efa shutdown action"))
        self.shutdownHBox.pack_start(self.shutdownLabel, False, False, 5)
        self.shutdownLabel.show()

        self.shutdownCombo=Gtk.ComboBoxText()
        self.shutdownHBox.pack_end(self.shutdownCombo, False, False, 2)
        self.shutdownCombo.show()
        
class EfaSettingsTabController(object):
    def __init__(self, settings):
        self._logger = logging.getLogger('EfaSettingsTabController')
        
        self._view = EfaSettingsTabView()
        self._view.shutdownCombo.append_text(_("shutdown pc"))
        self._view.shutdownCombo.append_text(_("restart pc"))
        self._view.shutdownCombo.append_text(_("restart efa"))
        self._view.shutdownCombo.append_text(_("stop efa"))

        self._model = EfaSettingsTabModel(settings)
        self._model.registerEfaShutdownActionCb(self.efaShutdownActionChanged)
        self._model.registerEfaPortCb(self.efaPortChanged)
        self._init_events()

    def _init_events(self):
        self._view.shutdownCombo.connect("changed", self.setEfaShutdownAction)
        self._view.port_adjustment.connect("value_changed", self.setEfaPort)

    def get_view(self):
        return self._view

    def efaPortChanged(self, port):
        self._view.port_button.set_value(port)

    def efaShutdownActionChanged(self, action):
        index=0
        if(action == "\"shutdown\""):
            index = 0
        elif(action == "\"restart\""):
            index = 1
        elif(action == "\"start_efa\""):
            index = 2
        elif(action == "\"stop_efa\""):
            index = 3
        self._view.shutdownCombo.set_active(index)

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

    def setEfaPort(self, widget):
        self._model.setEfaPort(widget.get_value())


