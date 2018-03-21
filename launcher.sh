#!/bin/sh
#launcher.sh
#exec grab with python3

cd /home/pi/grab/
export DISPLAY=:0
sudo XAUTHORITY=~/.Xauthority /usr/bin/python3 /home/pi/grab/grab.py
