#!/usr/bin/python
'''
Created on 23.04.2015

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
import logging
import smtplib
# For guessing MIME type based on file name extension
import mimetypes

from optparse import OptionParser

from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class MailData(object):

    def __init__(self):
        self.recipient_addresses = None
        self.recipient_name = None
        self.sender_address = None
        self.sender_name = None
        self.subject = None
        self.body = None
        self.file_attachments = None


class MailerConfig(object):

    def __init__(self):
        self.smtp_host = None
        self.smtp_port = None
        self.use_starttls = True
        self.use_ssl = True
        self.user = None
        self.password = None

class Mailer(object):

    def __init__(self):
        self._logger = logging.getLogger('common.Mailer')

    def create_mail(self, mail):
        message_text = MIMEText(mail.body)
        if mail.file_attachments != None:
            msg = MIMEMultipart()
            msg.attach(message_text)
            for attachment_file in mail.file_attachments:
                attachment = self.create_attachment(attachment_file)
                msg.attach(attachment)
        else:
            msg = message_text
        msg["Subject"] = mail.subject
        msg["From"] = mail.sender_address
        msg["To"] = ', '.join(mail.recipient_addresses)
        return msg

    def send_mail(self, config, mail):
        self._logger.debug("Send mail from %s to %s:\n%s" % (mail["From"], mail["To"], mail.as_string()))
        if config.use_ssl:
            sender = smtplib.SMTP_SSL(config.smtp_host, config.smtp_port)
        else:
            sender = smtplib.SMTP(config.smtp_host, config.smtp_port)
            if config.use_starttls:
                sender.starttls()
        if config.user != None:
            sender.login(config.user, config.password)
        sender.sendmail(mail["From"], mail["To"], mail.as_string())
        sender.quit()
        self._logger.info("Sent mail to %s." % mail["To"])

    def open_file(self, file_name):
        return open(file_name, "rb")

    def create_attachment(self, file_attachment):
        ctype, encoding = mimetypes.guess_type(file_attachment)
        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        fp = self.open_file(file_attachment)
        if maintype == 'text':
            msg = MIMEText(fp.read(), _subtype=subtype)
        elif maintype == 'image':
            msg = MIMEImage(fp.read(), _subtype=subtype)
        elif maintype == 'audio':
            msg = MIMEAudio(fp.read(), _subtype=subtype)
        else:
            msg = MIMEBase(maintype, subtype)
            msg.set_payload(fp.read())
            # Encode the payload using Base64
            encoders.encode_base64(msg)
        fp.close()
        # Set the filename parameter
        msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_attachment))
        return msg

