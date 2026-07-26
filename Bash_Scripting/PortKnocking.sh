#!/bin/bash
if [[ -z "$1" || -z "$2" ]]
then 
	echo "PortKnocking Bash Script"
    	echo "Usage: $0 <IP/Domain> <Port_dst>"
    	exit
fi

if [ "$EUID" -ne 0 ]
then
	echo "Run the script as a root."
	exit
fi

target="$1"
target_port="$2"

read -p "Insert the port sequence: " port_sequence

for port in $port_sequence; do
    hping3 -S -c 1 -p "$port" "$target" >/dev/null 2>&1
done

if hping3 -S -c 1 -p "$target_port" "$target" >/dev/null 2>&1; then
	echo "Port knocking sucessful, port $target_port is open."
	echo "Grabbing banner..."
	echo "" | timeout 3 nc "$target" "$target_port"

else
	echo "Port knocking failed, port $target_port remains closed."
fi