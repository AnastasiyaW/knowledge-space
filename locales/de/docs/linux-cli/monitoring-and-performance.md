---
title: "Überwachung und Performance"
category: reference
tags: [linux-cli, monitoring, performance, memory, disk-io, network, cgroups]
level: 4
source_sha256: e253c0b7f91a2152ae33a30d104f56ed60a2b80f0436bcda59acaa389312f9c9
translation: machine
translated_at: '2026-10-24'
---
# Überwachung und Performance {#monitoring-and-performance}

Systemüberwachungswerkzeuge für CPU, Speicher, Festplatten-I/O und Netzwerk. Dieser Eintrag behandelt Echtzeit-Monitore, Snapshot-Werkzeuge, Ressourcenlimits und Control Groups.

## Speicher {#memory}

```bash
free -h                     # human-readable memory usage
free -m                     # in megabytes
cat /proc/meminfo           # detailed kernel memory info
vmstat 1 5                  # virtual memory stats every 1s, 5 times
```

Ausgabespalten: total, used, free, shared, buff/cache, available.

## Festplatten-I/O {#disk-io}

```bash
iostat                      # I/O stats for devices
iostat -x 1                 # extended stats, refresh every 1s
iotop                       # per-process I/O (like top for disk)
```

## Netzwerk {#network}

```bash
netstat -tulpn              # listening ports and services
ss -tulpn                   # same, newer/faster tool
netstat -an                 # all connections
iftop                       # real-time network usage by host
nload                       # bandwidth monitor
```

## Systemlast und Laufzeit {#system-load-and-uptime}

```bash
uptime                      # uptime, users, load average
cat /proc/loadavg           # load average values
```

**Load Average** = auf CPU wartende Prozesse + laufende Prozesse. Drei Werte: 1 Min., 5 Min., 15 Min.
- < CPU-Kerne: unkritisch
- = Kerne: am Limit
- \> Kerne: überlastet

## Ressourcenlimits {#resource-limits}

```bash
ulimit -a                   # show all limits
ulimit -n 4096              # set max open files
```

## Control Groups (cgroups) {#control-groups-cgroups}

Kernel-Funktion zum Begrenzen und Isolieren der Ressourcennutzung pro Prozessgruppe.

Funktionen:
- CPU-Pinning auf bestimmte Kerne
- CPU-Zeit- bzw. Gewichtungslimits
- Speicherlimits (harte Obergrenze)
- I/O-Limits (absolut oder gewichtet)
- Ressourcenerfassung und Auditing

```bash
cat /proc/PID/cgroup        # view process cgroup
ls /sys/fs/cgroup/          # cgroup v2 hierarchy
```

## Protokollbasiertes Monitoring {#log-based-monitoring}

```bash
tail -f /var/log/syslog         # follow system log
tail -f /var/log/auth.log       # follow auth log
journalctl -f                   # follow systemd journal
journalctl -u nginx             # specific service
journalctl --since "1 hour ago"
journalctl -p err               # errors only
```

## Stolperfallen {#gotchas}

- Die Load Average in `top` enthält Prozesse im D-Zustand (Warten auf Festplatte) – hohe Last bedeutet also nicht immer einen CPU-Engpass
- In `free` enthält „used“ Buffer und Cache – für den tatsächlich freien Speicher die Spalte „available“ betrachten
- `ss` wird auf modernen Systemen gegenüber `netstat` bevorzugt (schneller, mehr Informationen)
- `iotop` erfordert root-Rechte und die Kernel-Option CONFIG_TASK_IO_ACCOUNTING
- Hohes `wa` (I/O wait) in `top` deutet auf einen Festplatten-Engpass hin, nicht auf ein CPU-Problem

## Siehe auch {#see-also}

- [[process-management]] - ps, top, htop, kill
- [[logging-and-journald]] - Werkzeuge zur Log-Analyse
- [[disks-and-filesystems]] - Festplattenzustand, SMART
- [[systemd-and-services]] - Dienstüberwachung
