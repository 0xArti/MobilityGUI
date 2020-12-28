#!/bin/bash

if (gnome-screensaver-command -q | grep "is active")
then
    echo "Workstation is locked"
    exit
fi


if pgrep -x "mobility" >/dev/null
then
    echo "Mobility instance already running"
    exit
fi


export DISPLAY=:0.0
echo $MOBILITY_PATH
cd $MOBILITY_PATH
source venv/bin/activate
mobility &
