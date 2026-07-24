#!/bin/bash

if [ -z "$1" ]
then
        echo "Parsing HTML"
        echo "Usage: $0 <domain>"
        echo "Example: $0 google.com"
        exit
fi

TARGET=$1

HTML=$(wget -q -O - "http://${TARGET}" 2> /dev/null)
if [ -z "$HTML" ]; then
        HTML=$(wget -q -O - "https://${TARGET}" 2> /dev/null)
fi

DOMAIN=$(printf '%s' "$TARGET" | sed 's/\./\\./g')

HOSTS=$(echo "$HTML" | grep -oE "([a-zA-Z0-9_-]+\.)+${DOMAIN}" | sort -u)

IPS=$(echo "$HTML" | grep -oE "([0-9]{1,3}\.){3}[0-9]{1,3}(:[0-9]{1,5})?" | sort -u)

[ -n "$IPS" ] && echo "$IPS"
[ -n "$HOSTS" ] && echo "$HOSTS"

if [ -z "$IPS" ] && [ -z "$HOSTS" ]; then
        echo "No hosts found"
fi

for h in $HOSTS; do
        host "$h" 2>/dev/null | grep "has address"
done