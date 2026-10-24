---
title: "Fondamentaux du système Linux pour la sécurité"
category: concepts
tags: [security, linux, filesystem, kernel, boot-process, disk-encryption]
level: 3
source_sha256: 8be16dab731ce6ff11c6e1f909a4899ed1dc70c0ecaf7d338329e24ab9a6575b
translation: machine
translated_at: '2026-10-24'
---
# Fondamentaux du système Linux pour la sécurité {#linux-os-fundamentals-for-security}

Éléments internes de Linux pertinents pour la sécurité : arborescence du système de fichiers, modèle utilisateur, noyau et espace utilisateur, processus de démarrage, chiffrement de disque (LUKS), fonctionnement interne du système de fichiers (inodes), gestion des périphériques et gestion des paquets.

## Points clés {#key-facts}
- Sous Linux, tout est fichier (fichiers réguliers, répertoires, périphériques, sockets, tubes)
- Root (UID 0) dispose d'un accès illimité ; les utilisateurs système (1-999) exécutent les services ; les utilisateurs ordinaires (1000+)
- `/etc/shadow` stocke les hachages de mots de passe (lisible uniquement par root) ; `/etc/passwd` est lisible par tous
- LUKS fournit le chiffrement complet du disque, avec une phrase de passe requise au démarrage
- L'espace noyau accède directement au matériel ; l'espace utilisateur n'accède au matériel que via des appels système
- UEFI Secure Boot empêche le chargement de noyaux et de modules non signés

## Arborescence du système de fichiers (FHS) {#filesystem-hierarchy-fhs}
```javascript
/bin     Essential user binaries
/sbin    System binaries (fdisk, iptables)
/etc     Configuration files
/home    User home directories
/root    Root's home
/var     Variable data (logs, databases)
/tmp     Temporary (cleared on reboot)
/usr     User programs and libraries
/dev     Device files
/proc    Virtual FS - process/kernel info
/sys     Virtual FS - hardware/driver info
/boot    Bootloader, kernel, initramfs
```

## Modèle utilisateur {#user-model}
- Format de `/etc/passwd` : `username:x:UID:GID:comment:home:shell`
- Format de `/etc/shadow` : `username:$hash:last_change:min:max:warn:inactive:expire`
- `/etc/group` - définitions de l'appartenance aux groupes
- Les utilisateurs système exécutent les services avec des privilèges minimaux (www-data, mysql, nobody)

## Architecture du noyau {#kernel-architecture}

### Espace utilisateur et espace noyau {#user-space-vs-kernel-space}
- **Espace noyau** - mode privilégié, accès direct au matériel, gestion de la mémoire, ordonnancement
- **Espace utilisateur** - non privilégié, où s'exécutent les applications
- **Appels système** - interface entre les deux espaces (open, read, write, fork, exec, socket)

### Modules du noyau {#kernel-modules}
```bash
lsmod                    # List loaded modules
modprobe <module>        # Load module
rmmod <module>           # Remove module
modinfo <module>         # Module information
```
Risque de sécurité : les rootkits chargés comme modules du noyau peuvent masquer des processus, des fichiers et des connexions.

## Processus de démarrage {#boot-process}
1. Mise sous tension -> POST du BIOS/UEFI
2. Le BIOS charge le MBR / l'UEFI lit la partition EFI
3. Le chargeur de démarrage GRUB charge le noyau + initramfs
4. Le noyau initialise le matériel et monte le système de fichiers racine
5. systemd (PID 1) démarre les services de l'espace utilisateur
6. Invite de connexion

### BIOS et UEFI {#bios-vs-uefi}
| Caractéristique | BIOS | UEFI |
|---------|------|------|
| Largeur de bits | 16 bits | 32/64 bits |
| Partitionnement | MBR (4 primaires, 2 To max) | GPT (128 partitions, 9,4 Zo) |
| Sécurité | Aucune | Secure Boot |
| Vitesse de démarrage | Séquentielle | Parallèle |

## Chiffrement de disque (LUKS) {#disk-encryption-luks}
- Chiffre une partition ou un volume logique entier
- Phrase de passe requise au démarrage (avant le chargement du système d'exploitation)
- Peut utiliser des fichiers de clé stockés sur un périphérique USB séparé
- Standard pour le chiffrement complet du disque sous Linux

## Gestion des disques et des systèmes de fichiers {#disk-and-filesystem-management}
```bash
lsblk                          # List block devices
fdisk /dev/sda                 # MBR partition editor
gdisk /dev/sda                 # GPT partition editor
mkfs.ext4 /dev/sda1            # Format as ext4
mount /dev/sda1 /mnt           # Mount
umount /mnt                    # Unmount
fsck /dev/sda1                 # Check/repair (unmounted only!)
```
Montages persistants : `/etc/fstab`.

## Inodes {#inodes}
Chaque fichier possède un inode contenant : le type, les permissions, le propriétaire, la taille, les horodatages, les pointeurs vers les blocs de données et le nombre de liens. L'inode ne contient PAS le nom du fichier, qui est stocké dans l'entrée du répertoire.
```bash
ls -i          # Show inode numbers
df -i          # Show inode usage
```

## Récupération de fichiers supprimés {#deleted-file-recovery}
Lorsqu'un fichier est supprimé, son inode est marqué comme libre, mais les blocs de données restent intacts jusqu'à leur écrasement :
- **extundelete** - récupération sur ext3/ext4
- **testdisk / photorec** - récupération sur plusieurs systèmes de fichiers
- Agir vite : plus l'activité disque est importante, plus les données sont écrasées

## Gestion des paquets {#package-management}
```bash
# Debian/Ubuntu (APT)
apt update && apt upgrade
apt install <package>
dpkg -l                    # List installed
dpkg -S /path/to/file      # Find owning package

# Red Hat (RPM/DNF)
dnf install <package>
rpm -qa                    # List all installed
rpm -qf /path/to/file      # Find owning package
```

## Gestion des processus {#process-management}
```bash
ps aux                     # All processes
ps -ef --forest            # Process tree
top / htop                 # Interactive monitor
strace -p PID              # Trace system calls
kill PID / kill -9 PID    # Terminate
nice -n 10 command         # Adjusted priority
ss -tulnp                  # Listening sockets with process info
lsof -i :80               # Process using port 80
```

## Pièges à éviter {#gotchas}
- `/etc/passwd` est lisible par tous par conception ; les hachages de mots de passe se trouvent dans `/etc/shadow`
- Exécuter `fsck` sur un système de fichiers monté provoque une corruption des données
- Les fichiers supprimés restent récupérables tant qu'ils n'ont pas été écrasés ; utilisez `shred` pour une suppression sécurisée
- Les processus zombies (état Z) ne sont pas des fuites de ressources : ils conservent simplement un statut de sortie non récupéré
- `/proc` et `/sys` sont virtuels : ils n'existent qu'en mémoire, et non sur le disque

## Voir aussi {#see-also}
- [[linux-system-hardening]] - SSH, fail2ban, auditd, sysctl
- [[privilege-escalation-techniques]] - SUID, sudo, exploits du noyau
- [[network-security-and-protocols]] - Réseau Linux
