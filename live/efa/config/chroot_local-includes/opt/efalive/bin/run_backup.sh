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
# Copyright 2008-2010 Kay Hannay <klinux@hannay.de>
#
###
#
# Create backup of efa data to a ZIP file
# Usage: run_backup.sh <PATH_TO_STORE_BACKUP>
#
EFA_BACKUP_PATHS="/opt/efa/ausgabe/layout /opt/efa/daten /home/efa/efa"
BACKUP_FILE=Sicherung_`/bin/date +%Y%m%d_%k%M%S`.zip

. /home/efa/.efalive/backup.conf

### Sleep a while until the device is mounted completely
/bin/sleep 5


if [ ! $1 ]
then
	/bin/echo "Error, no backup path specified!"
	/usr/bin/beep -f 2000 -r 5 -d 50 -l 1000
	exit 1
fi

if [ ! -d $1 ]
then
	/bin/echo "Error, specified path does not exist!"
	/usr/bin/beep -f 2000 -r 5 -d 50 -l 1000
	exit 1
fi

### Create backup
cd /
/usr/bin/zip -r $1/$BACKUP_FILE $EFA_BACKUP_PATHS
### Make sure that all data are transferred to the device
/bin/sync
### Some sticks need more time to write all data ...
/bin/sleep 5
/bin/sync
/bin/sleep 5
/bin/sync

if [ -e $1/$BACKUP_FILE ]
then
	### Play a sound to inform that the backup is finished (3 short beep)
	/usr/bin/beep -f 1000 -r 3 -d 50
else
	### Backup was not successfull, play error sound (5 long beep)
	/usr/bin/beep -f 2000 -r 5 -d 50 -l 1000
	/bin/echo "Error, backup was not successful"
fi

