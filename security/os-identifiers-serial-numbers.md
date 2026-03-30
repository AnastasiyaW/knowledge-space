---
title: OS Identifiers and Serial Numbers
category: identification
tags: [os-fingerprinting, serial-numbers, hardware-id, machine-fingerprint, windows, linux]
---

# OS Identifiers and Serial Numbers

## Key Facts

- OS serial numbers and hardware identifiers provide persistent device identification that survives browser changes
- Windows identifiers: MachineGUID (HKLM\SOFTWARE\Microsoft\Cryptography), ProductId, BIOS serial, disk serial, motherboard serial
- Linux identifiers: `/etc/machine-id`, `/var/lib/dbus/machine-id`, disk UUIDs in `/dev/disk/by-uuid/`, DMI data in `/sys/class/dmi/id/`
- MAC address embedded in IPv6 via EUI-64 unless privacy extensions are enabled
- Virtual machines have detectable artifacts: VM-specific hardware IDs, BIOS strings ("VBOX", "QEMU"), hypervisor CPUID bit
- [[browser-fingerprinting]] operates at browser level; OS identifiers operate at system level and are harder to spoof
- [[anti-fraud-systems]] cross-reference browser-reported hardware (via WebGL, hardwareConcurrency) against OS-level identifiers

## Patterns

```bash
# Linux - retrieve machine identifiers
cat /etc/machine-id
# e.g., d4c8e5f2a3b1094c7e6d5f8a9b0c1d2e

cat /sys/class/dmi/id/product_uuid  # requires root
dmidecode -s system-uuid
lsblk -o NAME,UUID  # disk UUIDs

# Regenerate machine-id (for privacy/testing)
sudo rm /etc/machine-id
sudo systemd-machine-id-setup
```

```powershell
# Windows - retrieve identifiers
# MachineGUID (unique per Windows installation)
(Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Cryptography').MachineGuid

# BIOS serial
wmic bios get serialnumber

# Disk serial
wmic diskdrive get serialnumber

# Motherboard serial
wmic baseboard get serialnumber
```

```python
# VM detection patterns
import subprocess
import platform

def detect_virtual_machine() -> dict:
    """Detect common VM artifacts"""
    indicators = {}
    if platform.system() == 'Linux':
        try:
            dmi = open('/sys/class/dmi/id/product_name').read().strip()
            indicators['product_name'] = dmi
            indicators['is_vm'] = any(
                v in dmi.lower()
                for v in ['virtualbox', 'vmware', 'qemu', 'kvm', 'xen', 'hyper-v']
            )
        except FileNotFoundError:
            pass
    return indicators
```

## Gotchas

- MachineGUID persists across Windows updates but changes on reinstallation - cloning a disk preserves it
- Virtual machine detection can be bypassed by modifying BIOS strings (SMBIOS data) in VM configuration
- `/etc/machine-id` is regenerated on first boot of cloned systems but NOT on package updates
- Some anti-fraud systems access hardware serials via browser plugins or native messaging APIs
- Disk serial numbers are readable without admin privileges on many systems
- Docker containers share the host's machine-id unless explicitly overridden

## See Also

- [NIST SP 800-147 BIOS Protection Guidelines](https://csrc.nist.gov/publications/detail/sp/800-147/final)
- [dmidecode documentation](https://linux.die.net/man/8/dmidecode)
