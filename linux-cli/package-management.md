---
title: Package Management
category: reference
tags: [apt, dpkg, snap, packages, install, update]
---
# Package Management

Installing, updating, and removing software packages on Debian/Ubuntu systems.

## Key Facts

- **apt** / **apt-get** - high-level package manager, downloads from remote repositories
- **dpkg** - low-level package manager, works with local `.deb` files only (no dependency resolution)
- **snap** - universal package manager, sandboxed applications from Snap Store
- `apt update` refreshes package index (metadata); `apt upgrade` installs available updates
- `apt` is the modern frontend; `apt-get` is the older equivalent (both work)
- `apt remove` keeps config files; `apt purge` removes package AND config files
- Packages require [[users-and-groups]] root privileges (`sudo`) for installation
- [[process-management]] with `systemctl` manages services installed by packages

## Patterns

```bash
# Update package index (always do first)
sudo apt update

# Upgrade all installed packages
sudo apt upgrade -y

# Install a package
sudo apt install htop
sudo apt-get install htop    # equivalent

# Remove a package (keeps configs)
sudo apt remove htop
sudo apt-get remove htop

# Remove package AND config files
sudo apt purge htop
sudo apt-get purge htop

# Search for packages in repositories
apt search nginx
snap find opera

# Show package info
apt show nginx
dpkg -l nginx                # if installed

# Download .deb file without installing
apt download htop

# Install from .deb file (low-level)
sudo dpkg -i htop_3.0-11_amd64.deb

# List installed packages
dpkg -l
dpkg -l | wc -l              # count installed packages

# Snap package management
sudo apt install snapd        # install snap daemon
sudo snap install opera       # install via snap
snap list                     # list snap packages
sudo snap remove opera        # uninstall snap package

# Clean up unused packages
sudo apt autoremove
sudo apt autoclean
```

## Gotchas

- `apt update` does NOT install updates - it only refreshes the package list; `apt upgrade` does the actual updating
- `dpkg -i` does not resolve dependencies - if a `.deb` has unmet deps, run `sudo apt install -f` afterward
- `apt remove` leaves config files behind - use `apt purge` for complete removal
- `snap` packages are sandboxed and may have limited filesystem access compared to apt packages
- `dpkg` can manage installed packages but CANNOT download from remote repositories - that is apt's job
- Running `apt upgrade` without `apt update` first may install outdated versions

## See Also

- [[process-management]] - managing services installed by packages
- [[users-and-groups]] - sudo privileges needed for package management
- [[filesystem-hierarchy]] - where packages install files (`/usr/bin`, `/etc`, `/var`)
- `man apt` - https://man7.org/linux/man-pages/man8/apt.8.html
- `man dpkg` - https://man7.org/linux/man-pages/man1/dpkg.1.html
