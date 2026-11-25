---
title: "Rechenzentrums-Netzwerkdesign"
category: concepts
tags: [devops, networking, datacenter, vxlan, evpn, bgp, leaf-spine, clos]
level: 3
source_sha256: e1ba8962a199f889206bbde8798b405dc7994ceb3a78773a88d9870d60780afc
translation: machine
translated_at: '2026-10-24'
---
# Rechenzentrums-Netzwerkdesign {#data-center-network-design}

Moderne Rechenzentrumsnetze verwenden Leaf-Spine-(CLOS-)Topologien mit VXLAN-Overlay und EVPN-Control-Plane. Dies ersetzt traditionelle Drei-Schichten-Architekturen, die durch Spanning Tree eingeschränkt sind.

## CLOS / Leaf-Spine-Architektur {#clos-leaf-spine-architecture}

- **Spine** (Routing-Schicht) + **Leaf** (Zugangsschicht)
- Jeder Leaf ist mit jedem Spine verbunden (Full Mesh an der Verbindungsstelle)
- Kein STP erforderlich – alle Pfade sind durch ECMP aktiv
- Skalierung: mehr Spines für Bandbreite, mehr Leafs für Ports

### Rollen {#roles}

| Rolle | Funktion |
|-------|----------|
| Leaf | Zugangsswitches, die Server anbinden |
| Spine | Routing-Backbone, keine Serververbindungen |
| Border Leaf | Verbindet das Fabric mit externen Netzwerken |
| Super Spine | Zusätzliche Ebene für sehr große Fabrics |

### Underlay vs. Overlay {#underlay-vs-overlay}

- **Underlay** – physische IP-Konnektivität zwischen Switches (BGP/OSPF)
- **Overlay** – virtuelle Netzwerke auf dem Underlay (VXLAN-Tunnel)

## VXLAN (Virtual Extensible LAN) {#vxlan-virtual-extensible-lan}

Kapselt L2-Frames in UDP und erweitert L2-Domänen über ein L3-Underlay. Löst das VLAN-Limit (4096 -> 16M VNIs).

- **VTEP** – Quell- bzw. Ziel-IP für die Kapselung (Loopback-Adresse des Leafs)
- **VNI** – 24-Bit-Kennung. L2-VNI = Bridge-Domäne. L3-VNI = VRF
- Kapselung: Originaler L2 -> VXLAN-Header (VNI) -> UDP -> äußeres IP -> äußeres Ethernet

## EVPN-Control-Plane {#evpn-control-plane}

BGP-basierte Control-Plane für VXLAN, die Flood-and-Learn durch explizite MAC-/IP-Ankündigung ersetzt.

### Route-Typen {#route-types}

| Typ | Name | Zweck |
|-----|------|-------|
| 1 | Ethernet Auto-Discovery | Multi-Homing, schnelle Konvergenz |
| 2 | MAC/IP Advertisement | Gelernte MAC- und IP-Adressen |
| 3 | Inclusive Multicast | Behandlung von BUM-Traffic (Flood-Listen) |
| 4 | Ethernet Segment | Wahl des Designated Forwarders |
| 5 | IP Prefix | Externe Routen, Routenoptimierung |

### L3-Routing-Modelle {#l3-routing-models}

- **Symmetric IRB** – Routing am Quell- und Ziel-Leaf (L3-VNI zwischen Leafs). Standard
- **Asymmetric IRB** – Routing am Quell-Leaf, Bridging am Ziel-Leaf (erfordert alle VLANs überall)
- **Anycast Gateway** – gleiche virtuelle IP/MAC auf jedem Leaf. Ermöglicht Live-Migration von VMs

## BGP als Underlay {#bgp-as-underlay}

### eBGP (empfohlen für CLOS) {#ebgp-recommended-for-clos}

- Jeder Leaf hat eine eindeutige ASN, jeder Spine hat eine eindeutige ASN
- Kein Route Reflector nötig – eBGP propagiert Routen auf natürliche Weise
- Im Betrieb einfacher (RFC 7938)

### iBGP-Alternative {#ibgp-alternative}

- Einzelne AS, erfordert Full Mesh oder Route Reflector auf den Spines
- Verwendet Cluster ID/Originator ID zur Schleifenverhinderung

### Vergleich der Underlay-Protokolle {#underlay-protocol-comparison}

| Protokoll | Vorteile | Nachteile |
|-----------|----------|-----------|
| OSPF | Bekannt, schnelle Konvergenz | Komplex in großen Fabrics, LSA-Flooding |
| IS-IS | Einfacherer Topologieaufbau, TLV-Erweiterbarkeit | Weniger verbreitetes Know-how |
| eBGP | Kein RR nötig, einfache Schleifenverhinderung | Mehr ASNs zu verwalten |

## VPC (Virtual Port Channel) {#vpc-virtual-port-channel}

Zwei Switches erscheinen den angeschlossenen Hosts als einer (Cisco NX-OS):

- **VIP** – gemeinsame VTEP-IP für beide Peers
- **PIP** – individuelle VTEP-IP pro Switch (für L3-Routing)
- Peer-Link + Peer-Keepalive für Steuerung/Synchronisation

### EVPN MC-LAG (standardbasierte Alternative) {#evpn-mc-lag-standards-based-alternative}

Verwendet EVPN-Route Typ 1 + Typ 4. Kein proprietäres Protokoll. Herstellerübergreifend kompatibel.

## Multi-Site-Architekturen {#multi-site-architectures}

| Typ | Beschreibung |
|-----|--------------|
| Multi-Pod | Ein Fabric, Super-Spines zwischen den Pods |
| Multi-Fabric | Unabhängige Fabrics, L2-Interconnect |
| Multi-Site | Unabhängige Fabrics, EVPN-DCI, Re-Encapsulation an den Grenzen |

## Stolperfallen {#gotchas}

- VXLAN fügt jedem Paket 50 Byte Overhead hinzu – MTU entsprechend planen
- ARP-Suppression auf den Leafs reduziert BUM-Flooding deutlich
- Typ-5-Routen sind für große Skalierung essenziell – sie reduzieren den Control-Plane-Overhead gegenüber Host-Routen
- VPC-Orphan-Ports (einfach angebundene Hosts) erfordern besondere Behandlung
- Multi-Site: VNI muss über alle Standorte übereinstimmen, auto-generierte RT benötigt `rewrite-rt`

## Siehe auch {#see-also}

- [[kubernetes-services-and-networking]] – Konzepte der Container-Netzwerke
- [[aws-cloud-fundamentals]] – VPC-Netzwerke in AWS
- [[monitoring-and-observability]] – Netzwerkmonitoring
