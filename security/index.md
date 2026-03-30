---
title: Security Knowledge Base - Map of Content
category: index
tags: [security, moc, index]
---

# Security Knowledge Base

## Anti-Fraud & Identification

Techniques and systems for detecting fraud through user identification and behavioral analysis.

- [[anti-fraud-systems]] - Multi-layered fraud detection architecture, risk scoring, signal aggregation
- [[browser-fingerprinting]] - Canvas, WebGL, AudioContext fingerprints; anti-detect browser detection
- [[network-identifiers]] - IP reputation, ASN classification, proxy/VPN detection, IPv4/IPv6
- [[tls-fingerprinting]] - JA3/JA4 hashes, ClientHello analysis, User-Agent vs TLS mismatch detection
- [[os-identifiers-serial-numbers]] - MachineGUID, BIOS serials, machine-id, VM detection
- [[behavioral-analysis]] - Mouse movement patterns (MAP), typing cadence, bot vs human detection
- [[social-rating-identity]] - Account age, digital reputation, email age, purchase history scoring
- [[geolocation-security]] - IP geolocation, GPS, Wi-Fi triangulation, timezone consistency checks

## Image Forensics

- [[deepfake-detection]] - Face detection consistency, temporal analysis, liveness detection
- [[image-forensics-antifraud]] - Error Level Analysis (ELA), EXIF metadata, copy-move detection, document verification

## Web Application Security

Backend security patterns for authentication, authorization, and secure deployment.

- [[jwt-authentication]] - Access/refresh token pattern, token rotation, secure storage
- [[password-hashing]] - bcrypt, Argon2id, salt, work factor calibration
- [[cors-and-origin-security]] - Same-Origin Policy, CORS headers, preflight requests, origin whitelisting
- [[rbac-authorization]] - Role-based access control, guards/middleware, authorization matrix
- [[file-upload-security]] - Magic bytes validation, filename sanitization, web shell prevention
- [[nginx-reverse-proxy-security]] - TLS termination, security headers, rate limiting, deployment hardening

## Linux System Security

Foundational OS-level security for servers and development environments.

- [[linux-user-security]] - Users, groups, sudo, /etc/passwd, /etc/shadow, privilege management
- [[linux-kernel-security]] - Kernel space vs user space, modules, sysctl hardening, boot modes
- [[linux-filesystem-security]] - FHS, permissions, SUID/SGID, mount options, filesystem audit
- [[linux-networking-sockets]] - Sockets, iptables, port management, firewall configuration
- [[disk-encryption-lvm]] - dm-crypt, LUKS, LVM on LUKS, key management, full-disk encryption
