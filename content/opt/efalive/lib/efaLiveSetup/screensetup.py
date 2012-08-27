#!/usr/bin/python
'''
Created on 09.06.2011

Copyright (C) 2011 Kay Hannay

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
from screenlayout import widget
import os
import sys 

import dialogs

import locale
import gettext
APP="screenSetup"
LOCALEDIR=os.path.join(os.path.dirname(sys.argv[0]), "locale")
DIR=os.path.realpath(LOCALEDIR)
gettext.install(APP, DIR, unicode=True)

import logging

class ScreenSetupModel(object):
    def __init__(self):
        self._logger = logging.getLogger('screensetup.ScreenSetupModel')

class ScreenSetupView(gtk.Window):
    def __init__(self, type, controller=None):
        self._logger = logging.getLogger('screensetup.ScreenSetupView')
        gtk.Window.__init__(self, type)
        self.set_title(_("Screen setup"))
        self.set_border_width(5)
        self._controller = controller

        self.initComponents()

    def initComponents(self):
        main_box=gtk.VBox(False, 2)
        self.add(main_box)
        main_box.show()

        self.randr_widget = widget.ARandRWidget()
        self.randr_widget.load_from_x()
        main_box.pack_start(self.randr_widget, True, True, 2)
        self.randr_widget.show()
        
        button_box = gtk.HBox(False, 2)
        main_box.pack_end(button_box, False, False)
        button_box.show()

        save_button = gtk.Button(_("Ok"))
        button_box.pack_end(save_button, False, False, 2)
        save_button.show()
        save_button.connect("clicked", self._controller.save)

        apply_button = gtk.Button(_("Apply"))
        button_box.pack_end(apply_button, False, False, 2)
        apply_button.show()
        apply_button.connect("clicked", self._controller.apply)

        cancel_button = gtk.Button(_("Cancel"))
        button_box.pack_end(cancel_button, False, False, 2)
        cancel_button.show()
        cancel_button.connect("clicked", self._controller.cancel)

class ScreenSetupController(object):
    def __init__(self, argv, model=None, view=None, standalone=True, confPath=None):
        self._logger = logging.getLogger('screensetup.ScreenSetupController')
        if argv and (len(argv) > 1):
            confPath=argv[1]
        self._confPath = confPath
        if(model==None):
            self._model=ScreenSetupModel()
        else:
            self._model=model
        if(view==None):
            self._view=ScreenSetupView(gtk.WINDOW_TOPLEVEL, self)
        else:
            self._view=view
        self.init_events(standalone)
        self._view.show()
        
    def init_events(self, standalone):
        if standalone:
            self._view.connect('destroy', gtk.main_quit)

    def save(self, widget):
        script_file = 'screen_setup.sh'
        if self._confPath:
            script_file = os.path.join(self._confPath, script_file)
        self._view.randr_widget.save_to_file(script_file)
        self._view.randr_widget.save_to_x()
        self._view.destroy()

    def apply(self, widget):
        self._view.randr_widget.save_to_x()

    def cancel(self, widget):
        self._view.destroy()

if __name__ == '__main__':
    logging.basicConfig(filename='screenSetup.log',level=logging.INFO)
    controller = ScreenSetupController(sys.argv)
    gtk.main();

    

