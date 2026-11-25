---
title: "Python pour la sécurité"
category: tools
tags: [security, python, scripting, automation, sockets, port-scanning]
level: 4
source_sha256: 9d72ddb5b5b43183b5eea5f4fb19d32a492754829edc1d09ba95a4db1fd5a015
translation: machine
translated_at: '2026-10-24'
---
# Python pour la sécurité {#python-for-security}

Scripts Python destinés aux professionnels de la sécurité : programmation de sockets pour le scan de ports et la récupération de bannières, analyse de journaux avec des expressions régulières, requêtes HTTP pour les tests web, subprocess pour l'intégration d'outils, et modèles pratiques de scripts de sécurité.

## Points clés {#key-facts}
- Le module `socket` de Python fournit un accès réseau TCP/UDP bas niveau pour le scan de ports et la récupération de bannières
- `ThreadPoolExecutor` permet le scan de ports en parallèle (100+ threads)
- La bibliothèque `requests` route les requêtes via le proxy Burp grâce au paramètre `proxies` pour les tests web
- `argparse` assure une gestion professionnelle des arguments CLI pour les outils de sécurité
- Le module `re` analyse les fichiers journaux pour extraire les adresses IP et analyser les échecs d'authentification
- Utilisez toujours les instructions `with` pour la libération des fichiers et des sockets

## Bases des sockets réseau {#network-socket-basics}

### Client TCP / récupération de bannières {#tcp-client-banner-grabbing}
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

### Scanner de ports multithreadé {#threaded-port-scanner}
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

## Analyse de journaux {#log-analysis}

### Analyseur de journaux d'authentification {#auth-log-parser}
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

### Expressions régulières pour la sécurité {#regex-patterns-for-security}
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

## Requêtes HTTP pour les tests web {#http-requests-for-web-testing}
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

## Entrées/sorties de fichiers pour les données de sécurité {#file-io-for-security-data}
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

## Subprocess pour l'intégration d'outils {#subprocess-for-tool-integration}
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

## Analyse des arguments CLI {#cli-argument-parsing}
```python
import argparse

parser = argparse.ArgumentParser(description='Port Scanner')
parser.add_argument('target', help='Target IP address')
parser.add_argument('-p', '--ports', default='1-1024', help='Port range')
parser.add_argument('-t', '--threads', type=int, default=100)
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()
```

## Modèles pratiques {#practical-patterns}

### Vérificateur de robustesse des mots de passe {#password-strength-checker}
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

## Gestion des erreurs {#error-handling}
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

## Pièges à éviter {#gotchas}
- Le scan de sockets bruts peut nécessiter les privilèges root/administrateur
- `socket.settimeout()` est indispensable : sans lui, les connexions vers les ports filtrés restent bloquées indéfiniment
- `requests.get()` avec `verify=False` désactive la validation TLS : à réserver aux tests avec le proxy Burp
- `subprocess.run()` avec shell=True est vulnérable à l'injection de commandes : à éviter avec des entrées utilisateur
- Un nombre élevé de threads lors du scan de ports peut épuiser les descripteurs de fichiers : utilisez des limites raisonnables

## Voir aussi {#see-also}
- [[penetration-testing-methodology]] - outils que les scripts Python automatisent
- [[burp-suite-and-web-pentesting]] - routage des requêtes via un proxy
- [[network-traffic-analysis]] - complémentaire au scan Python
- [[linux-system-hardening]] - fichiers journaux analysés par les scripts Python
