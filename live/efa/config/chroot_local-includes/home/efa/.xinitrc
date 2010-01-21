export JAVA_HOME=/opt/jre
export PATH=$JAVA_HOME/bin:$PATH
#xterm
matchbox-window-manager &
#cd ~/efa
/opt/efa/efadirekt.sh >> ~/efa.log 2>&1
