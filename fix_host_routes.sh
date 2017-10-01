#!/bin/bash

GATEWAY=`ip route | grep "ens3  proto kernel" | awk '{ print $1 }' | awk -F "." '{ print $1 "."  $2 "." $3 ".1"}'`

sudo route add -net 10.1.0.0 netmask 255.255.0.0 gw $GATEWAY dev ens3
sudo route add -net 10.2.0.0 netmask 255.255.0.0 gw $GATEWAY dev ens3
sudo route add -net 10.16.0.0 netmask 255.254.0.0 gw $GATEWAY dev ens3
sudo route add -net 10.255.0.0 netmask 255.255.0.0 gw $GATEWAY dev ens3

