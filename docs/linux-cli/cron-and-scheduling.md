---
title: Cron and Task Scheduling
category: reference
tags: [linux-cli, cron, crontab, at, scheduling, automation]
---

# Cron and Task Scheduling

cron handles recurring scheduled tasks; `at` handles one-time future execution. This entry covers crontab syntax, special shortcuts, one-time scheduling, and system time management.

## cron - Recurring Tasks

### Service Management

```bash
systemctl status cron       # check status
sudo systemctl start cron   # start
sudo systemctl enable cron  # enable at boot
```

### crontab Commands

```bash
crontab -l                  # list current user's tasks
crontab -e                  # edit tasks (opens in $EDITOR)
crontab -r                  # delete ALL tasks for current user
crontab -u username -l      # list another user's tasks (needs sudo)
```

### Crontab Syntax

```text
* * * * * /path/to/command
| | | | |
| | | | +-- day of week (0-7, 0 and 7 = Sunday)
| | | +---- month (1-12 or jan-dec)
| | +------ day of month (1-31)
| +-------- hour (0-23)
+---------- minute (0-59)
```

Special values:
- `*` - every unit
- `*/n` - every n units (e.g., `*/5` = every 5 minutes)
- `1,15` - specific values
- `1-5` - range
- `jan,jul,oct` - named months

### Examples

```bash
15 * * * * /run/script.sh             # every hour at :15
0 22 * * 1-5 /run/script.sh          # 22:00 Mon-Fri
0 0 1,15 * * /run/script.sh          # midnight on 1st and 15th
*/5 * * * * /run/script.sh            # every 5 minutes
0 9 * * * /run/script.sh              # daily at 9:00
```

### Special Shortcuts

```text
@reboot    # run once at startup
@hourly    # = 0 * * * *
@daily     # = 0 0 * * *
@weekly    # = 0 0 * * 0
@monthly   # = 0 0 1 * *
```

### Cron Logging

```bash
grep CRON /var/log/syslog
journalctl -u cron
```

Reference: https://crontab.guru/ - interactive syntax tester

## at - One-Time Tasks

```bash
at 10pm                    # interactive mode, Ctrl+D to save
at 8:00am tomorrow
at -f script.sh 8:00am    # schedule a script
at now + 2 hours
at 14:30 Jul 31

atq                        # list pending jobs
atrm 3                     # cancel job #3
```

### Install at

```bash
sudo apt install at
sudo systemctl enable --now atd
```

### batch

Like `at`, but runs only when system load drops below threshold.

## System Time

### date

```bash
date                            # display current date/time
date +"%Y-%m-%d %H:%M:%S"      # formatted output
sudo date --set="2024-09-06 20:43:40"  # set manually (disable NTP first)
```

### hwclock - Hardware Clock

```bash
hwclock                     # show hardware clock
hwclock --systohc           # sync hw clock from system time
hwclock --hctosys           # sync system time from hw clock
```

### NTP Sync

```bash
timedatectl status          # show time, timezone, NTP status
timedatectl set-ntp true    # enable NTP
timedatectl set-timezone Europe/Moscow
```

Note: active NTP overwrites manual `date --set` immediately.

## Gotchas

- `crontab -r` deletes ALL tasks without confirmation - dangerous
- Minute 60 and hour 24 are invalid (0-59 and 0-23)
- Cron jobs run with a minimal environment - use full paths for commands
- `@reboot` runs once at system boot, not at cron service restart
- If both day-of-month and day-of-week are set, cron runs if EITHER matches (OR logic)
- cron sends email for job output - redirect to `/dev/null` or a log file to avoid mail accumulation

## See Also

- [[bash-scripting]] - Writing scripts to schedule
- [[systemd-and-services]] - systemd timers as cron alternative
- [[logging-and-journald]] - Viewing cron logs
