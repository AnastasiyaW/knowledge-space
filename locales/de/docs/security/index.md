---
title: "Sicherheit & Cybersicherheit"
type: MOC
level: 4
source_sha256: 517e7610aee20b6003730b2257063c2d355531a2f893104f034ff1f439a501f6
translation: machine
translated_at: '2026-10-24'
---
# Sicherheit & Cybersicherheit {#security-cybersecurity}

## Grundlagen {#foundations}
- [[information-security-fundamentals]] - CIA-Triade, Risikomanagement, Defense in Depth, Zero Trust, Bedrohungsakteure
- [[cryptography-and-pki]] - symmetrische/asymmetrische Verschlüsselung, Hashing, TLS/SSL, PKI, digitale Signaturen
- [[authentication-and-authorization]] - MFA, JWT, OAuth 2.0/OIDC, Kerberos, RBAC, PAM
- [[compliance-and-regulations]] - ISO 27001, NIST CSF, PCI DSS, DSGVO, Auditvorbereitung

## Sicherheit von Webanwendungen {#web-application-security}
- [[web-application-security-fundamentals]] - XSS, CSRF, SSRF, XXE, IDOR, Path Traversal, OWASP Top 10
- [[sql-injection-deep-dive]] - In-band-, Blind- und Out-of-band-SQLi, sqlmap, parametrisierte Abfragen, NoSQL-Injection
- [[burp-suite-and-web-pentesting]] - Proxy, Repeater, Intruder, Scanner, ergänzende Werkzeuge
- [[secure-backend-development]] - Sicherheitsmuster für NestJS/Express, Validierung, Guards, ORM-Sicherheit
- [[web-server-security]] - Nginx-/Apache-Konfiguration, TLS mit Let's Encrypt, Reverse Proxy, Security Headers

## Offensive Security {#offensive-security}
- [[penetration-testing-methodology]] - Recon, Scanning, Exploitation, Metasploit, Angriffe auf WLAN, Reporting
- [[privilege-escalation-techniques]] - Linux SUID/sudo/Kernel, Windows-Tokens/Dienste, Lateral Movement
- [[active-directory-attacks]] - Kerberoasting, Golden/Silver Ticket, DCSync, BloodHound, Mimikatz
- [[osint-and-reconnaissance]] - Shodan, Google Dorking, Metadatenextraktion, Recherche zu Benutzernamen/E-Mail-Adressen
- [[social-engineering-and-phishing]] - Phishing-Typen, Pretexting, E-Mail-Authentifizierung (SPF/DKIM/DMARC)

## Netzwerksicherheit {#network-security}
- [[network-security-and-protocols]] - OSI-Modell, TCP/IP, DNS, DHCP, VPN (OpenVPN, WireGuard), E-Mail-Authentifizierung
- [[firewall-and-ids-ips]] - iptables/ufw, Windows Firewall, Snort, Suricata, WAF (ModSecurity, Cloud)
- [[network-traffic-analysis]] - tcpdump, Wireshark, nmap, TCP/IP-Fingerprinting, Diagnose

## Systemsicherheit {#system-security}
- [[linux-os-fundamentals]] - Dateisystemhierarchie, Kernel, Boot-Prozess, Festplattenverschlüsselung (LUKS), Prozesse
- [[linux-system-hardening]] - SSH-Konfiguration, fail2ban, auditd, sysctl, Dateiberechtigungen, CIS-Benchmarks
- [[windows-security-and-powershell]] - SAM/LSASS, Event IDs, Registry, GPO, AppLocker, PowerShell-Sicherheit

## Unternehmenssicherheit {#enterprise-security}
- [[siem-and-incident-response]] - SIEM-Architektur, Korrelationsregeln, Incident-Lebenszyklus, SOC-Stufen, SOAR
- [[security-solutions-architecture]] - EDR, DLP, IAM/PAM, Implementierungslebenszyklus, Change Management
- [[vulnerability-scanning-and-management]] - Nessus, OpenVAS, CVSS, Patch-Management, Priorisierung
- [Datenbanksicherheit](database-security.md) - Benutzerprivilegien, Verschlüsselung, Auditing, Sicherheit von Backups, Sicherheit von Cloud-Datenbanken

## Anti-Fraud & Forensik {#anti-fraud-forensics}
- [[browser-and-device-fingerprinting]] - Canvas, WebGL, AudioContext, Evercookies, Hardware-Signale
- [[tls-fingerprinting-and-network-identifiers]] - IP-Klassifizierung, Geolokalisierung, VPN-Erkennung, IPv6-Leaks
- [[anti-fraud-behavioral-analysis]] - Maus- und Tastendynamik, Zahlungsbetrug, Velocity Checks, BIN-Analyse
- [[deepfake-and-document-forensics]] - Deepfake-Erkennung, Dokumentenfälschung, Bildforensik (ELA), E-Mail-Analyse

## Sicherheits-Scripting {#security-scripting}
- [[python-for-security]] - Socket-Programmierung, Port-Scanning, Log-Analyse, HTTP-Tests, Werkzeugintegration

## Weiterführende Referenzen {#additional-references}

- [[adobe-piracy-patterns]] - Datum: 2026-04-03 Kontext: Defensive Sicherheitsforschung
- [[ai-agent-production-disasters]] - Analyse kritischer Produktionsausfälle, die zwischen 2025 und 2026 durch autonome KI-Coding-Agenten verursacht wurden
- [[ai-powered-vulnerability-detection-april-2026]] - Der Stand der Technik bei automatisierten Sicherheitsaudits hat sich von musterbasiertem SAST hin zu hybriden Ansätzen verschoben
- [[ai-vulnerability-detection]] - Datum: 2026-04-14 Kontext: Stand KI-gestützter Sicherheitsscans im April 2026
- [[anti-piracy-legal]] - Datum: 2026-04-03 Kontext: Desktop-Produkt für ML-Inferenz
- [[claude-mythos-leak-and-ai-supply-chain-security]] - Der unautorisierte Zugriff auf die Claude Mythos Preview (April 2026) dient als Benchmark für KI-
- [[computation-obfuscation]] - Datum: 2026-04-03 Kontext: Desktop-Produkt für ML-Inferenz
- [[cwe-079-xss]] - CWE-79: Vom Angreifer kontrollierte Daten werden ohne Escaping in DOM/HTML eingefügt
- [[cwe-089-sql-injection]] - CWE-89: SQL-Injection - nicht vertrauenswürdige Daten verändern die Struktur der Abfrage
- [[cwe-125-oob-read]] - CWE-125: Out-of-bounds Read - Lesezugriffe hinter Puffergrenzen leaken Geheimnisse, Schlüssel, benachbarten Heap
- [[cwe-190-integer-overflow]] - CWE-190: Arithmetik erzeugt ein Ergebnis außerhalb des Wertebereichs, mit Umbruch oder Abschneiden
- [[cwe-400-resource-consumption]] - CWE-400: Angreifer löst unkontrollierten Verbrauch von CPU, Speicher, Festplatte oder fds aus, z. B. über Regex-DoS, Hash
- [[cwe-416-use-after-free]] - CWE-416: Use After Free - Zugriff auf freigegebenen Speicher ermöglicht RCE, Informationsoffenlegung oder DoS
- [[cwe-434-file-upload]] - CWE-434: Unbeschränkter Upload gefährlicher Dateitypen - hochgeladene Dateien werden auf dem Server ausgeführt
- [[cwe-502-deserialization]] - CWE-502: Deserialisierung vom Angreifer kontrollierter Daten ermöglicht beliebige Codeausführung über Gadget-Ketten
- [[cwe-787-oob-write]] - CWE-787: Out-of-bounds Write - Speicherbeschädigung durch Schreibzugriffe hinter Puffergrenzen
- [[cwe-918-ssrf]] - CWE-918: Server stellt HTTP-/Protokollanfragen an vom Angreifer kontrollierte URLs und legt dabei interne Ressourcen offen
- [[disposable-email-detection]] - Backend-Referenz zur Erkennung von Wegwerf-E-Mail-Adressen und Missbrauch durch Mehrfachkonten bei der Registrierung
- [[email-reputation-services]] - Signalkategorien, Trade-offs bei Anbieterdiensten und ein DIY-MVP-Stack zum Blockieren von Hochrisiko-
- [[hkdf-personalized-weights]] - Datum: 2026-04-03 Kontext: Desktop-C++-App, ONNX-Runtime-Inferenz
- [[licensing-implementation-cpp]] - Datum: 2026-04-03 Kontext: Desktop-C++-App (Mac + Windows), selbst gehosteter Lizenzserver, ONNX-Modelle
- [[lora-weight-protection]] - Datum: 2026-04-03 Kontext: Desktop-/Server-Bildgenerierung mit proprietären LoRA-Adaptern auf
- [[model-weight-encryption]] - Datum: 2026-04-03 Kontext: Desktop-C++-App (Mac + Windows)
- [[onnx-model-protection]] - Datum: 2026-04-03 Kontext: Desktop-C++-App (Mac + Windows), ONNX-Runtime-Inferenz, Schutz von
- [[output-scrambling-antipiracy]] - Datum: 2026-04-03 Kontext: Desktop-C++-App mit ONNX-Inferenz
- [[piracy-economics]] - Datum: 2026-04-03 Kontext: Desktop-Produkte für ML-Inferenz
- [[remote-kill-switch]] - Datum: 2026-04-03 Kontext: Desktop-C++-Retusche-App (Mac + Windows)
- [[retouch4me-competitive-analysis]] - Datum: 2026-04-03 Kontext: Architektur- und Produktanalyse für den Aufbau einer konkurrierenden Retusche-
- [[security-telemetry]] - Datum: 2026-04-03 Kontext: Desktop-Anwendung mit Online-Lizenzserver
- [[tamper-resistant-counters]] - Datum: 2026-04-03 Kontext: C++, Windows + macOS
- [[threat-modeling]] - Systematischer Prozess zur Identifizierung, Bewertung und Dokumentation potenzieller Bedrohungen für ein
- [[watermarking-encrypted-models]] - Datum: 2026-04-03 Kontext: C++-Desktop-Retusche-App
