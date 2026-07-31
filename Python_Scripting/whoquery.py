#!/usr/bin/python3
import sys, socket

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <IP/DOMAIN>")
    sys.exit(1)

target = sys.argv[1]

def create_socket(server: str):
    try:
        results = socket.getaddrinfo(server, None, socket.AF_UNSPEC, socket.SOCK_STREAM)

    except socket.gaierror as error:
        print(f"Error to resolve: {error}")
        results = []
        return False
    
    if not results:
        return False

    family, type_, proto, canonname, sockaddr = results[0]
    sock = socket.socket(family, type_, proto)
    sock.settimeout(10)

    return sock

def identify_refer(target: str) -> str:
    sock = create_socket("whois.iana.org")

    if not sock:
        print("Could not resolve: whois.iana.org")
        sys.exit(1)

    sock.connect(("whois.iana.org",43))
    sock.send(str.encode(target+"\r\n"))
    raw = recv_all(sock)
    sock.close()
    resp = raw.decode('utf-8', errors='replace')

    for line in resp.splitlines():
        if line.lower().startswith("refer:"):
            return line.split(":")[1].strip()
        
    print(f"Could not find a refer server to: {target}")
    sys.exit(1)

    return whois

def recv_all(sock) -> bytes:
    chunks = []

    while True:
        chunk = sock.recv(2048)
        if not chunk:
            break

        chunks.append(chunk)
    return b"".join(chunks)  

def get_whois_data(target: str, whois: str) -> str:
    sock = create_socket(whois)

    if not sock:
        print(f"Could not resolve {whois}")
        sys.exit(1)

    sock.connect((whois,43))
    sock.send(str.encode(target+"\r\n"))
    raw = recv_all(sock)
    sock.close()

    try:
        resp = raw.decode('utf-8')

    except UnicodeDecodeError:
        resp = raw.decode('latin-1')
        
    return resp

whois = identify_refer(target)
result = get_whois_data(target, whois)
print(result)
