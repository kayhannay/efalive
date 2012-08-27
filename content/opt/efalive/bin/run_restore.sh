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
# Restore efa backup
# Usage: run_restore.sh <BACKUP_ZIP_FILE>
#

EFA_BACKUP_PATHS="/opt/efa/ausgabe/layout /opt/efa/daten /home/efa/efa"
EFALIVE_BACKUP_PATHS="/home/efa/.efalive"
EFA_USER=efa
EFA_GROUP=efa

if [ -f ~/.efalive/settings.conf ]
then
    . ~/.efalive/settings.conf
else
    /bin/echo "efaLive has not been configured yet!"
    exit 1000
fi

if [ ! $1 ]
then
	/bin/echo "Error, no backup file specified!"
	exit 1001
fi

if [ ! -f $1 ]
then
	/bin/echo "Error, backup file does not exist!"
	exit 1002
fi

### Delete old backup of existing data, if exists
if [ -e ~/backup/restore_backup ]
then
    /bin/echo "Removing old restore backup ..."
	/bin/rm -Rf ~/backup/restore_backup
fi

### Create backup of existing data
/bin/echo "Creating backup of existing data ..."
/bin/mkdir -p ~/backup/restore_backup
run_backup.sh ~/backup/restore_backup

if [[ "$1" =~ ^/.* ]]
then
    BACKUP_FILE=$1
else
    BACKUP_FILE=`pwd`"/$1"
fi

### Remove old data
if [ $EFA_VERSION -eq 2 ]
then
    #check if an efa or an efaLive backup file was selected
    if [[ "$BACKUP_FILE" =~ .*/efaLive_backup_[0-9]{8}_[0-9]{6}\.zip ]]
    then
        #remove "efaLive_backup_" (and parent directory, if required)
        BACKUP_TIMESTAMP=${BACKUP_FILE#*"efaLive_backup_"}
        BACKUP_TIMESTAMP=${BACKUP_TIMESTAMP#*"efaLive_backup_"}
        #remove .zip ending
        BACKUP_TIMESTAMP=${BACKUP_TIMESTAMP%".zip"*}
        BACKUP_DIR=${BACKUP_FILE%"efaLive_backup_${BACKUP_TIMESTAMP}.zip"*}
    elif [[ "$BACKUP_FILE" =~ .*/efa_backup_[0-9]{8}_[0-9]{6}\.zip ]]
    then
        #remove "efaLive_backup_" (and parent directory, if required)
        BACKUP_TIMESTAMP=${BACKUP_FILE#*"efa_backup_"}
        BACKUP_TIMESTAMP=${BACKUP_TIMESTAMP#*"efa_backup_"}
        #remove .zip ending
        BACKUP_TIMESTAMP=${BACKUP_TIMESTAMP%".zip"*}
        BACKUP_DIR=${BACKUP_FILE%"efa_backup_${BACKUP_TIMESTAMP}.zip"*}
    else
        /bin/echo "Error, specified file is not an efaLive oder efa backup zip file!"
        exit 1003
    fi

    cd /
    /bin/rm -Rf $EFALIVE_BACKUP_PATHS
    EFALIVE_BACKUP_FILE=${BACKUP_DIR}efaLive_backup_${BACKUP_TIMESTAMP}.zip
    /bin/echo "Restoring efaLive backup from $EFALIVE_BACKUP_FILE ..."
    /usr/bin/unzip -o $EFALIVE_BACKUP_FILE 
    /bin/chown -R $EFA_USER:$EFA_GROUP $EFALIVE_BACKUP_PATHS
    EFA_BACKUP_FILE=${BACKUP_DIR}efa_backup_${BACKUP_TIMESTAMP}.zip
    /bin/echo "Restoring efa backup from $EFA_BACKUP_FILE ..."
    EFA_CRED=$EFA_CREDENTIALS_FILE /opt/efa2/efaCLI.sh efalive@localhost:$EFA_PORT -cmd "backup restore $EFA_BACKUP_FILE"
    CLI_RETURNCODE=$?
    if [ $CLI_RETURNCODE -ne 0 ]
    then
        /bin/echo "Error, could not restore efa backup ($CLI_RETURNCODE)!"
    else
        /bin/echo "Restore finished."
    fi
    exit $CLI_RETURNCODE
else
    cd /
    /bin/rm -Rf $EFA_BACKUP_PATHS
    /usr/bin/unzip -o $BACKUP_FILE
    /bin/chown -R $EFA_USER.$EFA_GROUP $EFA_BACKUP_PATHS
    /bin/echo "Restore finished."
    exit 0
fi

