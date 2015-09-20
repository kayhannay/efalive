'''
Created on 26.08.2010

Copyright (C) 2010-2015 Kay Hannay

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
import traceback
import logging
import gettext

from setupcommon import dialogs
from ..common import common
from ..common.settings import EfaLiveSettings
from efalive.setup.efasettingstab import EfaSettingsTabController
from efalive.setup.actionstab import ActionsTabController
from efalive.setup.backuptab import BackupTabController
from efalive.setup.toolstab import ToolsTabController
from efalive.setup.systemtab import SystemTabController

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


class SetupView(gtk.Window):
    def __init__(self, type):
        self._logger = logging.getLogger('efalivesetup.maingui.SetupView')
        gtk.Window.__init__(self, type)
        self.set_title(_("efaLive setup"))
        self.set_border_width(5)

        self.initComponents()

    def add_tab(self, label, component):
        tab_label = gtk.Label(_(label))
        self.tabpanel.append_page(component, tab_label)
        component.show()
        
    def initComponents(self):
        
        self.mainBox=gtk.VBox(False, 2)
        self.add(self.mainBox)
        self.mainBox.show()

        self.tabpanel = gtk.Notebook()
        self.mainBox.pack_start(self.tabpanel, True, True, 2)
        self.tabpanel.show()

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
        
        self.settings_gui_controller = EfaSettingsTabController(self._model._settings)
        self._view.add_tab(_("Settings"), self.settings_gui_controller.get_view())
        
        self.actions_gui_controller = ActionsTabController()
        self._view.add_tab(_("Actions"), self.actions_gui_controller.get_view())
        
        self.backup_tab_controller = BackupTabController(self._model._settings)
        self._view.add_tab(_("Backup"), self.backup_tab_controller.get_view())
        
        self.tools_tab_controller = ToolsTabController()
        self._view.add_tab(_("Tools"), self.tools_tab_controller.get_view())
        
        self.system_tab_controller = SystemTabController(self._model._settings)
        self._view.add_tab(_("System"), self.system_tab_controller.get_view())
        
        self.initEvents()
        self._view.connect("destroy", self.destroy)
        self._view.show()
        self._model.initModel()

    def destroy(self, widget):
        gtk.main_quit()

    def initEvents(self):
        self._logger.debug("Initialize events")
        self._view.closeButton.connect("clicked", self.destroy)
        self._view.okButton.connect("clicked", self.save)

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

