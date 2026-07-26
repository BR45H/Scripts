#!/usr/bin/python3
import socket
import sys

if len(sys.argv) != 3:
	print(f"Usage: {sys.argv[0]} <IP> <Port>")
	sys.exit(1)

ip = sys.argv[1]
port = int(sys.argv[2])

mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
resp = mysocket.connect_ex((ip,port))

if (resp == 0):
	print(f"Port {port} is open.")
else:
	print(f"Port {port} is closed.")