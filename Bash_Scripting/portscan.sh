#!/bin/bash

if [ -z "$1" ]
then
	echo "Port scan script"
	echo "Usage: $0 <IP>"
	echo "Example: $0 192.168.10.250"
	exit
fi

if [ "$EUID" -ne 0 ]
then
	echo "Run the script as a root."
	exit
fi

count=0

echo "Pinging host..."
if ping -c 1 "$1" > /dev/null 2>&1
then
	echo "Host $1 is online"
else
	echo "Host is down, exiting"
	exit
fi	
echo "Scanning TCP ports..."
for port in $(seq 19 1024)
do
	if hping3 -S -p "$port" -c 1 "$1" 2> /dev/null | grep -q "flags=SA"
	then
		echo "Port $port is opened"
		count=$((count + 1))
	fi
done
echo "Total: $count Opened Ports"
