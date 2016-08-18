#!/usr/bin/python
'''
Created on 16.02.2015

Copyright (C) 2015-2016 Kay Hannay

This file is part of efaLive.

efaLiveSetup is free software: you can redistribute it and/or modify
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
from daemon import runner

from efalive.daemon.efalivedaemon import EfaLiveDaemon

if __name__ == "__main__":
    logfile = "efaLiveDaemon.log"
    stdout = "efaLiveDaemonStdOut.log"
    daemon = EfaLiveDaemon(sys.argv, output=logfile, stdout=stdout)
    daemon_runner = runner.DaemonRunner(daemon)
    daemon_runner.daemon_context.working_directory = os.getcwd()
    daemon_runner.do_action()

