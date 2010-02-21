export JAVA_HOME=/opt/jre
export PATH=$JAVA_HOME/bin:$PATH
#xterm
matchbox-window-manager -use_dialog_mode free &
start=`date +%s`
/opt/efa/efadirekt.sh >> ~/efa.log 2>&1
stop=`date +%s`
delta=$(($stop-$start))
if [ $delta -lt 5 ]
then
    zenity --question --text="Das elektronische Fahrtenbuch EFA wurde unerwartet schnell beendet. Wollen Sie den Computer nun herunterfahren?"
    if [ $? -ne 0 ]
    then
        exit 0
    fi
fi
sudo /sbin/shutdown -h now
