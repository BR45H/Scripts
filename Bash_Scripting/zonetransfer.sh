#!/bin/bash

if [[ -z "$1" ]]
then
	echo "Usage: $0 <Domain>"
	exit
fi

target="$1"

readarray -t name_servers < <(host -t ns "$target" 2>/dev/null | cut -d " " -f 4 | sed 's/\.$//')
for name_server in "${name_servers[@]}"
do
	resp=$(host -l "$target" "$name_server" 2>/dev/null)
	if [[ "$resp" != *"Transfer failed."* ]]
	then
		echo "$resp"
	fi
done