#!/bin/sh

sudo cd /
sudo echo "@/usr/bin/python3 /home/pi/grab/grab.py" >> /home/pi/.config/lxsession/LXDE-pi/autostart
cd /home/pi/
sudo reboot
