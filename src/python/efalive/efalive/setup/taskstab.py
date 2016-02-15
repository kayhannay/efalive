'''
Created on 24.09.2015

Copyright (C) 2015-2015 Kay Hannay

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
import pygtk
import gobject
pygtk.require('2.0')
import gtk
import logging
import gettext

from ..common import common

APP="TasksTab"
gettext.install(APP, common.LOCALEDIR, unicode=True)

class TasksTabModel(object):
    def __init__(self, settings):
        self._logger = logging.getLogger('TasksTabModel')
        self._settings = settings

    def register_hourly_tasks_callback(self, callback):
        self._settings.hourly_tasks.registerObserverCb(callback)

    def register_daily_tasks_callback(self, callback):
        self._settings.daily_tasks.registerObserverCb(callback)

    def register_weekly_tasks_callback(self, callback):
        self._settings.weekly_tasks.registerObserverCb(callback)

    def register_monthly_tasks_callback(self, callback):
        self._settings.monthly_tasks.registerObserverCb(callback)

    def delete_task(self, task_id):
        self._settings.delete_task(task_id)

    def add_task(self, task_type, task_data, task_interval):
        self._settings.add_task(task_type, task_data, task_interval)

    def get_task(self, task_id):
        return self._settings.get_task(task_id)

class TasksTabView(gtk.VBox):
    def __init__(self):
        super(gtk.VBox, self).__init__()
        self._logger = logging.getLogger('TasksTabView')
        self._init_components()

    def _init_components(self):
        self.tasks_hbox = gtk.HBox()
        self.pack_start(self.tasks_hbox, True, True, 2)
        self.tasks_hbox.show()

        self.task_list_store = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING)

        self.task_list_cell = gtk.CellRendererText()
        self.task_list_cell.set_property('background-gdk', gtk.gdk.Color(red=50000, green=50000, blue=50000))
        self.task_list_column = gtk.TreeViewColumn(_("Task list"), self.task_list_cell, markup=1)

        self.task_list_id_cell = gtk.CellRendererText()
        self.task_list_id_column = gtk.TreeViewColumn('Id', self.task_list_id_cell, markup=0)
        self.task_list_id_column.set_visible(False)

        self.tasks_scoll_window = gtk.ScrolledWindow()
        self.tasks_hbox.pack_start(self.tasks_scoll_window, True, True, 2)
        self.tasks_scoll_window.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self.tasks_scoll_window.show()

        self.task_list = gtk.TreeView(self.task_list_store)
        selection = self.task_list.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        self.tasks_scoll_window.add(self.task_list) # pack_start(self.task_list, True, True, 2)
        self.task_list.show()
        self.task_list.append_column(self.task_list_id_column)
        self.task_list.append_column(self.task_list_column)

        self.task_button_vbox = gtk.VBox()
        self.tasks_hbox.pack_start(self.task_button_vbox, False, False, 2)
        self.task_button_vbox.show()

        self.task_add_button = gtk.Button()
        button_icon = gtk.image_new_from_file(common.get_icon_path("plus.png"))
        self.task_add_button.set_image(button_icon)
        self.task_add_button.set_tooltip_text(_("Add a new task"))
        self.task_button_vbox.pack_start(self.task_add_button, False, False, 2)
        self.task_add_button.show()

        self.task_edit_button = gtk.Button()
        button_icon = gtk.image_new_from_file(common.get_icon_path("settings.png"))
        self.task_edit_button.set_image(button_icon)
        self.task_edit_button.set_tooltip_text(_("Edit task"))
        self.task_button_vbox.pack_start(self.task_edit_button, False, False, 2)
        self.task_edit_button.show()

        self.task_del_button = gtk.Button()
        button_icon = gtk.image_new_from_file(common.get_icon_path("minus.png"))
        self.task_del_button.set_image(button_icon)
        self.task_del_button.set_tooltip_text(_("Remove task"))
        self.task_button_vbox.pack_start(self.task_del_button, False, False, 2)
        self.task_del_button.show()

class TasksTabController(object):
    def __init__(self, settings):
        self._logger = logging.getLogger('TasksTabController')
        
        self._view = TasksTabView()
        self._view.task_del_button.set_sensitive(False)
        self._view.task_edit_button.set_sensitive(False)
        
        self._model = TasksTabModel(settings)
        self._init_events()

    def _init_events(self):
        self._model.register_hourly_tasks_callback(self.a_task_list_changed)
        self._model.register_daily_tasks_callback(self.a_task_list_changed)
        self._model.register_weekly_tasks_callback(self.a_task_list_changed)
        self._model.register_monthly_tasks_callback(self.a_task_list_changed)
        self._view.task_add_button.connect("clicked", self.add_task)
        self._view.task_edit_button.connect("clicked", self.edit_task)
        self._view.task_del_button.connect("clicked", self.delete_task)
        self._view.task_list.get_selection().connect("changed", self.task_selection_changed)

    def get_view(self):
        return self._view

    def addTaskToView(self, task_hash, task_type, task_frequency, task_description):
        self._view.task_list_store.append([task_hash, "<b>%s</b> %s\n<i>%s</i>" % (task_type, task_frequency, task_description)])

    def a_task_list_changed(self, task_list):
        self._view.task_list_store.clear()
        self._process_task_list(_("Hourly"), self._model._settings.hourly_tasks.getData())
        self._process_task_list(_("Daily"), self._model._settings.daily_tasks.getData())
        self._process_task_list(_("Weekly"), self._model._settings.weekly_tasks.getData())
        self._process_task_list(_("Monthly"), self._model._settings.monthly_tasks.getData())

    def task_selection_changed(self, selection):
        if selection.count_selected_rows() < 1:
            self._view.task_del_button.set_sensitive(False)
            self._view.task_edit_button.set_sensitive(False)
        else:
            self._view.task_del_button.set_sensitive(True)
            self._view.task_edit_button.set_sensitive(True)

    def _process_task_list(self, task_frequency, tasks):
        if tasks == None:
            return
        for task_id in tasks.keys():
            task = tasks.get(task_id)
            if task[0] == "BACKUP_MAIL":
                task_type = _("Backup")
            elif task[0] == "SHELL":
                task_type = _("Shell")
            else:
                task_type = task[0]
            self.addTaskToView(task_id, task_type, task_frequency, task[1])

    def delete_task(self, widget):
        selection = self._view.task_list.get_selection()
        tree_model, tree_iter = selection.get_selected()
        task_id = tree_model.get_value(tree_iter, 0)
        self._logger.info("Delete task %s" % task_id)
        self._model.delete_task(task_id)
        
    def add_task(self, widget):
        editor = TaskEditor(self._view.get_toplevel())
        response = editor.run()
        if response == gtk.RESPONSE_OK:
            active_type = editor.task_type_combo.get_active()
            if active_type == 0:
                task_type = "BACKUP_MAIL"
                text = editor.backup_task_input.get_text()
            else:
                task_type = "SHELL"
                text = editor.script_task_input.get_text()
            interval = editor.task_interval_combo.get_active()
            if interval == 0:
                task_interval = "HOURLY"
            elif interval == 1:
                task_interval = "DAILY"
            elif interval == 2:
                task_interval = "WEEKLY"
            elif interval == 3:
                task_interval = "MONTHLY"
            self._logger.info("Save new task '%s' '%s' '%s'" % (task_type, text, task_interval))
            self._model.add_task(task_type, text, task_interval)
        editor.destroy()

    def edit_task(self, widget):
        selection = self._view.task_list.get_selection()
        tree_model, tree_iter = selection.get_selected()
        task_id = tree_model.get_value(tree_iter, 0)
        task_interval, task = self._model.get_task(task_id)

        editor = TaskEditor(self._view.get_toplevel())
        self._logger.info("Edit task: %s" % task)
        if task[0] == "BACKUP_MAIL":
            combo_index = 0
            input_field = editor.backup_task_input
        elif task[0] == "SHELL":
            combo_index = 1
            input_field = editor.script_task_input
        if task_interval == "HOURLY":
            interval_combo_index = 0
        elif task_interval == "DAILY":
            interval_combo_index = 1
        elif task_interval == "WEEKLY":
            interval_combo_index = 2
        elif task_interval == "MONTHLY":
            interval_combo_index = 3
        editor.task_type_combo.set_active(combo_index)
        input_field.set_text(task[1])
        editor.task_interval_combo.set_active(interval_combo_index)
        response = editor.run()
        if response == gtk.RESPONSE_OK:
            active_type = editor.task_type_combo.get_active()
            if active_type == 0:
                task_type = "BACKUP_MAIL"
                text = editor.backup_task_input.get_text()
            else:
                task_type = "SHELL"
                text = editor.script_task_input.get_text()
            interval = editor.task_interval_combo.get_active()
            if interval == 0:
                task_interval = "HOURLY"
            elif interval == 1:
                task_interval = "DAILY"
            elif interval == 2:
                task_interval = "WEEKLY"
            elif interval == 3:
                task_interval = "MONTHLY"
            self._logger.info("Save changed task '%s' '%s' '%s'" % (task_type, text, task_interval))
            self._model.delete_task(task_id)
            self._model.add_task(task_type, text, task_interval)
        editor.destroy()

class TaskEditor(gtk.Dialog):
    def __init__(self, widget):
        gtk.Dialog.__init__(self, _("Task editor"), widget)
        
        self.main_container_vbox = gtk.VBox()
        self.vbox.pack_start(self.main_container_vbox, False, False, 5)
        self.main_container_vbox.show()
        
        self.task_type_select_hbox = gtk.HBox()
        self.main_container_vbox.pack_start(self.task_type_select_hbox, False, False, 2)
        self.task_type_select_hbox.show()

        self.task_type_label = gtk.Label(_("Type"))
        self.task_type_select_hbox.pack_start(self.task_type_label, False, False, 2)
        self.task_type_label.show()

        self.task_type_combo = gtk.combo_box_new_text()
        self.task_type_select_hbox.pack_end(self.task_type_combo, False, False, 2)
        self.task_type_combo.show()
        self.task_type_combo.append_text(_("Backup"))
        self.task_type_combo.append_text(_("Shell"))
        self.task_type_combo.connect("changed", self.task_type_changed)

        self.task_edit_vbox = gtk.VBox()
        self.main_container_vbox.pack_start(self.task_edit_vbox, True, True, 2)
        self.task_edit_vbox.show()

        self.script_task_hbox = gtk.HBox()
        self.task_edit_vbox.pack_start(self.script_task_hbox, True, True, 2)
        self.script_task_label = gtk.Label(_("Command"))
        self.script_task_hbox.pack_start(self.script_task_label, False, False, 2)
        self.script_task_label.show()
        self.script_task_input = gtk.Entry(max=255)
        self.script_task_hbox.pack_end(self.script_task_input, True, True, 2)
        self.script_task_input.show()

        self.backup_task_hbox = gtk.HBox()
        self.task_edit_vbox.pack_start(self.backup_task_hbox, True, True, 2)
        self.backup_task_label = gtk.Label(_("Recipient"))
        self.backup_task_hbox.pack_start(self.backup_task_label, False, False, 2)
        self.backup_task_label.show()
        self.backup_task_input = gtk.Entry(max=255)
        self.backup_task_hbox.pack_end(self.backup_task_input, True, True, 2)
        self.backup_task_input.show()

        self.task_interval_select_hbox = gtk.HBox()
        self.main_container_vbox.pack_start(self.task_interval_select_hbox, False, False, 2)
        self.task_interval_select_hbox.show()

        self.task_interval_label = gtk.Label(_("Interval"))
        self.task_interval_select_hbox.pack_start(self.task_interval_label, False, False, 2)
        self.task_interval_label.show()

        self.task_interval_combo = gtk.combo_box_new_text()
        self.task_interval_select_hbox.pack_end(self.task_interval_combo, False, False, 2)
        self.task_interval_combo.show()
        self.task_interval_combo.append_text(_("Hourly"))
        self.task_interval_combo.append_text(_("Daily"))
        self.task_interval_combo.append_text(_("Weekly"))
        self.task_interval_combo.append_text(_("Monthly"))

        self.task_interval_combo.set_active(0)
        self.current_editor = self.backup_task_hbox
        self.task_type_combo.set_active(0)

        self.add_button(_("Cancel"), gtk.RESPONSE_CANCEL)
        self.add_button(_("Ok"), gtk.RESPONSE_OK)

    def task_type_changed(self, widget):
        task_type = widget.get_active()
        self.current_editor.hide()
        if task_type == 0:
            self.current_editor = self.backup_task_hbox
        elif task_type == 1:
            self.current_editor = self.script_task_hbox
        self.current_editor.show()

