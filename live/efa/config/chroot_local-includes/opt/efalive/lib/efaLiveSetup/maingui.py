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
import subprocess

from observable import Observable

import locale
import gettext
APP="efaLiveSetup"
LOCALEDIR=os.path.join(os.path.dirname(sys.argv[0]), "locale")
DIR=os.path.realpath(LOCALEDIR)
gettext.install(APP, DIR, unicode=True)

import logging
LOG_FILENAME = 'efaLiveSetup.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)

class SetupModel(object):
    def __init__(self, confPath):
        self._logger = logging.getLogger('efalivesetup.maingui.SetupModel')
        self._checkPath(confPath)
        self._confPath=confPath
        self._versionFileName = os.path.join(self._confPath, "version.conf")
        self._backupFileName = os.path.join(self._confPath, "backup.conf")
        self.efaVersion=Observable()
        self.efaBackupPaths=None

    def initModel(self):
        self.efaVersion.updateData(1)
        if os.path.isfile("version.conf"):
            self.versionFile=open(self._versionFileName, "r")
            self.parseVersionFile(self.versionFile)
            self.versionFile.close()

    def _checkPath(self, path):
        if not os.path.exists(path):
            self._logger.debug("Creating directory: %s" % path)
            os.makedirs(path, 0755)

    def parseVersionFile(self, file):
        for line in file:
            if line.startswith("EFA_VERSION="):
                versionStr=line[(line.index('=') + 1):]
                self.setEfaVersion(int(versionStr))
                self._logger.debug("Read version file: " + versionStr)

    def save(self):
        self._logger.debug("Saving files: %s, %s" % (self._versionFileName, self._backupFileName))
        try:
            versionFile=open(self._versionFileName, "w")
            versionFile.write("EFA_VERSION=%d\n" % self.efaVersion._data)
            versionFile.close()
            backupFile=open(self._backupFileName, "w")
            backupFile.write("EFA_BACKUP_PATHS=\"%s\"\n" % self.efaBackupPaths)
            backupFile.close()
        except IOError, exception:
            self._logger.error("Could not save files: %s" % exception)
            raise Exception("Could not save files")

    def setEfaVersion(self, version):
        self.efaVersion.updateData(version)
        if version == 1:
            self.efaBackupPaths = "/opt/efa/daten /home/efa/efa"
        elif version == 2:
            self.efaBackupPaths = "/opt/efa2/data /home/efa/efa2"
        else:
            self._logger.error("Undefined version received: %d" % version)
        self._logger.debug("EFA version: %d" % version)


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

        # version box
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

        # tools box
        self.toolsFrame=gtk.Frame(_("Tools"))
        self.mainBox.pack_start(self.toolsFrame, True, False, 2)
        self.toolsFrame.show()

        self.toolsSpaceBox=gtk.HBox(False, 5)
        self.toolsFrame.add(self.toolsSpaceBox)
        self.toolsSpaceBox.show()

        self.toolsVBox=gtk.VBox(False, 5)
        self.toolsSpaceBox.pack_start(self.toolsVBox, False, False, 10)
        self.toolsVBox.show()

        self.terminalButton=gtk.Button(_("Terminal"))
        self.toolsVBox.pack_start(self.terminalButton, False, False, 10)
        self.terminalButton.show()
        
        # button box
        self.buttonBox=gtk.HBox(False, 0)
        self.mainBox.pack_start(self.buttonBox, False, False, 2)
        self.buttonBox.show()

        self.closeButton=gtk.Button(_("Close"))
        self.buttonBox.pack_end(self.closeButton, False, False, 2)
        self.closeButton.show()
        
        self.applyButton=gtk.Button(_("Apply"))
        self.buttonBox.pack_end(self.applyButton, False, False, 2)
        self.applyButton.show()

    def showError(self, text):
        """
        This Function is used to show an error dialog when
        an error occurs.
        error_string - The error string that will be displayed
        on the dialog.
        """
        errorDialog = gtk.MessageDialog(type=gtk.MESSAGE_ERROR
            , message_format=text
            , buttons=gtk.BUTTONS_OK)
        errorDialog.run()
        errorDialog.destroy()


class SetupController(object):
    def __init__(self, argv, model=None, view=None):
        self._logger = logging.getLogger('efalivesetup.maingui.SetupController')
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

    def destroy(self, widget):
        gtk.main_quit()

    def initEvents(self):
        self._view.closeButton.connect("clicked", self.destroy)
        self._view.applyButton.connect("clicked", self.save)
        self._view.versionCombo.connect("changed", self.setEfaVersion)
        self._view.terminalButton.connect("clicked", self.runTerminal)

    def runTerminal(self, widget):
        subprocess.Popen(['xterm'])

    def setEfaVersion(self, widget):
        self._model.setEfaVersion(widget.get_active() + 1)

    def save(self, widget):
        try:
            self._model.save()
        except:
            self._view.showError(_("Could not save files!\n\n")
                + _("Please check the path you provided for ")
                + _("user rights and existance."))

if __name__ == '__main__':
    controller = SetupController(sys.argv)
    gtk.main();

