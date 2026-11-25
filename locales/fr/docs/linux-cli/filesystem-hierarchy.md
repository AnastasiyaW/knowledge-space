---
title: "Norme de hiérarchie du système de fichiers"
category: concepts
tags: [linux-cli, filesystem, fhs, directories]
level: 3
source_sha256: 0a116d7c529345203175b21a5a5682b4a13b39b184311494e9f56d900a9f66e5
translation: machine
translated_at: '2026-10-24'
---
# Norme de hiérarchie du système de fichiers {#filesystem-hierarchy-standard}

Linux suit la Filesystem Hierarchy Standard (FHS). Il n'existe pas de lettres de lecteur : tout part d'une racine unique `/`. Tous les périphériques, systèmes de fichiers réseau et interfaces spéciales sont rattachés à l'arborescence par montage. Cette entrée décrit la disposition des répertoires et la philosophie « tout est un fichier ».

## Points clés {#key-facts}

- Racine unique `/` - pas de lettres de lecteur (C:, D:)
- Système de fichiers sensible à la casse
- Tous les périphériques physiques, montages réseau et interfaces virtuelles apparaissent sous forme de fichiers dans l'arborescence
- Les fichiers de configuration se trouvent dans `/etc`, les journaux dans `/var/log`, les données utilisateur dans `/home`

## Disposition standard des répertoires {#standard-directory-layout}

| Répertoire | Rôle |
|-----------|---------|
| `/` | Racine de l'arborescence du système de fichiers |
| `/bin` | Binaires utilisateur essentiels (ls, cp, mv, bash) |
| `/sbin` | Binaires système (iptables, reboot, fdisk) |
| `/boot` | Noyau, initrd, chargeur de démarrage GRUB |
| `/dev` | Fichiers de périphériques (interfaces matérielles) |
| `/etc` | Fichiers de configuration à l'échelle du système |
| `/home` | Répertoires personnels des utilisateurs |
| `/lib`, `/lib64` | Bibliothèques partagées pour `/bin` et `/sbin` |
| `/media` | Périphériques amovibles montés automatiquement (USB, CD) |
| `/mnt` | Point de montage manuel ou temporaire |
| `/opt` | Logiciels optionnels ou tiers |
| `/proc` | FS virtuel : informations sur les processus et le noyau |
| `/root` | Répertoire personnel de l'utilisateur root |
| `/run` | Données d'exécution (PID, sockets) - vidé au redémarrage |
| `/srv` | Données des services (web, FTP) |
| `/sys` | Informations sur les périphériques et pilotes du noyau |
| `/tmp` | Fichiers temporaires - vidé au redémarrage |
| `/usr` | Programmes, bibliothèques et documentation utilisateur |
| `/var` | Données variables : journaux, courrier, caches |

## Tout est un fichier {#everything-is-a-file}

Philosophie Unix : périphériques, répertoires, tubes et sockets sont tous représentés sous forme de fichiers.

| Symbole dans `ls -l` | Type |
|-------------------|------|
| `-` | Fichier ordinaire |
| `d` | Répertoire |
| `l` | Lien symbolique |
| `b` | Périphérique bloc (accès aléatoire : HDD, SSD) |
| `c` | Périphérique caractère (séquentiel : terminal, clavier) |
| `p` | Tube nommé (FIFO) |
| `s` | Socket |

## Systèmes de fichiers spéciaux {#special-filesystems}

| Type | Montage | Rôle |
|------|-------|---------|
| **procfs** | `/proc` | Informations sur les processus, paramètres du noyau (requis par `ps`, `top`) |
| **sysfs** | `/sys` | Informations sur les périphériques et pilotes du noyau |
| **tmpfs** | `/tmp`, `/run` | Adossé à la RAM, rapide, vidé au redémarrage |
| **devfs** | `/dev` | Fichiers de périphériques (gérés par `udev` au démarrage) |

## Types de systèmes de fichiers pour les partitions {#filesystem-types-for-disk-partitions}

- **ext4** - valeur par défaut standard sous Linux
- **ext3** - ancien FS journalisé
- **XFS** - haute performance, par défaut sur RHEL/CentOS
- **btrfs** - moderne : instantanés, compression, sous-volumes
- **NTFS/FAT32** - systèmes de fichiers Windows (lecture et écriture prises en charge)

### Systèmes de fichiers virtuels et overlay {#virtualoverlay-filesystems}

- **VFS** - abstraction du noyau pour un accès uniforme aux FS
- **NFS** - montage d'un système de fichiers distant via le réseau
- **AUFS** - fusion de plusieurs systèmes de fichiers (utilisé par Docker)
- **EncFS** - chiffrement transparent des fichiers

## Commandes d'utilisation du disque {#disk-usage-commands}

```bash
df -h                    # mounted filesystems and space usage
df -h /home              # specific mount
du -sh /var/log          # total size of directory
du -h --max-depth=1 /    # size per top-level directory
lsblk                    # list block devices
```

## Utilitaires d'archivage {#archive-utilities}

```bash
# tar
tar -czf archive.tar.gz dir/         # create gzip archive
tar -xzf archive.tar.gz              # extract
tar -tf archive.tar.gz               # list contents

# zip
zip -r archive.zip dir/
unzip archive.zip
unzip -l archive.zip                  # list contents
```

## Pièges courants {#gotchas}

- `/tmp` a le sticky bit par défaut : tout le monde peut écrire, mais seuls les propriétaires peuvent supprimer leurs propres fichiers
- Les fichiers de `/proc` ont une taille de 0 dans `ls` mais contiennent des données à la lecture (générées à la volée par le noyau)
- `/run` ou `/var/run` : `/run` est un tmpfs (vidé au redémarrage), `/var/run` peut persister
- `/home` est souvent une partition séparée : réinstaller le système préserve les données utilisateur

## Voir aussi {#see-also}

- [[disks-and-filesystems]] - Partitions, formatage, fonctionnement interne d'ext4, LVM
- [[file-permissions]] - Modèle de permissions, chmod, chown
- [[links-and-inodes]] - Inodes, liens physiques, liens symboliques
