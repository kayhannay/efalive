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
from efaLiveSetup.Observable import Observable
import os

class SetupModel(object):
    def __init__(self, confPath):
        self._confPath=confPath
        self._versionFileName = os.path.join(self._confPath, "version.conf")
        self.efaVersion=Observable()

    def initModel(self):
        self.efaVersion.updateData(1)
        #if not os.path.isfile("version.conf"):
        #    os.path.
        self.versionFile=open(self._versionFileName, "rw")
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

