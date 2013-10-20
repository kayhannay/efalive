#!/bin/bash

prefix=/
args=$@

function get_abs_path() {
    cd $1
    local ABS_PATH=$(pwd)
    cd - >/dev/null
    echo $ABS_PATH
} 

while :
do
    case $1 in
        --prefix=*)
            prefix=${1#*=}        # Delete everything up till "="
            shift
            ;;
	'')
	    break
	    ;;
        *)  # no more options. Stop while loop
            shift
            ;;
    esac
done

echo "Installing to ${prefix} ..."

if [ ! -d ${prefix} ]
then
        mkdir -p ${prefix}
fi

echo "Replace paths ..."

if [[ ${prefix} =~ "debian" ]]
then
    sedprefix='\/usr'
else
    local absprefix=$(get_abs_path ${prefix})
    sedprefix=$(echo ${absprefix} | sed -e 's/[\/&]/\\&/g')
fi
sed -i "s/LOCALES=os.path.join(os.path.dirname(sys.argv\[0\]), os.pardir, 'i18n')/LOCALES=os.path.join('${sedprefix}', 'share', 'locale')/" efalivesetup/common/common.py
sed -i "s/icon_path = os.path.join(path, 'icons', icon_name)/icon_path = os.path.join('${sedprefix}', 'share', 'pixmaps', 'efalivesetup', icon_name)/" efalivesetup/common/common.py
sed -i "s/PYTHONPATH=.:$PYTHONPATH/PYTHONPATH=$sedprefix\/lib\/python2.7\/site-packages\/:$PYTHONPATH/" efalive-setup

echo "Call Python setup with arguments: $args"

python setup.py install $args
mkdir -p ${prefix}/share/pixmaps/efalivesetup
cp icons/* ${prefix}/share/pixmaps/efalivesetup/ 
mkdir -p ${prefix}/share/locale
cp -r i18n/* ${prefix}/share/locale/
mkdir -p ${prefix}/bin
cp efalive-setup ${prefix}/bin


#cp *.py ../../bash/efalive/content/usr/lib/efalive/lib/efaLiveSetup/ 
#cp locale/de/LC_MESSAGES/efaLiveSetup.mo ../../bash/efalive/content/usr/lib/efalive/lib/efaLiveSetup/locale/de/LC_MESSAGES/efaLiveSetup.mo
#cp icons/* ../../bash/efalive/content/usr/lib/efalive/lib/efaLiveSetup/icons/
