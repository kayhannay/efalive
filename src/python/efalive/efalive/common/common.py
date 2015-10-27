'''
Created on 10.01.2012

Copyright (C) 2012-2015 Kay Hannay

This file is part of efaLive.

efaLive is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
efaLiveSetup is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with efaLive.  If not, see <http://www.gnu.org/licenses/>.
'''
import os
import sys 
import subprocess
import logging

import pygtk
pygtk.require('2.0')
import gtk

LOCALES=os.path.join(os.path.dirname(sys.argv[0]), os.pardir, 'i18n')
LOCALEDIR=os.path.realpath(LOCALES)

def get_icon_path(icon_name):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, os.pardir)
    icon_path = os.path.join(path, 'icons', icon_name)
    logger = logging.getLogger('common')
    logger.debug("Resolved icon path: %s" % icon_path)
    return icon_path

def command_output(args, **kwds):
    kwds.setdefault("stdout", subprocess.PIPE)
    kwds.setdefault("stderr", subprocess.STDOUT)
    process = subprocess.Popen(args, **kwds)
    output = process.communicate()[0]
    returncode = process.returncode
    return (returncode, output)

def get_button_label(icon_name, label):
    button_vbox = gtk.VBox()
    button_label = gtk.Label(label)
    button_icon = gtk.image_new_from_file(get_icon_path(icon_name))
    button_vbox.pack_start(button_icon)
    button_vbox.pack_start(button_label)
    button_vbox.show_all()
    return button_vbox

