---
title: "Linux & Kommandozeile"
type: MOC
level: 2
source_sha256: 3d5a842201bfd9af2bfc98ce5564604760e7e5ba036d0368aa255e82cb8e2815
translation: machine
translated_at: '2026-10-24'
---
# Linux & Kommandozeile {#linux-command-line}

## Shell & Terminal {#shell-terminal}
- [[terminal-basics]] - Shells, grundlegende Befehle, Tastenkürzel, Einstieg in Linux
- [[text-editors]] - nano und vim: Modi, Tastenkürzel, Navigation

## Dateien & Dateisystem {#files-filesystem}
- [[filesystem-hierarchy]] - Verzeichnisstruktur nach FHS, Dateitypen, Speicherbelegung
- [[file-operations]] - Dateien und Verzeichnisse erstellen, kopieren, verschieben, löschen, anzeigen
- [[file-search-and-grep]] - find, grep, locate, whereis, which
- [[text-processing]] - wc, sort, uniq, cut, awk, sed, tr
- [[io-redirection-and-pipes]] - stdin/stdout/stderr, Pipes, Verkettung von Befehlen, Exit-Codes
- [[links-and-inodes]] - Hard Links, Symlinks, Inode-Struktur, ext4-Interna
- [[file-permissions]] - chmod, chown, SUID/SGID/Sticky Bit, umask, ACLs

## Benutzer & Sicherheit {#users-security}
- [[users-and-groups]] - Benutzertypen, passwd/shadow/group, useradd, sudo, su
- [[linux-security]] - DAC/MAC, Namespaces, seccomp, Malware-Typen, Pentesting-Tools
- [[firewall-and-iptables]] - iptables-Chains/Targets/Regeln, nftables, ufw

## Container {#containers}
- [[docker-basics]] - Images, Container, Volumes, Dockerfile, Lebenszyklus, Aufräumen

## Systemadministration {#system-administration}
- [[systemd-and-services]] - systemctl, Unit-Dateien, Kernel-Module, Hardware-Inspektion
- [[process-management]] - ps, top, htop, kill, Signale, Prozesszustände, Priorität
- [[package-management]] - apt, dpkg, snap, yum/dnf, rpm, winget
- [[cron-and-scheduling]] - crontab-Syntax, at, Systemzeit, NTP
- [[disks-and-filesystems]] - Partitionen, ext4, Mounting, fstab, LVM, LUKS-Verschlüsselung
- [[logging-and-journald]] - syslog, rsyslog, journalctl, logrotate, auditd
- [[monitoring-and-performance]] - Speicher, Disk-I/O, Netzwerk, Load Average, cgroups

## Netzwerk & Fernzugriff {#networking-remote}
- [[ssh-remote-access]] - SSH-Schlüssel, Konfiguration, Tunnel, SCP, Security-Hardening

## Scripting {#scripting}
- [[bash-scripting]] - Variablen, Bedingungen, Schleifen, Funktionen, Debugging
- [[python-and-node-cli]] - Python/pip/venv und Node.js/npm über die CLI

## Architektur & Interna {#architecture-internals}
- [[linux-kernel-and-boot]] - Kernel, Module, Boot-Sequenz, GRUB, Init-Systeme, Speicher
- [[linux-os-structure]] - Kernel vs. User Space, Sockets, Gerätedateien, Sicherheitsmodell

## Windows-Interoperabilität {#windows-interop}
- [[wsl]] - WSL-Installation, Dateiinteroperabilität, Netzwerk, Konfiguration
- [[powershell-basics]] - Cmdlets, Objekt-Pipelines, Variablen, Skripte

## Weitere Referenzen {#additional-references}

- [[disk-data-recovery]] - Wiederherstellung defekter oder großer (16 TB+) Laufwerke auf Blockebene: Imaging, Reparatur von Partitionen/GPT
- [[ffmpeg-encoding]] - CLI-Medienencoder
