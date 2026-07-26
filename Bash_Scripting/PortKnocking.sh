#!/bin/bash
if [ -z "$1" ]
then 
    echo "PortKnocking Bash Script"
    echo "Usage: $0 <IP/Domain>"
    exit 1
fi

read -p "Insert the port sequence: " port_sequence

for port in $port_sequence; do
    nc -w1 -z -v "$1" "$port"
done

if [ $? -eq 0 ]; then
    echo "Port knocking sucessful!"
else
    echo "Port knocking failed."
fi