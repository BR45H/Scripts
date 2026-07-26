#!/bin/bash
if [[ -z "$1" || -z "$2" ]]
then 
    echo "PortKnocking Bash Script"
    echo "Usage: $0 <IP/Domain> <Port_dst>"
    exit 1
fi

target="$1"
target_port="$2"

read -p "Insert the port sequence: " port_sequence

for port in $port_sequence; do
    nc -w1 -z "$target" "$port" 2>/dev/null
done

if nc -w2 -z "$target" "$target_port" 2>/dev/null; then
    echo "Port knocking sucessful, port $target_port is open."
else
    echo "Port knocking failed, port $target_port remains closed."
fi