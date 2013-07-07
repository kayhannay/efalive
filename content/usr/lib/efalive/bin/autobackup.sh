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
# Copyright 2008-2013 Kay Hannay <klinux@hannay.de>
#
###
#
# Automatic backup of efa data to an USB stick
# Usage: autobackup.sh [-q] [-d DELAY] <DEVICE>
#
# Where DEVICE is a mountable device and DELAY the time this script should
# wait before it starts the backup in seconds. With -q you can supress the 
# beep sound that is normally played and the dialog for an error or success.
#

/bin/date

if [ "x$LANG" = "x" ]
then
    export LANG=C.UTF-8
fi

BEEP_ERROR="/usr/bin/beep -f 2000 -r 5 -d 50 -l 1000"
BEEP_SUCCESS="/usr/bin/beep -f 1000 -r 3 -d 50"

QUIET="FALSE"
AUTO_USB_BACKUP_DIALOG="TRUE"

function inform_success {
	/bin/echo "$1"
    	if [ "x$AUTO_USB_BACKUP_DIALOG" = "xTRUE" ]
    	then
        	/usr/bin/zenity --info --text="Autobackup: $1"
    	fi
	if [ "x$QUIET" = "xFALSE" ]
	then
		$BEEP_SUCCESS
	fi
}

function inform_error {
	/bin/echo "$1"
    	if [ "x$AUTO_USB_BACKUP_DIALOG" = "xTRUE" ]
    	then
        	/usr/bin/zenity --error --text="Autobackup: $1"
    	fi
	if [ "x$QUIET" = "xFALSE" ]
	then
		$BEEP_ERROR
	fi
}

export DISPLAY=:0.0
if [ -f ~/.efalive/settings.conf ]
then
    . ~/.efalive/settings.conf
fi 

while getopts :hd:q opt; do
  case $opt in
	q)
		QUIET="TRUE"
		AUTO_USB_BACKUP_DIALOG="FALSE"
		;;
	d)
		if [[ $OPTARG =~ ^[0-9]+ ]]
		then
			/bin/echo "Wait for $OPTARG seconds ..."
			/bin/sleep $OPTARG
		else
			inform_error "Error, specified delay (-d) is not a number!"
			exit 1
		fi
		;;
	*)
		/bin/echo -e "Unknown argument: -$OPTARG\n"
		/bin/echo "Usage: autobackup.sh [-q] [-d DELAY] <DEVICE>"
		/bin/echo -e '\nWhere DEVICE is a mountable device and DELAY the time this script should'\
			     '\nwait before it starts the backup in seconds. With -q you can supress the'\
			     '\nbeep sound that is normally played and the dialog for an error or success.\n'
		inform_error "Unknown argument: -$OPTARG"
		exit 1
		;;
  esac
done
shift $((OPTIND-1))

if [ ! $1 ]
then
	inform_error "Error, no backup device specified!"
	exit 1
fi

if [ ! -b $1 ]
then
	inform_error "Error, specified device does not exist!"
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
    inform_error "Backup failed, error code: $BACKUP_RESULT !\n\nView autobackup.log for details."
else
    inform_success "Backup successful."
fi
exit $BACKUP_RESULT
