#!/bin/bash


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

