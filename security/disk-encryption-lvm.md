---
title: Disk Encryption with LVM and dm-crypt
category: system-security
tags: [encryption, lvm, dm-crypt, luks, full-disk-encryption, data-at-rest]
---

# Disk Encryption with LVM and dm-crypt

## Key Facts

- Disk encryption protects against physical access attacks: stolen laptop, copied VM disk image, compromised backup storage
- dm-crypt: Linux kernel subsystem for transparent block device encryption - data encrypted on write, decrypted on read
- LUKS (Linux Unified Key Setup): standard on-disk format for dm-crypt with key management, multiple passphrases, and header metadata
- LVM (Logical Volume Manager) + LUKS: encrypt the entire LVM volume group for full-disk encryption
- System cannot boot without passphrase entry - prevents data access even with physical disk access
- Encrypted system: boot partition (`/boot`) remains unencrypted (contains kernel and initramfs), everything else encrypted
- [[linux-user-security]] complements disk encryption with runtime access controls
- Virtual machines can be copied as a single file - full disk encryption is critical for VM security

## Patterns

```bash
# Create encrypted volume with LUKS
cryptsetup luksFormat /dev/sdb1
# Enter passphrase (used for decryption)

# Open encrypted volume
cryptsetup luksOpen /dev/sdb1 secure_volume
# Creates /dev/mapper/secure_volume

# Create filesystem on encrypted volume
mkfs.ext4 /dev/mapper/secure_volume

# Mount
mount /dev/mapper/secure_volume /mnt/secure

# Close (lock) encrypted volume
umount /mnt/secure
cryptsetup luksClose secure_volume
```

```bash
# LVM on LUKS setup (common for full-disk encryption)
# 1. Create LUKS container
cryptsetup luksFormat /dev/sda2

# 2. Open LUKS container
cryptsetup luksOpen /dev/sda2 crypt_pv

# 3. Create LVM physical volume on encrypted device
pvcreate /dev/mapper/crypt_pv

# 4. Create volume group
vgcreate vg0 /dev/mapper/crypt_pv

# 5. Create logical volumes
lvcreate -L 8G vg0 -n swap
lvcreate -l 100%FREE vg0 -n root

# 6. Format
mkswap /dev/vg0/swap
mkfs.ext4 /dev/vg0/root
```

```bash
# Key management
cryptsetup luksDump /dev/sdb1          # Show LUKS header info
cryptsetup luksAddKey /dev/sdb1        # Add additional passphrase (up to 8)
cryptsetup luksRemoveKey /dev/sdb1     # Remove a passphrase
cryptsetup luksChangeKey /dev/sdb1     # Change passphrase

# Backup LUKS header (critical for recovery)
cryptsetup luksHeaderBackup /dev/sdb1 --header-backup-file header.bak
```

## Gotchas

- `/boot` partition MUST be unencrypted - the bootloader (GRUB) needs to read the kernel before decryption is possible
- LUKS header damage = total data loss - always backup LUKS header to separate storage
- Swap partition must also be encrypted - otherwise sensitive data from RAM may be written to unencrypted swap
- Hibernate (suspend to disk) writes RAM contents to swap - if swap is not encrypted, encryption is bypassed
- dm-crypt performance overhead is minimal on modern CPUs with AES-NI instructions (2-5% throughput reduction)
- Full disk encryption does NOT protect running system - once booted and unlocked, data is accessible to anyone with OS-level access

## See Also

- [LUKS2 specification](https://gitlab.com/cryptsetup/cryptsetup/-/wikis/LUKS2-Format)
- [NIST SP 800-111 Guide to Storage Encryption](https://csrc.nist.gov/publications/detail/sp/800-111/final)
- [dm-crypt wiki](https://wiki.archlinux.org/title/Dm-crypt)
