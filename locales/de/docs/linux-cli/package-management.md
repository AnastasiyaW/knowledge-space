---
title: "Paketverwaltung"
category: reference
tags: [linux-cli, apt, dpkg, yum, dnf, rpm, snap, packages]
level: 3
source_sha256: 5c2b75702916d6036bcdfc6fa58a00e90bbb411a23e1d02738248150ffca15a2
translation: machine
translated_at: '2026-10-24'
---
# Paketverwaltung {#package-management}

Linux-Software wird als Pakete verteilt, also als Archive mit Binärdateien, Bibliotheken, Konfigurationen und Metadaten. Paketmanager übernehmen Installation, Auflösung von Abhängigkeiten, Aktualisierungen und Entfernung über zwei große Ökosysteme hinweg.

## Wichtige Fakten {#key-facts}

- **Debian/Ubuntu**: `.deb`-Pakete - Werkzeuge: dpkg, apt, aptitude
- **Red Hat/CentOS/Fedora**: `.rpm`-Pakete - Werkzeuge: rpm, yum, dnf
- High-Level-Werkzeuge (apt, yum, dnf) lösen Abhängigkeiten automatisch auf
- Low-Level-Werkzeuge (dpkg, rpm) verwalten nur einzelne Paketdateien

## APT - Debian/Ubuntu {#apt-debianubuntu}

### Aktualisieren und Upgrade {#update-and-upgrade}

```bash
sudo apt update               # refresh package index (no installs)
sudo apt upgrade              # upgrade all packages
sudo apt full-upgrade         # upgrade + install new deps + remove obsolete
```

**update vs. upgrade**: `update` synchronisiert die Paketliste; `upgrade` installiert neuere Versionen.

### Installieren und Entfernen {#install-and-remove}

```bash
sudo apt install package              # install
sudo apt install pkg1 pkg2 pkg3       # install multiple
sudo apt install pkg --no-upgrade     # install only if not present
sudo apt install pkg --only-upgrade   # upgrade only if already installed
sudo apt remove package               # remove (keep config)
sudo apt purge package                # remove + delete config files
sudo apt autoremove                   # remove unused dependencies
```

### Suche und Informationen {#search-and-info}

```bash
apt search keyword            # search packages
apt show package              # detailed info
apt list --installed          # list installed
apt list --upgradeable        # available upgrades
```

### Repositories {#repositories}

Konfiguration: `/etc/apt/sources.list` und `/etc/apt/sources.list.d/`

```bash
sudo add-apt-repository ppa:user/repo     # add PPA (Ubuntu)
```

## dpkg - Low-Level-Debian {#dpkg-low-level-debian}

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

## snap - Universelle Pakete {#snap-universal-packages}

```bash
sudo apt install snapd
snap find package             # search
sudo snap install package     # install
sudo snap remove package      # remove
snap list                     # installed snaps
snap refresh                  # update all
snap info package             # details
```

## YUM - RHEL/CentOS 7 {#yum-rhelcentos-7}

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

## DNF - RHEL 8+, Fedora {#dnf-rhel-8-fedora}

Moderner Ersatz für YUM mit gleicher Syntax.

```bash
dnf install package
dnf remove package
dnf update
dnf search keyword
dnf list installed
dnf history                   # transaction history
dnf history undo last         # undo last transaction
```

## RPM - Low-Level Red Hat {#rpm-low-level-red-hat}

```bash
sudo rpm -i package.rpm       # install
sudo rpm -U package.rpm       # upgrade
sudo rpm -e package           # remove
rpm -q package                # query if installed
rpm -qa                       # list all installed
rpm -ql package               # list files in package
rpm -qi package               # package info
```

## Vergleich {#comparison}

| Merkmal | APT | YUM/DNF | dpkg | RPM |
|---------|-----|---------|------|-----|
| Distribution | Debian | RHEL | Debian | Red Hat |
| Abhängigkeitsauflösung | Ja | Ja | Nein | Nein |
| Remote-Repositories | Ja | Ja | Nein | Nein |
| Paketformat | .deb | .rpm | .deb | .rpm |

## winget - Windows-Paketmanager {#winget-windows-package-manager}

```bash
winget search package         # search
winget install package        # install
winget uninstall package      # remove
winget upgrade --all          # upgrade all
winget list                   # list installed
winget export -o pkgs.json    # export package list
winget import -i pkgs.json    # import and install
```

## Stolperfallen {#gotchas}

- Führe immer `apt update` vor `apt install` aus, um die neuesten Paketlisten zu erhalten
- `apt remove` behält Konfigurationsdateien; `apt purge` entfernt alles
- `dpkg` kann keine Abhängigkeiten auflösen - verwende `apt install -f`, um defekte Abhängigkeiten nach dpkg zu reparieren
- RPM scheitert bei fehlenden Abhängigkeiten stillschweigend - bevorzuge daher immer yum/dnf
- `snap`-Pakete sind sandboxed und in sich geschlossen, aber größer als native Pakete
- Das Mischen von Paketmanagern (z. B. apt + snap für dieselbe Software) kann zu Konflikten führen

## Siehe auch {#see-also}

- [[python-and-node-cli]] - pip, npm Paketmanager
- [[docker-basics]] - Container-basierte Softwareverteilung
