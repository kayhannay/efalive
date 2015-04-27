#!/usr/bin/python
'''
Created on 27.04.2015

Copyright (C) 2015-2015 Kay Hannay

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
import logging

from efalive.common import common

class ShellTask(object):

    def __init__(self, task_id, command):
        self._logger = logging.getLogger('daemon.ShellTask')
        self._shell_command = command
        self.task_id = task_id

    def run(self):
        try:
            (returncode, output) = common.command_output(self._shell_command.split(' '))
            if returncode != 0:
                message = "Shell command '%s' failed!" % self._shell_command
                self._logger.error(message)
                self._logger.debug(output)
            else:
                message = "Shell command '%s' finished." % self._shell_command
                self._logger.info(message)
                self._logger.debug(output)
                return 0
        except OSError as error:
            message = "Could not run shell command '%s': %s" % (self._shell_command, error)
            self._logger.error(message)
        return 1

