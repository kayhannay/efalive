#!/usr/bin/python
'''
Created on 16.02.2015

Copyright (C) 2015-2019 Kay Hannay

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
import dateutil.parser
import json

from datetime import datetime

from efalive.common import common
from efalive.common.usbmonitor import UsbStorageMonitor
from efalive.common.settings import EfaLiveSettings
from .tasks import ShellTask
from efalive.daemon.tasks import BackupMailTask

class EfaLiveDaemon(object):
    """efaLive daemon main class which controls several modules. 

    These modules perform specific actions then.
    """

    def __init__(self, argv, output="/dev/tty", stdout="/dev/tty", stderr="/dev/tty", pidfile="/tmp/efaLiveDaemon.pid"):
        # These attributes are expected by the DaemonRunner
        self.logfile = output   
        self.stdin_path = "/dev/null"
        self.stdout_path = stdout
        self.stderr_path = stderr
        self.pidfile_path = pidfile
        self.pidfile_timeout = 5
        self.update_settings_counter = 0
        self._autobackup_module = None


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
        logging.basicConfig(filename=self.logfile, level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
        self._logger = logging.getLogger('efalivedaemon.EfaLiveDaemon')
        if self._settings.autoUsbBackup.getData():
            self._autobackup_module = AutoBackupModule()
            self._autobackup_module.start()
        scheduler = TaskSchedulerModule()
        scheduler.update_settings(self._settings)
        watchdog = WatchDogModule()
        update_settings_modules = [ scheduler ]

        while True:
            try:
                self._update_settings(update_settings_modules)
                watchdog.run_checks()
                scheduler.run_tasks()
                self._logger.debug("Running")
                time.sleep(10)
            except Exception as exception:
                self._logger.exception("An error occured which was not handled in it's sub module:")

    def _update_settings(self, modules):
        if self.update_settings_counter == 30:
            self.update_settings_counter = 0
            self._settings.load_settings()
            for update_module in modules:
                update_module.update_settings(self._settings)
        else:
            self.update_settings_counter += 1

    def _print_usage_and_exit(self):
        print("ERROR: No proper arguments given")
        print("Usage of efaLive daemon:\n")
        print("\t%s [confDir] start|stop|restart" % sys.argv[0])
        sys.exit(1)

class UpdateableModule(object):
    """Base class for modules that can update their settings at runtime.

    Make sure that each implementation of a module that need/can update their settings is a sub 
    class of this class.
    """

    def update_settings(self, settings):
        raise NotImplementedError("The update_settings() method has to be implemented.")


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
            self._logger.warning("Process '%s' is not running, wait for %d more checks before restart!" % (process_name, self._restart_threshold))
            if self._restart_threshold < 1:
                self._reset_restart_threshold()
                self._logger.warning("Trigger restart now...")
                common.command_output(["sudo", "/sbin/shutdown", "-r", "now"])
        else:
            self._logger.debug("Found %d instances of the process '%s'." % (process_count, process_name))
            self._reset_restart_threshold()

    def _check_for_process(self, process_name):
        (return_code, output) = common.command_output(["ps", "-Af"])
        process_count = output.count(process_name)
        return process_count


class AutoBackupModule(object):
    """Module to automatically create a backup.

    This module is used to automatically create a backup on any USB 
    stick that is plugged in. The implementation is based on UDEV and 
    the GUdev library.
    """

    def __init__(self):
        self._logger = logging.getLogger('efalivedaemon.AutoBackupModule')

        self._storage_monitor = UsbStorageMonitor(self._handle_usb_add_event)

    def start(self):
        self._logger.info("Start AutoBackup module ...")
        self._storage_monitor.start()

    def stop(self):
        self._logger.info("Stop AutoBackup module ...")
        self._storage_monitor.stop()

    def _handle_usb_add_event(self, device):
        self._logger.info("USB storage device added: [%s] %s %s (%s, %s)" % (device.bus_id, device.vendor, device.model, device.size, device.device_file))
        self._run_autobackup(device.device_file)

    def _run_autobackup(self, device_file):
        try:
            (returncode, output) = common.command_output(["/usr/lib/efalive/bin/autobackup.sh", device_file])
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


class TaskSchedulerModule(UpdateableModule):
    """Module to run repeating tasks

    This module can be used to run repeating tasks. It supports hourly, 
    daily and weekly tasks.
    """
    def __init__(self):
        self._logger = logging.getLogger('efalivedaemon.TaskScheduleModule')
        self._hourly_markers = {}
        self._daily_markers = {}
        self._weekly_markers = {}
        self._monthly_markers = {}
        self._logger.info("Initialization of efaLive daemon finished.")

    def update_settings(self, settings):
        self._settings = settings
        self.hourly_tasks = self._create_task_list(self._settings.hourly_tasks.getData())
        self.daily_tasks = self._create_task_list(self._settings.daily_tasks.getData())
        self.weekly_tasks = self._create_task_list(self._settings.weekly_tasks.getData())
        self.monthly_tasks = self._create_task_list(self._settings.monthly_tasks.getData())
        self._hourly_markers = self._load_marker_file("hourly_tasks.dat")
        self._daily_markers = self._load_marker_file("daily_tasks.dat")
        self._weekly_markers = self._load_marker_file("weekly_tasks.dat")
        self._monthly_markers = self._load_marker_file("monthly_tasks.dat")

    def _create_task_list(self, tasks):
        task_list = []
        if tasks == None:
            return task_list
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
        marker_file = os.path.join(self._settings.confPath, file_name)
        if not os.path.isfile(marker_file):
            self._logger.info("No marker file found at %s" % marker_file)
            return markers
        marker_file_handle = open(marker_file, "r")
        for line in marker_file_handle:
            entry = json.loads(line)
            self._logger.debug("Read marker line: %s" % entry)
            markers[entry[0]] = dateutil.parser.parse(entry[1])
        marker_file_handle.close()
        return markers

    def _save_marker_file(self, file_name, markers):
        marker_file = open(os.path.join(self._settings.confPath, file_name), "w")
        for marker in markers:
            marker_file.write("%s\n" % json.dumps([marker, markers[marker].isoformat()]))
        marker_file.close()

    def _already_executed(self, task, cycle):
        self._logger.debug("Execute task: %s" % task.task_id)
        if cycle == "HOURLY":
            self._logger.debug("Hourly markers: %s" % self._hourly_markers)
            if task.task_id in self._hourly_markers:
                last_run = self._hourly_markers[task.task_id]
                delta = datetime.now() - last_run
                self._logger.debug("Delta: %d" % delta.total_seconds())
                if (delta.total_seconds() < 1 * 60 * 60):
                    return True
            return False
        elif cycle == "DAILY":
            self._logger.debug("Daily markers: %s" % self._daily_markers)
            if task.task_id in self._daily_markers:
                last_run = self._daily_markers[task.task_id]
                delta = datetime.now() - last_run
                if (delta.total_seconds() < 24 * 60 * 60):
                    return True
            return False
        elif cycle == "WEEKLY":
            self._logger.debug("Weekly markers: %s" % self._weekly_markers)
            if task.task_id in self._weekly_markers:
                last_run = self._weekly_markers[task.task_id]
                delta = datetime.now() - last_run
                if (delta.total_seconds() < 7 * 24 * 60 * 60):
                    return True
            return False
        elif cycle == "MONTHLY":
            self._logger.debug("Monthly markers: %s" % self._monthly_markers)
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

