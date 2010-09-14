export JAVA_HOME=/opt/jre
export PATH=$JAVA_HOME/bin:$PATH
exec openbox &

if [ ! -f ~/.efalive/version.conf ]
then
	/opt/efalive/bin/efaLiveSetup.sh
fi

. ~/.efalive/version.conf

#Set the correct efa start script
if [ $EFA_VERSION -eq 2 ]
then
	EFA_PROG=/opt/efa2/efa_bh.sh
else
	EFA_PROG=/opt/efa/efadirekt.sh
fi

start=`date +%s`
$EFA_PROG >> ~/efa.log 2>&1
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

