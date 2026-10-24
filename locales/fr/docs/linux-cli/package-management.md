---
title: "Gestion des paquets"
category: reference
tags: [linux-cli, apt, dpkg, yum, dnf, rpm, snap, packages]
level: 3
source_sha256: 5c2b75702916d6036bcdfc6fa58a00e90bbb411a23e1d02738248150ffca15a2
translation: machine
translated_at: '2026-10-24'
---
# Gestion des paquets {#package-management}

Les logiciels Linux sont distribués sous forme de paquets, c'est-à-dire d'archives contenant des binaires, des bibliothèques, des fichiers de configuration et des métadonnées. Les gestionnaires de paquets prennent en charge l'installation, la résolution des dépendances, les mises à jour et la suppression, pour deux grands écosystèmes.

## Points clés {#key-facts}

- **Debian/Ubuntu** : paquets `.deb` - outils : dpkg, apt, aptitude
- **Red Hat/CentOS/Fedora** : paquets `.rpm` - outils : rpm, yum, dnf
- Les outils de haut niveau (apt, yum, dnf) résolvent automatiquement les dépendances
- Les outils de bas niveau (dpkg, rpm) ne gèrent que les fichiers des paquets individuels

## APT - Debian/Ubuntu {#apt-debianubuntu}

### Mise à jour et mise à niveau {#update-and-upgrade}

```bash
sudo apt update               # refresh package index (no installs)
sudo apt upgrade              # upgrade all packages
sudo apt full-upgrade         # upgrade + install new deps + remove obsolete
```

**update vs upgrade** : `update` synchronise la liste des paquets ; `upgrade` installe les versions plus récentes.

### Installation et suppression {#install-and-remove}

```bash
sudo apt install package              # install
sudo apt install pkg1 pkg2 pkg3       # install multiple
sudo apt install pkg --no-upgrade     # install only if not present
sudo apt install pkg --only-upgrade   # upgrade only if already installed
sudo apt remove package               # remove (keep config)
sudo apt purge package                # remove + delete config files
sudo apt autoremove                   # remove unused dependencies
```

### Recherche et informations {#search-and-info}

```bash
apt search keyword            # search packages
apt show package              # detailed info
apt list --installed          # list installed
apt list --upgradeable        # available upgrades
```

### Dépôts {#repositories}

Configuration : `/etc/apt/sources.list` et `/etc/apt/sources.list.d/`

```bash
sudo add-apt-repository ppa:user/repo     # add PPA (Ubuntu)
```

## dpkg - Debian bas niveau {#dpkg-low-level-debian}

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

## snap - Paquets universels {#snap-universal-packages}

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

Remplacement moderne de YUM, avec la même syntaxe.

```bash
dnf install package
dnf remove package
dnf update
dnf search keyword
dnf list installed
dnf history                   # transaction history
dnf history undo last         # undo last transaction
```

## RPM - Red Hat bas niveau {#rpm-low-level-red-hat}

```bash
sudo rpm -i package.rpm       # install
sudo rpm -U package.rpm       # upgrade
sudo rpm -e package           # remove
rpm -q package                # query if installed
rpm -qa                       # list all installed
rpm -ql package               # list files in package
rpm -qi package               # package info
```

## Comparaison {#comparison}

| Fonctionnalité | APT | YUM/DNF | dpkg | RPM |
|---------|-----|---------|------|-----|
| Distribution | Debian | RHEL | Debian | Red Hat |
| Résolution des dépendances | Oui | Oui | Non | Non |
| Dépôts distants | Oui | Oui | Non | Non |
| Format de paquet | .deb | .rpm | .deb | .rpm |

## winget - Gestionnaire de paquets Windows {#winget-windows-package-manager}

```bash
winget search package         # search
winget install package        # install
winget uninstall package      # remove
winget upgrade --all          # upgrade all
winget list                   # list installed
winget export -o pkgs.json    # export package list
winget import -i pkgs.json    # import and install
```

## Pièges courants {#gotchas}

- Exécutez toujours `apt update` avant `apt install` pour obtenir les dernières listes de paquets
- `apt remove` conserve les fichiers de configuration ; `apt purge` supprime tout
- `dpkg` ne peut pas résoudre les dépendances : utilisez `apt install -f` pour corriger les dépendances cassées après un passage par dpkg
- RPM échoue silencieusement en cas de dépendances manquantes : privilégiez toujours yum/dnf
- Les paquets `snap` sont isolés et autonomes, mais plus volumineux que les paquets natifs
- Mélanger les gestionnaires de paquets (par ex. apt + snap pour le même logiciel) peut provoquer des conflits

## Voir aussi {#see-also}

- [[python-and-node-cli]] - gestionnaires de paquets pip, npm
- [[docker-basics]] - Distribution de logiciels basée sur les conteneurs
