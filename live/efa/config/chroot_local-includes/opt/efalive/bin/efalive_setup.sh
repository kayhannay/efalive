#!/bin/bash
#
#

#EFALIVE_DIR=/opt/efalive/etc
EFALIVE_USR_DIR=~/.efalive
EFALIVE_VERSION=$EFALIVE_USR_DIR/version.conf
EFALIVE_BACKUP=$EFALIVE_USR_DIR/backup.conf

#if [ ! -d $EFALIVE_DIR ]
#then
#	mkdir -p $EFALIVE_DIR
#fi

if [ ! -d $EFALIVE_USR_DIR ]
then
	mkdir -p $EFALIVE_USR_DIR
fi

zenity --question --text="Wollen Sie das experimentelle efa 2 benutzen?"
if [ $? -ne 0 ]
then
	echo "EFA_VERSION=1" > $EFALIVE_VERSION
	echo "EFA_BACKUP_PATHS=\"/opt/efa/daten /home/efa/efa\"" > $EFALIVE_BACKUP
else
	echo "EFA_VERSION=2" > $EFALIVE_VERSION
	echo "EFA_BACKUP_PATHS=\"/opt/efa2/data /home/efa/efa\"" > $EFALIVE_BACKUP
fi


