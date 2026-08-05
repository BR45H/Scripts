#!/bin/bash

target="$1"
wordlist="$2"

if [[ -z "$target" || -z "$wordlist" ]]
then
    echo "Usage: $0 <Domain> <Wordlist>"
    exit
fi

if [[ ! -f "$wordlist" ]]
then
    echo "Wordlist not found: $wordlist"
    exit
fi

while IFS= read -r path; do
    [[ -z "$path" ]] && continue

    status=$(curl -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0" \
        -s -o /dev/null -w "%{http_code}" "${target}/${path}")
    
    case "$status" in 
        200|301|302|403)
            echo "[$status] ${target}/${path}"
            ;;
    esac
done < "$wordlist"
