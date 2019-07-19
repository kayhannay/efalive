'''
Created on 19.09.2015

Copyright (C) 2015-2019 Kay Hannay

This file is part of efaLiveTools.

efaLiveTools is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
efaLiveSetup is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with efaLiveTools.  If not, see <http://www.gnu.org/licenses/>.
'''
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import logging

from ..common.i18n import _

class MailTabModel(object):
    def __init__(self, settings):
        self._logger = logging.getLogger('MailTabModel')
        self._settings = settings
        
    def set_smtp_host(self, hostname):
        self._settings.mailer_host.updateData(hostname)

    def register_smtp_host_callback(self, callback):
        self._settings.mailer_host.registerObserverCb(callback)

    def set_smtp_port(self, port):
        self._settings.mailer_port.updateData(port)

    def register_smtp_port_callback(self, callback):
        self._settings.mailer_port.registerObserverCb(callback)

    def set_smtp_user(self, username):
        self._settings.mailer_user.updateData(username)

    def register_smtp_user_callback(self, callback):
        self._settings.mailer_user.registerObserverCb(callback)

    def set_smtp_password(self, password):
        self._settings.mailer_password.updateData(password)

    def set_sender(self, sender):
        self._settings.mailer_sender.updateData(sender)

    def register_sender_callback(self, callback):
        self._settings.mailer_sender.registerObserverCb(callback)

    def set_smtp_use_ssl(self, use_ssl):
        self._settings.mailer_use_ssl.updateData(use_ssl)

    def register_smtp_use_ssl_callback(self, callback):
        self._settings.mailer_use_ssl.registerObserverCb(callback)

    def set_smtp_use_starttls(self, use_starttls):
        self._settings.mailer_use_starttls.updateData(use_starttls)

    def register_smtp_use_starttls_callback(self, callback):
        self._settings.mailer_use_starttls.registerObserverCb(callback)

class MailTabView(Gtk.VBox):
    def __init__(self):
        super(Gtk.VBox, self).__init__()
        self._logger = logging.getLogger('MailTabView')
        self._init_components()

    def _init_components(self):
        self.host_hbox = Gtk.HBox()
        self.pack_start(self.host_hbox, False, False, 5)
        self.host_label = Gtk.Label(_("SMTP host"))
        self.host_hbox.pack_start(self.host_label, False, False, 2)
        self.host_input = Gtk.Entry()
        self.host_input.set_max_length(255)
        self.host_hbox.pack_end(self.host_input, False, False, 2)
        self.host_hbox.show_all()
        
        self.port_hbox = Gtk.HBox()
        self.pack_start(self.port_hbox, False, False, 2)
        self.port_label = Gtk.Label(_("SMTP port"))
        self.port_hbox.pack_start(self.port_label, False, False, 2)
        self.port_adjustment = Gtk.Adjustment(0, 0, 65565, 1, 1000)
        self.port_button = Gtk.SpinButton()
        self.port_button.set_adjustment(self.port_adjustment)
        self.port_button.set_wrap(True)
        self.port_hbox.pack_end(self.port_button, False, False, 2)
        self.port_hbox.show_all()
        
        self.user_hbox = Gtk.HBox()
        self.pack_start(self.user_hbox, False, False, 2)
        self.user_label = Gtk.Label(_("User"))
        self.user_hbox.pack_start(self.user_label, False, False, 2)
        self.user_input = Gtk.Entry()
        self.user_input.set_max_length(255)
        self.user_hbox.pack_end(self.user_input, False, False, 2)
        self.user_hbox.show_all()
        
        self.password_hbox = Gtk.HBox()
        self.pack_start(self.password_hbox, False, False, 2)
        self.password_label = Gtk.Label(_("Password"))
        self.password_hbox.pack_start(self.password_label, False, False, 2)
        self.password_input = Gtk.Entry()
        self.password_input.set_max_length(255)
        self.password_input.set_visibility(False)
        self.password_hbox.pack_end(self.password_input, False, False, 2)
        self.password_hbox.show_all()
        
        self.sender_hbox = Gtk.HBox()
        self.pack_start(self.sender_hbox, False, False, 2)
        self.sender_label = Gtk.Label(_("Sender address"))
        self.sender_hbox.pack_start(self.sender_label, False, False, 2)
        self.sender_input = Gtk.Entry()
        self.sender_input.set_max_length(255)
        self.sender_hbox.pack_end(self.sender_input, False, False, 2)
        self.sender_hbox.show_all()
        
        self.ssl_hbox = Gtk.HBox()
        self.pack_start(self.ssl_hbox, False, False, 2)
        self.ssl_checkbox = Gtk.CheckButton(_("Use SSL/TLS"))
        self.ssl_hbox.pack_start(self.ssl_checkbox, False, False, 2)
        self.ssl_hbox.show_all()
        
        self.starttls_hbox = Gtk.HBox()
        self.pack_start(self.starttls_hbox, False, False, 2)
        self.starttls_checkbox = Gtk.CheckButton(_("Use startTLS"))
        self.starttls_hbox.pack_start(self.starttls_checkbox, False, False, 2)
        self.starttls_hbox.show_all()

class MailTabController(object):
    def __init__(self, settings):
        self._logger = logging.getLogger('MailTabController')
        
        self._view = MailTabView()
        
        self._model = MailTabModel(settings)
        
        self._model.register_smtp_host_callback(self.smtp_host_changed)
        self._model.register_smtp_port_callback(self.smtp_port_changed)
        self._model.register_smtp_user_callback(self.smtp_user_changed)
        self._model.register_sender_callback(self.sender_changed)
        self._model.register_smtp_use_ssl_callback(self.smtp_use_ssl_changed)
        self._model.register_smtp_use_starttls_callback(self.smtp_use_starttls_changed)
        
        self._init_events()

    def _init_events(self):
        self._view.host_input.connect("changed", self.set_smtp_host)
        self._view.port_adjustment.connect("value_changed", self.set_smtp_port)
        self._view.user_input.connect("changed", self.set_smtp_user)
        self._view.password_input.connect("changed", self.set_smtp_password)
        self._view.sender_input.connect("changed", self.set_sender)
        self._view.ssl_checkbox.connect("toggled", self.set_smtp_use_ssl)
        self._view.starttls_checkbox.connect("toggled", self.set_smtp_use_starttls)

    def get_view(self):
        return self._view

    def smtp_host_changed(self, hostname):
        self._view.host_input.set_text(hostname)

    def smtp_port_changed(self, port):
        self._view.port_adjustment.set_value(port)

    def smtp_user_changed(self, username):
        self._view.user_input.set_text(username)

    def sender_changed(self, sender):
        self._view.sender_input.set_text(sender)

    def smtp_use_ssl_changed(self, enable):
        self._view.ssl_checkbox.set_active(enable)

    def smtp_use_starttls_changed(self, enable):
        self._view.starttls_checkbox.set_active(enable)

    def set_smtp_host(self, widget):
        self._model.set_smtp_host(widget.get_text())

    def set_smtp_port(self, widget):
        self._model.set_smtp_port(widget.get_value())

    def set_smtp_user(self, widget):
        self._model.set_smtp_user(widget.get_text())

    def set_smtp_password(self, widget):
        self._model.set_smtp_password(widget.get_text())

    def set_sender(self, sender):
        self._model.set_sender(sender.get_text())

    def set_smtp_use_ssl(self, widget):
        self._model.set_smtp_use_ssl(widget.get_active())

    def set_smtp_use_starttls(self, widget):
        self._model.set_smtp_use_starttls(widget.get_active())
