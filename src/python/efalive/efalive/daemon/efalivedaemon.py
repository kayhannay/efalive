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
from efalive.common.settings import EfaLiveSettings

class EfaLiveDaemon(object):
    """efaLive daemon main class which controls several modules. 

    These modules perform specific actions then.
    """

    def __init__(self, argv, output="/dev/tty", pidfile="/tmp/efaLiveDaemon.pid"):
        # These attributes are expected by the DaemonRunner
        self.stdin_path = "/dev/null"
        self.stdout_path = output
        self.stderr_path = output
        self.pidfile_path = pidfile
        self.pidfile_timeout = 5

        self._logger = logging.getLogger('efalivedaemon.EfaLiveDaemon')

        daemon_args = ["start", "stop", "restart"]
        if(len(argv) < 2 or len(argv) > 3):
            self._print_usage_and_exit()
        elif(len(argv) == 3):
            if argv[1] in daemon_args:
                confPath = argv[2]
                command = argv[1]
                #Override argv for the python-daemon, it accepts one argument only
                sys.argv = [argv[0], argv[1]]
            elif argv[2] in daemon_args:
                confPath = argv[1]
                command = argv[2]
                #Override argv for the python-daemon, it accepts one argument only
                sys.argv = [argv[0], argv[2]]
            else:
                self._print_usage_and_exit()

            if command != "stop":
                self._settings = EfaLiveSettings(confPath)
                self._settings.initSettings()
        elif(len(argv) == 2):
            if not argv[1] in daemon_args:
                self._print_usage_and_exit()
            elif argv[1] != "stop":
                self._settings = EfaLiveSettings()
                self._settings.initSettings()

    def run(self):
        if self._settings.autoUsbBackup.getData():
            AutoBackupModule().start()
        watchdog = WatchDogModule()

        while True:
            watchdog.run_checks()
            self._logger.debug("Running")
            time.sleep(10)

    def _print_usage_and_exit(self):
        print "ERROR: No proper arguments given"
        print "Usage of efaLive daemon:\n"
        print "\t%s [confDir] start|stop|restart" % sys.argv[0]
        sys.exit(1)

class WatchDogModule(object):
    """Watchdog that is triggered by the efaLive daemon.

    This watchdog checks whether the window manager is still running. If not, 
    the PC is restarted.
    """

    def __init__(self):
        self._logger = logging.getLogger('efalivedaemon.WatchDogModule')
        self._reset_restart_threshold()

    def _reset_restart_threshold(self):
        #How many cycles do we wait before we restart?
        self._restart_threshold = 3

    def run_checks(self):
        self._logger.debug("Check system conditions ...")
        process_name = "openbox"
        process_count = self._check_for_process(process_name)
        if process_count < 1:
            self._restart_threshold -= 1
            self._logger.warn("Process '%s' is not running, wait for %d more checks before restart!" % (process_name, self._restart_threshold))
            if self._restart_threshold < 1:
                self._logger.warn("Trigger restart now...")
                common.command_output(["sudo", "/sbin/shutdown", "-r", "now"])
        else:
            self._logger.debug("Found %d instances of the process '%s'." % (process_count, process_name))
            self._reset_restart_threshold()

    def _check_for_process(self, process_name):
        (return_code, output) = common.command_output(["ps", "-Af"])
        process_count = output.count(process_name)
        return process_count


class AutoBackupModule(object):
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
            (returncode, output) = common.command_output(["/usr/lib/efalive/bin/autobackup.sh", device_file, ">>", "~/autobackup.log", "2>&1"])
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


