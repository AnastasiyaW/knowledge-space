---
title: Process Management
category: reference
tags: [ps, top, htop, kill, systemctl, processes, services]
---
# Process Management

Monitoring, controlling, and managing running processes and system services.

## Key Facts

- Every running program is a process identified by a PID (Process ID)
- `ps` - snapshot of current processes; `top` / `htop` - real-time interactive monitors
- `systemctl` - manage systemd services (start, stop, enable, status)
- `kill` sends signals to processes; default signal is SIGTERM (15), SIGKILL (9) forces termination
- `pidof <name>` - find PID by process name
- Processes run under a [[users-and-groups]] identity that determines their [[file-permissions]]
- Background processes: append `&` to command; `Ctrl+Z` suspends foreground process
- `systemctl enable <service>` - start service on boot; `systemctl disable` - remove from boot

## Patterns

```bash
# View current process
ps

# View all processes (table format)
ps aux
# USER  PID %CPU %MEM  VSZ   RSS  TTY  STAT START TIME COMMAND

# View process tree
ps afx

# Find PID of a process
pidof firefox
pidof nginx

# Interactive process monitor
top
top -o PID          # Sort by PID descending
top -u salesguy     # Filter by user

# Better interactive monitor (install first)
sudo apt-get install htop
htop

# Kill process by PID
kill 1234           # SIGTERM (graceful)
kill -9 1234        # SIGKILL (force, last resort)
kill -15 1234       # SIGTERM (explicit)

# Kill all processes by name
killall firefox

# Service management with systemctl
systemctl status ssh       # Check service status
sudo systemctl start ssh   # Start service
sudo systemctl stop ssh    # Stop service
sudo systemctl restart ssh # Restart service
sudo systemctl reload ssh  # Reload config without restart
sudo systemctl enable ssh  # Enable on boot
sudo systemctl disable ssh # Disable on boot
systemctl is-active ssh    # Check if running (returns active/inactive)

# List all running services
systemctl list-units --type=service --state=running

# View service logs
journalctl -u ssh -f       # Follow logs for ssh service
```

## Gotchas

- `kill -9` (SIGKILL) cannot be caught or ignored - process gets no chance to clean up; use as last resort
- `top -o -PID` (with minus) sorts descending; `top -o PID` sorts ascending
- `systemctl enable` does NOT start the service - it only configures boot startup; use `systemctl enable --now` for both
- `ps aux` vs `ps -ef`: both show all processes but with different column formats; `aux` is BSD-style, `-ef` is POSIX
- `Ctrl+C` sends SIGINT (2), `Ctrl+Z` sends SIGTSTP (20, suspend) - suspended processes still consume memory
- Zombie processes (state Z) cannot be killed - they are already dead, waiting for parent to collect exit status

## See Also

- [[cron-scheduling]] - scheduling automated process execution
- [[users-and-groups]] - processes inherit user privileges
- [[io-redirection-and-pipes]] - background processes with `&`
- `man ps` - https://man7.org/linux/man-pages/man1/ps.1.html
- `man systemctl` - https://man7.org/linux/man-pages/man1/systemctl.1.html
