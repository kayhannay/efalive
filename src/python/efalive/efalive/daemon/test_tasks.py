#!/usr/bin/python
'''
Created on 27.04.2015

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
import unittest
from mock import call, patch, MagicMock

from tasks import ShellTask
from efalive.common import common

class ShellTaskTestCase(unittest.TestCase):

    def test_run(self):
        common.command_output = MagicMock(return_value = (0, "testfile.txt"))

        class_under_test = ShellTask("123def", "ls /tmp")
        class_under_test.run()

        self.assertEqual(1, common.command_output.call_count)
        self.assertEqual(call(["ls", "/tmp"]), common.command_output.call_args)

