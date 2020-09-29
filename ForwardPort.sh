#!/bin/bash

# Script used to forward ports as well as delete port forwarding rules

action=$1
IP=$2
PORT=$3

if [ "$action" = "-a" ]
then
    upnpc -a $IP $PORT $PORT tcp
elif [ "$action" = "-d" ]
then
    upnpc -d $PORT tcp
fi