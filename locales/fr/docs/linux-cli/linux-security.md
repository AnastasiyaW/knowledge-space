---
title: "Sécurité Linux"
category: concepts
tags: [linux-cli, security, dac, mac, selinux, namespaces, malware, pentesting]
level: 4
source_sha256: fe7bac2638a03a9c90ee6a1adb69be58e9eb39b9a66bf3b830e5cd7d653e6b9c
translation: machine
translated_at: '2026-10-24'
---
# Sécurité Linux {#linux-security}

Linux offre plusieurs couches de sécurité : des permissions de fichiers de base (DAC) au contrôle d'accès obligatoire (MAC), en passant par l'isolation des processus (namespaces) et les systèmes d'audit. Cette entrée couvre les mécanismes de sécurité, les menaces courantes, les techniques de reconnaissance et les outils de tests de sécurité.

## Mécanismes de sécurité {#security-mechanisms}

| Mécanisme | Description |
|-----------|-------------|
| **DAC** | Contrôle d'accès discrétionnaire : le propriétaire du fichier définit la politique |
| **ACL** | Permissions fines par utilisateur ou groupe |
| **Capabilities** | Privilèges élevés spécifiques, sans root complet |
| **Namespaces** | Isolent les PID, noms d'hôte, UID, réseaux, systèmes de fichiers : fondement des conteneurs |
| **MAC** | Contrôle d'accès obligatoire : centralisé, même le propriétaire ne peut pas le contourner (SELinux, AppArmor) |
| **Seccomp** | Restreint le processus aux seuls appels système nécessaires |
| **Audit** | Journalise tous les événements liés à la sécurité |
| **Integrity** | Vérifie l'intégrité des fichiers système via des empreintes (hashes) |

### API LSM (Linux Security Modules) {#lsm-linux-security-modules-api}

Fournit le cadre permettant à tous les mécanismes de sécurité de communiquer avec le noyau. Implémentations : SELinux, AppArmor, Smack.

## Reconnaissance du système {#system-reconnaissance}

Commandes qu'un attaquant (ou un administrateur effectuant un audit) utiliserait :

```bash
hostname                          # machine name
uname -a                          # kernel version and distro
cat /etc/*-release                # distribution info
cat /etc/passwd                   # user list
ps aux                            # running processes
systemctl list-units --state=running  # running services
```

Informations collectées : CVE du noyau, comptes utilisateurs pour les attaques par mot de passe, rôles des services, chemins d'élévation de privilèges.

## Élévation de privilèges {#privilege-escalation}

La plupart des exploits ciblent des vulnérabilités du noyau pour obtenir des privilèges maximaux.

```bash
uname -a              # kernel version
cat /etc/*-release    # distro info
```

Sources d'exploits : exploit-db.com, cvedetails.com, packetstormsecurity.org, cve.mitre.org

### Transfert d'exploits avec netcat {#transferring-exploits-with-netcat}

```bash
# Receiver (target):
nc -l -p 1234 > exploit_file

# Sender:
nc <target_ip> 1234 < exploit_file
```

## Types de malwares {#malware-types}

| Type | Description |
|------|-------------|
| **Virus** | Se réplique en s'injectant dans d'autres programmes |
| **Trojan** | Malware déguisé, sans propagation autonome (inclut les ransomwares) |
| **Rootkit** | Dissimule le malware à un niveau profond du système |
| **Backdoor** | Accès distant persistant |
| **Botnet** | Réseau d'appareils infectés sous contrôle à distance |
| **Exploit** | Code ciblant une vulnérabilité spécifique |

## chroot {#chroot}

Modifie le répertoire racine apparent d'un processus.

```bash
# Rescue mode example
mount /dev/sda1 /mnt
mount -o bind /dev /mnt/dev
mount -o bind /proc /mnt/proc
mount -o bind /sys /mnt/sys
chroot /mnt /bin/bash
# Now inside broken system - repair bootloader, reset passwords
exit
umount /mnt/{dev,proc,sys}
umount /mnt
```

Avertissement : chroot n'est PAS une frontière de sécurité à lui seul.

## Outils de tests de sécurité {#security-testing-tools}

| Outil | Usage |
|-------|-------|
| **Metasploit** | Framework de tests de vulnérabilités et d'exploitation |
| **Nmap** | Scan réseau et inventaire |
| **Wireshark** | Inspection de paquets |
| **Nikto** | Scanner de vulnérabilités de serveurs web |
| **SQLmap** | Tests de sécurité des bases de données |
| **OWASP ZAP** | Sécurité des applications web |
| **John the Ripper** | Craquage de mots de passe hors ligne |
| **Hydra** | Attaque par force brute en ligne sur l'authentification |
| **Maltego** | OSINT et analyse de liens |

### John the Ripper {#john-the-ripper}

```bash
john /etc/shadow                    # crack shadow file
john --wordlist=wordlist.txt hash   # dictionary attack
john --show /etc/shadow             # show cracked
```

### Hydra {#hydra}

```bash
hydra -l admin -P wordlist.txt ssh://192.168.1.10
hydra -L users.txt -P pass.txt ftp://192.168.1.10
```

### Nikto {#nikto}

```bash
nikto -h <IP_or_hostname>
nikto -h <hostname> -ssl           # HTTPS
nikto -h <IP> -Format msf+        # export for Metasploit
```

## Distributions orientées sécurité {#security-distros}

| Distribution | Base | Orientation |
|--------------|------|-------------|
| **Kali Linux** | Debian | Pentesting général |
| **Parrot OS** | Debian | Cloud, anonymat, cryptographie |
| **BlackArch** | Arch | Vaste dépôt d'outils |
| **BackBox** | Ubuntu | Pentesting minimaliste |

## Étapes d'une attaque {#attack-stages}

1. **Reconnaissance** : collecter des informations sur le système
2. **Scanning** : identifier les services, versions et vulnérabilités
3. **Obtention d'accès** : exploiter les vulnérabilités
4. **Maintien d'accès** : backdoors, nouveaux utilisateurs
5. **Effacement des traces** : nettoyer ou corrompre les journaux

## Pièges à éviter {#gotchas}

- « Linux est intrinsèquement sécurisé » est un mythe : la sécurité exige une configuration adéquate
- Des malwares Linux existent, notamment ciblant les serveurs, l'IoT et le cloud
- chroot peut être contourné par un processus root : il ne convient pas comme isolation unique
- Exécuter des services en root augmente la surface d'attaque : utiliser des comptes de service dédiés
- Les exploits du noyau donnent les privilèges les plus élevés : maintenir le noyau à jour
- Les namespaces (conteneurs) offrent une meilleure isolation que chroot, mais ne sont pas des VM

## Voir aussi {#see-also}

- [[file-permissions]] - DAC, ACL, bits spéciaux
- [[users-and-groups]] - Gestion des comptes, sudo
- [[firewall-and-iptables]] - Sécurité réseau
- [[ssh-remote-access]] - Durcissement de l'accès distant
- [[logging-and-journald]] - auditd, journalisation de sécurité
