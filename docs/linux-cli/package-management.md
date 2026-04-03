---
title: Package Management
category: reference
tags: [linux-cli, apt, dpkg, yum, dnf, rpm, snap, packages]
---

# Package Management

Linux software is distributed as packages - archives containing binaries, libraries, configs, and metadata. Package managers handle installation, dependency resolution, updates, and removal across two major ecosystems.

## Key Facts

- **Debian/Ubuntu**: `.deb` packages - tools: dpkg, apt, aptitude
- **Red Hat/CentOS/Fedora**: `.rpm` packages - tools: rpm, yum, dnf
- High-level tools (apt, yum, dnf) resolve dependencies automatically
- Low-level tools (dpkg, rpm) manage individual package files only

## APT - Debian/Ubuntu

### Update and Upgrade

```bash
sudo apt update               # refresh package index (no installs)
sudo apt upgrade              # upgrade all packages
sudo apt full-upgrade         # upgrade + install new deps + remove obsolete
```

**update vs upgrade**: `update` syncs the package list; `upgrade` installs newer versions.

### Install and Remove

```bash
sudo apt install package              # install
sudo apt install pkg1 pkg2 pkg3       # install multiple
sudo apt install pkg --no-upgrade     # install only if not present
sudo apt install pkg --only-upgrade   # upgrade only if already installed
sudo apt remove package               # remove (keep config)
sudo apt purge package                # remove + delete config files
sudo apt autoremove                   # remove unused dependencies
```

### Search and Info

```bash
apt search keyword            # search packages
apt show package              # detailed info
apt list --installed          # list installed
apt list --upgradeable        # available upgrades
```

### Repositories

Config: `/etc/apt/sources.list` and `/etc/apt/sources.list.d/`

```bash
sudo add-apt-repository ppa:user/repo     # add PPA (Ubuntu)
```

## dpkg - Low-Level Debian

```bash
dpkg -l                       # list all installed packages
dpkg -l | wc -l               # count installed
dpkg -i package.deb           # install .deb file
dpkg -r package               # remove (keep config)
dpkg -P package               # purge (remove + config)
dpkg -s package               # package status
dpkg -L package               # list files in package
dpkg -S /path/to/file         # find which package owns a file
apt download package           # download .deb without installing
```

## snap - Universal Packages

```bash
sudo apt install snapd
snap find package             # search
sudo snap install package     # install
sudo snap remove package      # remove
snap list                     # installed snaps
snap refresh                  # update all
snap info package             # details
```

## YUM - RHEL/CentOS 7

```bash
yum install package           # install
yum install -y package        # no confirmation
yum remove package            # remove
yum update                    # update all
yum search keyword            # search
yum info package              # info
yum list installed            # list installed
yum autoremove                # remove unused deps
yum downgrade package         # rollback
```

## DNF - RHEL 8+, Fedora

Modern replacement for YUM with same syntax.

```bash
dnf install package
dnf remove package
dnf update
dnf search keyword
dnf list installed
dnf history                   # transaction history
dnf history undo last         # undo last transaction
```

## RPM - Low-Level Red Hat

```bash
sudo rpm -i package.rpm       # install
sudo rpm -U package.rpm       # upgrade
sudo rpm -e package           # remove
rpm -q package                # query if installed
rpm -qa                       # list all installed
rpm -ql package               # list files in package
rpm -qi package               # package info
```

## Comparison

| Feature | APT | YUM/DNF | dpkg | RPM |
|---------|-----|---------|------|-----|
| Distro | Debian | RHEL | Debian | Red Hat |
| Dependency resolution | Yes | Yes | No | No |
| Remote repos | Yes | Yes | No | No |
| Package format | .deb | .rpm | .deb | .rpm |

## winget - Windows Package Manager

```bash
winget search package         # search
winget install package        # install
winget uninstall package      # remove
winget upgrade --all          # upgrade all
winget list                   # list installed
winget export -o pkgs.json    # export package list
winget import -i pkgs.json    # import and install
```

## Gotchas

- Always run `apt update` before `apt install` to get latest package lists
- `apt remove` keeps config files; `apt purge` removes everything
- `dpkg` cannot resolve dependencies - use `apt install -f` to fix broken deps after dpkg
- RPM fails silently on missing deps - always prefer yum/dnf
- `snap` packages are sandboxed and self-contained but larger than native packages
- Mixing package managers (e.g., apt + snap for same software) can cause conflicts

## See Also

- [[python-and-node-cli]] - pip, npm package managers
- [[docker-basics]] - Container-based software distribution
