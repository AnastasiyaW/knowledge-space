---
title: "Sécurité et cybersécurité"
type: MOC
level: 4
source_sha256: 517e7610aee20b6003730b2257063c2d355531a2f893104f034ff1f439a501f6
translation: machine
translated_at: '2026-10-24'
---
# Sécurité et cybersécurité {#security-cybersecurity}

## Fondamentaux {#foundations}
- [[information-security-fundamentals]] - Triade CIA, gestion des risques, défense en profondeur, zero trust, acteurs de la menace
- [[cryptography-and-pki]] - chiffrement symétrique/asymétrique, hachage, TLS/SSL, PKI, signatures numériques
- [[authentication-and-authorization]] - MFA, JWT, OAuth 2.0/OIDC, Kerberos, RBAC, PAM
- [[compliance-and-regulations]] - ISO 27001, NIST CSF, PCI DSS, RGPD, préparation aux audits

## Sécurité des applications web {#web-application-security}
- [[web-application-security-fundamentals]] - XSS, CSRF, SSRF, XXE, IDOR, path traversal, OWASP Top 10
- [[sql-injection-deep-dive]] - SQLi in-band, aveugle, out-of-band, sqlmap, requêtes paramétrées, injection NoSQL
- [[burp-suite-and-web-pentesting]] - proxy, repeater, intruder, scanner, outils complémentaires
- [[secure-backend-development]] - patterns de sécurité NestJS/Express, validation, guards, sécurité de l'ORM
- [[web-server-security]] - configuration Nginx/Apache, TLS avec Let's Encrypt, reverse proxy, en-têtes de sécurité

## Sécurité offensive {#offensive-security}
- [[penetration-testing-methodology]] - reconnaissance, scan, exploitation, Metasploit, attaques sans fil, rapport
- [[privilege-escalation-techniques]] - SUID/sudo/noyau sous Linux, tokens/services Windows, mouvement latéral
- [[active-directory-attacks]] - Kerberoasting, Golden/Silver Ticket, DCSync, BloodHound, Mimikatz
- [[osint-and-reconnaissance]] - Shodan, Google Dorking, extraction de métadonnées, investigation sur les noms d'utilisateur et les e-mails
- [[social-engineering-and-phishing]] - types de phishing, pretexting, authentification des e-mails (SPF/DKIM/DMARC)

## Sécurité réseau {#network-security}
- [[network-security-and-protocols]] - modèle OSI, TCP/IP, DNS, DHCP, VPN (OpenVPN, WireGuard), authentification des e-mails
- [[firewall-and-ids-ips]] - iptables/ufw, Pare-feu Windows, Snort, Suricata, WAF (ModSecurity, cloud)
- [[network-traffic-analysis]] - tcpdump, Wireshark, nmap, fingerprinting TCP/IP, diagnostic

## Sécurité des systèmes {#system-security}
- [[linux-os-fundamentals]] - hiérarchie du système de fichiers, noyau, processus de démarrage, chiffrement de disque (LUKS), processus
- [[linux-system-hardening]] - configuration SSH, fail2ban, auditd, sysctl, permissions de fichiers, benchmarks CIS
- [[windows-security-and-powershell]] - SAM/LSASS, Event IDs, registre, GPO, AppLocker, sécurité PowerShell

## Sécurité d'entreprise {#enterprise-security}
- [[siem-and-incident-response]] - architecture SIEM, règles de corrélation, cycle de vie des incidents, niveaux SOC, SOAR
- [[security-solutions-architecture]] - EDR, DLP, IAM/PAM, cycle de vie de l'implémentation, gestion des changements
- [[vulnerability-scanning-and-management]] - Nessus, OpenVAS, CVSS, gestion des correctifs, priorisation
- [Sécurité des bases de données](database-security.md) - privilèges utilisateurs, chiffrement, audit, sécurité des sauvegardes, sécurité des bases de données cloud

## Anti-fraude et investigation numérique {#anti-fraud-forensics}
- [[browser-and-device-fingerprinting]] - canvas, WebGL, AudioContext, evercookies, signaux matériels
- [[tls-fingerprinting-and-network-identifiers]] - classification des IP, géolocalisation, détection de VPN, fuites IPv6
- [[anti-fraud-behavioral-analysis]] - dynamique de la souris et des frappes, fraude au paiement, contrôles de vélocité, analyse des BIN
- [[deepfake-and-document-forensics]] - détection de deepfakes, falsification de documents, forensique d'image (ELA), analyse d'e-mails

## Scripts de sécurité {#security-scripting}
- [[python-for-security]] - programmation socket, scan de ports, analyse de logs, tests HTTP, intégration d'outils

## Références complémentaires {#additional-references}

- [[adobe-piracy-patterns]] - Date : 2026-04-03 Contexte : recherche en sécurité défensive
- [[ai-agent-production-disasters]] - Analyse des défaillances critiques en production causées par des agents de codage IA autonomes entre 2025 et 2026
- [[ai-powered-vulnerability-detection-april-2026]] - L'état de l'art de l'audit de sécurité automatisé est passé du SAST basé sur les motifs à l'hybride
- [[ai-vulnerability-detection]] - Date : 2026-04-14 Contexte : état de la détection de vulnérabilités assistée par IA en avril 2026
- [[anti-piracy-legal]] - Date : 2026-04-03 Contexte : produit d'inférence ML sur poste de travail
- [[claude-mythos-leak-and-ai-supply-chain-security]] - L'accès non autorisé à Claude Mythos Preview (avril 2026) sert de référence pour l'IA
- [[computation-obfuscation]] - Date : 2026-04-03 Contexte : produit d'inférence ML sur poste de travail
- [[cwe-079-xss]] - CWE-79 : données contrôlées par un attaquant insérées dans le DOM/HTML sans échappement
- [[cwe-089-sql-injection]] - CWE-89 : injection SQL - des données non fiables modifient la structure de la requête
- [[cwe-125-oob-read]] - CWE-125 : lecture hors limites - la lecture au-delà des bornes d'un tampon fuite des secrets, des clés, du tas adjacent
- [[cwe-190-integer-overflow]] - CWE-190 : une opération arithmétique produit un résultat hors plage, avec repliement ou troncature
- [[cwe-400-resource-consumption]] - CWE-400 : un attaquant déclenche une consommation incontrôlée de CPU, mémoire, disque ou descripteurs de fichiers via un DoS par expression régulière, par hachage
- [[cwe-416-use-after-free]] - CWE-416 : Use After Free - l'accès à une mémoire libérée permet une RCE, une divulgation d'informations ou un DoS
- [[cwe-434-file-upload]] - CWE-434 : téléversement illimité de types de fichiers dangereux - les fichiers téléversés s'exécutent sur le serveur
- [[cwe-502-deserialization]] - CWE-502 : la désérialisation de données contrôlées par un attaquant permet l'exécution de code arbitraire via des chaînes de gadgets
- [[cwe-787-oob-write]] - CWE-787 : écriture hors limites - corruption de la mémoire par des écritures au-delà des bornes d'un tampon
- [[cwe-918-ssrf]] - CWE-918 : le serveur envoie des requêtes HTTP/de protocole vers des URL contrôlées par un attaquant, exposant des ressources internes
- [[disposable-email-detection]] - Référence backend pour la détection d'adresses e-mail jetables et des abus multi-comptes lors de l'inscription
- [[email-reputation-services]] - Catégories de signaux, compromis entre services de fournisseurs, et stack MVP en autonomie pour bloquer les risques élevés
- [[hkdf-personalized-weights]] - Date : 2026-04-03 Contexte : application C++ de bureau, inférence ONNX Runtime
- [[licensing-implementation-cpp]] - Date : 2026-04-03 Contexte : application C++ de bureau (Mac + Windows), serveur de licences auto-hébergé, modèles ONNX
- [[lora-weight-protection]] - Date : 2026-04-03 Contexte : génération d'images sur poste de travail/serveur avec adaptateurs LoRA propriétaires
- [[model-weight-encryption]] - Date : 2026-04-03 Contexte : application C++ de bureau (Mac + Windows)
- [[onnx-model-protection]] - Date : 2026-04-03 Contexte : application C++ de bureau (Mac + Windows), inférence ONNX Runtime, protection de
- [[output-scrambling-antipiracy]] - Date : 2026-04-03 Contexte : application C++ de bureau avec inférence ONNX
- [[piracy-economics]] - Date : 2026-04-03 Contexte : produits d'inférence ML sur poste de travail
- [[remote-kill-switch]] - Date : 2026-04-03 Contexte : application C++ de retouche photo de bureau (Mac + Windows)
- [[retouch4me-competitive-analysis]] - Date : 2026-04-03 Contexte : analyse architecturale et produit pour la construction d'un concurrent de retouche
- [[security-telemetry]] - Date : 2026-04-03 Contexte : application de bureau avec serveur de licences en ligne
- [[tamper-resistant-counters]] - Date : 2026-04-03 Contexte : C++, Windows + macOS
- [[threat-modeling]] - Processus systématique d'identification, d'évaluation et de documentation des menaces potentielles pour un
- [[watermarking-encrypted-models]] - Date : 2026-04-03 Contexte : application C++ de retouche de bureau
