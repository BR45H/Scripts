#!/usr/bin/python3
import sys, socket

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <IP/DOMAIN> <PORT>")
    sys.exit(1)

host = sys.argv[1]
port = int(sys.argv[2])

mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
resp = mysocket.connect_ex((host,port))

if resp != 0:
    print(f"Could not connect to {host}:{port}")
    mysocket.close()
    sys.exit(1)

print("Connected...")

mysocket.settimeout(3)
banner = None
try:
    banner = mysocket.recv(1024)
    if banner:
        print(banner.decode(errors="ignore"))
except socket.timeout:
    print("[No banner - server wait you talk first]")

mysocket.settimeout(10)

while True:
    cmd = input("> ")
    if cmd == 'exit':
        break
    
    if ";;" in cmd:
        payload = cmd.replace(";;", "\r\n") + "\r\n\r\n"    
    else:
        payload = cmd + "\r\n"    

    try:
        mysocket.send(str.encode(payload))
        data = mysocket.recv(4096)
    except (ConnectionResetError, ConnectionAbortedError, OSError) as e:
        print(f"[Connection error: {e}]")
        break

    if not data:
        print("[Connection closed by remote host]")
        break

    print(data.decode(errors="ignore"))

mysocket.close()
