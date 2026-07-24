#!/bin/bash

if [ -z "$1" ]
then
	echo "Host discover script"
	echo "Usage: $0 <Network>"
	echo "Example: $0 10.0.2"
	exit
fi

count=0

echo "Scaning Network $1 to discover hosts..."
for host in $(seq 1 254)
do
	if ping -c 1 -W 1 "$1.$host" > /dev/null 2>&1
	then
		echo "Host: $1.$host Active"
		count=$((count + 1))
	fi
done
echo "Total: $count Active Hosts"
