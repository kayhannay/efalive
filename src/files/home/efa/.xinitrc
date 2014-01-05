#Apply screen setup settings
XRANDR_CONFIG=~/.efalive/screen_setup.sh

if [ -x $XRANDR_CONFIG ]
then
    $XRANDR_CONFIG
fi
#Set the background image
feh --bg-fill /usr/share/plymouth/themes/efa-live/efaLive.png
#Start a gnome session for D-BUS and Keyring functionality
#####exec gnome-session &
#Start the screensaver
exec xscreensaver -no-splash &
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

start_halevt()
{
    if [ "x$AUTO_USB_BACKUP" = "xTRUE" ]
    then
        /usr/bin/halevt -c ~/.halevt/efaLive.xml -p /tmp/efalive_halevt.pid
    fi
}

stop_halevt()
{
    if [ -f /tmp/efalive_halevt.pid ]
    then
        kill -TERM $(cat /tmp/efalive_halevt.pid)
    fi
}

start_efa()
{
    #Set the correct efa start script
    if [ $EFA_VERSION -eq 2 ]
    then
        EFA_PROG=efabths
    else
        EFA_PROG=efadirekt
    fi

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
    stop_halevt
    exit 0
}

shutdown()
{
    stop_halevt
    sudo /sbin/shutdown -h now
    exit 0
}

restart()
{
    stop_halevt
    sudo /sbin/shutdown -r now
    exit 0
}

load_settings
start_halevt
start_efa
while :
do
    $EFA_SHUTDOWN_ACTION
done

