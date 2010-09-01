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

import locale
import gettext
APP="efaLiveSetup"
DIR="locale"
locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)
_ = gettext.gettext


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
        self.versionSpaceBox.pack_start(self.versionVBox, False, False, 10)
        self.versionVBox.show()

        self.versionDesc=gtk.Label(_("Here you can choose the efa version that "
            + "you would like to use. Please note that efa 2 is a development "
            + "version, which might me unstable. If you need a stable version, "
            + "choose efa 1."))
        self.versionDesc.set_line_wrap(True)
        self.versionVBox.pack_start(self.versionDesc, False, False, 5)
        self.versionDesc.show()
        
        self.versionHBox=gtk.HBox(False, 5)
        self.versionVBox.pack_start(self.versionHBox, False, False, 10)
        self.versionHBox.show()

        self.versionLabel=gtk.Label(_("version"))
        self.versionHBox.pack_start(self.versionLabel, False, False, 2)
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

