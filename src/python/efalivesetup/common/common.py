'''
Created on 10.01.2012

Copyright (C) 2012 Kay Hannay

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
import os
import sys 
import subprocess

LOCALES=os.path.join(os.path.dirname(sys.argv[0]), os.pardir, 'i18n')
LOCALEDIR=os.path.realpath(LOCALES)

def get_icon_path(icon_name):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir)
    icon_path = os.path.join(path, 'icons', icon_name)
    return icon_path

def command_output(args, **kwds):
    kwds.setdefault("stdout", subprocess.PIPE)
    kwds.setdefault("stderr", subprocess.STDOUT)
    process = subprocess.Popen(args, **kwds)
    output = process.communicate()[0]
    returncode = process.returncode
    return (returncode, output)

