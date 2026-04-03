---
title: Python for Security
category: tools
tags: [security, python, scripting, automation, sockets, port-scanning]
---

# Python for Security

Python scripting for security professionals: socket programming for port scanning and banner grabbing, log analysis with regex, HTTP requests for web testing, subprocess for tool integration, and practical security script patterns.

## Key Facts
- Python's `socket` module provides raw TCP/UDP networking for port scanning and banner grabbing
- `ThreadPoolExecutor` enables parallel port scanning (100+ threads)
- `requests` library routes through Burp proxy via `proxies` parameter for web testing
- `argparse` provides professional CLI argument handling for security tools
- `re` module parses log files for IP extraction, auth failure analysis
- Always use `with` statements for file/socket cleanup

## Network Socket Basics

### TCP Client / Banner Grabbing
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

### Threaded Port Scanner
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

## Log Analysis

### Auth Log Parser
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

### Regex Patterns for Security
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

## HTTP Requests for Web Testing
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

## File I/O for Security Data
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

## Subprocess for Tool Integration
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

## CLI Argument Parsing
```python
import argparse

parser = argparse.ArgumentParser(description='Port Scanner')
parser.add_argument('target', help='Target IP address')
parser.add_argument('-p', '--ports', default='1-1024', help='Port range')
parser.add_argument('-t', '--threads', type=int, default=100)
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()
```

## Practical Patterns

### Password Strength Checker
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

## Error Handling
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

## Gotchas
- Raw socket scanning may require root/admin privileges
- `socket.settimeout()` is essential - without it, connections to filtered ports hang indefinitely
- `requests.get()` with `verify=False` disables TLS validation - only for testing with Burp proxy
- `subprocess.run()` with shell=True is vulnerable to command injection - avoid with user input
- Large thread counts in port scanning can exhaust file descriptors - use reasonable limits

## See Also
- [[penetration-testing-methodology]] - tools Python scripts automate
- [[burp-suite-and-web-pentesting]] - routing requests through proxy
- [[network-traffic-analysis]] - complementary to Python scanning
- [[linux-system-hardening]] - log files Python scripts analyze
