---
title: "Windows 11: windows-11-memory-integrity — Windows 11 Memory Integrity"
category: "projects"
date: 2026-11-20
tags: ["project", "windows-11", "windows-11-memory-integrity", "windows_11"]
aliases: ["Windows 11", "Windows 11: windows-11-memory-integrity"]
---

# Windows 11: windows-11-memory-integrity — Windows 11 Memory Integrity

Windows 11 Memory Integrity is a hypervisor-enforced security feature that isolates kernel memory, for administrators and endpoint users.

**Development line:** project:windows-11 · thread windows-11-memory-integrity  
**Last event:** 2026-11-20 · 1 dated since 2026-11-20 · **Researched:** 2026-11-21 · confidence: medium

## What it is

Memory Integrity isolates kernel memory allocations with virtualization-based security (VBS). It does not rely only on kernel-mode software checks.

What it does:

- Hypervisor-protected code integrity (HVCI): enforces it for loaded kernel drivers.
- Driver blocking: stops unsigned or vulnerable kernel-level modules from running.
- Control flow integrity: validates it inside kernel memory space.

It needs hardware-assisted virtualization. It does not stop local lock-screen user-interface escapes, or physical console access on unlocked BitLocker sessions.

It is a baseline defense against kernel rootkits. It is not enough alone against physical lock-screen execution flaws.

## Development line

- **2026-11-20 — FastUnlock vulnerability lets attackers bypass Windows 11 lock screen despite BitLocker.** The researcher Nightmare Eclipse disclosed a Windows 11 vulnerability named FastUnlock. It lets programs launch without a password or PIN, even with BitLocker enabled. It needs physical access and built-in accessibility features. Researchers confirmed programs can be run from a USB drive. At the time of the disclosure, Microsoft had not released a fix.
  - The disclosure came from security researcher Abdelhamid Naceri (Nightmare Eclipse / MSNightmare). The FastUnlock zero-day targets the modernized Windows Narrator accessibility interface, reached through Win+U and the PIN recovery flow. From there an attacker can navigate into Windows Settings and run arbitrary programs from USB drives under the restricted WsiAccount context. No volume re-encryption happens first on running BitLocker sessions. (2026-11-20) — <https://rozetked.me/news/49588>

## What changed

Virtualization-based code integrity used to be an optional enterprise feature. On compliant hardware it is now a default protection. Hardware compatibility lists grew, and vulnerable driver blocklists were built into core operating system updates.

The security boundary needs a second look. Physical-access lock-screen attacks bypass user authentication on running encrypted volumes, and they do not touch kernel integrity directly.

## How to use this

1. Keep physical control of running Windows 11 hardware. Disable automatic wake and disconnect external ports on unattended machines.
  — <https://rozetked.me/news/49588>
2. Shut down or hibernate unattended devices instead of only locking them, so BitLocker encryption is in force at rest.
  — <https://rozetked.me/news/49588>

## Best practices

- In shared or untrusted physical environments, shut down or hibernate instead of using the standard lock screen. This prevents BitLocker access while memory is decrypted.
  — <https://rozetked.me/news/49588>
- Restrict execution from external USB mass storage. Watch vendor security updates for a patch to the accessibility flaw.
  — <https://rozetked.me/news/49588>

## Superseded by this

- The belief that the standard Windows 11 lock screen alone prevents unauthorized local code execution on BitLocker-protected devices.
  — <https://rozetked.me/news/49588>

## Still unknown

- The page label mixes two different things. Memory Integrity (hypervisor-protected code integrity / HVCI) works at kernel VBS boundaries. FastUnlock is an accessibility-layer lock-screen bypass that navigates the user interface under WsiAccount on unencrypted active BitLocker sessions.
- The canonical article paths on The Hacker News, Privacy Affairs and MLQ are unknown. Search redirects masked them, so they are not cited.
- As of the observation date, Microsoft has assigned no formal CVE identifier and issued no official patch for the FastUnlock zero-day.

## Sources

| source | title | read |
|---|---|---|
| https://rozetked.me/news/49588 | Уязвимость FastUnlock позволяет запускать программы в обход экрана блокировки Windows 11 | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** project:windows-11, thread windows-11-memory-integrity, 1 dated events 2026-11-20 → 2026-11-20.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
