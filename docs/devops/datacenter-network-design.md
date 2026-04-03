---
title: Data Center Network Design
category: concepts
tags: [devops, networking, datacenter, vxlan, evpn, bgp, leaf-spine, clos]
---

# Data Center Network Design

Modern data center networks use leaf-spine (CLOS) topologies with VXLAN overlay and EVPN control plane. This replaces traditional three-tier architectures limited by Spanning Tree.

## CLOS / Leaf-Spine Architecture

- **Spine** (routing layer) + **Leaf** (access layer)
- Every leaf connects to every spine (full mesh at interconnect)
- No STP needed - all paths active via ECMP
- Scale: add more spines for bandwidth, more leafs for ports

### Roles

| Role | Function |
|------|----------|
| Leaf | Access switches connecting servers |
| Spine | Routing backbone, no server connections |
| Border Leaf | Connects fabric to external networks |
| Super Spine | Additional tier for very large fabrics |

### Underlay vs Overlay

- **Underlay** - physical IP connectivity between switches (BGP/OSPF)
- **Overlay** - virtual networks on top of underlay (VXLAN tunnels)

## VXLAN (Virtual Extensible LAN)

Encapsulates L2 frames in UDP, extending L2 domains across L3 underlay. Solves VLAN limit (4096 -> 16M VNIs).

- **VTEP** - source/destination IP for encapsulation (leaf loopback address)
- **VNI** - 24-bit identifier. L2 VNI = bridge domain. L3 VNI = VRF
- Encapsulation: Original L2 -> VXLAN header (VNI) -> UDP -> Outer IP -> Outer Ethernet

## EVPN Control Plane

BGP-based control plane for VXLAN, replacing flood-and-learn with explicit MAC/IP advertisement.

### Route Types

| Type | Name | Purpose |
|------|------|---------|
| 1 | Ethernet Auto-Discovery | Multi-homing, fast convergence |
| 2 | MAC/IP Advertisement | Learned MAC and IP addresses |
| 3 | Inclusive Multicast | BUM traffic handling (flood lists) |
| 4 | Ethernet Segment | Designated Forwarder election |
| 5 | IP Prefix | External routes, route optimization |

### L3 Routing Models

- **Symmetric IRB** - routed at source and destination leaf (L3 VNI between leafs). Standard
- **Asymmetric IRB** - routed at source, bridged at destination (requires all VLANs everywhere)
- **Anycast Gateway** - same virtual IP/MAC on every leaf. Enables live VM migration

## BGP as Underlay

### eBGP (Recommended for CLOS)

- Each leaf has unique ASN, each spine has unique ASN
- No route reflector needed - eBGP naturally propagates
- Simpler operationally (RFC 7938)

### iBGP Alternative

- Single AS, requires full mesh or Route Reflector on spines
- Uses Cluster ID/Originator ID for loop prevention

### Underlay Protocol Comparison

| Protocol | Pros | Cons |
|----------|------|------|
| OSPF | Well-known, fast convergence | Complex in large fabrics, LSA flooding |
| IS-IS | Simpler topology build, TLV extensibility | Less common expertise |
| eBGP | No RR needed, simple loop prevention | More ASNs to manage |

## VPC (Virtual Port Channel)

Two switches appear as one to connected hosts (Cisco NX-OS):

- **VIP** - shared VTEP IP for both peers
- **PIP** - individual VTEP IP per switch (for L3 routing)
- Peer Link + Peer Keepalive for control/sync

### EVPN MC-LAG (Standards-Based Alternative)

Uses EVPN Type 1 + Type 4 routes. No proprietary protocol. Multi-vendor compatible.

## Multi-Site Architectures

| Type | Description |
|------|-------------|
| Multi-Pod | Single fabric, super-spines between pods |
| Multi-Fabric | Independent fabrics, L2 interconnect |
| Multi-Site | Independent fabrics, EVPN DCI, re-encapsulation at borders |

## Gotchas

- VXLAN adds 50-byte overhead to every packet - plan MTU accordingly
- ARP suppression on leafs reduces BUM flooding significantly
- Type 5 routes essential for large-scale - reduces control-plane overhead vs host routes
- VPC orphan ports (single-connected hosts) need special handling
- Multi-site: VNI must match across sites, auto-generated RT needs `rewrite-rt`

## See Also

- [[kubernetes-services-and-networking]] - container networking concepts
- [[aws-cloud-fundamentals]] - VPC networking in AWS
- [[monitoring-and-observability]] - network monitoring
