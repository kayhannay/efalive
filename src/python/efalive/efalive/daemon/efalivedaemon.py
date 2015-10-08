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
import time
import logging
import md5
import dateutil.parser
import json

from datetime import datetime

from efalive.common import common
from efalive.common.usbmonitor import UsbStorageMonitor
from efalive.common.settings import EfaLiveSettings
from tasks import ShellTask
from efalive.daemon.tasks import BackupMailTask

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
        scheduler = TaskSchedulerModule()
        scheduler.load_tasks(self._settings)
        watchdog = WatchDogModule()

        while True:
            watchdog.run_checks()
            scheduler.run_tasks()
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


class TaskSchedulerModule(object):
    """Module to run repeating tasks

    This module can be used to run repeating tasks. It supports hourly, 
    daily and weekly tasks.
    """
    def __init__(self):
        self._hourly_markers = {}
        self._daily_markers = {}
        self._weekly_markers = {}
        self._monthly_markers = {}

    def load_tasks(self, settings):
        self._settings = settings
        self.hourly_tasks = self._create_task_list(self._settings.hourly_tasks.getData())
        self.daily_tasks = self._create_task_list(self._settings.daily_tasks.getData())
        self.weekly_tasks = self._create_task_list(self._settings.weekly_tasks.getData())
        self.monthly_tasks = self._create_task_list(self._settings.monthly_tasks.getData())
        self._load_marker_file("hourly_tasks.dat")
        self._load_marker_file("daily_tasks.dat")
        self._load_marker_file("weekly_tasks.dat")
        self._load_marker_file("monthly_tasks.dat")

    def _create_task_list(self, tasks):
        task_list = []
        for task_id in tasks.keys():
            if tasks[task_id][0] == "SHELL":
                shellTask = ShellTask(task_id, tasks[task_id][1])
                task_list.append(shellTask)
            elif tasks[task_id][0] == "BACKUP_MAIL":
                backupMailTask = BackupMailTask(task_id, tasks[task_id][1], self._settings)
                task_list.append(backupMailTask)
        return task_list

    def run_tasks(self):
        for task in self.hourly_tasks:
            if not self._already_executed(task, "HOURLY"):
                task.run()
                self._mark_task_run(task, "HOURLY")
        for task in self.daily_tasks:
            if not self._already_executed(task, "DAILY"):
                task.run()
                self._mark_task_run(task, "DAILY")
        for task in self.weekly_tasks:
            if not self._already_executed(task, "WEEKLY"):
                task.run()
                self._mark_task_run(task, "WEEKLY")
        for task in self.monthly_tasks:
            if not self._already_executed(task, "MONTHLY"):
                task.run()
                self._mark_task_run(task, "MONTHLY")

    def _load_marker_file(self, file_name):
        markers = {}
        marker_file = open(os.path.join(self._settings.confPath, file_name), "r")
        for line in marker_file:
            entry = json.loads(line)
            markers[entry[0]] = dateutil.parser.parse(entry[1])
        return markers

    def _save_marker_file(self, file_name, markers):
        marker_file = open(os.path.join(self._settings.confPath, file_name), "w")
        for marker in markers:
            marker_file.write(json.dumps([marker, markers[marker].isoformat()]))

    def _already_executed(self, task, cycle):
        if cycle == "HOURLY":
            if task.task_id in self._hourly_markers:
                last_run = self._hourly_markers[task.task_id]
                delta = datetime.now() - last_run
                if (delta.total_seconds() < 1 * 60 * 60):
                    return True
            return False
        elif cycle == "DAILY":
            if task.task_id in self._daily_markers:
                last_run = self._daily_markers[task.task_id]
                delta = datetime.now() - last_run
                if (delta.total_seconds() < 24 * 60 * 60):
                    return True
            return False
        elif cycle == "WEEKLY":
            if task.task_id in self._weekly_markers:
                last_run = self._weekly_markers[task.task_id]
                delta = datetime.now() - last_run
                if (delta.total_seconds() < 7 * 24 * 60 * 60):
                    return True
            return False
        elif cycle == "MONTHLY":
            if task.task_id in self._monthly_markers:
                last_run = self._monthly_markers[task.task_id]
                delta = datetime.now() - last_run
                if (delta.total_seconds() < 4 * 7 * 24 * 60 * 60):
                    return True
            return False

    def _mark_task_run(self, task, cycle):
        if cycle == "HOURLY":
            self._hourly_markers[task.task_id] = datetime.now()
            self._save_marker_file("hourly_tasks.dat", self._hourly_markers)
        elif cycle == "DAILY":
            self._daily_markers[task.task_id] = datetime.now()
            self._save_marker_file("daily_tasks.dat", self._daily_markers)
        elif cycle == "WEEKLY":
            self._weekly_markers[task.task_id] = datetime.now()
            self._save_marker_file("weekly_tasks.dat", self._weekly_markers)
        elif cycle == "MONTHLY":
            self._monthly_markers[task.task_id] = datetime.now()
            self._save_marker_file("monthly_tasks.dat", self._monthly_markers)

