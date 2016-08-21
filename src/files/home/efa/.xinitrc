LOGFILE=~/startup.log
exec 1>> $LOGFILE 2>&1

#Apply screen setup settings
XRANDR_CONFIG=~/.efalive/screen_setup.sh

if [ -x $XRANDR_CONFIG ]
then
    $XRANDR_CONFIG
fi
#Set the background image
feh --bg-fill /usr/share/plymouth/themes/efa-live/efaLive.png
#Start the screensaver
exec xscreensaver -no-splash &
#Start power manager
exec xfce4-power-manager &
#Start the window manager
exec openbox &

load_settings()
{
    #Start efaLive setup if there are no settings
    if [ ! -f ~/.efalive/settings.conf ]
    then
        efalive-setup
    fi

    . ~/.efalive/settings.conf
}

start_efalive_daemon()
{
    /usr/bin/efalive-daemon start
}

stop_efalive_daemon()
{
    /usr/bin/efalive-daemon stop
    sudo /sbin/hwclock -w
}

start_efa()
{
    EFA_PROG=efabths

    #Start efa and check that it does not stop immediately or show a dialog
    start=`date +%s`
    EFA_CRED=~/.efalive/.efacred $EFA_PROG >> ~/efa.log 2>&1
    stop=`date +%s`
    delta=$(($stop-$start))
    if [ $delta -lt 5 ]
    then
        zenity --question --text="The electronic logbook efa was stopped unexpectedly quick. Should we continue with the configured action for efa shutdown?"
        if [ $? -ne 0 ]
        then
            exit 0
        fi
    fi
}

stop_efa()
{
    stop_efalive_daemon
    exit 0
}

shutdown()
{
    stop_efalive_daemon
    sudo /sbin/shutdown -h now
    exit 0
}

restart()
{
    stop_efalive_daemon
    sudo /sbin/shutdown -r now
    exit 0
}

load_settings
start_efalive_daemon
start_efa
while :
do
    $EFA_SHUTDOWN_ACTION
done

