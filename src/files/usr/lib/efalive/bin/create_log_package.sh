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
# Create a ZIP package that contains the most important efaLive log files.
# Usage: create_log_package.sh <TARGET_DIR>
#
# Where TARGET_DIR is the directory where the ZIP file should be stored.
#

if [ ! $1 ]
then
	/bin/echo "Error, please specify a target directory for the log ZIP file!"
	exit 1
fi
if [ ! -d $1 ]
then
	/bin/echo "Error, please specify a target directory for the log ZIP file!"
	exit 1
fi

TIMESTAMP=`/bin/date +%Y%m%d_%H%M%S`
ZIP_FILE="efaLive_logPackage_${TIMESTAMP}.zip"
PWD=`/bin/pwd`
USER=`/usr/bin/id -un`
TMP_PATH=/tmp/log_package

/bin/mkdir $TMP_PATH
/bin/mkdir ${TMP_PATH}/system
/bin/mkdir ${TMP_PATH}/efa
/bin/mkdir ${TMP_PATH}/efalive

sudo /usr/lib/efalive/bin/copy_log_files.sh ${TMP_PATH}/system $USER
/bin/dmesg > ${TMP_PATH}/system/dmesg.log
cp ~/*.log ${TMP_PATH}/efalive
cp ~/efa2/log/*.log ${TMP_PATH}/efa

cd $TMP_PATH
/usr/bin/zip -r $ZIP_FILE *
/bin/mv $ZIP_FILE $1
cd $PWD
/bin/rm -r $TMP_PATH

exit 0

