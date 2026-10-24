---
title: "Python für Security"
category: tools
tags: [security, python, scripting, automation, sockets, port-scanning]
level: 4
source_sha256: 9d72ddb5b5b43183b5eea5f4fb19d32a492754829edc1d09ba95a4db1fd5a015
translation: machine
translated_at: '2026-10-24'
---
# Python für Security {#python-for-security}

Python-Scripting für Security-Profis: Socket-Programmierung für Port-Scanning und Banner Grabbing, Log-Analyse mit Regex, HTTP-Requests für Web-Testing, subprocess zur Tool-Integration sowie praktische Muster für Security-Skripte.

## Key Facts {#key-facts}
- Das `socket`-Modul von Python bietet rohe TCP/UDP-Netzwerkfunktionen für Port-Scanning und Banner Grabbing
- `ThreadPoolExecutor` ermöglicht paralleles Port-Scanning (100+ Threads)
- Die `requests`-Bibliothek leitet Anfragen über den `proxies`-Parameter an den Burp-Proxy weiter, für Web-Testing
- `argparse` bietet eine professionelle CLI-Argumentverarbeitung für Security-Tools
- Das `re`-Modul parst Logdateien zur IP-Extraktion und Analyse fehlgeschlagener Authentifizierungen
- Immer `with`-Anweisungen für die Bereinigung von Dateien und Sockets verwenden

## Netzwerk-Socket-Grundlagen {#network-socket-basics}

### TCP-Client / Banner Grabbing {#tcp-client-banner-grabbing}
```python
import socket

def grab_banner(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    try:
        sock.connect((host, port))
        sock.send(b"HEAD / HTTP/1.1\r\nHost: %s\r\n\r\n" % host.encode())
        return sock.recv(4096).decode(errors='ignore')
    except:
        return None
    finally:
        sock.close()
```

### Threaded Port Scanner {#threaded-port-scanner}
```python
import socket
from concurrent.futures import ThreadPoolExecutor

def check_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((host, port))
    sock.close()
    return port if result == 0 else None

def scan_host(host, ports=range(1, 1025), threads=100):
    open_ports = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(check_port, host, p): p for p in ports}
        for future in futures:
            result = future.result()
            if result:
                open_ports.append(result)
    return sorted(open_ports)
```

## Log-Analyse {#log-analysis}

### Auth-Log-Parser {#auth-log-parser}
```python
import re

def analyze_auth_log(filepath):
    failed_attempts = {}
    pattern = r'Failed password for (\w+) from ([\d.]+) port (\d+)'
    with open(filepath) as f:
        for line in f:
            if "Failed password" in line:
                match = re.search(r'from ([\d.]+)', line)
                if match:
                    ip = match.group(1)
                    failed_attempts[ip] = failed_attempts.get(ip, 0) + 1
    return dict(sorted(failed_attempts.items(), key=lambda x: x[1], reverse=True))
```

### Regex-Muster für Security {#regex-patterns-for-security}
```python
import re

# Extract IP addresses
ips = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', log_text)

# Match email addresses
emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.]+', text)

# Parse auth failures
pattern = r'Failed password for (\w+) from ([\d.]+) port (\d+)'
for match in re.finditer(pattern, auth_log):
    user, ip, port = match.groups()
```

## HTTP-Requests für Web-Testing {#http-requests-for-web-testing}
```python
import requests

# GET request
resp = requests.get("https://api.example.com/endpoints", verify=True)

# POST with Burp proxy
resp = requests.post(
    "https://target.com/login",
    data={"username": "admin", "password": "test"},
    headers={"User-Agent": "Mozilla/5.0"},
    proxies={"http": "http://127.0.0.1:8080",
             "https": "http://127.0.0.1:8080"},
    allow_redirects=False
)
print(resp.status_code, resp.headers, resp.text[:500])
```

## Datei-I/O für Security-Daten {#file-io-for-security-data}
```python
# Read log files
with open("/var/log/auth.log") as f:
    for line in f:
        if "Failed password" in line:
            print(line.strip())

# JSON handling
import json
with open("scan_results.json") as f:
    results = json.load(f)

# CSV output
import csv
with open("vulnerabilities.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["cve", "severity", "host"])
    writer.writeheader()
    writer.writerows(findings)
```

## Subprocess zur Tool-Integration {#subprocess-for-tool-integration}
```python
import subprocess

result = subprocess.run(
    ["nmap", "-sV", "-p", "1-1000", target],
    capture_output=True, text=True, timeout=120
)
print(result.stdout)

# Ping sweep
def ping_host(ip):
    result = subprocess.run(
        ["ping", "-c", "1", "-W", "1", ip],
        capture_output=True, text=True
    )
    return result.returncode == 0
```

## CLI-Argumentverarbeitung {#cli-argument-parsing}
```python
import argparse

parser = argparse.ArgumentParser(description='Port Scanner')
parser.add_argument('target', help='Target IP address')
parser.add_argument('-p', '--ports', default='1-1024', help='Port range')
parser.add_argument('-t', '--threads', type=int, default=100)
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()
```

## Praktische Muster {#practical-patterns}

### Passwortstärke-Prüfer {#password-strength-checker}
```python
import re

def check_password_strength(password):
    checks = {
        "length >= 12": len(password) >= 12,
        "uppercase": bool(re.search(r'[A-Z]', password)),
        "lowercase": bool(re.search(r'[a-z]', password)),
        "digit": bool(re.search(r'\d', password)),
        "special": bool(re.search(r'[!@#$%^&*]', password)),
    }
    return sum(checks.values()), checks
```

## Fehlerbehandlung {#error-handling}
```python
import socket

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    sock.connect((host, port))
    banner = sock.recv(1024).decode()
except socket.timeout:
    print(f"Connection to {host}:{port} timed out")
except ConnectionRefusedError:
    print(f"Port {port} is closed")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
finally:
    sock.close()
```

## Gotchas {#gotchas}
- Rohes Socket-Scanning erfordert unter Umständen Root- bzw. Administratorrechte
- `socket.settimeout()` ist unverzichtbar – ohne dieses hängen Verbindungen zu gefilterten Ports unbegrenzt
- `requests.get()` mit `verify=False` deaktiviert die TLS-Validierung – nur zum Testen mit dem Burp-Proxy verwenden
- `subprocess.run()` mit `shell=True` ist anfällig für Command Injection – bei Benutzereingaben vermeiden
- Zu viele Threads beim Port-Scanning können Dateideskriptoren erschöpfen – sinnvolle Grenzen verwenden

## Siehe auch {#see-also}
- [[penetration-testing-methodology]] - Tools, die Python-Skripte automatisieren
- [[burp-suite-and-web-pentesting]] - Weiterleitung von Anfragen über den Proxy
- [[network-traffic-analysis]] - Ergänzung zum Python-Scanning
- [[linux-system-hardening]] - Logdateien, die Python-Skripte analysieren
