# Disk Data Recovery — Block-Level and Partition Repair

Recovering failed or large (16 TB+) drives at the block level: imaging, partition/GPT repair, filesystem repair. Assumes the drive is electrically responsive. For basics (fdisk, mkfs, mount, fsck on healthy drives) see [[disks-and-filesystems]].

## Key Facts

- **Image before touching** — every write to a failing drive reduces recoverability. Clone first to a healthy destination, then work on the clone.
- GPT stores a **backup header at the last LBA** of the disk; primary corruption alone is recoverable via the backup.
- MBR max capacity is 2 TB (2^32 × 512 bytes). Drives >2 TB **require GPT** — see [[disks-and-filesystems]].
- 512e drives (e.g. WD Ultrastar HC550) report 512-byte logical sectors but use 4096-byte physical sectors. Some older recovery tools miscalculate offsets on 4Kn (4096 native) drives.
- `ddrescue` is resumable: interrupted runs restart from a map file, preserving already-read good data.
- CMR drives are simpler to recover than SMR (shingled) — no inter-track dependency during imaging.
- `smartctl` triage comes first: if Reallocated_Sector_Ct, Current_Pending_Sector, or Reported_Uncorrect are >0, treat the drive as actively failing and image immediately.

## Triage

### smartctl health check

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

**Critical attributes — any RAW value > 0 means image immediately:**

| ID | Name | Action |
|----|------|--------|
| 5 | Reallocated_Sector_Ct | Backup now |
| 187 | Reported_Uncorrect | Image immediately |
| 197 | Current_Pending_Sector | Image immediately |
| 198 | Offline_Uncorrectable | Image immediately |
| 199 | UDMA_CRC_Error_Count | Check cable first |
| 22 | Current_Helium_Level (normalized) | <25 = imminent failure on helium drives |

**Do-not-write rule:** once any of the above trips, stop all write operations to the drive (no fsck, no chkdsk, no partition tools). Every write risks overwriting sectors that recovery tools could retry.

### Verify sector size before recovery tools

```bash
sudo smartctl -i /dev/sdX | grep "Sector Size"
# "512 bytes logical, 4096 bytes physical" = 512e (tools treat it as 512)
# "4096 bytes logical/physical" = 4Kn (older tools may misplace offsets)
```

## Imaging

### ddrescue — clone-first workflow

`ddrescue` reads in passes, marks bad areas in a map file, retries with progressively smaller block sizes. The map file enables resuming an interrupted session without re-reading good data.

```bash
# Pass 1 — fast, skip bad areas
sudo ddrescue -d -r0 /dev/sdX /mnt/dest/disk.img /mnt/dest/disk.map

# Pass 2 — retry bad sectors (up to 3 attempts, smaller blocks)
sudo ddrescue -d -r3 /dev/sdX /mnt/dest/disk.img /mnt/dest/disk.map

# Pass 3 — reverse direction (sometimes reads stuck sectors)
sudo ddrescue -d -r3 -R /dev/sdX /mnt/dest/disk.img /mnt/dest/disk.map
```

**Flags:**
- `-d` — direct I/O, bypasses kernel page cache (critical for failing drives)
- `-r N` — retry count per bad block; `-r0` skips retries on first pass
- `-R` — reverse direction for stubborn bad areas
- Map file is plain text — check progress: `cat /mnt/dest/disk.map`

### Destination requirements

- Destination must be **at least as large** as the source device (not just the used data).
- Write destination to a **different physical drive** — never image a drive back to itself.
- For a 16 TB drive: at ~150 MB/s (USB 3 bridge), a full pass takes ~30 hours. Bad sectors extend this significantly.

### Verify image integrity

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

### HDDSuperClone — for severely failing drives

When ddrescue stalls because the drive disconnects under load or bus-resets on specific zones:

```bash
# HDDSuperClone has SCSI passthrough for finer head/zone control
# Run from a live Linux environment
sudo hddsuperclone --drive /dev/sdX --image /mnt/dest/disk.img \
  --log /mnt/dest/hsc.log --timeout 30
```

HDDSuperClone can skip data tied to failing heads and recover the rest, which ddrescue cannot do at that granularity.

## Partition / Boot Sector Repair

**Work on the image (loop device), not the original drive.**

### GPT structure (16 TB example, 512e)

| LBA | Content |
|-----|---------|
| 0 | Protective MBR (0xEE entry covering full disk) |
| 1 | Primary GPT Header (CRC32 protected) |
| 2–33 | Primary Partition Table (128 entries) |
| 34+ | Partition data |
| last LBA − 33 to last LBA − 1 | Backup Partition Table |
| last LBA | Backup GPT Header |

### Restore primary GPT from backup with gdisk

```bash
sudo gdisk /dev/loop0   # or /dev/sdX on the clone
# Inside gdisk interactive prompt:
r          # recovery and transformation menu
b          # use backup GPT header to rebuild primary
w          # write changes
y          # confirm
```

### sgdisk — scriptable GPT operations

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

### Rewrite protective MBR with dd

When LBA 0 is corrupt but LBA 1 (primary GPT) is intact, a minimal protective MBR can be written:

```bash
# Zero out MBR region (first 512 bytes), preserving GPT at LBA 1
sudo dd if=/dev/zero of=/dev/loop0 bs=512 count=1 conv=notrunc

# Reapply protective MBR (gdisk does this automatically on write)
sudo gdisk /dev/loop0
# Then: w -> y
```

### testdisk — partition table scanner

testdisk scans for partition signatures without writing anything until explicitly confirmed.

```bash
sudo apt install testdisk
sudo testdisk /dev/loop0
```

**Interactive workflow:**
1. Select device → Partition table type: `EFI GPT` (auto-detected on large drives)
2. `Analyse` → `Quick Search` (read-only)
3. If partitions found: press `p` to list files (confirms data is accessible)
4. `Deeper Search` if Quick Search finds nothing (scans full disk surface, hours on 16 TB)
5. `Write` only after confirming files are visible, and only on the image/clone

### gpart — BSD partition repair (available on Linux via package)

```bash
# Recover partition table from partition signatures
sudo gpart recover /dev/loop0
sudo gpart show /dev/loop0
```

## Filesystem Repair

Run on the image's loop partition (`/dev/loop0p1`), never on the original device.

### ext4

```bash
# Check only (no writes)
sudo fsck.ext4 -n /dev/loop0p1

# Repair automatically (drive must be unmounted)
sudo fsck.ext4 -y /dev/loop0p1

# Force check even if filesystem marked clean
sudo fsck.ext4 -f -y /dev/loop0p1
```

### XFS

```bash
# Check only
sudo xfs_repair -n /dev/loop0p1

# Repair (must be unmounted)
sudo xfs_repair /dev/loop0p1

# If repair fails due to dirty log
sudo xfs_repair -L /dev/loop0p1   # zeroes journal — data loss risk, last resort
```

### NTFS (Windows volumes)

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

`ntfsfix` resets the dirty bit so Windows will run chkdsk on next boot. For deep NTFS repair, use Windows `chkdsk` against the mounted image — but only after confirming the original is imaged.

### PhotoRec — file carving when partition structure is gone

```bash
sudo photorec /dev/loop0
# Carves known file signatures regardless of filesystem structure
# Recovers files but loses directory structure and filenames
```

## Gotchas

- **Writing to the failing original destroys recoverability.** fsck, testdisk Write, chkdsk, partition tools — all write to disk. A single write to a bad-sector zone can corrupt an adjacent readable area. Image first, always. This is the single most important rule in data recovery.

- **GPT backup header is at the very last LBA, not a fixed offset.** On a 16 TB drive the last LBA is around 31,251,693,567. Tools that hardcode the backup GPT location (some old partition editors) place it wrong and corrupt the backup. Use gdisk/sgdisk which read the primary header's `BackupLBA` field.

- **4Kn vs 512e confusion breaks offset calculations.** A drive configured as 4Kn (4096-byte logical sectors) has a different LBA count for the same capacity. testdisk and some older versions of gdisk assume 512-byte sectors. Verify with `smartctl -i` before running any partition tool, and use only 4Kn-aware tool versions.

- **ddrescue's map file is the checkpoint.** If you lose the map file, the next run starts from scratch — potentially re-reading 12+ hours of already-good data. Keep the map file on the destination drive alongside the image.

- **losetup -P is required for partition access.** Without `-P` (partition scan), only `/dev/loop0` exists and individual partition nodes (`/dev/loop0p1`, etc.) are not created.

- **Helium drives (e.g. Ultrastar HC550) must not be opened.** Seal breach in air causes head-to-platter contact within seconds. Physical head swap requires a helium-refilled cleanroom; DIY is not viable.

## See Also

- [[disks-and-filesystems]] — partition tables, mkfs, mount, fsck on healthy drives, SMART basics
- [[linux-kernel-and-boot]] — boot process context for MBR/GPT role at system start
- [[monitoring-and-performance]] — disk I/O monitoring (iostat, iotop) during recovery operations
- [[bash-scripting]] — automating ddrescue loop with retry logic and notifications

**Tool docs:**
- ddrescue manual: https://www.gnu.org/software/ddrescue/manual/ddrescue_manual.html
- testdisk step-by-step: https://www.cgsecurity.org/wiki/TestDisk_Step_By_Step
- sgdisk manpage: https://rodsbooks.com/gdisk/sgdisk-walkthrough.html
- smartmontools attribute reference: https://www.smartmontools.org/browser/trunk/smartmontools/drivedb.h
