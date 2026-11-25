---
title: "Conception de réseaux de centres de données"
category: concepts
tags: [devops, networking, datacenter, vxlan, evpn, bgp, leaf-spine, clos]
level: 3
source_sha256: e1ba8962a199f889206bbde8798b405dc7994ceb3a78773a88d9870d60780afc
translation: machine
translated_at: '2026-10-24'
---
# Conception de réseaux de centres de données {#data-center-network-design}

Les réseaux modernes de centres de données utilisent des topologies leaf-spine (CLOS) avec une superposition VXLAN et un plan de contrôle EVPN. Cette approche remplace les architectures traditionnelles à trois niveaux, limitées par Spanning Tree.

## Architecture CLOS / Leaf-Spine {#clos-leaf-spine-architecture}

- **Spine** (couche de routage) + **Leaf** (couche d'accès)
- Chaque leaf est connecté à chaque spine (maillage complet au niveau de l'interconnexion)
- Pas besoin de STP : tous les chemins sont actifs via ECMP
- Mise à l'échelle : ajouter des spines pour la bande passante, des leafs pour les ports

### Rôles {#roles}

| Rôle | Fonction |
|------|----------|
| Leaf | Commutateurs d'accès connectant les serveurs |
| Spine | Backbone de routage, sans connexion aux serveurs |
| Border Leaf | Connecte la fabric aux réseaux externes |
| Super Spine | Niveau supplémentaire pour les fabrics très larges |

### Underlay vs Overlay {#underlay-vs-overlay}

- **Underlay** - connectivité IP physique entre les commutateurs (BGP/OSPF)
- **Overlay** - réseaux virtuels au-dessus de l'underlay (tunnels VXLAN)

## VXLAN (Virtual Extensible LAN) {#vxlan-virtual-extensible-lan}

Encapsule des trames L2 dans UDP, étendant les domaines L2 à travers un underlay L3. Résout la limite des VLAN (4096 -> 16M VNI).

- **VTEP** - IP source/destination pour l'encapsulation (adresse loopback du leaf)
- **VNI** - identifiant de 24 bits. VNI L2 = domaine de pont. VNI L3 = VRF
- Encapsulation : trame L2 d'origine -> en-tête VXLAN (VNI) -> UDP -> IP externe -> Ethernet externe

## Plan de contrôle EVPN {#evpn-control-plane}

Plan de contrôle basé sur BGP pour VXLAN, remplaçant le flood-and-learn par une annonce explicite des adresses MAC et IP.

### Types de routes {#route-types}

| Type | Nom | Objectif |
|------|-----|----------|
| 1 | Ethernet Auto-Discovery | Multi-homing, convergence rapide |
| 2 | MAC/IP Advertisement | Adresses MAC et IP apprises |
| 3 | Inclusive Multicast | Gestion du trafic BUM (listes de flood) |
| 4 | Ethernet Segment | Élection du Designated Forwarder |
| 5 | IP Prefix | Routes externes, optimisation des routes |

### Modèles de routage L3 {#l3-routing-models}

- **Symmetric IRB** - routage au leaf source et au leaf destination (VNI L3 entre les leafs). Standard
- **Asymmetric IRB** - routage au source, pont au destination (nécessite tous les VLAN partout)
- **Anycast Gateway** - même IP/MAC virtuelle sur chaque leaf. Permet la migration à chaud de VM

## BGP comme underlay {#bgp-as-underlay}

### eBGP (recommandé pour CLOS) {#ebgp-recommended-for-clos}

- Chaque leaf a un ASN unique, chaque spine a un ASN unique
- Pas de route reflector nécessaire - eBGP propage naturellement les routes
- Plus simple à exploiter (RFC 7938)

### Alternative iBGP {#ibgp-alternative}

- AS unique, nécessite un maillage complet ou un Route Reflector sur les spines
- Utilise Cluster ID/Originator ID pour la prévention des boucles

### Comparaison des protocoles d'underlay {#underlay-protocol-comparison}

| Protocole | Avantages | Inconvénients |
|-----------|-----------|---------------|
| OSPF | Bien connu, convergence rapide | Complexe dans les grandes fabrics, inondation de LSA |
| IS-IS | Construction de topologie plus simple, extensibilité par TLV | Expertise moins répandue |
| eBGP | Pas de RR nécessaire, prévention des boucles simple | Plus d'ASN à gérer |

## VPC (Virtual Port Channel) {#vpc-virtual-port-channel}

Deux commutateurs apparaissent comme un seul pour les hôtes connectés (Cisco NX-OS) :

- **VIP** - IP VTEP partagée par les deux pairs
- **PIP** - IP VTEP individuelle par commutateur (pour le routage L3)
- Peer Link + Peer Keepalive pour le contrôle et la synchronisation

### EVPN MC-LAG (alternative standardisée) {#evpn-mc-lag-standards-based-alternative}

Utilise les routes EVPN de type 1 et 4. Aucun protocole propriétaire. Compatible multi-constructeurs.

## Architectures multi-site {#multi-site-architectures}

| Type | Description |
|------|-------------|
| Multi-Pod | Fabric unique, super-spines entre les pods |
| Multi-Fabric | Fabrics indépendantes, interconnexion L2 |
| Multi-Site | Fabrics indépendantes, DCI EVPN, ré-encapsulation aux frontières |

## Pièges courants {#gotchas}

- VXLAN ajoute 50 octets de surcharge à chaque paquet : prévoir le MTU en conséquence
- La suppression ARP sur les leafs réduit fortement l'inondation BUM
- Les routes de type 5 sont essentielles à grande échelle : elles réduisent la surcharge du plan de contrôle par rapport aux routes d'hôte
- Les ports VPC orphelins (hôtes à connexion unique) nécessitent une gestion spécifique
- Multi-site : le VNI doit correspondre entre les sites, et le RT généré automatiquement nécessite `rewrite-rt`

## Voir aussi {#see-also}

- [[kubernetes-services-and-networking]] - concepts de réseau pour conteneurs
- [[aws-cloud-fundamentals]] - réseau VPC dans AWS
- [[monitoring-and-observability]] - supervision réseau
