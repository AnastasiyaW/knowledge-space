---
title: Cron Task Scheduling
category: patterns
tags: [cron, crontab, scheduling, automation]
---
# Cron Task Scheduling

Scheduling recurring tasks with the cron daemon and crontab utility.

## Key Facts

- `cron` is a systemd service that executes scheduled commands
- `crontab` - user utility to view/edit scheduled tasks
- Cron syntax: `minute hour day-of-month month day-of-week command`
- Fields: minute (0-59), hour (0-23), day (1-31), month (1-12 or jan-dec), weekday (0-7, 0=7=Sunday)
- Special characters: `*` (any), `,` (list), `-` (range), `/` (step)
- Predefined schedules: `@hourly`, `@daily`, `@weekly`, `@monthly`, `@reboot`
- Editing another user's crontab requires `sudo`: `crontab -u username -e`
- Cron service must be running: check with [[process-management]] `systemctl status cron`
- Scripts called by cron need [[file-permissions]] execute bit set
- Cron jobs run with minimal environment - specify full paths to commands

## Patterns

```bash
# Check cron service status
systemctl status cron
sudo systemctl start cron
sudo systemctl enable cron

# View current user's crontab
crontab -l

# Edit current user's crontab
crontab -e

# Remove ALL cron jobs for current user
crontab -r

# Edit another user's crontab (requires sudo)
sudo crontab -u officemanager -e

# Cron syntax:
# min  hour  dom  month  dow  command
# ---- ----  ---  -----  ---  -------
  15   *     *    *      *    /run/my/script.sh    # Every hour at :15
  0    9     *    *      1-5  /run/backup.sh       # Weekdays at 9:00
  0    22    *    *      *    /run/cleanup.sh       # Daily at 22:00
  30   6     1    *      *    /run/monthly.sh       # 1st of month at 6:30
  */5  *     *    *      *    /run/check.sh         # Every 5 minutes
  0    0     1,15 *      *    /run/biweekly.sh      # 1st and 15th at midnight

# Predefined schedules
  @hourly   /run/script.sh       # Same as: 0 * * * *
  @daily    /run/script.sh       # Same as: 0 0 * * *
  @weekly   /run/script.sh       # Same as: 0 0 * * 0
  @monthly  /run/script.sh       # Same as: 0 0 1 * *
  @reboot   /run/startup.sh      # Run once at system boot

# Redirect cron output to log
0 * * * * /run/script.sh >> /var/log/myscript.log 2>&1

# Cron with environment variable
0 9 * * * PATH=/usr/local/bin:/usr/bin /run/script.sh
```

## Gotchas

- Minute value 60 is INVALID (0-59 only); hour 24 is INVALID (0-23 only)
- `0 22 * 1-5` is WRONG syntax - 5 fields required: `0 22 * * 1-5` (missing day-of-week position)
- Cron has minimal `$PATH` - always use absolute paths (`/usr/bin/python3` not `python3`)
- `crontab -r` removes ALL jobs instantly with no confirmation - extremely dangerous typo if you meant `-e`
- Cron does not send output anywhere by default - redirect stdout/stderr or output is silently lost
- `crontab -u user -l` works without sudo for listing; `-e` (edit) requires sudo for other users
- Online validator: https://crontab.guru/ - always test complex expressions there first

## See Also

- [[process-management]] - cron runs as a systemd service
- [[bash-scripting]] - scripts executed by cron
- [[io-redirection-and-pipes]] - redirecting cron job output
- `man 5 crontab` - https://man7.org/linux/man-pages/man5/crontab.5.html
