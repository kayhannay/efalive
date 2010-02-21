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
# Restore efa backup
# Usage: run_restore.sh <BACKUP_ZIP_FILE>
#
EFA_DIR=/opt/efa
EFA_BACKUP_PATHS="/opt/efa/ausgabe/layout /opt/efa/daten /home/efa/efa/cfg /home/efa/efa/daten"
EFA_USER=efa
EFA_GROUP=efa

if [ ! $1 ]
then
	/bin/echo "Error, no backup file specified!"
	exit 1
fi

if [ ! -f $1 ]
then
	/bin/echo "Error, backup file does not exist!"
	exit 1
fi

### Delete old backup of existing data, if exists
if [ -e $EFA_DIR/backup/restore_backup ]
then
	/bin/rm -Rf $EFA_DIR/backup/restore_backup
fi

### Create backup of existing data
/bin/mkdir $EFA_DIR/backup/restore_backup
run_backup.sh $EFA_DIR/backup/restore_backup
cd /
/usr/bin/zip -r $EFA_DIR/backup/restore_backup/Restore_`/bin/date +%Y%m%d_%k%M%S`.zip $EFA_BACKUP_PATHS

### Remove old data
cd /
/bin/rm -Rf $EFA_BACKUP_PATHS

### Restore backup file to efa directory
cd /
/usr/bin/unzip $1
/bin/chown -R $EFA_USER.$EFA_GROUP $EFA_BACKUP_PATHS

/bin/echo "Restore finished."
