---
title: "LG Electronics: lg-smart-tv-data-privacy — Lg Smart Tv Data Privacy"
category: "organizations"
date: 2026-09-14
tags: ["lg-electronics", "lg-smart-tv-data-privacy", "organization"]
aliases: ["LG Electronics: lg-smart-tv-data-privacy"]
---

# LG Electronics: smart TV data privacy

**Development line:** organization:lg-electronics · thread lg-smart-tv-data-privacy  
**Last event:** 2026-09-14 · 2 dated since 2026-09-14 · **Researched:** 2026-11-18 · confidence: high

## What it is

LG webOS is the operating system on LG smart TVs. It competes with Samsung Tizen and Google TV for home entertainment.

- App streaming: runs streaming apps on the TV.
- Device discovery: finds other devices on the local network.
- Automatic Content Recognition: tracks what is being watched.
- Voice recognition: takes commands through the remote or far-field microphones.

Automated viewing recommendations need the user to accept consent agreements. Ad tracking and voice telemetry can be switched off by hand. Where security matters, fully stopping background network scanning means putting the TV on an untrusted VLAN. The other option is to cut its network access and use an external media player.

## Development line

- **2026-09-14 — LG accused of spying on people through smart TVs.** Researchers claim some LG TVs collect more user data than expected. They say the TVs scan home networks, detect connected phones and other devices, and process audio even with the screen off. They also say data is sent once the internet connection comes back. LG denies this. It says unrecognized sounds are deleted locally and data collection can be turned off by hand.
- **2026-09-14 — LG accused of spying on people through smart TVs.** Researchers claim some LG TVs collect more user data than expected. They say the TVs scan home networks, detect connected phones and other devices, and process audio even with the screen off. They also say data is stored locally while offline and sent later. LG denies the claims. It says unrecognized sounds are deleted locally and data collection can be turned off by hand.
- **2026-09-14 — other reporting on this date.**
  - Technical investigations say webOS devices scan the local network to identify connected hardware, including smartphones, and nearby SSIDs for telemetry. LG says device discovery is standard for smart home interoperability. It also says unrecognized audio captured in standby is discarded locally, not transmitted. (2026-09-14) — <https://www.drweb.de/lg-smart-tv-ton-heimnetz-datenschutz/>
  - The offline storage is described as telemetry queuing while the network is down. Users can opt out of Automatic Content Recognition (Live Plus) and voice recognition in the webOS system settings. That stops background audio sampling and viewing data aggregation. (2026-09-14) — <https://www.drweb.de/lg-smart-tv-ton-heimnetz-datenschutz/>

## What changed

The first webOS releases focused on delivering consumer apps and finding smart home devices on local networks. Later revisions added Automatic Content Recognition and voice command telemetry for targeted advertising. Users then questioned the background network scanning and standby audio capture. That led to clearer privacy disclosures and confirmation that audio is disposed of locally. It also brought easier switches to turn off telemetry and device profiling.

## How to use this

1. Open Settings, then All Settings, then General or System. Find the User Agreements or Privacy menu.
  — <https://www.drweb.de/lg-smart-tv-ton-heimnetz-datenschutz/>
2. Turn off Live Plus and Viewing Information. This opts out of Automatic Content Recognition and HDMI content fingerprinting.
  — <https://www.drweb.de/lg-smart-tv-ton-heimnetz-datenschutz/>
3. Open AI Service settings and turn off Voice Recognition and voice telemetry. If the chassis has a physical far-field microphone switch, switch it off too.
  — <https://www.drweb.de/lg-smart-tv-ton-heimnetz-datenschutz/>
4. Open Additional Settings under General and turn off personalized advertising. Withdraw consent for interest-based cross-device promotions.
  — <https://www.drweb.de/lg-smart-tv-ton-heimnetz-datenschutz/>

## Best practices

- Put smart TVs on a separate guest VLAN or IoT subnet. It should have no access to trusted workstations, phones or network-attached storage.
  — <https://www.drweb.de/lg-smart-tv-ton-heimnetz-datenschutz/>
- Disconnect the TV from Wi-Fi and Ethernet entirely and use an external streaming box or a display-only HDMI source. That removes network discovery and telemetry.
  — <https://www.drweb.de/lg-smart-tv-ton-heimnetz-datenschutz/>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Forum discussions (e.g., Reddit) and Chinese press coverage came back only as redirect URLs, not direct ones. They are left out so the links cannot break.
- Public summaries do not fully separate which firmware builds and hardware revisions cache standby audio and which discard it locally at once.

## Sources

| source | title | read |
|---|---|---|
| https://www.drweb.de/lg-smart-tv-ton-heimnetz-datenschutz/ | LG Smart-TV: Ton, Heimnetz, Datenschutz | 2026-11-18 |

## Agent brief {#agent-brief}

- **Subject:** organization:lg-electronics, thread lg-smart-tv-data-privacy, 2 dated events 2026-09-14 → 2026-09-14.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
