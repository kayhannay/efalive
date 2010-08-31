'''
Created on 26.08.2010

Copyright (C) 2010 Kay Hannay

This file is part of efaLiveSetup.

efaLiveSetup is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
pyTimeSheet is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyTimeSheet.  If not, see <http://www.gnu.org/licenses/>.
'''
from SetupView import SetupView
from SetupModel import SetupModel

import pygtk
pygtk.require('2.0')
import gtk

class SetupController(object):
    def __init__(self, model=None, view=None):
        if(model==None):
            self._model=SetupModel()
        else:
            self._model=model
        if(view==None):
            self._view=SetupView(gtk.WINDOW_TOPLEVEL)
        else:
            self._view=view

        self.initEvents()
        self._view.connect("destroy", self.destroy)
        self._view.connect("delete_event", self.close)
        self._view.show()

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def close(self, widget, event, data=None):
        print("Currently we have no implementation for quit.")
        return False

    def initEvents(self):
        self._view.cancelButton.connect("clicked", self.destroy, None)
        self._view.okButton.connect("clicked", self.saveAndClose, None)

    def saveAndClose(self, widget, data=None):
        self.destroy(None)
