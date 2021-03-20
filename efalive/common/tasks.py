#!/usr/bin/python
'''
Created on 27.04.2015

Copyright (C) 2015-2021 Kay Hannay

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
import os
import shutil

from efalive.common import common
from efalive.common.i18n import _
from efalive.common.mailer import Mailer, MailData, MailerConfig


class Task(object):
    """Base class for all tasks

    Make sure that each implementation of a tasks is a sub class of this class.
    """
    def __init__(self, task_id):
        self.task_id = task_id

    def run(self):
        raise NotImplementedError("The run() method has to be implemented by every task.")


class ShellTask(Task):
    """Implementation of a shell task

    This task type is used to execute shell commands but it is not running in a shell, 
    so you can not use shell built ins. Write a script instead.
    """
    def __init__(self, task_id, command):
        super(ShellTask, self).__init__(task_id)
        self._logger = logging.getLogger('daemon.ShellTask')
        self._shell_command = command

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


class BackupMailTask(Task):
    """Implementation to send efaLive backups via mail

    This task type can be used to send e-mails with an efaLive backup attached.
    """
    def __init__(self, task_id, recipients, efalive_settings):
        super(BackupMailTask, self).__init__(task_id)

        self._logger = logging.getLogger('daemon.BackupMailTask')

        self._mail_data = MailData()
        self._mail_data.recipients = [ recipients ]
        self._mail_data.subject = _("Backup efaLive today")
        self._mail_data.body = _("Hi,\n\nattached to this mail you can find the latest backup of your efaLive system.\n\nregards\nefaLive")

        self._mailer_config = MailerConfig()
        self._mailer_config.smtp_host = efalive_settings.mailer_host.getData()
        self._mailer_config.smtp_port = efalive_settings.mailer_port.getData()
        self._mailer_config.use_starttls = efalive_settings.mailer_use_starttls.getData()
        self._mailer_config.use_ssl = efalive_settings.mailer_use_ssl.getData()
        self._mailer_config.user = efalive_settings.mailer_user.getData()
        self._mailer_config.password = efalive_settings.mailer_password.getData()
        self._mailer_config.sender = efalive_settings.mailer_sender.getData()

    def run(self, mailer = None):
        self._logger.info("Running automatic e-mail backup task.")
        directory = "/tmp/efalive_backup_mail"
        if not os.path.exists(directory):
            os.makedirs(directory)
        try:
            (returncode, output) = common.command_output(["/usr/bin/efalive-backup", directory])
            if returncode != 0:
                self._logger.error("Could not create backup (%d): \n %s" % (returncode, output))
                return
            self._logger.debug("Backup finished (%d): \n %s" % (returncode, output))
        except OSError as exception:
            self._logger.error("Could not create backup: %s" % exception)
            return

        if mailer == None:
            mailer = Mailer()
        self._mail_data.file_attachments = self._get_backup_files(directory)
        msg = mailer.create_mail(self._mail_data)
        mailer.send_mail(self._mailer_config, msg)
        shutil.rmtree(directory)

    def _get_backup_files(self, directory):
        backup_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                backup_files.append(os.path.join(root, file))
        return backup_files
