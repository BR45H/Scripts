#!/usr/bin/python3
import sys
import json
import requests
import ipaddress
import re
import whoquery

DOMAIN_REGEX = r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z0-9-]{1,63}(?<!-))+$'
ASN_REGEX = r'^(?:AS|as)?\d+$'

BOOTSTRAP_URLS = {
    "dns": "https://data.iana.org/rdap/dns.json",
    "ipv4": "https://data.iana.org/rdap/ipv4.json",
    "ipv6": "https://data.iana.org/rdap/ipv6.json",
    "asn": "https://data.iana.org/rdap/asn.json",
}

def identify_type(target: str) -> str:
    try:
        ip = ipaddress.ip_address(target)
        if ip.version == 4:
            return "ipv4"
        else:
            return "ipv6"
        
    except ValueError:
        pass

    if re.match(ASN_REGEX, target):
        return "asn"

    if re.match(DOMAIN_REGEX, target):
        return "dns"
    else:
        print("Invalid type of target")
        return None

def search_rdap_server(type_: str, target: str) -> str | None:
    bootstrap_url = BOOTSTRAP_URLS[type_]
    resp = requests.get(bootstrap_url)
    data = resp.json()

    if type_ == "dns":
        tld = target.split(".")[-1].lower()
        for tlds, servers in data["services"]:
            if tld in tlds:
                return servers[0]

    elif type_ in ("ipv4", "ipv6"):
        target_ip = ipaddress.ip_address(target)
        for cidrs, servers in data["services"]:
            for cidr in cidrs:
                network = ipaddress.ip_network(cidr)
                if target_ip in network:
                    return servers[0]

    elif type_ == "asn":
        target_range = int(target.upper().replace("AS", ""))
        for number_strips, servers in data["services"]:
            for number_strip in number_strips:
                r1, r2 = str(number_strip).split("-")
                r1, r2 = int(r1), int(r2)
                if target_range in range(r1, r2 + 1):
                    return servers[0]

    else:
        return None

def consult_rdap(server: str, type_: str, target: str) -> dict | None:
    if not server.endswith("/"):
        server += "/"

    if type_ in ("ipv4", "ipv6"):
        url_server = f"{server}ip/{target}"
    elif type_ == "dns":
        url_server = f"{server}domain/{target}"
    elif type_ == "asn":
        number = target.upper().replace("AS", "")
        url_server = f"{server}autnum/{number}"
    else:
        return None
    
    resp = requests.get(url_server)

    if resp.status_code != 200:
        return None

    return resp.json()

def fallback_whois(target: str):
    print("RDAP unavaliable, fallback to WHOIS")
    whois = whoquery.identify_refer(target)
    result = whoquery.get_whois_data(target, whois)
    print(result)

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <DOMAIN|IP|ASN>")
        sys.exit(1)

    target = sys.argv[1]
    type_ = identify_type(target)
    if type_ is None:
        print("Cannot found a target type")
        sys.exit(1)

    server = search_rdap_server(type_, target)

    if server:
        data = consult_rdap(server, type_, target)
        if data:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            fallback_whois(target)
    else: 
        fallback_whois(target)

if __name__ == "__main__":
    main()