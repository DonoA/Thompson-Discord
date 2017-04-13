#!/bin/bash

echo Installing firefox and virtual display system
sudo apt-get install -y xvfb firefox

echo Installing mysql connector, splinter, virtual display, and discord
pip3 install https://cdn.mysql.com/Downloads/Connector-Python/mysql-connector-python-2.1.3.tar.gz splinter selenium pyvirtualdisplay discord.py

echo Installing geckodriver for
wget https://github.com/mozilla/geckodriver/releases/download/v0.15.0/geckodriver-v0.15.0-linux64.tar.gz
tar -xvzf geckodriver*
chmod 755 geckodriver
sudo mv geckodriver /usr/bin
rm geckodriver*
