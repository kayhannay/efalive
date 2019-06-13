#!/usr/bin/python
'''
Created on 23.04.2015

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
import unittest
from mock import call, patch, MagicMock
import base64

from mailer import Mailer, MailData, MailerConfig
import mimetypes

class MailerTestCase(unittest.TestCase):

    def test_create_mail__text(self):
        mail = MailData()
        mail.recipients = ["recipient@test.local"]
        mail.subject = "Test mail"
        mail.body = "Test body"

        mailer = Mailer()
        result = mailer.create_mail(mail)

        self.assertEqual("recipient@test.local", result["To"])
        self.assertEqual(mail.subject, result["Subject"])
        self.assertFalse(result.is_multipart())
        self.assertEqual("text/plain", result.get_content_type())
        self.assertEqual(mail.body, result.get_payload())

    def test_create_mail__text_two_recipients(self):
        mail = MailData()
        mail.recipients = ["recipient1@test.local", "recipient2@test.local"]
        mail.subject = "Test mail"
        mail.body = "Test body"

        mailer = Mailer()
        result = mailer.create_mail(mail)

        self.assertEqual("recipient1@test.local, recipient2@test.local", result["To"])
        self.assertEqual(mail.subject, result["Subject"])
        self.assertFalse(result.is_multipart())
        self.assertEqual("text/plain", result.get_content_type())
        self.assertEqual(mail.body, result.get_payload())

    def test_create_mail__attach_zip(self):
        mail = MailData()
        mail.recipients = ["recipient@test.local"]
        mail.subject = "Test mail"
        mail.body = "Test body"
        mail.file_attachments = ["test.zip"]
        return_file = FileStub("BINARY")
        Mailer.open_file = MagicMock(return_value = return_file)
        mimetypes.guess_type = MagicMock(return_value = ("application/zip", None))

        mailer = Mailer()
        result = mailer.create_mail(mail)

        self.assertEqual("recipient@test.local", result["To"])
        self.assertEqual(mail.subject, result["Subject"])
        self.assertTrue(result.is_multipart())
        messages = result.get_payload()
        self.assertEqual(2, len(messages))
        text_message = messages[0]
        self.assertEqual("text/plain", text_message.get_content_type())
        self.assertEqual(mail.body, text_message.get_payload())
        attachment_message = messages[1]
        self.assertEqual("application/zip", attachment_message.get_content_type())
        self.assertEqual(base64.b64encode("BINARY"), attachment_message.get_payload())

    def test_create_mail__attach_text(self):
        mail = MailData()
        mail.recipients = ["recipient@test.local"]
        mail.subject = "Test mail"
        mail.body = "Test body"
        mail.file_attachments = ["test.txt"]
        return_file = FileStub("This is text")
        Mailer.open_file = MagicMock(return_value = return_file)
        mimetypes.guess_type = MagicMock(return_value = ("text/plain", None))

        mailer = Mailer()
        result = mailer.create_mail(mail)

        self.assertEqual("recipient@test.local", result["To"])
        self.assertEqual(mail.subject, result["Subject"])
        self.assertTrue(result.is_multipart())
        messages = result.get_payload()
        self.assertEqual(2, len(messages))
        text_message = messages[0]
        self.assertEqual("text/plain", text_message.get_content_type())
        self.assertEqual(mail.body, text_message.get_payload())
        attachment_message = messages[1]
        self.assertEqual("text/plain", attachment_message.get_content_type())
        self.assertEqual("This is text", attachment_message.get_payload())

    def test_create_mail__attach_image(self):
        mail = MailData()
        mail.recipients = ["recipient@test.local"]
        mail.subject = "Test mail"
        mail.body = "Test body"
        mail.file_attachments = ["test.png"]
        return_file = FileStub("PNG IMAGE")
        Mailer.open_file = MagicMock(return_value = return_file)
        mimetypes.guess_type = MagicMock(return_value = ("image/png", None))

        mailer = Mailer()
        result = mailer.create_mail(mail)

        self.assertEqual("recipient@test.local", result["To"])
        self.assertEqual(mail.subject, result["Subject"])
        self.assertTrue(result.is_multipart())
        messages = result.get_payload()
        self.assertEqual(2, len(messages))
        text_message = messages[0]
        self.assertEqual("text/plain", text_message.get_content_type())
        self.assertEqual(mail.body, text_message.get_payload())
        attachment_message = messages[1]
        self.assertEqual("image/png", attachment_message.get_content_type())
        self.assertEqual(base64.b64encode("PNG IMAGE"), attachment_message.get_payload())

    def test_create_mail__attach_audio(self):
        mail = MailData()
        mail.recipients = ["recipient@test.local"]
        mail.subject = "Test mail"
        mail.body = "Test body"
        mail.file_attachments = ["test.wav"]
        return_file = FileStub("SOUND")
        Mailer.open_file = MagicMock(return_value = return_file)
        mimetypes.guess_type = MagicMock(return_value = ("audio/x-wav", None))

        mailer = Mailer()
        result = mailer.create_mail(mail)

        self.assertEqual("recipient@test.local", result["To"])
        self.assertEqual(mail.subject, result["Subject"])
        self.assertTrue(result.is_multipart())
        messages = result.get_payload()
        self.assertEqual(2, len(messages))
        text_message = messages[0]
        self.assertEqual("text/plain", text_message.get_content_type())
        self.assertEqual(mail.body, text_message.get_payload())
        attachment_message = messages[1]
        self.assertEqual("audio/x-wav", attachment_message.get_content_type())
        self.assertEqual(base64.b64encode("SOUND"), attachment_message.get_payload())

    def test_create_mail__attach_text_and_zip(self):
        mail = MailData()
        mail.recipients = ["recipient@test.local"]
        mail.subject = "Test mail"
        mail.body = "Test body"
        mail.file_attachments = ["test.txt", "test.zip"]
        text_file = FileStub("TEXT")
        zip_file = FileStub("BINARY")
        Mailer.open_file = MagicMock(side_effect = [text_file, zip_file])
        mimetypes.guess_type = MagicMock(side_effect = [("text/plain", None), ("application/zip", None)])

        mailer = Mailer()
        result = mailer.create_mail(mail)

        self.assertEqual("recipient@test.local", result["To"])
        self.assertEqual(mail.subject, result["Subject"])
        self.assertTrue(result.is_multipart())
        messages = result.get_payload()
        self.assertEqual(3, len(messages))
        text_message = messages[0]
        self.assertEqual("text/plain", text_message.get_content_type())
        self.assertEqual(mail.body, text_message.get_payload())
        attachment1_message = messages[1]
        self.assertEqual("text/plain", attachment1_message.get_content_type())
        self.assertEqual("TEXT", attachment1_message.get_payload())
        attachment2_message = messages[2]
        self.assertEqual("application/zip", attachment2_message.get_content_type())
        self.assertEqual(base64.b64encode("BINARY"), attachment2_message.get_payload())

    @patch("efalive.common.mailer.smtplib.SMTP", autospec=True)
    def test_send_mail__unencrypted_unauthorized(self, smtp_mock):
        mail_data = MailData()
        mail_data.recipients = ["recipient@test.local"]
        mail_data.subject = "Test mail"
        mail_data.body = "Test body"
        mailer_config = MailerConfig()
        mailer_config.smtp_host = "localhost"
        mailer_config.smtp_port = 25
        mailer_config.use_starttls = False
        mailer_config.use_ssl = False
        mailer_config.sender = "sender@test.local"

        mailer = Mailer()
        mail = mailer.create_mail(mail_data)
        mailer.send_mail(mailer_config, mail)

        assert smtp_mock.call_count == 1
        assert smtp_mock.call_args == ((mailer_config.smtp_host, mailer_config.smtp_port),)
        assert smtp_mock.return_value.starttls.call_count == 0
        assert smtp_mock.return_value.login.call_count == 0
        assert smtp_mock.return_value.sendmail.call_count == 1
        assert smtp_mock.return_value.sendmail.call_args == ((mail["From"], mail["To"], mail.as_string()),)
        assert smtp_mock.return_value.quit.call_count == 1

    @patch("efalive.common.mailer.smtplib.SMTP", autospec=True)
    def test_send_mail__starttls_unauthorized(self, smtp_mock):
        mail_data = MailData()
        mail_data.recipients = ["recipient@test.local"]
        mail_data.subject = "Test mail"
        mail_data.body = "Test body"
        mailer_config = MailerConfig()
        mailer_config.smtp_host = "localhost"
        mailer_config.smtp_port = 25
        mailer_config.use_starttls = True
        mailer_config.use_ssl = False
        mailer_config.sender = "sender@test.local"

        mailer = Mailer()
        mail = mailer.create_mail(mail_data)
        mailer.send_mail(mailer_config, mail)

        assert smtp_mock.call_count == 1
        assert smtp_mock.call_args == ((mailer_config.smtp_host, mailer_config.smtp_port),)
        assert smtp_mock.return_value.starttls.call_count == 1
        assert smtp_mock.return_value.login.call_count == 0
        assert smtp_mock.return_value.sendmail.call_count == 1
        assert smtp_mock.return_value.sendmail.call_args == ((mail["From"], mail["To"], mail.as_string()),)
        assert smtp_mock.return_value.quit.call_count == 1

    @patch("efalive.common.mailer.smtplib.SMTP_SSL", autospec=True)
    def test_send_mail__ssl_unauthorized(self, smtp_mock):
        mail_data = MailData()
        mail_data.recipients = ["recipient@test.local"]
        mail_data.subject = "Test mail"
        mail_data.body = "Test body"
        mailer_config = MailerConfig()
        mailer_config.smtp_host = "localhost"
        mailer_config.smtp_port = 25
        mailer_config.use_starttls = True
        mailer_config.use_ssl = True
        mailer_config.sender = "sender@test.local"

        mailer = Mailer()
        mail = mailer.create_mail(mail_data)
        mailer.send_mail(mailer_config, mail)

        assert smtp_mock.call_count == 1
        assert smtp_mock.call_args == ((mailer_config.smtp_host, mailer_config.smtp_port),)
        assert smtp_mock.return_value.starttls.call_count == 0
        assert smtp_mock.return_value.login.call_count == 0
        assert smtp_mock.return_value.sendmail.call_count == 1
        assert smtp_mock.return_value.sendmail.call_args == ((mail["From"], mail["To"], mail.as_string()),)
        assert smtp_mock.return_value.quit.call_count == 1

    @patch("efalive.common.mailer.smtplib.SMTP", autospec=True)
    def test_send_mail__unencrypted_authorized(self, smtp_mock):
        mail_data = MailData()
        mail_data.recipients = ["recipient@test.local"]
        mail_data.subject = "Test mail"
        mail_data.body = "Test body"
        mailer_config = MailerConfig()
        mailer_config.smtp_host = "localhost"
        mailer_config.smtp_port = 25
        mailer_config.use_starttls = False
        mailer_config.use_ssl = False
        mailer_config.user = "Tester"
        mailer_config.password = "Secret"
        mailer_config.sender = "sender@test.local"

        mailer = Mailer()
        mail = mailer.create_mail(mail_data)
        mailer.send_mail(mailer_config, mail)

        assert smtp_mock.call_count == 1
        assert smtp_mock.call_args == ((mailer_config.smtp_host, mailer_config.smtp_port),)
        assert smtp_mock.return_value.starttls.call_count == 0
        assert smtp_mock.return_value.login.call_count == 1
        assert smtp_mock.return_value.login.call_args == ((mailer_config.user, mailer_config.password),)
        assert smtp_mock.return_value.sendmail.call_count == 1
        assert smtp_mock.return_value.sendmail.call_args == ((mail["From"], mail["To"], mail.as_string()),)
        assert smtp_mock.return_value.quit.call_count == 1


class FileStub(object):

    def __init__(self, content):
        self._content = content

    def read(self):
        return self._content

    def close(self):
        pass
