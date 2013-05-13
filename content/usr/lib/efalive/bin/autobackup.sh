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
# Copyright 2008-2012 Kay Hannay <klinux@hannay.de>
#
###
#
# Automatic backup of efa data to an USB stick
# Usage: autobackup.sh <DEVICE>
#

if [ "x$LANG" = "x" ]
then
    export LANG=C.UTF-8
fi

BEEP_ERROR="/usr/bin/beep -f 2000 -r 5 -d 50 -l 1000"
BEEP_SUCCESS="/usr/bin/beep -f 1000 -r 3 -d 50"

AUTO_USB_BACKUP_DIALOG="TRUE"
export DISPLAY=:0.0
if [ -f ~/.efalive/settings.conf ]
then
    . ~/.efalive/settings.conf
fi 


if [ ! $1 ]
then
	/bin/echo "Error, no backup device specified!"
	$BEEP_ERROR
	exit 1
fi

if [ ! -b $1 ]
then
	/bin/echo "Error, specified device does not exist!"
	$BEEP_ERROR
	exit 1
fi

/bin/echo "Mounting $1 to /media/backup..."
/usr/bin/pmount $1 backup
/bin/echo "Creating backup to /media/backup..."
efalive-backup /media/backup
BACKUP_RESULT=$?
/bin/echo "Unmounting $1..."
/usr/bin/pumount backup

if [ $BACKUP_RESULT -ne 0 ]
then
    if [ $BACKUP_RESULT -eq 1 ] || [ $BACKUP_RESULT -eq 5 ]
    then
        /bin/echo "Login to efa2 server failed, please check that the efaLive administrator is created in efa2 configuration"
    fi
    /bin/echo "Error, backup failed!"
    $BEEP_ERROR
    if [ "x$AUTO_USB_BACKUP_DIALOG" = "xTRUE" ]
    then
        /usr/bin/zenity --error --text="Backup failed, error code: $BACKUP_RESULT !\n\nView autobackup.log for details."
    fi
else
    /bin/echo "Backup successful."
    $BEEP_SUCCESS
    if [ "x$AUTO_USB_BACKUP_DIALOG" = "xTRUE" ]
    then
        /usr/bin/zenity --info --text="Backup successful."
    fi
fi
exit $BACKUP_RESULT
