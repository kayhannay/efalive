#!/usr/bin/python
'''
Created on 03.01.2012

Copyright (C) 2012 Kay Hannay

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
import gtk
import os
import sys 
import subprocess
import traceback
import time

import dialogs
import common
from observable import Observable

import locale
import gettext
APP="dateTime"
LOCALEDIR=os.path.join(os.path.dirname(sys.argv[0]), "locale")
DIR=os.path.realpath(LOCALEDIR)
gettext.install(APP, DIR, unicode=True)

import logging

class DateTimeModel(object):
    def __init__(self):
        self._logger = logging.getLogger('datetime.DateTimeModel')
        self.hour = Observable()
        self.minute = Observable()
        self.second = Observable()
        self.day = Observable()
        self.month = Observable()
        self.year = Observable()
        self.ntp = Observable()

    def initModel(self):
        localtime = time.localtime(time.time())
        self.hour.updateData(localtime[3])
        self.minute.updateData(localtime[4])
        self.second.updateData(localtime[5])
        self.day.updateData(localtime[2])
        self.month.updateData(localtime[1])
        self.year.updateData(localtime[0])
        self.ntp.updateData(self._check_ntp())

    def _check_ntp(self):
        try:
            (returncode, ntp_output) = common.command_output(["grep", "-l", "ntp", "/etc/init.d/.depend.start"])
        except OSError as error:
            message = _("Could not check NTP service status: %s") % error
            dialogs.show_exception_dialog(self._view, message, traceback.format_exc())
        if ntp_output == None or ntp_output == "":
            return False
        else:
            return True

    def set_hour(self, hour):
        self.hour.updateData(hour)

    def set_minute(self, minute):
        self.minute.updateData(minute)

    def set_second(self, second):
        self.second.updateData(second)

    def set_day(self, day):
        self.day.updateData(day)

    def set_month(self, month):
        self.month.updateData(month)

    def set_year(self, year):
        self.year.updateData(year)

    def set_ntp(self, enable):
        self.ntp.updateData(enable)

    def save(self):
        if self.ntp.getData() == True:
            self._logger.info("Enable NTP service")
            try:
                subprocess.Popen(['sudo', 'insserv', '-d', 'ntp'])
            except OSError as error:
                message = _("Could not enable NTP service: %s") % error
                self._logger.error(message)
                dialogs.show_exception_dialog(self._view, message, traceback.format_exc())
        else:
            date = "%02d%02d%02d%02d%04d.%02d" % (self.month.getData(), self.day.getData(), self.hour.getData(), self.minute.getData(), self.year.getData(), self.second.getData())
            self._logger.info("Setting date to %s" % date)
            try:
                subprocess.Popen(['sudo', 'insserv', '-r', 'ntp'])
            except OSError as error:
                message = _("Could not disable NTP service: %s") % error
                self._logger.error(message)
                dialogs.show_exception_dialog(self._view, message, traceback.format_exc())
            try:
                subprocess.Popen(['sudo', 'date', date])
            except OSError as error:
                message = _("Could not set time: %s") % error
                self._logger.error(message)
                dialogs.show_exception_dialog(self._view, message, traceback.format_exc())


class DateTimeView(gtk.Window):
    def __init__(self, type, controller=None):
        self._logger = logging.getLogger('datetime.DateTimeView')
        gtk.Window.__init__(self, type)
        self.set_title(_("Date & Time"))
        self.set_border_width(5)
        self._controller = controller

        self.initComponents()

    def initComponents(self):
        main_box=gtk.VBox(False, 2)
        self.add(main_box)
        main_box.show()

        calendar_box = gtk.HBox(False, 0)
        main_box.pack_start(calendar_box, False, False)
        calendar_box.show()

        self.calendar = gtk.Calendar()
        calendar_box.pack_start(self.calendar, True, True, 0)
        self.calendar.show()

        time_box = gtk.HBox(False, 2)
        main_box.pack_start(time_box, False, False)
        time_box.show()

        self.time_label = gtk.Label(_("Time (h m s)"))
        time_box.pack_start(self.time_label, True, True, 2)
        self.time_label.show()

        second_adjustment = gtk.Adjustment(0, 0, 59, 1, 10)
        self.second_button = gtk.SpinButton(second_adjustment)
        self.second_button.set_wrap(True)
        time_box.pack_end(self.second_button, False, False)
        self.second_button.show()

        minute_adjustment = gtk.Adjustment(0, 0, 59, 1, 10)
        self.minute_button = gtk.SpinButton(minute_adjustment)
        self.minute_button.set_wrap(True)
        time_box.pack_end(self.minute_button, False, False)
        self.minute_button.show()

        hour_adjustment = gtk.Adjustment(0, 0, 23, 1, 10)
        self.hour_button = gtk.SpinButton(hour_adjustment)
        self.hour_button.set_wrap(True)
        time_box.pack_end(self.hour_button, False, False)
        self.hour_button.show()

        ntp_frame=gtk.Frame(_("Network time protocol"))
        main_box.pack_start(ntp_frame, False, False, 2)
        ntp_frame.show()

        ntp_box = gtk.HBox(False, 2)
        ntp_frame.add(ntp_box)
        ntp_box.show()

        self.ntp_checkbox = gtk.CheckButton(_("Use network time protocol (NTP)"))
        ntp_box.pack_start(self.ntp_checkbox, False, False)
        self.ntp_checkbox.show()

        button_box = gtk.HBox(False, 2)
        main_box.pack_end(button_box, False, False)
        button_box.show()

        save_button = gtk.Button(_("Ok"))
        button_box.pack_end(save_button, False, False, 2)
        save_button.show()
        save_button.connect("clicked", self._controller.save)

        cancel_button = gtk.Button(_("Cancel"))
        button_box.pack_end(cancel_button, False, False, 2)
        cancel_button.show()
        cancel_button.connect("clicked", self._controller.cancel)

class DateTimeController(object):
    def __init__(self, argv, model=None, view=None, standalone=True, confPath=None):
        self._logger = logging.getLogger('datetime.DateTimeController')
        if argv and (len(argv) > 1):
            confPath=argv[1]
        self._confPath = confPath
        if(model==None):
            self._model=DateTimeModel()
        else:
            self._model=model
        if(view==None):
            self._view=DateTimeView(gtk.WINDOW_TOPLEVEL, self)
        else:
            self._view=view
        self._model.hour.registerObserverCb(self.hour_changed)
        self._model.minute.registerObserverCb(self.minute_changed)
        self._model.second.registerObserverCb(self.second_changed)
        self._model.day.registerObserverCb(self.day_changed)
        self._model.month.registerObserverCb(self.month_changed)
        self._model.year.registerObserverCb(self.year_changed)
        self._model.ntp.registerObserverCb(self.ntp_changed)
        self.init_events(standalone)
        self._model.initModel()
        self._view.show()
        
    def init_events(self, standalone):
        if standalone:
            self._view.connect('destroy', gtk.main_quit)
        self._view.ntp_checkbox.connect('toggled', self.ntp_toggled)

    def save(self, widget):
        date = self._view.calendar.get_date()
        self._model.set_day(date[2])
        self._model.set_month(date[1] + 1)
        self._model.set_year(date[0])
        self._model.set_hour(self._view.hour_button.get_value())
        self._model.set_minute(self._view.minute_button.get_value())
        self._model.set_second(self._view.second_button.get_value())
        self._model.set_ntp(self._view.ntp_checkbox.get_active())
        self._model.save()
        self._view.destroy()

    def cancel(self, widget):
        self._view.destroy()

    def ntp_toggled(self, widget):
        active = widget.get_active()
        self._view.calendar.set_sensitive(not active)
        self._view.hour_button.set_sensitive(not active)
        self._view.minute_button.set_sensitive(not active)
        self._view.second_button.set_sensitive(not active)
        self._view.time_label.set_sensitive(not active)

    def hour_changed(self, hour):
        self._view.hour_button.set_value(hour)

    def minute_changed(self, minute):
        self._view.minute_button.set_value(minute)

    def second_changed(self, second):
        self._view.second_button.set_value(second)

    def day_changed(self, day):
        self._view.calendar.select_day(day)

    def month_changed(self, month):
        self._view.calendar.select_month(month - 1, self._view.calendar.get_date()[0])

    def year_changed(self, year):
        self._view.calendar.select_month(self._view.calendar.get_date()[1], year)

    def ntp_changed(self, enable):
        self._view.ntp_checkbox.set_active(enable)

if __name__ == '__main__':
    logging.basicConfig(filename='dateTime.log',level=logging.INFO)
    controller = DateTimeController(sys.argv)
    gtk.main();

    

