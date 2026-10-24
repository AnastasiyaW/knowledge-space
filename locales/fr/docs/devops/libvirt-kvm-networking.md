---
level: 3
source_sha256: 4048dd4f9ec51ce6c9e77d5f5b00ff9ec5507228c5dc03686ca1285340a9fa10
translation: machine
translated_at: '2026-10-24'
---
# libvirt/KVM Guest Networking — Stabilité des connexions TCP de longue durée {#libvirtkvm-guest-networking-long-lived-tcp-stability}

Diagnostic et correction des coupures intermittentes de connexions sur les invités KVM utilisant le NAT de virbr0. Couvre les bogues de déchargement virtio-net, les classes de délais d'expiration de conntrack et les solutions de contournement.

## Points clés {#key-facts}

- Coupure synchrone de plusieurs connexions (3 à 4 connexions au même horodatage) = empreinte de l'hôte ou de l'hyperviseur, et NON un problème au niveau applicatif
- Les bogues de déchargement de somme de contrôle virtio-net restent actifs en 2025 : [[linux-server-administration]], RHEL bugzilla 490266
- Réseau par défaut virbr0 : NAT MASQUERADE via iptables, conntrack suit tous les flux
- Le délai d'expiration UDP de conntrack (`nf_conntrack_udp_timeout`) vaut 30 s par défaut : les tunnels QUIC meurent silencieusement
- Le délai d'expiration des connexions TCP établies de conntrack vaut 432000 s (5 jours) par défaut : ce n'est pas la cause des coupures au bout de 3 à 15 min
- `nf_conntrack_tcp_timeout_unacknowledged = 300s` : peut tuer des flux si le déchargement corrompt un segment et provoque une tempête de retransmissions
- vhost-net s'exécute comme thread noyau ; la contention d'ordonnancement CPU provoque une gigue d'IRQ par lots → toutes les files se bloquent simultanément
- Issue #212 de virtio-spec (début 2025) : `VIRTIO_NET_F_GUEST_UDP_TUNNEL_GSO` utilise des bits supérieurs à 64, alors que `VIRTIO_NET_CTRL_GUEST_OFFLOADS_SET` est sur 64 bits : l'UDP/QUIC encapsulé est directement concerné

## Diagnostic préalable {#diagnostic-first}

Exécutez les diagnostics **avant** de modifier quoi que ce soit dans le réglage. Identifiez la classe de bogue en cause.

### Étape 1 — État de référence des interfaces {#step-1-baseline-interface-state}

```bash
# Guest: identify NIC name and driver
ip link show
ethtool -i ens3            # confirm virtio_net driver

# Guest: current offload state
ethtool -k ens3 | grep -E 'tx-check|gso|gro|tso|large-receive'

# Guest: driver-level counters
ethtool -S ens3 2>/dev/null | grep -iE 'drop|err|stall'

# Host: virbr0 and vnet tap stats — look for non-zero RX/TX errors or drops
ip -s -s link show virbr0
ip -s -s link show vnet0   # substitute actual vnet interface name

# Host: offload state on bridge and tap
ethtool -k virbr0 | grep -E 'tx-check|gso|gro|tso'
ethtool -k vnet0  | grep -E 'tx-check|gso|gro|tso'

# Host: confirm VM XML — model type and vhost setting
virsh dumpxml <vm-name> | grep -A5 'interface'
```

### Étape 2 — conntrack -E (capture d'événements en direct pendant la reproduction) {#step-2-conntrack-e-live-event-capture-during-reproducer}

```bash
# Host: stream DESTROY events for guest IP while reproducer runs
sudo conntrack -E -s 192.168.122.10 -e DESTROY 2>&1 | tee /tmp/conntrack-destroy.log

# Host: check conntrack table pressure
cat /proc/sys/net/netfilter/nf_conntrack_count
cat /proc/sys/net/netfilter/nf_conntrack_max
grep . /proc/net/stat/nf_conntrack   # 'drop' column must be 0
```

Si des événements DESTROY apparaissent pour les entrées UDP après environ 30 s, sans fin de session → **classe de délai d'expiration UDP du NAT** (passez à la correction 2).
Si DESTROY apparaît pour des entrées TCP avec `[UNREPLIED]` ou en milieu de session → **minuterie des segments non acquittés de conntrack** déclenchée par une tempête de retransmissions (passez d'abord à la correction 1, puis à la correction 3).

### Étape 3 — Capture tcpdump en parallèle (distinguer bogue de déchargement et PMTU) {#step-3-tcpdump-parallel-capture-decide-offload-bug-vs-pmtu}

```bash
# Host: capture virbr0 traffic — run before reproducer, stop after drop occurs
sudo timeout 1800 tcpdump -i virbr0 -w /tmp/virbr0.pcap \
    'host 192.168.122.10 and (port 7844 or port 443 or icmp)' &

# Host: capture uplink simultaneously
sudo timeout 1800 tcpdump -i eth0 -w /tmp/uplink.pcap \
    '(port 7844 or port 443) and (tcp or udp or icmp)' &
```

**Reconnaissance des motifs dans la capture pcap :**

| Observation | Diagnostic |
|---|---|
| RST TCP provenant de l'hôte à l'horodatage de la coupure | corruption due au déchargement → RST TCP |
| Les paquets QUIC cessent brutalement, sans RST | délai d'expiration UDP du NAT |
| ICMP type 3 code 4 (fragmentation nécessaire) envoyé sans réponse vers l'invité | trou noir PMTU |
| Retransmissions côté hôte absentes côté invité | corruption de données par le déchargement virtio-net |
| Toutes les connexions coupent à moins d'une seconde d'écart | blocage du thread vhost-net ou famine d'IRQ |

---

## Corrections {#fixes}

Appliquez une correction à la fois ; testez pendant 30 à 60 minutes entre chaque étape.

### Correction 1 — Désactiver les déchargements virtio-net dans l'invité (rendement maximal, environ 5 min) {#fix-1-disable-virtio-net-offloads-in-guest-highest-yield-5-min}

Traite les bogues de déchargement de somme de contrôle (RHEL bz 490266, Ubuntu LP 1629053).

```bash
# Guest — immediate, reversible
sudo ethtool -K ens3 tx off rx off tso off gso off gro off lro off

# Verify
ethtool -k ens3 | grep -E 'tx-check|gso|gro|tso|large-receive'
```

**Persistant (ancien `/etc/network/interfaces`) :**

```bash
# /etc/network/interfaces.d/ens3-offload
post-up ethtool -K ens3 tx off rx off tso off gso off gro off lro off
```

### Correction 2 — Forcer cloudflared en HTTP/2 (contourne la classe de délai d'expiration UDP/QUIC du NAT) {#fix-2-force-cloudflared-to-http2-bypasses-udpquic-nat-timeout-class}

cloudflared utilise par défaut QUIC sur UDP/7844. Le délai UDP par défaut de conntrack, 30 s pour un flux, provoque la fermeture du tunnel. Forcer HTTP/2 maintient un unique flux TCP établi de longue durée (délai de conntrack de 5 jours).

```yaml
# /etc/cloudflared/config.yml
tunnel: <tunnel-id>
credentials-file: /etc/cloudflared/<id>.json
protocol: http2    # was: quic (default)
```

```bash
sudo systemctl restart cloudflared
```

Confirmez le protocole actif :

```bash
journalctl -u cloudflared --since "1 min ago" | grep -i protocol
```

Si les coupures cessent après ce changement, la cause racine est confirmée sur le chemin UDP/QUIC (délai d'expiration NAT ou bogue GSO sur UDP de virtio-spec #212).

### Correction 3 — Désactiver les déchargements sur virbr0 et la tap vnet (côté hôte) {#fix-3-disable-offloads-on-virbr0-and-vnet-tap-host-side}

Supprime le double déchargement (pont de l'hôte et virtio). Pratique courante sous Proxmox pour les ponts virtuels.

```bash
# Host — find vnet interface for the VM
ip link | grep vnet

# Apply
sudo ethtool -K virbr0 tx off gso off tso off
sudo ethtool -K vnet0  tx off gso off tso off   # substitute actual name
```

**Persistant via udev (s'exécute à chaque création de vnet) :**

```bash
# /etc/udev/rules.d/99-vnet-offload.rules
ACTION=="add", SUBSYSTEM=="net", KERNEL=="vnet*", \
  RUN+="/sbin/ethtool -K %k tx off gso off tso off"
```

```bash
sudo udevadm control --reload-rules
```

### Correction 4 — Clamping MSS (trou noir PMTU à travers le NAT) {#fix-4-mss-clamping-pmtu-black-hole-through-nat}

Le MASQUERADE de virbr0 peut avaler les ICMP fragmentation-nécessaire, ce qui casse la découverte PMTU pour les rafales volumineuses.

```bash
# Host — add to FORWARD chain
sudo iptables -t mangle -A FORWARD -p tcp --tcp-flags SYN,RST SYN \
    -j TCPMSS --clamp-mss-to-pmtu

# Verify rule is in place
sudo iptables -t mangle -L FORWARD -nv
```

**Persistant via netfilter-persistent :**

```bash
sudo apt install netfilter-persistent
sudo netfilter-persistent save
```

### Correction 5 — Allongement du délai d'expiration UDP de conntrack {#fix-5-conntrack-udp-timeout-extension}

Si le protocole doit rester QUIC et que la correction 2 n'est pas acceptable :

```bash
# Host — extend UDP stream timeout (seconds); persist in /etc/sysctl.d/99-conntrack.conf
sudo sysctl -w net.netfilter.nf_conntrack_udp_timeout=300
sudo sysctl -w net.netfilter.nf_conntrack_udp_timeout_stream=600
```

### Correction 6 — Épinglage CPU de vhost-net (supprime la gigue d'IRQ) {#fix-6-vhost-net-cpu-pinning-eliminates-irq-jitter}

Épinglez le thread noyau vhost-net sur des cœurs hôtes dédiés, non partagés avec les vCPU de l'invité. Empêche la migration SMT qui provoque les blocages de files par lots.

```xml
<!-- virsh edit <vm-name> — add inside <domain> -->
<cputune>
  <vcpupin vcpu='0' cpuset='2'/>
  <vcpupin vcpu='1' cpuset='3'/>
  <emulatorpin cpuset='0-1'/>    <!-- dedicated host cores, not in vcpupin -->
  <iothreadpin iothread='1' cpuset='0-1'/>
</cputune>
```

```bash
virsh shutdown <vm-name> && virsh edit <vm-name> && virsh start <vm-name>
ps -eLo pid,tid,psr,comm | grep vhost   # verify placement
```

Réglez aussi le multi-files pour qu'il corresponde au nombre de vCPU dans le XML de l'interface : `<driver name='vhost' queues='8'/>`, puis dans l'invité : `sudo ethtool -L ens3 combined 8`.

---

## Solutions de contournement {#escape-hatches}

À utiliser si les corrections 1 à 6 ne résolvent pas les coupures après 24 heures de tests ou plus.

### macvtap (supprime entièrement la couche de pont hôte) {#macvtap-removes-host-bridge-layer-entirely}

Le trafic des VM contourne virbr0 et atteint directement la carte réseau physique.
**Limitation :** la communication hôte vers VM ne fonctionne plus (restriction de conception de macvtap).

```xml
<!-- virsh edit <vm-name> — replace existing interface block -->
<interface type='direct'>
  <source dev='eth0' mode='bridge'/>
  <model type='virtio'/>
  <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
</interface>
```

```bash
virsh shutdown <vm-name>
virsh edit <vm-name>
virsh start <vm-name>
```

Référence : https://wiki.libvirt.org/TroubleshootMacvtapHostFail.html

### Pont Linux vers la carte physique (adresse IP routable sur le réseau physique) {#linux-bridge-to-physical-nic-full-routable-ip-on-physical-network}

Supprime complètement le NAT. La VM reçoit une adresse IP routable sur le LAN physique, ce qui élimine la surcharge de conntrack.

```bash
# Host — create bridge and attach physical NIC
sudo ip link add name br0 type bridge
sudo ip link set eth0 master br0
sudo ip link set br0 up
sudo dhclient br0
```

```xml
<!-- VM XML -->
<interface type='bridge'>
  <source bridge='br0'/>
  <model type='virtio'/>
</interface>
```

### Passthrough de VF SR-IOV (stabilité maximale, nécessite la prise en charge de la carte réseau et du BIOS) {#sr-iov-vf-passthrough-highest-stability-requires-nic-bios-support}

Transmet une fonction virtuelle de la carte réseau physique directement à la VM. Supprime virtio : plus de bogues de déchargement, plus de gigue vhost-net, et aucune intervention du noyau hôte dans le chemin de données.

```bash
# Host — check VF support
cat /sys/class/net/eth0/device/sriov_totalvfs

# Create VFs (example: 4)
echo 4 | sudo tee /sys/class/net/eth0/device/sriov_numvfs

# List VF PCI addresses
lspci | grep -i "Virtual Function"
```

```xml
<!-- VM XML — attach VF as hostdev -->
<hostdev mode='subsystem' type='pci' managed='yes'>
  <source>
    <address domain='0x0000' bus='0x00' slot='0x10' function='0x1'/>
  </source>
</hostdev>
```

Référence : https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/virtualization_host_configuration_and_guest_installation_guide/sect-virtualization_host_configuration_and_guest_installation_guide-sr_iov-how_sr_iov_libvirt_works

---

## Pièges courants {#gotchas}

- **Problème :** les bogues de déchargement virtio-net sont signalés comme « corrigés » dans d'anciens journaux de modifications, mais se déclenchent toujours sur les chemins pont/NAT dans Linux 6.x. Le bogue RHEL bugzilla 490266 reste ouvert en 2025. L'issue #212 de virtio-spec a ajouté `VIRTIO_NET_F_GUEST_UDP_TUNNEL_GSO` via des bits supérieurs à 64, mais le chemin de contrôle `VIRTIO_NET_CTRL_GUEST_OFFLOADS_SET` est sur 64 bits : l'UDP/QUIC encapsulé se trouve donc dans une zone d'ambiguïté. -> **Correction :** désactivez toujours explicitement les déchargements ; ne supposez jamais qu'une version du noyau garantit la sécurité.

- **Problème :** le tunnel QUIC (par défaut pour cloudflared) se coupe toutes les 2 à 3 minutes sur le NAT, alors que les connexions TCP de la même invité restent stables pendant des heures. `nf_conntrack_udp_timeout = 30s` par défaut ; si l'intervalle de keepalive QUIC dépasse cette valeur, l'entrée NAT expire et le paquet suivant est traité comme un nouveau flux non suivi → l'edge ferme la connexion. `conntrack -E -e DESTROY` montre la destruction de l'entrée UDP en cours de session. -> **Correction :** `protocol: http2` dans la configuration de cloudflared (correction 2), ou relever `nf_conntrack_udp_timeout_stream` à ≥ 600 s (correction 5).

- **Problème :** désactiver les déchargements sur la carte réseau de l'invité ne suffit pas si le pont hôte virbr0 a toujours `tx-checksumming on`. Le pont peut réactiver le déchargement sur le chemin vers la liaison montante. -> **Correction :** appliquez `ethtool -K virbr0 tx off gso off tso off` sur l'hôte, en plus de l'invité (correction 3).

- **Problème :** macvtap en `mode='bridge'` empêche par conception la communication hôte ↔ VM (le hairpin forwarding est désactivé dans le pilote macvlan). Les services de l'hôte qui doivent joindre l'adresse IP de la VM expirent silencieusement. -> **Correction :** ajoutez une seconde carte virtuelle sur virbr1 pour la gestion hôte ↔ VM, et n'utilisez macvtap que pour le trafic externe. Ou utilisez plutôt un pont Linux vers la carte physique.

---

## Voir aussi {#see-also}

- [[linux-server-administration]] — ethtool, persistance sysctl, unités de service systemd
- [[datacenter-network-design]] — découverte PMTU, ECMP, compromis entre pontage et routage
- [[monitoring-and-observability]] — métriques conntrack, compteurs de pertes d'interface, statistiques IRQ

**Références :**
- https://www.kernel.org/doc/Documentation/networking/nf_conntrack-sysctl.rst
- https://github.com/oasis-tcs/virtio-spec/issues/212
- https://github.com/oasis-tcs/virtio-spec/issues/225
- https://bugzilla.redhat.com/show_bug.cgi?id=490266
- https://bugs.launchpad.net/ubuntu/+source/openvswitch/+bug/1629053
- https://github.com/cloudflare/cloudflared/issues/917
- https://github.com/homeassistant-apps/app-cloudflared/issues/152
- https://forum.proxmox.com/threads/should-i-turn-off-tso-and-gso-on-vmbr0.39011/
- https://wiki.libvirt.org/TroubleshootMacvtapHostFail.html
- https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/virtualization_tuning_and_optimization_guide/sect-virtualization_tuning_optimization_guide-networking-techniques
- https://www.linux-kvm.org/page/Multiqueue
- https://tldp.org/HOWTO/Adv-Routing-HOWTO/lartc.cookbook.mtu-mss.html
