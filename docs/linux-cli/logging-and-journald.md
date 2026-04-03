---
title: Logging and journald
category: reference
tags: [linux-cli, logging, journald, journalctl, rsyslog, logrotate, syslog]
---

# Logging and journald

Linux logging covers system events, service output, security audit trails, and application logs. This entry covers syslog, rsyslog, journald/journalctl, logrotate, auditd, and log analysis tools.

## Key Facts

- Log files live in `/var/log/`
- journald (systemd) stores binary logs; journalctl queries them
- rsyslog handles text-based syslog forwarding and filtering
- logrotate prevents log files from consuming all disk space
- auditd tracks security-critical events

## Important Log Files

| Path | Contents |
|------|---------|
| `/var/log/syslog` (or `messages`) | Global system log |
| `/var/log/auth.log` (or `secure`) | Authentication events |
| `/var/log/dmesg` | Hardware and drivers |
| `/var/log/boot.log` | System boot |
| `/var/log/kern.log` | Kernel messages |
| `/var/log/cron` | Cron daemon |
| `/var/log/faillog` | Failed logins |
| `/var/log/audit/` | auditd audit log |
| `/var/log/dpkg.log` | Package manager (Debian) |

## Syslog Severity Levels

| Code | Name | Description |
|------|------|-------------|
| 0 | emerg | System unusable |
| 1 | alert | Immediate action required |
| 2 | crit | Critical failures |
| 3 | err | Errors |
| 4 | warning | Warnings |
| 5 | notice | Unusual but normal events |
| 6 | info | Informational |
| 7 | debug | Debug messages |

## journalctl - Querying systemd Journal

```bash
journalctl                              # all logs
journalctl -b 0                         # current boot
journalctl -b -2                        # two boots ago
journalctl --list-boots                 # list boot IDs
journalctl -u nginx.service             # specific service
journalctl -u nginx -f                  # follow (live tail)
journalctl _UID=1001                    # by user UID
journalctl -p err                       # errors and above
journalctl -n 3 -p crit                 # last 3 critical messages
journalctl --since yesterday
journalctl --since "2024-01-13 00:01" --until "2024-01-14 23:59"
journalctl --since "10 hours ago"
journalctl -xe -o json-pretty           # JSON output
journalctl --disk-usage                 # space used by logs
journalctl --vacuum-size=1G             # limit stored size
journalctl --vacuum-time=1years         # remove old logs
journalctl --flush                      # move from /run to /var
```

### journald Configuration

Config: `/etc/systemd/journald.conf`

Key settings:
- `Storage` - `volatile` | `persistent` | `auto` | `none`
- `Compress` - compress logs (yes/no)
- `SystemMaxUse` - max disk space
- `SystemKeepFree` - min free space to maintain
- `ForwardToSyslog` - forward to rsyslog

Storage: `/run/log/journal/` (temp), `/var/log/journal/` (persistent)

## rsyslog

Central logging daemon with filtering, forwarding, and database output.

Config: `/etc/rsyslog.conf` and `/etc/rsyslog.d/`

```ini
# facility.severity   destination
authpriv.*            /var/log/secure
mail.*               -/var/log/maillog     # dash = async write
cron.*                /var/log/cron
*.emerg              :omusrmsg:*           # broadcast to all users
kern.*                /var/log/kern.log

# Custom filter
if $programname == 'internal-sftp' then /var/log/sftp.log & stop
```

Module types: `im*` (input), `om*` (output), `fm*` (filter), `pm*` (parser), `mm*` (modification).

## logrotate

Automatic rotation, compression, and deletion of log files.

Config: `/etc/logrotate.conf` and `/etc/logrotate.d/`

```bash
/var/log/nginx/*.log {
    daily
    rotate 52
    compress
    delaycompress
    missingok
    notifempty
    create 0640 www-data adm
    sharedscripts
    postrotate
        invoke-rc.d nginx rotate >/dev/null 2>&1
    endscript
}
```

Key parameters:
- `rotate N` - keep N old files
- `compress` / `delaycompress` - gzip compression
- `copytruncate` - truncate original instead of moving
- `size` / `maxsize` / `minsize` - size-based rotation
- `postrotate/endscript` - commands after rotation

```bash
logrotate -d /etc/logrotate.d/nginx    # dry-run (debug)
logrotate -v /etc/logrotate.conf       # verbose, apply all
```

## auditd - Security Audit

```bash
# Add rules
auditctl -a entry,always -S all -F pid=1005        # all syscalls from PID
auditctl -w /home/user/test/ -k watch_test          # watch directory
auditctl -w /sbin/insmod -p x -k module_insertion   # watch insmod

# Search audit log
ausearch -ul root                                    # events by account
ausearch -p 6222                                     # events by PID
ausearch -x '/usr/sbin/crond'                        # by executable
ausearch -ts 08/06/2024 20:59 -te 08/06/2024 21:59  # by date range
```

Config: `/etc/audit/auditd.conf`, rules: `/etc/audit/audit.rules`

## Reading Logs

```bash
tail -f /var/log/syslog         # follow in real time
tail -n 50 /var/log/auth.log    # last 50 lines
less /var/log/syslog            # interactive navigation
zcat /var/log/syslog.2.gz       # read compressed log
zgrep "error" /var/log/*.gz     # search in compressed logs

# lnav - interactive log viewer
sudo apt install lnav
lnav /var/log/syslog
```

## User Login Tracking

```bash
who                     # currently connected users
last username           # login history
lastlog                 # all users' last login
```

## lsof - List Open Files

```bash
lsof                    # all open files
lsof -u username        # by user
sudo lsof -i TCP:80     # process on port 80
lsof /dev/null          # files on specific device
```

## Gotchas

- journald binary format provides tamper detection but requires `journalctl` to read
- rsyslog `dash prefix` (-/var/log/maillog) means async write - faster but may lose data on crash
- logrotate with `copytruncate` can lose lines written between copy and truncate
- auditd rules are lost on reboot unless saved to `/etc/audit/audit.rules`
- Centralized logging is recommended for distributed systems - local logs are easily tampered with

## See Also

- [[systemd-and-services]] - Service management and journald
- [[monitoring-and-performance]] - System resource monitoring
- [[linux-security]] - Security audit and compliance
- [[firewall-and-iptables]] - Network security logging
