#!/bin/sh
#launcher.sh
#exec grab with python3

cd /home/pi/grab/
env DISPLAY=:0
sudo /usr/bin/python3 /home/pi/grab/grab.py
