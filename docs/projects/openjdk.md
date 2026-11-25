---
title: "Openjdk: openjdk-java4shell-vulnerability — Openjdk Java4Shell Vulnerability"
category: "projects"
date: 2026-11-18
tags: ["openjdk", "openjdk-java4shell-vulnerability", "project"]
aliases: ["Openjdk: openjdk-java4shell-vulnerability"]
---

# Openjdk: openjdk-java4shell-vulnerability — Openjdk Java4Shell Vulnerability

**Development line:** project:openjdk · thread openjdk-java4shell-vulnerability  
**Last event:** 2026-11-18 · 5 dated since 2026-11-17 · **Researched:** 2026-11-23 · confidence: high

## What it is

OpenJDK Java4Shell is a heap memory-corruption vulnerability in the HotSpot virtual machine Base64 decoder. It matters to operators of Java application servers on modern x86-64 hardware.

- Heap buffer out-of-bounds write: triggered by malformed Base64 padding.
- Remote code execution: permitted without authentication on default enterprise services.
- Attack surface: HTTP header parsing, SAML tokens and file upload endpoints.

It only hits x86-64 processors with AVX-512 VBMI extensions running HotSpot builds with Base64 intrinsics. ARM64 and older x86 CPUs are unaffected.

Upgrade to a patched OpenJDK release. Until then, disable Base64 intrinsics at startup.

## Development line

- **2026-11-17 — Openjdk: openjdk-java4shell-vulnerability update.** Oracle and the OpenJDK Vulnerability Group released official vendor security fixes for CVE-2026-114938 across supported OpenJDK branches.
- **2026-11-18 — Java4Shell vulnerability in OpenJDK found with Codex.** Researcher Calif reported using Codex to find Java4Shell, a memory-corrupting OpenJDK flaw that can lead to remote code execution. The search reportedly took about an hour. A working exploit followed about two hours later. Affected systems are x86-64 with AVX-512 VBMI where a Java application decodes Base64 input from outside. Oracle and Red Hat issued advisories recommending prompt Java updates.
- **2026-11-18 — Critical memory-corruption vulnerability found in OpenJDK Base64 decoder.** Reported 2026-11-18: a critical vulnerability in the optimized AVX-512 assembly Base64 decoder of OpenJDK can write bytes past an allocated array. Keycloak, Jira, Confluence and Jenkins are reported as affected. Reported workarounds are disabling -XX:UseAVX=2 or -XX:-UseBASE64Intrinsics until OpenJDK is updated. The same report says the flaw was found with Codex in about an hour, and a working exploit followed in about two more hours.
- **2026-11-18 — Researcher finds Java4Shell vulnerability in OpenJDK using Codex; fixes released Nov 17.** A researcher reported using Codex to find the Java4Shell vulnerability in OpenJDK in about one hour. Demonstrating remote code execution took roughly two more hours and about $200 in tokens. The vulnerability affects systems on some Intel and AMD processors. Oracle and OpenJDK released fixes on November 17.
- **2026-11-18 — Java4Shell vulnerability in OpenJDK found with Codex; fixes released 17 November.** A researcher reported using Codex to find the Java4Shell vulnerability in OpenJDK in about one hour. Demonstrating remote code execution took about two more hours and roughly $200 in token costs. The flaw affects systems on some Intel and AMD processors. Oracle and OpenJDK released fixes on 17 November.
- **2026-11-18 — other reporting on this date.**
  - Calif's technical disclosure confirms the designation CVE-2026-114938 and a CVSS 4.0 score of 9.2. The cause is an integer underflow in AVX-512 VBMI vector assembly, which produces an invalid heap write mask when decoding malformed padding. (2026-11-18) — <https://calif.io/java4shell>
  - The out-of-bounds write affects OpenJDK 17.0.6 and newer, including versions 21, 25, and 27, on Intel Ice Lake and AMD Zen 4 or newer processors. OpenJ9 and ARM64 are completely unaffected. (2026-11-18) — <https://calif.io/java4shell>
  - The advisory records verify pre-authentication remote code execution against default deployments of Keycloak, Atlassian Jira, Confluence, Jenkins, Artifactory, and PingFederate. The route is unauthenticated HTTP header and token decoders. (2026-11-18) — <https://calif.io/java4shell>
  - The documentation gives two mitigation flags, -XX:-UseBASE64Intrinsics and -XX:UseAVX=2. Both disable the vulnerable SIMD paths without downtime, until the vendor patch is deployed. (2026-11-18) — <https://calif.io/java4shell>

## What changed

It began with an integer underflow in the hand-written AVX-512 assembly intrinsic for Base64 decoding. Heap-corrupting exploit primitives were then demonstrated against standard server frameworks. Upstream maintainers prepared security updates. Deployments that could not upgrade at once used the intrinsic-disabling flags to cut the remote execution risk.

## How to use this

1. Check the CPU architecture and instruction set, to see whether the host supports AVX-512 VBMI extensions.
  — <https://calif.io/java4shell>
2. Check the OpenJDK version in every environment for affected releases: 17.0.6+, 21, 25, and 27.
  — <https://calif.io/java4shell>
3. Deploy the official vendor security update for CVE-2026-114938, which patches the HotSpot Base64 decoder intrinsic.
  — <https://calif.io/java4shell>
4. If patching is not possible right away, add -XX:-UseBASE64Intrinsics to the JVM arguments. It disables the vulnerable assembly decoding path.
  — <https://calif.io/java4shell>

## Best practices

- Patch first. A vendor runtime update keeps the optimized Base64 performance, so intrinsics are not left disabled for good.
  — <https://calif.io/java4shell>
- Use -XX:-UseBASE64Intrinsics as a stopgap on unpatched container fleets exposed to untrusted Base64 payloads.
  — <https://calif.io/java4shell>
- Audit public ingress points that handle unauthenticated Base64 tokens: authentication gateways, SAML endpoints and reverse proxies.
  — <https://calif.io/java4shell>

## Superseded by this

- Claim: OpenJDK Base64 decoding in standard HotSpot runtime configurations is inherently memory-safe against heap overflow and memory corruption on modern x86-64 hardware.
  — <https://calif.io/java4shell>
- Claim: default AVX-512 VBMI accelerated Base64 intrinsics can process untrusted network inputs safely, without vendor security updates or intrinsic disabling flags.
  — <https://calif.io/java4shell>

## Still unknown

- Simplified Chinese search queries returned only redirects, with no verifiable direct canonical paths. The zh-CN lane has no exact cited Chinese sources.
- Independent community discussion threads on Reddit or Hacker News could not be reached as exact canonical URLs without resolving redirects.

## Sources

| source | title | read |
|---|---|---|
| https://calif.io/java4shell | Java4Shell: Memory corruption in OpenJDK Base64 decoding | 2026-11-23 |

## Agent brief {#agent-brief}

- **Subject:** project:openjdk, thread openjdk-java4shell-vulnerability, 5 dated events 2026-11-17 → 2026-11-18.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. The dated supersedes above are the authority for what is obsolete.
