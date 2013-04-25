#! /bin/sh
### BEGIN INIT INFO
# Provides:          efa
# Required-Start:    $local_fs $remote_fs
# Required-Stop:     $local_fs $remote_fs
# Should-Start:	     console-screen acpid dbus hal
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: EFA - electronic logbook
# Description:       EFA is a electronic logbook for rowing and canoeing clubs. 
### END INIT INFO

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
DAEMON=/usr/bin/startx
NAME=efa
PROCESS=xinit
DAEMONUSER=efa
DAEMONGROUP=efa
DESC="electronic logbook"
DAEMON_OPTS="-- -br"

HALEVT_DAEMON=/usr/bin/halevt
HALEVT_PIDFILE=/tmp/${NAME}_halevt.pid
HALEVT_DAEMON_OPTS="-p $HALEVT_PIDFILE -c /home/efa/.halevt/efaLive.xml"

. /lib/lsb/init-functions

AUTO_USB_BACKUP="FALSE"
if [ -f /home/efa/.efalive/settings.conf ]
then
    . /home/efa/.efalive/settings.conf
fi

test -x $DAEMON || exit 0

set -e

do_start() {
    x_running=`ps a | grep $PROCESS | grep -v grep | wc -l`
    if [ $x_running -eq 0 ]
    then
        if [ $AUTO_USB_BACKUP = "TRUE" ]
        then
            # halevt change user/group before write pidfile, so use this
            if [ ! -f $HALEVT_PIDFILE ]; then
                echo > $HALEVT_PIDFILE; chown $DAEMONUSER.$DAEMONGROUP $HALEVT_PIDFILE
                # clean possible trash
                rm -f /var/lib/halevt/*
            fi
            start-stop-daemon --start --quiet --pidfile $HALEVT_PIDFILE \
                --chuid $DAEMONUSER --exec $HALEVT_DAEMON -- $HALEVT_DAEMON_OPTS
        fi
        /bin/su -l $DAEMONUSER -c "$DAEMON $DAEMON_OPTS" >> /dev/null &
    fi
}

do_stop() {
    start-stop-daemon --stop --oknodo --quiet --pidfile $HALEVT_PIDFILE \
        --exec $HALEVT_DAEMON
    x_running=`ps ax | grep $PROCESS | grep -v grep | wc -l`
    if [ $x_running -gt 0 ]
    then
        killall $PROCESS >> /dev/null 2>&1
    fi
}

case "$1" in
  start)
	log_daemon_msg "Starting $DESC" "$NAME"
	do_start
	log_end_msg $?
	;;
  stop)
	log_daemon_msg "Stopping $DESC" "$NAME"
	do_stop
	log_end_msg $?
	;;
  restart|force-reload)
	log_daemon_msg "Restarting $DESC" "$NAME"
	do_stop
	sleep 1
	do_start
	log_end_msg $?
	;;
  *)
	log_success_msg "Usage: $0 {start|stop|restart|force-reload}" >&2
	exit 1
	;;
esac

exit 0
