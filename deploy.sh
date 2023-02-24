#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

echo 'copying agent to /home'
mv main.py /home

echo 'installing dependencies'
apt-get install -y systemd

echo 'copying service to /etc/systemd/system'
mv main.service /etc/systemd/system

echo 'reloading daemon'
systemctl daemon-reload

echo 'enabling service'
systemctl enable main.service

echo 'starting service'
systemctl start main.service

echo 'done'
