#!/bin/bash

cwd=`cd $(dirname $0); pwd -P`
echo "$cwd/$(basename $0)"
echo "========================================================================"
echo "| This script will set www-data to restart nginx withour sudo password |"
echo "========================================================================"

sudo touch /etc/sudoers.d/www-data
sudo echo "www-data ALL=(ALL:ALL) NOPASSWD: /usr/sbin/service nginx *" > /etc/sudoers.d/www-data
