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

start_efa()
{
    #Start efaLive setup if there are no settings
    if [ ! -f ~/.efalive/settings.conf ]
    then
        efalive-setup
    fi

    . ~/.efalive/settings.conf

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
        zenity --question --text="Das elektronische Fahrtenbuch efa wurde unerwartet schnell beendet. Soll nun die Aktion beim Herunterfahren von efa gestartet werden?"
        if [ $? -ne 0 ]
        then
            exit 0
        fi
    fi
}

start_efa
while :
do
    $EFA_SHUTDOWN_ACTION
done

