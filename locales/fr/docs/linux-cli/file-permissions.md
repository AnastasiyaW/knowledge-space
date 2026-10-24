---
title: "Permissions de fichiers"
category: reference
tags: [linux-cli, permissions, chmod, chown, acl, security]
level: 3
source_sha256: 98cf21b2eebcd3749e552706e608081d620e5f7334504f9859d6fe68abf4670f
translation: machine
translated_at: '2026-10-24'
---
# Permissions de fichiers {#file-permissions}

Chaque fichier et répertoire sous Linux possède un propriétaire, un groupe et des bits de permission pour trois catégories : propriétaire (u), groupe (g), autres (o). Cette entrée couvre la lecture, la définition et l'extension des permissions.

## Points clés {#key-facts}

- Trois types de permission : lecture (r=4), écriture (w=2), exécution (x=1)
- Les nouveaux fichiers ont par défaut 666 moins umask ; les répertoires 777 moins umask
- Seul root peut modifier la propriété d'un fichier
- Les ACL offrent des permissions fines par utilisateur ou par groupe, au-delà du modèle de base

## Lecture des permissions {#reading-permissions}

```bash
ls -l file.txt
# -rw-r--r-- 1 alice users 2048 May 10 14:30 file.txt
```

```typescript
- rw- r-- r--
| |   |   +-- others: read only
| |   +------ group: read only
| +---------- owner: read + write
+------------- type (- = file, d = dir, l = symlink)
```

| Symbole | Sur les fichiers | Sur les répertoires |
|--------|----------|----------------|
| `r` | Lire le contenu | Lister le contenu |
| `w` | Modifier le fichier | Créer/supprimer des fichiers à l'intérieur |
| `x` | Exécuter comme programme | Entrer (cd) |

## chmod - Modifier les permissions {#chmod-change-permissions}

### Notation symbolique {#symbolic-notation}

```bash
chmod u+x file          # add execute for owner
chmod g-w file          # remove write for group
chmod o+r file          # add read for others
chmod a+x file          # add execute for all
chmod u+rwx,g-w,o-r file  # multiple changes
chmod u=rwx,g=rx,o= file  # set exact permissions
chmod -R 755 dir/       # recursive
```

Catégories : `u` = propriétaire, `g` = groupe, `o` = autres, `a` = tous

### Notation octale {#octal-notation}

| Octal | Symbolique | Usage typique |
|-------|----------|-------------|
| 755 | rwxr-xr-x | Exécutables, répertoires |
| 644 | rw-r--r-- | Fichiers ordinaires |
| 600 | rw------- | Fichiers privés (clés SSH) |
| 700 | rwx------ | Répertoires privés |
| 777 | rwxrwxrwx | Totalement ouvert (à éviter) |

```bash
chmod 644 file          # rw-r--r--
chmod 755 file          # rwxr-xr-x
chmod 700 file          # rwx------
```

## chown - Modifier le propriétaire {#chown-change-owner}

```bash
sudo chown alice file              # change owner
sudo chown alice:devs file         # change owner and group
sudo chown :devs file              # change group only
sudo chown -R alice:devs dir/      # recursive
```

## chgrp - Modifier le groupe {#chgrp-change-group}

```bash
sudo chgrp groupname file
sudo chgrp -R groupname dir/
```

## Bits de permission spéciaux {#special-permission-bits}

### SUID (Set User ID) - bit 4 {#suid-set-user-id-bit-4}

L'exécutable s'exécute avec l'UID du **propriétaire** du fichier, et non celui de l'appelant.

```bash
chmod u+s file          # set SUID
chmod 4755 file         # octal
# ls -l shows: -rwsr-xr-x
```

Exemple : `/usr/bin/passwd` possède le SUID afin que tout utilisateur puisse changer son mot de passe.

### SGID (Set Group ID) - bit 2 {#sgid-set-group-id-bit-2}

Sur les exécutables : le programme s'exécute avec le groupe du fichier. Sur les répertoires : les nouveaux fichiers héritent du groupe du répertoire.

```bash
chmod g+s dir/          # set SGID
chmod 2755 dir/         # octal
# ls -l shows: drwxr-sr-x
```

### Sticky bit - bit 1 {#sticky-bit-bit-1}

Sur les répertoires : les utilisateurs ne peuvent supprimer que les fichiers qu'ils possèdent.

```bash
chmod +t dir/           # set sticky bit
chmod 1777 dir/         # octal
# ls -l shows: drwxrwxrwt
```

`/tmp` possède le sticky bit par défaut.

## umask - Permissions par défaut {#umask-default-permissions}

Définit les bits qui sont **retirés** des permissions par défaut.

```bash
umask              # show current umask
umask -S           # show in symbolic form
umask 022          # set umask
```

Avec un umask de 022 : les fichiers obtiennent 644 (666-022), les répertoires 755 (777-022).

## ACL - Listes de contrôle d'accès {#acl-access-control-lists}

Permissions fines pour des utilisateurs et groupes individuels.

```bash
# View
getfacl file

# Set
setfacl -m u:alice:rw file          # give alice read+write
setfacl -m g:devs:r file            # give group read
setfacl -x u:alice file             # remove alice's ACL entry
setfacl -b file                     # remove all ACL entries
setfacl -d -m u:alice:rw dir/       # set default ACL (inherited by new files)
setfacl -R -m u:alice:rw dir/       # recursive
```

Types d'ACL : **ACL d'accès** (directe), **ACL par défaut** (héritée par les nouveaux fichiers des répertoires).

## chroot - Changer de racine {#chroot-change-root}

Isole un processus en modifiant son répertoire racine apparent.

```bash
sudo chroot /new/root command
```

Cas d'usage : séparation de privilèges, environnements de récupération, pots de miel. Ce n'est pas une frontière de sécurité complète à elle seule.

## Pièges courants {#gotchas}

- `chmod 777` n'est presque jamais la bonne solution : identifiez la permission réellement nécessaire
- Le SUID sur les scripts est ignoré par la plupart des noyaux pour des raisons de sécurité
- `chown` exige root même si vous êtes propriétaire du fichier (cela empêche l'usurpation d'UID)
- L'indicateur `+` des ACL dans la sortie de `ls -l` (par exemple `drwxr-xr-x+`) signifie que des ACL sont définies
- umask est propre à chaque session : définissez-le dans `~/.bashrc` pour le rendre persistant
- Un chmod récursif sur `/` cassera le système

## Voir aussi {#see-also}

- [[users-and-groups]] - Gestion des utilisateurs et sudo
- [[linux-security]] - Vue d'ensemble des mécanismes de sécurité
- [[ssh-remote-access]] - Permissions des fichiers de clés SSH
