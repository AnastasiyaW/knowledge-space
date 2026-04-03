---
title: Process Management
category: reference
tags: [linux-cli, processes, signals, kill, ps, top, htop]
---

# Process Management

A process is a running program with a PID, state, priority, and resource allocation. This entry covers viewing, filtering, and controlling processes - essential for system administration and debugging.

## Key Facts

- Every process has a PID (Process ID) and PPID (Parent Process ID)
- PID 1 is the init/systemd process - parent of all others
- **Daemon** = background process (system service)
- **Thread** = unit of execution within a process, shares memory space

## Process States

| State | Symbol | Description |
|-------|--------|-------------|
| Running | R | Actively executing or ready |
| Sleeping (interruptible) | S | Waiting for event, can be interrupted |
| Sleeping (uninterruptible) | D | Waiting for I/O, cannot be interrupted |
| Stopped | T | Paused (Ctrl+Z or signal) |
| Zombie | Z | Terminated but parent hasn't collected exit status |

## ps - Process Snapshot

```bash
ps                          # processes in current terminal
ps aux                      # all processes, full info (BSD syntax)
ps -ef                      # all processes (UNIX syntax)
ps afx                      # process tree
ps -u username              # processes for specific user
ps -T -p PID                # show threads of a process
ps 1                        # info for PID 1
```

### ps aux Columns

```
USER  PID  %CPU  %MEM  VSZ  RSS  TTY  STAT  START  TIME  COMMAND
```

- **VSZ**: virtual memory size
- **RSS**: resident set size (actual RAM)
- **STAT**: process state

## top - Interactive Monitor

```bash
top                     # default (sort by CPU%)
top -o PID              # sort by PID
top -u username         # filter by user
top -p PID1,PID2        # monitor specific PIDs
```

### Inside top

| Key | Action |
|-----|--------|
| q | Quit |
| k | Kill a process |
| r | Renice (change priority) |
| M | Sort by memory |
| P | Sort by CPU |
| 1 | Toggle per-CPU stats |
| u | Filter by user |

### Load Average

Shown in top header: `load average: 0.15, 0.20, 0.18` (1, 5, 15 min)

- Value < CPU cores = not overloaded
- Value = cores = at capacity
- Value > cores = overloaded

## htop - Enhanced Monitor

```bash
sudo apt install htop
htop                    # visual CPU/memory bars, mouse support
htop -u username        # filter by user
```

## Finding Processes

```bash
pidof firefox           # PID by exact name
pgrep pattern           # PIDs matching pattern
pgrep -la nginx         # PIDs + full command lines
```

## Signals

```bash
kill PID                # SIGTERM (graceful, default)
kill -9 PID             # SIGKILL (force, immediate)
kill -15 PID            # SIGTERM explicitly
kill -1 PID             # SIGHUP (reload config)
killall processname     # kill all by name
pkill pattern           # kill by pattern
kill -l                 # list all signals
```

| Signal | Number | Description |
|--------|--------|-------------|
| SIGHUP | 1 | Hangup / reload config |
| SIGINT | 2 | Interrupt (Ctrl+C) |
| SIGQUIT | 3 | Quit with core dump |
| SIGKILL | 9 | Force kill (cannot be caught) |
| SIGTERM | 15 | Graceful terminate |
| SIGSTOP | 19 | Pause (cannot be caught) |
| SIGCONT | 18 | Resume paused process |

## Process Priority (nice)

Range: -20 (highest priority) to +19 (lowest).

```bash
nice -n 10 command      # start with lower priority
renice -n 5 -p PID      # change running process priority
```

## Process Creation

1. Name assigned to process
2. Added to process list
3. Priority determined
4. Process control block (PCB) formed
5. Resources allocated

### Process Attributes

| Attribute | Description |
|-----------|-------------|
| `pid` | Process ID |
| `ppid` | Parent Process ID |
| `fd` | Open file descriptors |
| `cwd` | Current working directory |
| `environ` | Environment variables |
| `nice` | Priority value |

## Gotchas

- `kill -9` should be last resort - process cannot clean up (temp files, locks, sockets)
- Zombie processes can't be killed - they're already dead; kill their parent instead
- `top` load average includes processes in D state (waiting for I/O)
- `killall` on Solaris kills ALL processes - on Linux it kills by name (be careful on mixed environments)
- Background processes with `&` still die when terminal closes - use `nohup` or `disown`

## See Also

- [[systemd-and-services]] - Service management with systemctl
- [[monitoring-and-performance]] - System resource monitoring
- [[linux-kernel-and-boot]] - Kernel, init, process lifecycle
