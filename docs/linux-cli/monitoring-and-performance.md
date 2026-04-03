---
title: Monitoring and Performance
category: reference
tags: [linux-cli, monitoring, performance, memory, disk-io, network, cgroups]
---

# Monitoring and Performance

System monitoring tools for CPU, memory, disk I/O, and network. This entry covers real-time monitors, snapshot utilities, resource limits, and control groups.

## Memory

```bash
free -h                     # human-readable memory usage
free -m                     # in megabytes
cat /proc/meminfo           # detailed kernel memory info
vmstat 1 5                  # virtual memory stats every 1s, 5 times
```

Output columns: total, used, free, shared, buff/cache, available.

## Disk I/O

```bash
iostat                      # I/O stats for devices
iostat -x 1                 # extended stats, refresh every 1s
iotop                       # per-process I/O (like top for disk)
```

## Network

```bash
netstat -tulpn              # listening ports and services
ss -tulpn                   # same, newer/faster tool
netstat -an                 # all connections
iftop                       # real-time network usage by host
nload                       # bandwidth monitor
```

## System Load and Uptime

```bash
uptime                      # uptime, users, load average
cat /proc/loadavg           # load average values
```

**Load average** = processes waiting for CPU + running. Three values: 1-min, 5-min, 15-min.
- < CPU cores: healthy
- = cores: at capacity
- \> cores: overloaded

## Resource Limits

```bash
ulimit -a                   # show all limits
ulimit -n 4096              # set max open files
```

## Control Groups (cgroups)

Kernel feature for limiting and isolating resource usage per process group.

Capabilities:
- CPU pinning to specific cores
- CPU time/weight limits
- Memory limits (hard cap)
- I/O limits (absolute or weighted)
- Resource accounting and auditing

```bash
cat /proc/PID/cgroup        # view process cgroup
ls /sys/fs/cgroup/          # cgroup v2 hierarchy
```

## Log-Based Monitoring

```bash
tail -f /var/log/syslog         # follow system log
tail -f /var/log/auth.log       # follow auth log
journalctl -f                   # follow systemd journal
journalctl -u nginx             # specific service
journalctl --since "1 hour ago"
journalctl -p err               # errors only
```

## Gotchas

- `top` load average includes D-state (disk wait) processes - high load does not always mean CPU bottleneck
- `free` "used" includes buffers/cache - look at "available" for actual free memory
- `ss` is preferred over `netstat` on modern systems (faster, more information)
- `iotop` requires root and the kernel CONFIG_TASK_IO_ACCOUNTING option
- High `wa` (I/O wait) in top indicates disk bottleneck, not CPU issue

## See Also

- [[process-management]] - ps, top, htop, kill
- [[logging-and-journald]] - Log analysis tools
- [[disks-and-filesystems]] - Disk health, SMART
- [[systemd-and-services]] - Service monitoring
