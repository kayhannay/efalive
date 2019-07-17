'''
Created on 10.01.2012

Copyright (C) 2012-2016 Kay Hannay

This file is part of efaLiveSetup.

efaLiveSetup is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
efaLiveSetup is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with efaLiveSetup.  If not, see <http://www.gnu.org/licenses/>.
'''
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import os
import sys
import pam

from efalive.common.i18n import _

LOCALEDIR=os.path.join(os.path.dirname(sys.argv[0]), "locale")
DIR=os.path.realpath(LOCALEDIR)

def show_confirm_dialog(widget, message):
    dialog = Gtk.MessageDialog(widget, Gtk.DialogFlags.MODAL, Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, message)
    response = dialog.run()
    dialog.destroy()
    if response == Gtk.ResponseType.YES:
        return True
    else:
        return False

def show_error_dialog(widget, message):
    dialog = Gtk.MessageDialog(widget, Gtk.DialogFlags.MODAL, Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE, message)
    dialog.run()
    dialog.destroy()

def show_exception_dialog(widget, message, details):
    show_details_dialog(widget, Gtk.MessageType.ERROR, _("Details"), message, details)

def show_output_dialog(widget, message, details):
    show_details_dialog(widget, Gtk.MessageType.INFO, _("Output"), message, details)

def show_warning_dialog(widget, message, details):
    show_details_dialog(widget, Gtk.MessageType.WARNING, _("Details"), message, details)

def show_details_dialog(widget, type, details_label, message, details):
    dialog = Gtk.MessageDialog(parent=widget, flags=Gtk.DialogFlags.MODAL, message_type=type, buttons=Gtk.ButtonsType.CLOSE, text=message)
    dialog.set_resizable(True)

    expander = Gtk.Expander()
    scroll_area = Gtk.ScrolledWindow()
    details_area = Gtk.TextView()

    details_area.get_buffer().set_text(details)
    details_area.show()

    scroll_area.set_shadow_type(Gtk.ShadowType.NONE)
    scroll_area.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
    scroll_area.add(details_area)
    scroll_area.show()

    expander.add(scroll_area)
    expander.show()

    dialog.vbox.pack_start(Gtk.Label(details_label), False, False, 0)
    dialog.vbox.pack_start(expander, True, True, 0)

    dialog.run()
    dialog.destroy()

def get_password_dialog(widget, user, error):
    dialog = Gtk.MessageDialog(widget, Gtk.DialogFlags.MODAL, Gtk.MessageType.INFO, Gtk.ButtonsType.OK_CANCEL, None)
    dialog.set_markup(_("Please enter the password of user %s") % user)
    if error == True:
        dialog.format_secondary_markup("<span foreground='red'>" + _("The password you entered did not match!") + "</span>")
    dialog.set_resizable(False)
    dialog.set_default_response(Gtk.ResponseType.OK)
    password_entry = Gtk.Entry()
    password_entry.set_max_length(255)
    password_entry.set_visibility(False)
    password_entry.set_activates_default(True)
    dialog.vbox.pack_start(password_entry, False, False, 2)
    password_entry.show()
    response = dialog.run()
    password = None
    if response == Gtk.ResponseType.OK:
        password = password_entry.get_text()
    dialog.destroy()
    return password

def authenticate(user, password):
    auth = pam.pam()
    try:
        return auth.authenticate(user, password)
    except pam.error:
        return False
    except:
        raise(BaseException(_("Internal error in PAM authentication module")))
    return False

def show_password_dialog(widget, user):
    authenticated = False
    error = False
    while authenticated == False:
        password = get_password_dialog(widget, user, error)
        if password == None:
            return False
        authenticated = authenticate(user, password)
        error = True
    return True

