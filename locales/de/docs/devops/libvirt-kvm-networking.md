---
level: 3
source_sha256: 4048dd4f9ec51ce6c9e77d5f5b00ff9ec5507228c5dc03686ca1285340a9fa10
translation: machine
translated_at: '2026-10-24'
---
# libvirt/KVM-Gastnetzwerk: Stabilität langlebiger TCP-Verbindungen {#libvirtkvm-guest-networking-long-lived-tcp-stability}

Diagnose und Behebung sporadischer Verbindungsabbrüche bei KVM-Gästen mit virbr0-NAT. Behandelt Fehler beim virtio-net-Offloading, Timeout-Klassen des Conntrack und Notausgänge.

## Wichtige Fakten {#key-facts}

- Synchroner Abbruch mehrerer Verbindungen (3–4 Verbindungen mit demselben Zeitstempel) = Signatur von Host/Hypervisor, NICHT der Anwendungsebene
- virtio-net-Fehler bei der Checksummen-Offload-Berechnung sind Stand 2025 weiterhin aktiv: [[linux-server-administration]], RHEL-Bugzilla 490266
- Standard-Netzwerk virbr0: MASQUERADE-NAT über iptables, conntrack verfolgt alle Flows
- Der UDP-Conntrack-Timeout (`nf_conntrack_udp_timeout`) beträgt standardmäßig 30 s – QUIC-Tunnel brechen lautlos ab
- Der Conntrack-Timeout für etablierte TCP-Verbindungen beträgt standardmäßig 432000 s (5 Tage) – er ist nicht die Ursache für Abbrüche nach 3–15 Minuten
- `nf_conntrack_tcp_timeout_unacknowledged = 300s` – kann Flows beenden, wenn das Offloading ein Segment beschädigt und dadurch Retransmit-Stürme ausgelöst werden
- vhost-net läuft als Kernel-Thread; Konkurrenz um CPU-Zeit verursacht gebündeltes IRQ-Jitter → alle Queues stehen gleichzeitig still
- virtio-spec Issue #212 (Anfang 2025): `VIRTIO_NET_F_GUEST_UDP_TUNNEL_GSO` verwendet Bits oberhalb von 64, `VIRTIO_NET_CTRL_GUEST_OFFLOADS_SET` ist jedoch 64-Bit breit – getunnelter UDP-/QUIC-Verkehr ist direkt betroffen

## Zuerst diagnostizieren {#diagnostic-first}

Führen Sie Diagnosen **vor** jeder Änderung an der Konfiguration aus. Ermitteln Sie, welche Fehlerklasse vorliegt.

### Schritt 1 – Ausgangszustand der Schnittstellen {#step-1-baseline-interface-state}

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

### Schritt 2 – conntrack -E (Live-Erfassung von Ereignissen während der Reproduktion) {#step-2-conntrack-e-live-event-capture-during-reproducer}

```bash
# Host: stream DESTROY events for guest IP while reproducer runs
sudo conntrack -E -s 192.168.122.10 -e DESTROY 2>&1 | tee /tmp/conntrack-destroy.log

# Host: check conntrack table pressure
cat /proc/sys/net/netfilter/nf_conntrack_count
cat /proc/sys/net/netfilter/nf_conntrack_max
grep . /proc/net/stat/nf_conntrack   # 'drop' column must be 0
```

Treten DESTROY-Ereignisse für UDP-Einträge nach ca. 30 s auf, ohne dass die Sitzung beendet wurde → **Klasse: UDP-NAT-Timeout** (weiter mit Fix 2).
Tritt DESTROY für TCP-Einträge mit `[UNREPLIED]` oder mitten in einer Sitzung auf → **Timer für nicht bestätigte Verbindungen** wurde durch einen Retransmit-Sturm ausgelöst (zuerst Fix 1, danach Fix 3).

### Schritt 3 – Parallele tcpdump-Erfassung (Unterscheidung Offload-Fehler vs. PMTU) {#step-3-tcpdump-parallel-capture-decide-offload-bug-vs-pmtu}

```bash
# Host: capture virbr0 traffic — run before reproducer, stop after drop occurs
sudo timeout 1800 tcpdump -i virbr0 -w /tmp/virbr0.pcap \
    'host 192.168.122.10 and (port 7844 or port 443 or icmp)' &

# Host: capture uplink simultaneously
sudo timeout 1800 tcpdump -i eth0 -w /tmp/uplink.pcap \
    '(port 7844 or port 443) and (tcp or udp or icmp)' &
```

**Mustererkennung im pcap:**

| Beobachtung | Diagnose |
|---|---|
| TCP-RST vom Host zum Zeitpunkt des Abbruchs | Offload-Beschädigung → TCP-RST |
| QUIC-Pakete brechen abrupt ab, kein RST | UDP-NAT-Timeout |
| ICMP Typ 3 Code 4 (frag needed) gesendet, aber keine Antwort an den Gast | PMTU-Black-Hole |
| Retransmits auf Host-Seite, auf Gast-Seite fehlen sie | Datenkorruption durch virtio-net-Offloading |
| Alle Verbindungen brechen innerhalb einer Sekunde voneinander ab | Stillstand des vhost-net-Threads oder IRQ-Starvation |

---

## Korrekturen {#fixes}

Wenden Sie jeweils nur eine Korrektur an und testen Sie zwischen den Schritten 30–60 Minuten.

### Fix 1 – virtio-net-Offloads im Gast deaktivieren (größte Wirkung, ca. 5 min) {#fix-1-disable-virtio-net-offloads-in-guest-highest-yield-5-min}

Behebt Fehler bei der Checksummen-Offload-Berechnung (RHEL-bz 490266, Ubuntu LP 1629053).

```bash
# Guest — immediate, reversible
sudo ethtool -K ens3 tx off rx off tso off gso off gro off lro off

# Verify
ethtool -k ens3 | grep -E 'tx-check|gso|gro|tso|large-receive'
```

**Persistent (veraltete Datei `/etc/network/interfaces`):**

```bash
# /etc/network/interfaces.d/ens3-offload
post-up ethtool -K ens3 tx off rx off tso off gso off gro off lro off
```

### Fix 2 – cloudflared auf HTTP/2 erzwingen (umgeht die UDP/QUIC-NAT-Timeout-Klasse) {#fix-2-force-cloudflared-to-http2-bypasses-udpquic-nat-timeout-class}

cloudflared verwendet standardmäßig QUIC über UDP/7844. Der UDP-Conntrack-Standard von 30 s für Streams beendet den Tunnel. Das Erzwingen von HTTP/2 hält einen einzigen langlebigen, etablierten TCP-Flow aufrecht (5-Tage-Conntrack-Timeout).

```yaml
# /etc/cloudflared/config.yml
tunnel: <tunnel-id>
credentials-file: /etc/cloudflared/<id>.json
protocol: http2    # was: quic (default)
```

```bash
sudo systemctl restart cloudflared
```

Aktives Protokoll bestätigen:

```bash
journalctl -u cloudflared --since "1 min ago" | grep -i protocol
```

Hören die Abbrüche nach dieser Änderung auf, ist die Ursache im UDP/QUIC-Pfad bestätigt (NAT-Timeout oder virtio-spec #212, GSO-über-UDP-Fehler).

### Fix 3 – Offloads auf virbr0 und dem vnet-Tap deaktivieren (Host-Seite) {#fix-3-disable-offloads-on-virbr0-and-vnet-tap-host-side}

Beseitigt das doppelte Offloading (Host-Bridge und virtio). Proxmox-Community-Standard für virtuelle Bridges.

```bash
# Host — find vnet interface for the VM
ip link | grep vnet

# Apply
sudo ethtool -K virbr0 tx off gso off tso off
sudo ethtool -K vnet0  tx off gso off tso off   # substitute actual name
```

**Persistent über udev (greift bei jeder Erstellung eines vnet):**

```bash
# /etc/udev/rules.d/99-vnet-offload.rules
ACTION=="add", SUBSYSTEM=="net", KERNEL=="vnet*", \
  RUN+="/sbin/ethtool -K %k tx off gso off tso off"
```

```bash
sudo udevadm control --reload-rules
```

### Fix 4 – MSS-Clamping (PMTU-Black-Hole durch NAT) {#fix-4-mss-clamping-pmtu-black-hole-through-nat}

Die MASQUERADE-Regel auf virbr0 kann ICMP frag-needed verschlucken und damit die PMTU-Erkennung bei großen Burst-Übertragungen unterbrechen.

```bash
# Host — add to FORWARD chain
sudo iptables -t mangle -A FORWARD -p tcp --tcp-flags SYN,RST SYN \
    -j TCPMSS --clamp-mss-to-pmtu

# Verify rule is in place
sudo iptables -t mangle -L FORWARD -nv
```

**Persistent über netfilter-persistent:**

```bash
sudo apt install netfilter-persistent
sudo netfilter-persistent save
```

### Fix 5 – Verlängerung des UDP-Conntrack-Timeouts {#fix-5-conntrack-udp-timeout-extension}

Falls das Protokoll QUIC bleiben muss und Fix 2 nicht akzeptabel ist:

```bash
# Host — extend UDP stream timeout (seconds); persist in /etc/sysctl.d/99-conntrack.conf
sudo sysctl -w net.netfilter.nf_conntrack_udp_timeout=300
sudo sysctl -w net.netfilter.nf_conntrack_udp_timeout_stream=600
```

### Fix 6 – CPU-Pinning für vhost-net (beseitigt IRQ-Jitter) {#fix-6-vhost-net-cpu-pinning-eliminates-irq-jitter}

Den vhost-net-Kernel-Thread auf dedizierte Host-Kerne pinnen, die nicht mit den vCPUs des Gasts geteilt werden. Verhindert SMT-Migration und dadurch gebündelte Queue-Stillstände.

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

Außerdem Multiqueue in der Schnittstellen-XML auf die Anzahl der vCPUs setzen: `<driver name='vhost' queues='8'/>`, anschließend im Gast: `sudo ethtool -L ens3 combined 8`.

---

## Notausgänge {#escape-hatches}

Einsetzen, wenn die Fixes 1–6 die Abbrüche nach mindestens 24 Stunden Test nicht beheben.

### macvtap (entfernt die Host-Bridge-Schicht vollständig) {#macvtap-removes-host-bridge-layer-entirely}

Der VM-Verkehr umgeht virbr0 und trifft direkt auf die physische NIC.
**Einschränkung:** Kommunikation zwischen Host und VM funktioniert nicht (Designbeschränkung von macvtap).

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

Referenz: https://wiki.libvirt.org/TroubleshootMacvtapHostFail.html

### Linux-Bridge auf die physische NIC (vollwertige routbare IP im physischen Netz) {#linux-bridge-to-physical-nic-full-routable-ip-on-physical-network}

Entfernt das NAT vollständig. Die VM erhält eine routbare IP im physischen LAN – der Conntrack-Overhead entfällt.

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

### SR-IOV-VF-Passthrough (höchste Stabilität, erfordert NIC- und BIOS-Unterstützung) {#sr-iov-vf-passthrough-highest-stability-requires-nic-bios-support}

Reicht eine Virtual Function der physischen NIC direkt in die VM durch. virtio entfällt vollständig – keine Offload-Fehler, kein vhost-net-Jitter, keine Beteiligung des Host-Kernels am Datenpfad.

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

Referenz: https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/virtualization_host_configuration_and_guest_installation_guide/sect-virtualization_host_configuration_and_guest_installation_guide-sr_iov-how_sr_iov_libvirt_works

---

## Stolpersteine {#gotchas}

- **Problem:** virtio-net-Offload-Fehler werden in älteren Changelogs als „behoben“ geführt, treten aber unter Linux 6.x auf Bridge- und NAT-Pfaden weiterhin auf – RHEL-Bugzilla 490266 ist Stand 2025 noch offen. virtio-spec #212 hat `VIRTIO_NET_F_GUEST_UDP_TUNNEL_GSO` über Bits oberhalb von 64 eingeführt, der Steuerpfad `VIRTIO_NET_CTRL_GUEST_OFFLOADS_SET` ist jedoch 64-Bit breit: getunnelter UDP-/QUIC-Verkehr befindet sich direkt in der Unklarheitszone. -> **Lösung:** Offloads immer explizit deaktivieren; nicht davon ausgehen, dass eine bestimmte Kernel-Version sicher ist.

- **Problem:** Der QUIC-Tunnel (cloudflared-Standard) bricht im NAT alle 2–3 Minuten ab, obwohl TCP-Verbindungen desselben Gasts stundenlang stabil bleiben. `nf_conntrack_udp_timeout = 30s` ist der Standard; überschreitet das QUIC-Keepalive-Intervall diesen Wert, läuft der NAT-Eintrag ab, und das nächste Paket wird als neuer, nicht verfolgter Flow behandelt → der Edge-Server schließt die Verbindung. `conntrack -E -e DESTROY` zeigt, dass der UDP-Eintrag mitten in der Sitzung gelöscht wird. -> **Lösung:** `protocol: http2` in der cloudflared-Konfiguration (Fix 2) oder `nf_conntrack_udp_timeout_stream` auf ≥ 600 s erhöhen (Fix 5).

- **Problem:** Das Deaktivieren der Offloads an der NIC des Gasts reicht nicht aus, wenn die Host-Bridge virbr0 weiterhin `tx-checksumming on` aktiviert hat. Die Bridge kann das Offloading auf dem Weg zum Uplink wieder aktivieren. -> **Lösung:** `ethtool -K virbr0 tx off gso off tso off` zusätzlich zum Gast auf dem Host anwenden (Fix 3).

- **Problem:** macvtap mit `mode='bridge'` verhindert konstruktionsbedingt die Kommunikation zwischen Host und VM (Hairpin-Weiterleitung im macvlan-Treiber deaktiviert). Dienste auf dem Host, die die VM-IP erreichen müssen, laufen stillschweigend in ein Timeout. -> **Lösung:** eine zweite virtuelle NIC auf virbr1 für die Verwaltung Host↔VM hinzufügen; macvtap nur für externen Verkehr nutzen. Alternativ eine Linux-Bridge auf die physische NIC verwenden.

---

## Siehe auch {#see-also}

- [[linux-server-administration]] – ethtool, Persistenz von sysctl, systemd-Serviceunits
- [[datacenter-network-design]] – PMTU-Erkennung, ECMP, Abwägung zwischen Bridging und Routing
- [[monitoring-and-observability]] – Conntrack-Metriken, Drop-Zähler der Schnittstellen, IRQ-Statistiken

**Quellenangaben:**
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
