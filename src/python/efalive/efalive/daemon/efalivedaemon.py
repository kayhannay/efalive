import os
import sys 
import subprocess
import time
import logging
from pyudev import Context, Monitor, MonitorObserver

from datetime import datetime

from efalive.common import common

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

        AutoBackupModule()
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

        udev_context = Context()
        udev_monitor = Monitor.from_netlink(udev_context)
        udev_monitor.filter_by('block', device_type='partition')
        udev_observer = MonitorObserver(udev_monitor, callback=self._handle_device_event, name='monitor-observer')
        udev_observer.start()

    def _handle_device_event(self, device):
        self._debug_device(device)
        if (device.__getitem__("ID_BUS") != "usb"):
            return
        self._logger.info("Action %s for device %s" % (device.action, device.device_node))
        if device.action == "add":
            self._logger.info("Could start backup now.")
            self._run_autobackup(device.device_node)
        else:
            self._logger.warn("Unhandled action: %s" % device.action)

    def _debug_device(self, device):
        self._logger.debug("Device:")
        self._logger.debug("\tSubsystem: %s" % device.subsystem)
        self._logger.debug("\tType: %s" % device.device_type)
        self._logger.debug("\tName: %s" % device.sys_name)
        self._logger.debug("\tNumber: %s" % device.sys_number)
        self._logger.debug("\tSYS-fs path: %s" % device.sys_path)
        self._logger.debug("\tDriver: %s" % device.driver)
        self._logger.debug("\tAction: %s" % device.action)
        self._logger.debug("\tFile: %s" % device.device_node)
        #self._logger.debug("\tLinks: %s" % device.get_device_file_symlinks())
        #self._logger.debug("\tProperties: %s" % device.get_property_keys())
        #self._logger.debug("\tSYBSYSTEM: %s" % device.get_property("SUBSYSTEM"))
        #self._logger.debug("\tDEVTYPE: %s" % device.get_property("DEVTYPE"))
        ##self._logger.debug("\tID_VENDOR: %s" % device.__getitem__("ID_VENDOR"))
        self._logger.debug("\tID_MODEL: %s" % device.__getitem__("ID_MODEL"))
        self._logger.debug("\tID_TYPE: %s" % device.__getitem__("ID_TYPE"))
        self._logger.debug("\tID_BUS: %s" % device.__getitem__("ID_BUS"))
        self._logger.debug("\tID_FS_LABEL: %s" % device.__getitem__("ID_FS_LABEL"))
        self._logger.debug("\tID_FS_TYPE: %s" % device.__getitem__("ID_FS_TYPE"))
        self._logger.debug("\tUDISKS_PARTITION_SIZE: %s" % device.__getitem__("UDISKS_PARTITION_SIZE"))

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


