'''
Created on 10.01.2012

Copyright (C) 2012-2014 Kay Hannay

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
import pygtk
pygtk.require('2.0')
import gtk
import os
import sys
import PAM

import locale
import gettext
APP="efaLiveSetup"
LOCALEDIR=os.path.join(os.path.dirname(sys.argv[0]), "locale")
DIR=os.path.realpath(LOCALEDIR)
gettext.install(APP, DIR, unicode=True)

def show_confirm_dialog(widget, message):
    dialog = gtk.MessageDialog(widget, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, message)
    response = dialog.run()
    dialog.destroy()
    if response == gtk.RESPONSE_YES:
        return True
    else:
        return False

def show_error_dialog(widget, message):
    dialog = gtk.MessageDialog(widget, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, message)
    dialog.run()
    dialog.destroy()

def show_exception_dialog(widget, message, details):
    show_details_dialog(widget, gtk.MESSAGE_ERROR, _("Details"), message, details)

def show_output_dialog(widget, message, details):
    show_details_dialog(widget, gtk.MESSAGE_INFO, _("Output"), message, details)

def show_warning_dialog(widget, message, details):
    show_details_dialog(widget, gtk.MESSAGE_WARNING, _("Details"), message, details)

def show_details_dialog(widget, type, details_label, message, details):
    dialog = gtk.MessageDialog(widget, gtk.DIALOG_MODAL, type, gtk.BUTTONS_CLOSE, message)
    dialog.set_resizable(True)
    expander = gtk.Expander(details_label)
    dialog.vbox.pack_start(expander)
    expander.show()
    details_area = gtk.TextView()
    details_area.get_buffer().set_text(details)
    details_area.show()
    scroll_area = gtk.ScrolledWindow()
    scroll_area.set_shadow_type(gtk.SHADOW_NONE)
    scroll_area.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    if details_area.set_scroll_adjustments(scroll_area.get_hadjustment(),
                                           scroll_area.get_vadjustment()):
        scroll_area.add(details_area)
    else:
        scroll_area.add_with_viewport(details_area)
    expander.add(scroll_area)
    scroll_area.show()
    dialog.run()
    dialog.destroy()

def get_password_dialog(widget, user, error):
    dialog = gtk.MessageDialog(widget, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_OK_CANCEL, None)
    dialog.set_markup(_("Please enter the password of user %s") % user)
    if error == True:
	dialog.format_secondary_markup("<span foreground='red'>" + _("The password you entered did not match!") + "</span>")
    dialog.set_resizable(False)
    dialog.set_default_response(gtk.RESPONSE_OK)
    password_entry = gtk.Entry(max=255)
    password_entry.set_visibility(False)
    password_entry.set_activates_default(gtk.TRUE)
    dialog.vbox.pack_start(password_entry, False, False, 2)
    password_entry.show()
    response = dialog.run()
    password = None
    if response == gtk.RESPONSE_OK:
        password = password_entry.get_text()
    dialog.destroy()
    return password

def authenticate(user, password):
    def get_pass(authx, query_list, user_data):
        resp = []
        resp.append((password,0))
        return resp
    auth = PAM.pam()
    auth.start('passwd')
    auth.set_item(PAM.PAM_USER, user)
    auth.set_item(PAM.PAM_CONV, get_pass)
    try:
        auth.authenticate()
        auth.acct_mgmt()
    except PAM.error:
        return False
    except:
        raise(BaseException(_("Internal error in PAM authentication module")))
    else:
        return True
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

