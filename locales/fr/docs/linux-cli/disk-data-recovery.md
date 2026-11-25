---
level: 3
source_sha256: a6d03443b411217a8385a96942b529e42b3daf90fd219a4effa23dbdf643ffbe
translation: machine
translated_at: '2026-10-24'
---
# Récupération de données sur disque : réparation au niveau bloc et des partitions {#disk-data-recovery-block-level-and-partition-repair}

Récupération de disques défaillants ou de grande capacité (16 To et plus) au niveau bloc : imagerie, réparation des partitions et de la GPT, réparation du système de fichiers. Suppose que le disque répond électriquement. Pour les bases (fdisk, mkfs, mount, fsck sur des disques sains), voir [[disks-and-filesystems]].

## Faits clés {#key-facts}

- **Imager avant toute intervention** : chaque écriture sur un disque défaillant réduit la probabilité de récupération. Cloner d'abord vers une destination saine, puis travailler sur le clone.
- La GPT stocke un **en-tête de sauvegarde au dernier LBA** du disque ; la seule corruption de l'en-tête primaire est récupérable grâce à la sauvegarde.
- La capacité maximale du MBR est de 2 To (2^32 × 512 octets). Les disques de plus de 2 To **nécessitent la GPT** : voir [[disks-and-filesystems]].
- Les disques 512e (par exemple WD Ultrastar HC550) annoncent des secteurs logiques de 512 octets mais utilisent des secteurs physiques de 4096 octets. Certains outils de récupération anciens calculent mal les décalages sur les disques 4Kn (4096 natifs).
- `ddrescue` peut être repris : une exécution interrompue redémarre à partir d'un fichier de cartographie, en préservant les données déjà lues correctement.
- Les disques CMR sont plus simples à récupérer que les disques SMR (à recouvrement) : pas de dépendance entre pistes pendant l'imagerie.
- Le triage avec `smartctl` vient en premier : si Reallocated_Sector_Ct, Current_Pending_Sector ou Reported_Uncorrect sont supérieurs à 0, considérer le disque comme défaillant en cours et l'imager immédiatement.

## Triage {#triage}

### Contrôle de santé avec smartctl {#smartctl-health-check}

```bash
# Install on Debian/Ubuntu
sudo apt install smartmontools

# Overall pass/fail
sudo smartctl -H /dev/sdX

# Full attribute dump (use -d sat for SATA drives accessed over USB)
sudo smartctl -a -d sat /dev/sdX

# Run short self-test (2 min); read results with -l selftest
sudo smartctl -t short /dev/sdX
sudo smartctl -l selftest /dev/sdX
```

**Attributs critiques : toute valeur RAW supérieure à 0 impose une imagerie immédiate :**

| ID | Nom | Action |
|----|-----|--------|
| 5 | Reallocated_Sector_Ct | Sauvegarder immédiatement |
| 187 | Reported_Uncorrect | Imager immédiatement |
| 197 | Current_Pending_Sector | Imager immédiatement |
| 198 | Offline_Uncorrectable | Imager immédiatement |
| 199 | UDMA_CRC_Error_Count | Vérifier d'abord le câble |
| 22 | Current_Helium_Level (normalisé) | <25 = panne imminente sur les disques à hélium |

**Règle d'interdiction d'écriture :** dès qu'un des attributs ci-dessus est déclenché, arrêter toute opération d'écriture sur le disque (pas de fsck, pas de chkdsk, pas d'outil de partitionnement). Chaque écriture risque d'écraser des secteurs que les outils de récupération pourraient relire.

### Vérifier la taille des secteurs avant les outils de récupération {#verify-sector-size-before-recovery-tools}

```bash
sudo smartctl -i /dev/sdX | grep "Sector Size"
# "512 bytes logical, 4096 bytes physical" = 512e (tools treat it as 512)
# "4096 bytes logical/physical" = 4Kn (older tools may misplace offsets)
```

## Imagerie {#imaging}

### ddrescue : flux de travail cloner d'abord {#ddrescue-clone-first-workflow}

`ddrescue` lit en plusieurs passes, marque les zones défectueuses dans un fichier de cartographie et réessaie avec des tailles de bloc de plus en plus petites. Le fichier de cartographie permet de reprendre une session interrompue sans relire les données correctes.

```bash
# Pass 1 — fast, skip bad areas
sudo ddrescue -d -r0 /dev/sdX /mnt/dest/disk.img /mnt/dest/disk.map

# Pass 2 — retry bad sectors (up to 3 attempts, smaller blocks)
sudo ddrescue -d -r3 /dev/sdX /mnt/dest/disk.img /mnt/dest/disk.map

# Pass 3 — reverse direction (sometimes reads stuck sectors)
sudo ddrescue -d -r3 -R /dev/sdX /mnt/dest/disk.img /mnt/dest/disk.map
```

**Options :**
- `-d` : E/S directes, contourne le cache de pages du noyau (essentiel pour les disques défaillants)
- `-r N` : nombre de nouvelles tentatives par bloc défectueux ; `-r0` ignore les nouvelles tentatives lors de la première passe
- `-R` : inversion du sens de lecture pour les zones défectueuses tenaces
- Le fichier de cartographie est en texte brut : pour suivre la progression, `cat /mnt/dest/disk.map`

### Exigences concernant la destination {#destination-requirements}

- La destination doit être **au moins aussi grande** que le périphérique source (et non seulement que les données utilisées).
- Écrire la destination sur un **disque physique différent** : ne jamais imager un disque sur lui-même.
- Pour un disque de 16 To : à environ 150 Mo/s (pont USB 3), une passe complète prend environ 30 heures. Les secteurs défectueux allongent nettement ce délai.

### Vérifier l'intégrité de l'image {#verify-image-integrity}

```bash
# Mount image as loop device, read-only
sudo losetup -P -r /dev/loop0 /mnt/dest/disk.img

# Check partition table is visible
sudo fdisk -l /dev/loop0

# Attempt read-only mount of data partition
sudo mount -o ro /dev/loop0p1 /mnt/verify
ls /mnt/verify

# Clean up
sudo umount /mnt/verify
sudo losetup -d /dev/loop0
```

### HDDSuperClone : pour les disques gravement défaillants {#hddsuperclone-for-severely-failing-drives}

Lorsque ddrescue se bloque parce que le disque se déconnecte sous charge ou subit des réinitialisations du bus sur certaines zones :

```bash
# HDDSuperClone has SCSI passthrough for finer head/zone control
# Run from a live Linux environment
sudo hddsuperclone --drive /dev/sdX --image /mnt/dest/disk.img \
  --log /mnt/dest/hsc.log --timeout 30
```

HDDSuperClone peut ignorer les données liées aux têtes défaillantes et récupérer le reste, ce que ddrescue ne peut pas faire à cette granularité.

## Réparation des partitions et du secteur de démarrage {#partition-boot-sector-repair}

**Travailler sur l'image (périphérique loop), pas sur le disque d'origine.**

### Structure de la GPT (exemple 16 To, 512e) {#gpt-structure-16-tb-example-512e}

| LBA | Contenu |
|-----|---------|
| 0 | MBR de protection (entrée 0xEE couvrant tout le disque) |
| 1 | En-tête GPT primaire (protégé par CRC32) |
| 2–33 | Table de partitions primaire (128 entrées) |
| 34+ | Données des partitions |
| dernier LBA − 33 à dernier LBA − 1 | Table de partitions de sauvegarde |
| dernier LBA | En-tête GPT de sauvegarde |

### Restaurer la GPT primaire à partir de la sauvegarde avec gdisk {#restore-primary-gpt-from-backup-with-gdisk}

```bash
sudo gdisk /dev/loop0   # or /dev/sdX on the clone
# Inside gdisk interactive prompt:
r          # recovery and transformation menu
b          # use backup GPT header to rebuild primary
w          # write changes
y          # confirm
```

### sgdisk : opérations GPT scriptables {#sgdisk-scriptable-gpt-operations}

```bash
# Verify GPT integrity (reads both primary and backup headers)
sudo sgdisk --verify /dev/loop0

# Back up GPT to file before any changes (the single most important step)
sudo sgdisk --backup=/mnt/dest/gpt-backup.bin /dev/loop0

# Restore GPT from backup file
sudo sgdisk --load-backup=/mnt/dest/gpt-backup.bin /dev/loop0

# Rebuild protective MBR (if LBA 0 is corrupt)
sudo sgdisk --mbrtogpt /dev/loop0

# Print partition table
sudo sgdisk --print /dev/loop0
```

### Réécrire le MBR de protection avec dd {#rewrite-protective-mbr-with-dd}

Lorsque le LBA 0 est corrompu mais que le LBA 1 (GPT primaire) est intact, on peut écrire un MBR de protection minimal :

```bash
# Zero out MBR region (first 512 bytes), preserving GPT at LBA 1
sudo dd if=/dev/zero of=/dev/loop0 bs=512 count=1 conv=notrunc

# Reapply protective MBR (gdisk does this automatically on write)
sudo gdisk /dev/loop0
# Then: w -> y
```

### testdisk : analyseur de tables de partitions {#testdisk-partition-table-scanner}

testdisk recherche les signatures de partitions sans rien écrire tant qu'on ne l'a pas explicitement confirmé.

```bash
sudo apt install testdisk
sudo testdisk /dev/loop0
```

**Déroulement interactif :**
1. Sélectionner le périphérique → type de table de partitions : `EFI GPT` (détecté automatiquement sur les grands disques)
2. `Analyse` → `Quick Search` (lecture seule)
3. Si des partitions sont trouvées : appuyer sur `p` pour lister les fichiers (confirme que les données sont accessibles)
4. `Deeper Search` si Quick Search ne trouve rien (analyse toute la surface du disque, plusieurs heures sur 16 To)
5. `Write` uniquement après avoir confirmé que les fichiers sont visibles, et uniquement sur l'image ou le clone

### gpart : réparation des partitions BSD (disponible sous Linux via un paquet) {#gpart-bsd-partition-repair-available-on-linux-via-package}

```bash
# Recover partition table from partition signatures
sudo gpart recover /dev/loop0
sudo gpart show /dev/loop0
```

## Réparation du système de fichiers {#filesystem-repair}

À exécuter sur la partition loop de l'image (`/dev/loop0p1`), jamais sur le périphérique d'origine.

### ext4 {#ext4}

```bash
# Check only (no writes)
sudo fsck.ext4 -n /dev/loop0p1

# Repair automatically (drive must be unmounted)
sudo fsck.ext4 -y /dev/loop0p1

# Force check even if filesystem marked clean
sudo fsck.ext4 -f -y /dev/loop0p1
```

### XFS {#xfs}

```bash
# Check only
sudo xfs_repair -n /dev/loop0p1

# Repair (must be unmounted)
sudo xfs_repair /dev/loop0p1

# If repair fails due to dirty log
sudo xfs_repair -L /dev/loop0p1   # zeroes journal — data loss risk, last resort
```

### NTFS (volumes Windows) {#ntfs-windows-volumes}

```bash
# Install ntfs-3g tools
sudo apt install ntfs-3g

# Safe check and fix (non-destructive)
sudo ntfsfix /dev/loop0p1

# Mount read-only first to verify data
sudo mount -t ntfs-3g -o ro /dev/loop0p1 /mnt/ntfs
ls /mnt/ntfs
sudo umount /mnt/ntfs
```

`ntfsfix` réinitialise le bit « dirty » afin que Windows exécute chkdsk au prochain démarrage. Pour une réparation NTFS approfondie, utiliser `chkdsk` de Windows sur l'image montée, mais seulement après avoir confirmé que l'original est imagé.

### PhotoRec : extraction de fichiers lorsque la structure de partitions a disparu {#photorec-file-carving-when-partition-structure-is-gone}

```bash
sudo photorec /dev/loop0
# Carves known file signatures regardless of filesystem structure
# Recovers files but loses directory structure and filenames
```

## Pièges à éviter {#gotchas}

- **Écrire sur le disque d'origine défaillant détruit toute possibilité de récupération.** fsck, l'écriture de testdisk, chkdsk, les outils de partitionnement : tous écrivent sur le disque. Une seule écriture dans une zone de secteurs défectueux peut corrompre une zone voisine encore lisible. Imager d'abord, toujours. C'est la règle la plus importante de la récupération de données.

- **L'en-tête GPT de sauvegarde se trouve au tout dernier LBA, et non à un décalage fixe.** Sur un disque de 16 To, le dernier LBA est d'environ 31 251 693 567. Les outils qui codent en dur l'emplacement de la GPT de sauvegarde (certains éditeurs de partitions anciens) la placent mal et corrompent la sauvegarde. Utiliser gdisk ou sgdisk, qui lisent le champ `BackupLBA` de l'en-tête primaire.

- **La confusion entre 4Kn et 512e fausse les calculs de décalage.** Un disque configuré en 4Kn (secteurs logiques de 4096 octets) a un nombre de LBA différent pour la même capacité. testdisk et certaines versions anciennes de gdisk supposent des secteurs de 512 octets. Vérifier avec `smartctl -i` avant d'exécuter un outil de partitionnement, et n'utiliser que des versions d'outils prenant en charge le 4Kn.

- **Le fichier de cartographie de ddrescue est le point de reprise.** Si on le perd, la prochaine exécution repart de zéro, avec le risque de relire plus de 12 heures de données déjà correctes. Conserver le fichier de cartographie sur le disque de destination, à côté de l'image.

- **losetup -P est nécessaire pour accéder aux partitions.** Sans `-P` (analyse des partitions), seul `/dev/loop0` existe et les nœuds de partitions individuels (`/dev/loop0p1`, etc.) ne sont pas créés.

- **Les disques à hélium (par exemple Ultrastar HC550) ne doivent jamais être ouverts.** Une rupture du joint à l'air provoque un contact tête-plateau en quelques secondes. Le remplacement physique d'une tête exige une salle blanche avec recharge en hélium ; le faire soi-même n'est pas envisageable.

## Voir aussi {#see-also}

- [[disks-and-filesystems]] : tables de partitions, mkfs, mount, fsck sur des disques sains, bases de SMART
- [[linux-kernel-and-boot]] : contexte du processus de démarrage, rôle du MBR/GPT au lancement du système
- [[monitoring-and-performance]] : surveillance des E/S disque (iostat, iotop) pendant les opérations de récupération
- [[bash-scripting]] : automatisation de la boucle ddrescue avec logique de nouvelles tentatives et notifications

**Documentation des outils :**
- Manuel de ddrescue : https://www.gnu.org/software/ddrescue/manual/ddrescue_manual.html
- Pas à pas de testdisk : https://www.cgsecurity.org/wiki/TestDisk_Step_By_Step
- Manuel de sgdisk : https://rodsbooks.com/gdisk/sgdisk-walkthrough.html
- Référence des attributs smartmontools : https://www.smartmontools.org/browser/trunk/smartmontools/drivedb.h
