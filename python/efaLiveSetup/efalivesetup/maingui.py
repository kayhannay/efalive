'''
Created on 26.08.2010

Copyright (C) 2010 Kay Hannay

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

from observable import Observable

import locale
import gettext
APP="efaLiveSetup"
DIR="locale"
gettext.install(APP, DIR, unicode=True)
#locale.setlocale(locale.LC_ALL, '')
#gettext.bindtextdomain(APP, DIR)
#gettext.textdomain(APP)
#_ = gettext.gettext

#def getText(text):
#    return gettext.gettext(text).decode('iso8859-1')
#_ = getText

class SetupModel(object):
    def __init__(self, confPath):
        self._confPath=confPath
        self._versionFileName = os.path.join(self._confPath, "version.conf")
        self.efaVersion=Observable()

    def initModel(self):
        self.efaVersion.updateData(1)
        if os.path.isfile("version.conf"):
            self.versionFile=open(self._versionFileName, "r")
            self.parseVersionFile(self.versionFile)
            self.versionFile.close()

    def parseVersionFile(self, file):
        for line in file:
            if line.startswith("EFA_VERSION="):
                versionStr=line[(line.index('=') + 1):]
                self.setEfaVersion(int(versionStr))
                print("Read file: " + versionStr)

    def save(self):
        print("Saving file")
        versionFile=open(self._versionFileName, "w")
        versionFile.write("EFA_VERSION=%d\n" % self.efaVersion._data)
        versionFile.close()

    def setEfaVersion(self, version):
        self.efaVersion.updateData(version)
        print("EFA version: %d" % version)


class SetupView(gtk.Window):
    def __init__(self, type):
        gtk.Window.__init__(self, type)
        self.set_title(_("efaLive setup"))
        self.set_border_width(5)

        self.initComponents()

    def initComponents(self):
        self.mainBox=gtk.VBox(False, 2)
        self.add(self.mainBox)
        self.mainBox.show()

        self.versionFrame=gtk.Frame(_("efa version"))
        self.mainBox.pack_start(self.versionFrame, True, False, 2)
        self.versionFrame.show()

        self.versionSpaceBox=gtk.HBox(False, 5)
        self.versionFrame.add(self.versionSpaceBox)
        self.versionSpaceBox.show()

        self.versionVBox=gtk.VBox(False, 5)
        self.versionSpaceBox.pack_start(self.versionVBox, True, True, 10)
        self.versionVBox.show()

        self.versionDesc=gtk.Label(_("Here you can choose the efa version that ")
            + _("you would like to use. Please note that efa 2 is a development ")
            + _("version, which might me unstable. If you need a stable version, ")
            + _("choose efa 1."))
        self.versionDesc.set_line_wrap(True)
        self.versionVBox.pack_start(self.versionDesc, True, True, 5)
        self.versionDesc.show()
        
        self.versionHBox=gtk.HBox(False, 5)
        self.versionVBox.pack_start(self.versionHBox, True, True, 10)
        self.versionHBox.show()

        self.versionLabel=gtk.Label(_("version"))
        self.versionHBox.pack_start(self.versionLabel, True, True, 2)
        self.versionLabel.show()

        self.versionCombo=gtk.combo_box_new_text()
        self.versionHBox.pack_start(self.versionCombo, True, True, 2)
        self.versionCombo.show()

        self.buttonBox=gtk.HBox(False, 0)
        self.mainBox.pack_start(self.buttonBox, False, False, 2)
        self.buttonBox.show()

        self.cancelButton=gtk.Button(_("Cancel"))
        self.buttonBox.pack_end(self.cancelButton, False, False, 2)
        self.cancelButton.show()
        
        self.okButton=gtk.Button(_("Ok"))
        self.buttonBox.pack_end(self.okButton, False, False, 2)
        self.okButton.show()


class SetupController(object):
    def __init__(self, argv, model=None, view=None):
        if(len(argv) < 2):
            raise(BaseException("No arguments given"))
        confPath=argv[1]
        if(model==None):
            self._model=SetupModel(confPath)
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

        self._view.versionCombo.append_text(_("1 (stable)"))
        self._view.versionCombo.append_text(_("2 (development)"))

        self._model.efaVersion.registerObserverCb(self.efaVersionChanged)
        self._model.initModel()

    def efaVersionChanged(self, version):
        index=0
        if(version==1):
            index=0
        elif(version==2):
            index=1
        self._view.versionCombo.set_active(index)

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def close(self, widget, event, data=None):
        print("Currently we have no implementation for quit.")
        return False

    def initEvents(self):
        self._view.cancelButton.connect("clicked", self.destroy, None)
        self._view.okButton.connect("clicked", self.saveAndClose, None)
        self._view.versionCombo.connect("changed", self.setEfaVersion)

    def setEfaVersion(self, widget):
        self._model.setEfaVersion(widget.get_active() + 1)

    def saveAndClose(self, widget, data=None):
        self._model.save()
        self.destroy(None)

if __name__ == '__main__':
    controller = SetupController(sys.argv)
    gtk.main();
