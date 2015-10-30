#!/usr/bin/env sh
sudo apt-get install python3.4
wget https://bootstrap.pypa.io/ez_setup.py -O - | sudo python3.4
sudo easy_install-3.4 gitpython
sudo easy_install-3.4 termcolor
sudo easy_install-3.4 deepdiff