---
title: "Surveillance et performances"
category: reference
tags: [linux-cli, monitoring, performance, memory, disk-io, network, cgroups]
level: 4
source_sha256: e253c0b7f91a2152ae33a30d104f56ed60a2b80f0436bcda59acaa389312f9c9
translation: machine
translated_at: '2026-10-24'
---
# Surveillance et performances {#monitoring-and-performance}

Outils de surveillance système pour le CPU, la mémoire, les E/S disque et le réseau. Cette entrée couvre les moniteurs en temps réel, les utilitaires de capture instantanée, les limites de ressources et les groupes de contrôle.

## Mémoire {#memory}

```bash
free -h                     # human-readable memory usage
free -m                     # in megabytes
cat /proc/meminfo           # detailed kernel memory info
vmstat 1 5                  # virtual memory stats every 1s, 5 times
```

Colonnes de sortie : total, used, free, shared, buff/cache, available.

## E/S disque {#disk-io}

```bash
iostat                      # I/O stats for devices
iostat -x 1                 # extended stats, refresh every 1s
iotop                       # per-process I/O (like top for disk)
```

## Réseau {#network}

```bash
netstat -tulpn              # listening ports and services
ss -tulpn                   # same, newer/faster tool
netstat -an                 # all connections
iftop                       # real-time network usage by host
nload                       # bandwidth monitor
```

## Charge système et durée de fonctionnement {#system-load-and-uptime}

```bash
uptime                      # uptime, users, load average
cat /proc/loadavg           # load average values
```

**Load average** = processus en attente de CPU + processus en cours d'exécution. Trois valeurs : sur 1 min, 5 min, 15 min.
- < nombre de cœurs CPU : sain
- = nombre de cœurs : à pleine capacité
- \> nombre de cœurs : surchargé

## Limites de ressources {#resource-limits}

```bash
ulimit -a                   # show all limits
ulimit -n 4096              # set max open files
```

## Groupes de contrôle (cgroups) {#control-groups-cgroups}

Fonctionnalité du noyau permettant de limiter et d'isoler l'utilisation des ressources par groupe de processus.

Fonctionnalités :
- Épinglage CPU sur des cœurs spécifiques
- Limites de temps ou de poids CPU
- Limites de mémoire (plafond strict)
- Limites d'E/S (absolues ou pondérées)
- Comptabilisation et audit des ressources

```bash
cat /proc/PID/cgroup        # view process cgroup
ls /sys/fs/cgroup/          # cgroup v2 hierarchy
```

## Surveillance basée sur les journaux {#log-based-monitoring}

```bash
tail -f /var/log/syslog         # follow system log
tail -f /var/log/auth.log       # follow auth log
journalctl -f                   # follow systemd journal
journalctl -u nginx             # specific service
journalctl --since "1 hour ago"
journalctl -p err               # errors only
```

## Pièges courants {#gotchas}

- La charge moyenne affichée par `top` inclut les processus en état D (attente disque) : une charge élevée n'indique pas toujours un goulot d'étranglement CPU
- La valeur « used » de `free` inclut les buffers et le cache : consultez « available » pour connaître la mémoire réellement libre
- `ss` est préféré à `netstat` sur les systèmes récents (plus rapide, davantage d'informations)
- `iotop` nécessite les droits root et l'option du noyau CONFIG_TASK_IO_ACCOUNTING
- Un `wa` (I/O wait) élevé dans `top` indique un goulot d'étranglement disque, et non un problème de CPU

## Voir aussi {#see-also}

- [[process-management]] - ps, top, htop, kill
- [[logging-and-journald]] - Outils d'analyse des journaux
- [[disks-and-filesystems]] - Santé des disques, SMART
- [[systemd-and-services]] - Surveillance des services
