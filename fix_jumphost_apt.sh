#!/bin/bash
# script to fix apt repos for ubuntu 15.10 jumphosts
# run this with sudo!
APT_SRC=/etc/apt/sources.list
echo "" > $APT_SRC
echo "deb http://old-releases.ubuntu.com/ubuntu wily-updates main multiverse universe restricted" >> $APT_SRC
echo "deb http://old-releases.ubuntu.com/ubuntu wily-security main multiverse universe restricted" >> $APT_SRC
echo "deb http://old-releases.ubuntu.com/ubuntu wily main multiverse universe restricted" >> $APT_SRC

apt-get update
apt-get upgrade -y
