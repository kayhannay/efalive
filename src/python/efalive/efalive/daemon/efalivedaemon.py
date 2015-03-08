#!/usr/bin/python
'''
Created on 16.02.2015

Copyright (C) 2015 Kay Hannay

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
import subprocess
import time
import logging

from datetime import datetime

from efalive.common import common
from efalive.common.usbmonitor import UsbStorageMonitor, UsbStorageDevice

class EfaLiveDaemon():
    """efaLive daemon main class which controls several modules. 

    These modules perform specific actions then.
    """

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/tmp/efalivedaemon.pid'
        self.pidfile_timeout = 5

    def run(self):
        logging.basicConfig(filename='/tmp/efaLiveDaemon.log',level=logging.DEBUG)
        self._logger = logging.getLogger('efalivedaemon.EfaLiveDaemon')

        AutoBackupModule().start()
        watchdog = WatchDogModule()

        while True:
            watchdog.run_checks()
            self._logger.debug("Running")
            time.sleep(10)


class WatchDogModule():
    """Watchdog that is triggered by the efaLive daemon.

    This watchdog checks whether the X server is still running. If not, 
    the PC is restarted.
    """

    def __init__(self):
        self._logger = logging.getLogger('efalivedaemon.WatchDogModule')

    def run_checks(self):
        self._logger.info("Check system conditions ...")


class AutoBackupModule():
    """Module to autmatically create a backup.

    This module is used to automatically create a backup on any USB 
    stick that is plugged in. The implementation is based on UDEV and 
    the pyudev library.
    """

    def __init__(self):
        self._logger = logging.getLogger('efalivedaemon.AutoBackupModule')

        self._storage_monitor = UsbStorageMonitor(self._handle_usb_add_event)

    def start(self):
        self._storage_monitor.start()

    def stop(self):
        self._storage_monitor.stop()

    def _handle_usb_add_event(self, device):
        self._logger.info("USB storage device added: [%s] %s %s (%s, %s)" % (device.bus_id, device.vendor, device.model, device.size, device.device_file))
        self._run_autobackup(device.device_file)

    def _run_autobackup(self, device_file):
        try:
            (returncode, output) = common.command_output(["/usr/lib/efalive/bin/autobackup", device_file])
            if returncode != 0:
                if returncode == 1 or returncode == 5:
                    message = "Backup failed! Please check that the efalive user is configured correctly in efa."
                    self._logger.error(message)
                    self._logger.debug(output)
                else:
                    message = "Backup to device %s failed!" % device_file
                    self._logger.error(message)
                    self._logger.debug(output)
            else:
                message = "Backup to device %s finished." % device_file
                self._logger.info(message)
                self._logger.debug(output)
                return 0
        except OSError as error:
            message = "Could not create backup: %s" % error
            self._logger.error(message)
        return 1


