#!/bin/bash

if [[ -z "$1" || -z "$2" ]]
then
	echo "==============================="
	echo "           DorkFetch           " 
	echo "==============================="
	echo ""
	echo "Usage: $0 <Domain> <filetype>"
	exit
fi

target="$1"
filetype="$2"

readarray -t urls < <(curl -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0" -sS "https://search.brave.com/search?q=site:$target+ext:$filetype" | grep -oP 'http[s]?://[^"]+\.'"$filetype" | sort -u)

for url in "${urls[@]}"; do
	archive="${url##*/}"
	echo "Downloading $archive..."
	wget -q "$url"
done