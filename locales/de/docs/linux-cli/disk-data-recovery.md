---
level: 3
source_sha256: a6d03443b411217a8385a96942b529e42b3daf90fd219a4effa23dbdf643ffbe
translation: machine
translated_at: '2026-10-24'
---
# Datenrettung — Repair auf Blockebene und an Partitionen {#disk-data-recovery-block-level-and-partition-repair}

Wiederherstellung ausgefallener oder großer (16 TB+) Laufwerke auf Blockebene: Imaging, Reparatur von Partition/GPT, Reparatur des Dateisystems. Vorausgesetzt wird, dass das Laufwerk elektrisch ansprechbar ist. Zu den Grundlagen (fdisk, mkfs, mount, fsck auf gesunden Laufwerken) siehe [[disks-and-filesystems]].

## Wichtige Fakten {#key-facts}

- **Vor jeder Veränderung imagen** — jeder Schreibvorgang auf einem ausfallenden Laufwerk verringert die Wiederherstellbarkeit. Zuerst auf ein gesundes Ziel klonen, dann mit dem Klon arbeiten.
- GPT speichert einen **Backup-Header an der letzten LBA** der Festplatte; eine Beschädigung allein des primären Headers lässt sich über das Backup wiederherstellen.
- Die maximale Kapazität von MBR beträgt 2 TB (2^32 × 512 Byte). Laufwerke über 2 TB **erfordern GPT** — siehe [[disks-and-filesystems]].
- 512e-Laufwerke (z. B. WD Ultrastar HC550) melden 512-Byte-Logiksektoren, verwenden aber 4096-Byte-Physiksektoren. Einige ältere Recovery-Tools berechnen Offsets auf 4Kn-Laufwerken (4096 Byte nativ) falsch.
- `ddrescue` ist fortsetzbar: unterbrochene Läufe starten anhand einer Map-Datei neu und bewahren bereits gelesene gute Daten.
- CMR-Laufwerke lassen sich einfacher wiederherstellen als SMR-Laufwerke (Shingled) — beim Imaging gibt es keine Abhängigkeit zwischen Spuren.
- Die Triage mit `smartctl` kommt zuerst: Wenn Reallocated_Sector_Ct, Current_Pending_Sector oder Reported_Uncorrect größer als 0 sind, ist das Laufwerk als aktiv ausfallend zu behandeln und sofort zu imagen.

## Triage {#triage}

### Zustandsprüfung mit smartctl {#smartctl-health-check}

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

**Kritische Attribute — jeder RAW-Wert > 0 bedeutet sofortiges Imaging:**

| ID | Name | Maßnahme |
|----|------|----------|
| 5 | Reallocated_Sector_Ct | Jetzt sichern |
| 187 | Reported_Uncorrect | Sofort imagen |
| 197 | Current_Pending_Sector | Sofort imagen |
| 198 | Offline_Uncorrectable | Sofort imagen |
| 199 | UDMA_CRC_Error_Count | Zuerst Kabel prüfen |
| 22 | Current_Helium_Level (normalisiert) | <25 = bevorstehender Ausfall bei Helium-Laufwerken |

**Regel: nicht schreiben.** Sobald einer der oben genannten Werte auslöst, sind alle Schreibvorgänge auf dem Laufwerk einzustellen (kein fsck, kein chkdsk, keine Partitionswerkzeuge). Jeder Schreibvorgang riskiert, Sektoren zu überschreiben, die Recovery-Tools erneut lesen könnten.

### Sektorgröße prüfen, bevor Recovery-Tools eingesetzt werden {#verify-sector-size-before-recovery-tools}

```bash
sudo smartctl -i /dev/sdX | grep "Sector Size"
# "512 bytes logical, 4096 bytes physical" = 512e (tools treat it as 512)
# "4096 bytes logical/physical" = 4Kn (older tools may misplace offsets)
```

## Imaging {#imaging}

### ddrescue — Workflow mit Klonen zuerst {#ddrescue-clone-first-workflow}

`ddrescue` liest in mehreren Durchgängen, markiert fehlerhafte Bereiche in einer Map-Datei und wiederholt Versuche mit schrittweise kleineren Blockgrößen. Die Map-Datei ermöglicht es, eine unterbrochene Sitzung fortzusetzen, ohne bereits gute Daten erneut zu lesen.

```bash
# Pass 1 — fast, skip bad areas
sudo ddrescue -d -r0 /dev/sdX /mnt/dest/disk.img /mnt/dest/disk.map

# Pass 2 — retry bad sectors (up to 3 attempts, smaller blocks)
sudo ddrescue -d -r3 /dev/sdX /mnt/dest/disk.img /mnt/dest/disk.map

# Pass 3 — reverse direction (sometimes reads stuck sectors)
sudo ddrescue -d -r3 -R /dev/sdX /mnt/dest/disk.img /mnt/dest/disk.map
```

**Flags:**
- `-d` — Direct I/O, umgeht den Kernel-Seitencache (entscheidend bei ausfallenden Laufwerken)
- `-r N` — Anzahl der Wiederholungen pro fehlerhaften Block; `-r0` überspringt Wiederholungen im ersten Durchgang
- `-R` — Umgekehrte Leserichtung für hartnäckige Problembereiche
- Die Map-Datei ist reiner Text — Fortschritt prüfen mit `cat /mnt/dest/disk.map`

### Anforderungen an das Ziel {#destination-requirements}

- Das Ziel muss **mindestens so groß** sein wie das Quellgerät (nicht nur die belegten Daten).
- Das Ziel muss auf einem **anderen physischen Laufwerk** liegen — niemals ein Laufwerk auf sich selbst imagen.
- Bei einem 16-TB-Laufwerk benötigt ein vollständiger Durchgang bei etwa 150 MB/s (USB-3-Bridge) rund 30 Stunden. Fehlerhafte Sektoren verlängern dies erheblich.

### Integrität des Images prüfen {#verify-image-integrity}

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

### HDDSuperClone — für stark ausfallende Laufwerke {#hddsuperclone-for-severely-failing-drives}

Wenn ddrescue ins Stocken gerät, weil das Laufwerk unter Last abbricht oder in bestimmten Zonen Bus-Resets auslöst:

```bash
# HDDSuperClone has SCSI passthrough for finer head/zone control
# Run from a live Linux environment
sudo hddsuperclone --drive /dev/sdX --image /mnt/dest/disk.img \
  --log /mnt/dest/hsc.log --timeout 30
```

HDDSuperClone kann Daten überspringen, die an ausfallende Köpfe gebunden sind, und den Rest wiederherstellen. Das kann ddrescue auf dieser Granularität nicht.

## Reparatur von Partition und Bootsektor {#partition-boot-sector-repair}

**Auf dem Image (Loop-Device) arbeiten, nicht auf dem Originallaufwerk.**

### GPT-Struktur (Beispiel 16 TB, 512e) {#gpt-structure-16-tb-example-512e}

| LBA | Inhalt |
|-----|--------|
| 0 | Protective MBR (0xEE-Eintrag über die gesamte Festplatte) |
| 1 | Primärer GPT-Header (CRC32-geschützt) |
| 2–33 | Primäre Partitionstabelle (128 Einträge) |
| 34+ | Partitionsdaten |
| letzte LBA − 33 bis letzte LBA − 1 | Backup-Partitionstabelle |
| letzte LBA | Backup-GPT-Header |

### Primäre GPT aus dem Backup mit gdisk wiederherstellen {#restore-primary-gpt-from-backup-with-gdisk}

```bash
sudo gdisk /dev/loop0   # or /dev/sdX on the clone
# Inside gdisk interactive prompt:
r          # recovery and transformation menu
b          # use backup GPT header to rebuild primary
w          # write changes
y          # confirm
```

### sgdisk — skriptbare GPT-Operationen {#sgdisk-scriptable-gpt-operations}

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

### Protective MBR mit dd neu schreiben {#rewrite-protective-mbr-with-dd}

Wenn LBA 0 beschädigt ist, LBA 1 (primäre GPT) aber intakt ist, kann eine minimale Protective MBR geschrieben werden:

```bash
# Zero out MBR region (first 512 bytes), preserving GPT at LBA 1
sudo dd if=/dev/zero of=/dev/loop0 bs=512 count=1 conv=notrunc

# Reapply protective MBR (gdisk does this automatically on write)
sudo gdisk /dev/loop0
# Then: w -> y
```

### testdisk — Scanner für Partitionstabellen {#testdisk-partition-table-scanner}

testdisk sucht nach Partitionssignaturen und schreibt nichts, bis ausdrücklich bestätigt wird.

```bash
sudo apt install testdisk
sudo testdisk /dev/loop0
```

**Interaktiver Ablauf:**
1. Gerät auswählen → Partitionstabellentyp: `EFI GPT` (bei großen Laufwerken automatisch erkannt)
2. `Analyse` → `Quick Search` (nur lesend)
3. Wenn Partitionen gefunden werden: `p` drücken, um Dateien aufzulisten (bestätigt, dass auf die Daten zugegriffen werden kann)
4. `Deeper Search`, falls Quick Search nichts findet (durchsucht die gesamte Festplattenoberfläche, auf 16 TB mehrere Stunden)
5. `Write` erst ausführen, wenn die Dateien sichtbar sind, und nur auf dem Image/Klon

### gpart — Reparatur von BSD-Partitionen (unter Linux über ein Paket verfügbar) {#gpart-bsd-partition-repair-available-on-linux-via-package}

```bash
# Recover partition table from partition signatures
sudo gpart recover /dev/loop0
sudo gpart show /dev/loop0
```

## Reparatur des Dateisystems {#filesystem-repair}

Auf der Loop-Partition des Images (`/dev/loop0p1`) ausführen, niemals auf dem Originalgerät.

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

### NTFS (Windows-Volumes) {#ntfs-windows-volumes}

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

`ntfsfix` setzt das Dirty-Bit zurück, sodass Windows beim nächsten Start chkdsk ausführt. Für eine tiefgehende NTFS-Reparatur kann Windows-`chkdsk` auf das eingebundene Image angewendet werden — aber erst, nachdem bestätigt ist, dass das Original gesichert wurde.

### PhotoRec — File Carving, wenn die Partitionsstruktur verloren ist {#photorec-file-carving-when-partition-structure-is-gone}

```bash
sudo photorec /dev/loop0
# Carves known file signatures regardless of filesystem structure
# Recovers files but loses directory structure and filenames
```

## Stolperfallen {#gotchas}

- **Schreiben auf das ausfallende Original zerstört die Wiederherstellbarkeit.** fsck, testdisk Write, chkdsk, Partitionswerkzeuge — all das schreibt auf die Festplatte. Ein einzelner Schreibvorgang in einen Bereich mit fehlerhaften Sektoren kann einen benachbarten lesbaren Bereich beschädigen. Immer zuerst imagen. Dies ist die wichtigste Regel der Datenrettung.

- **Der GPT-Backup-Header liegt auf der allerletzten LBA, nicht auf einem festen Offset.** Auf einem 16-TB-Laufwerk liegt die letzte LBA bei etwa 31.251.693.567. Werkzeuge, die den Speicherort des Backup-GPT fest codieren (manche älteren Partitionseditoren), setzen ihn falsch und beschädigen das Backup. Gdisk und sgdisk verwenden, die das Feld `BackupLBA` des primären Headers auslesen.

- **Die Verwechslung von 4Kn und 512e bricht die Offset-Berechnung.** Ein als 4Kn konfiguriertes Laufwerk (4096-Byte-Logiksektoren) hat bei gleicher Kapazität eine andere Anzahl an LBAs. testdisk und einige ältere Versionen von gdisk gehen von 512-Byte-Sektoren aus. Vor dem Einsatz eines Partitionswerkzeugs mit `smartctl -i` prüfen und nur 4Kn-fähige Werkzeugversionen verwenden.

- **Die Map-Datei von ddrescue ist der Kontrollpunkt.** Geht die Map-Datei verloren, beginnt der nächste Lauf von vorn — möglicherweise werden dabei mehr als 12 Stunden bereits guter Daten erneut gelesen. Die Map-Datei zusammen mit dem Image auf dem Ziellaufwerk aufbewahren.

- **`losetup -P` ist für den Zugriff auf Partitionen erforderlich.** Ohne `-P` (Partitionserkennung) existiert nur `/dev/loop0`, und die einzelnen Partitionsknoten (`/dev/loop0p1` usw.) werden nicht angelegt.

- **Helium-Laufwerke (z. B. Ultrastar HC550) dürfen nicht geöffnet werden.** Ein Bruch der Dichtung führt an Luft innerhalb von Sekunden zu Kopf-Scheiben-Kontakt. Ein physischer Kopftausch erfordert einen Reinraum mit Helium-Befüllung; Eigenbau ist nicht praktikabel.

## Siehe auch {#see-also}

- [[disks-and-filesystems]] — Partitionstabellen, mkfs, mount, fsck auf gesunden Laufwerken, SMART-Grundlagen
- [[linux-kernel-and-boot]] — Bootvorgang als Kontext für die Rolle von MBR/GPT beim Systemstart
- [[monitoring-and-performance]] — Überwachung der Festplatten-I/O (iostat, iotop) während der Wiederherstellung
- [[bash-scripting]] — Automatisierung der ddrescue-Schleife mit Retry-Logik und Benachrichtigungen

**Tool-Dokumentation:**
- ddrescue-Handbuch: https://www.gnu.org/software/ddrescue/manual/ddrescue_manual.html
- testdisk Schritt für Schritt: https://www.cgsecurity.org/wiki/TestDisk_Step_By_Step
- sgdisk-Manpage: https://rodsbooks.com/gdisk/sgdisk-walkthrough.html
- smartmontools-Attributreferenz: https://www.smartmontools.org/browser/trunk/smartmontools/drivedb.h
