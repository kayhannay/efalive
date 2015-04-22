#!/bin/bash
#
####
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2013-2015 Kay Hannay <klinux@hannay.de>
#
###
#
# Copy a fix set of lg files to the specified directory and change the
# owner of that directory to the specified user.
# Usage: copy_log_files.sh <TARGET_DIR> <USER>
#
# Where TARGET_DIR is the directory where the log files should be stored.
#

if [ ! $1 ]
then
	/bin/echo "Error, please specify a target directory for the log files!"
	exit 1
fi
if [ ! -d $1 ]
then
	/bin/echo "Error, please specify a target directory for the log files!"
	exit 1
fi

if [ ! $2 ]
then
	/bin/echo "Error, please specify a user name to set proper rights for the log files!"
	exit 1
fi

/bin/cp /var/log/syslog /var/log/Xorg.0.log /var/log/mail.* /var/log/auth.log $1
/bin/chown $2:users $1/*
/bin/chmod 644 $1/*

