'''
Created on 27.04.2009

Copyright (C) 2009-2010 Kay Hannay

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

class Observable(object):
    '''
    classdocs
    '''

    def __init__(self, initdata=None, observers=None):
        '''
        Constructor
        '''
        self._data = initdata
        if(observers == None):
            self._observerCbs = []
        else:
            self._observerCbs = observers
        
    def registerObserverCb(self, observerCb):
        self._observerCbs.append(observerCb)
        
    def removeObserverCb(self, observerCb):
        if observerCb in self._observerCbs:
            self._observerCbs.remove(observerCb)
        
    def updateData(self, data):
        self._data = data
        self.__notifyObservers()

    def getData(self):
        return self._data

    def __notifyObservers(self):
        for observerCb in self._observerCbs:
            observerCb(self._data)
