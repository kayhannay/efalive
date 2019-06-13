'''
Created on 10.01.2012

Copyright (C) 2012-2016 Kay Hannay

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

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

LOCALES=os.path.join(os.path.dirname(sys.argv[0]), os.pardir, 'i18n')
LOCALEDIR=os.path.realpath(LOCALES)

class Platform(object):
    PC = 1
    RASPI = 2

def get_icon_path(icon_name):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, os.pardir)
    icon_path = os.path.join(path, 'icons', icon_name)
    logger = logging.getLogger('common')
    logger.debug("Resolved icon path: %s" % icon_path)
    return icon_path

def command_output(args):
    logger = logging.getLogger('common')
    logger.debug("Command to execute: '%s'" % args)
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
    output = process.communicate()[0]
    returncode = process.returncode
    return (returncode, output)

def get_button_label(icon_name, label):
    button_vbox = Gtk.VBox()
    button_label = Gtk.Label(label)
    button_icon = Gtk.Image.new_from_file(get_icon_path(icon_name))
    button_vbox.pack_start(button_icon, True, True, 0)
    button_vbox.pack_start(button_label, True, True, 0)
    button_vbox.show_all()
    return button_vbox

def get_efalive_platform():
    os_id = None
    os_release_file = os.path.join(os.sep, "etc", "os-release")
    if os.path.exists(os_release_file):
        os_release_content = open(os_release_file, "r")
        for line in os_release_content:
            if line.startswith("ID="):
                os_id = line[(line.index('=') + 1):].rstrip()
    if os_id == "raspbian":
        return Platform.RASPI
    else:
        return Platform.PC
