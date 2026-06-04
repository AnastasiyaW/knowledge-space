# libvirt/KVM Guest Networking — Long-Lived TCP Stability

Diagnosing and fixing intermittent connection drops on KVM guests using virbr0 NAT. Covers virtio-net offload bugs, conntrack timeout classes, and escape hatches.

## Key Facts

- Synchronous multi-connection drop (3-4 connections in one timestamp) = host/hypervisor fingerprint — NOT application-level
- virtio-net checksum offload bugs remain active as of 2025: [[linux-server-administration]], RHEL bugzilla 490266
- virbr0 default network: MASQUERADE NAT via iptables, conntrack tracks all flows
- UDP conntrack timeout (`nf_conntrack_udp_timeout`) defaults 30s — QUIC tunnels die silently
- TCP established conntrack timeout defaults 432000s (5 days) — not the cause of 3–15 min drops
- `nf_conntrack_tcp_timeout_unacknowledged = 300s` — can kill flows if offload corrupts a segment causing retransmit storms
- vhost-net runs as a kernel thread; CPU scheduling contention causes batch IRQ jitter → all queues stall simultaneously
- virtio-spec issue #212 (early 2025): `VIRTIO_NET_F_GUEST_UDP_TUNNEL_GSO` uses bits >64 but `VIRTIO_NET_CTRL_GUEST_OFFLOADS_SET` is 64-bit — tunneled UDP/QUIC directly affected

## Diagnostic First

Run diagnostics **before** changing any tuning. Identify which class of bug is present.

### Step 1 — Baseline interface state

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

### Step 2 — conntrack -E (live event capture during reproducer)

```bash
# Host: stream DESTROY events for guest IP while reproducer runs
sudo conntrack -E -s 192.168.122.10 -e DESTROY 2>&1 | tee /tmp/conntrack-destroy.log

# Host: check conntrack table pressure
cat /proc/sys/net/netfilter/nf_conntrack_count
cat /proc/sys/net/netfilter/nf_conntrack_max
grep . /proc/net/stat/nf_conntrack   # 'drop' column must be 0
```

If DESTROY events fire for UDP entries after ~30s with no session tear-down → **NAT UDP timeout class** (go to Fix 2).
If DESTROY fires for TCP entries with `[UNREPLIED]` or mid-session → **conntrack unacknowledged timer** triggered by retransmit storm (go to Fix 1 first, Fix 3 second).

### Step 3 — tcpdump parallel capture (decide offload-bug vs PMTU)

```bash
# Host: capture virbr0 traffic — run before reproducer, stop after drop occurs
sudo timeout 1800 tcpdump -i virbr0 -w /tmp/virbr0.pcap \
    'host 192.168.122.10 and (port 7844 or port 443 or icmp)' &

# Host: capture uplink simultaneously
sudo timeout 1800 tcpdump -i eth0 -w /tmp/uplink.pcap \
    '(port 7844 or port 443) and (tcp or udp or icmp)' &
```

**Pattern recognition in pcap:**

| Observation | Diagnosis |
|---|---|
| TCP RST from host at drop timestamp | offload corruption → TCP RST |
| QUIC packets stop abruptly, no RST | UDP NAT timeout |
| ICMP type 3 code 4 (frag needed) sent but no reply to guest | PMTU black hole |
| Retransmits on host side absent on guest side | virtio-net offload data corruption |
| All connections drop within 1s of each other | vhost-net thread stall or IRQ starvation |

---

## Fixes

Apply one at a time; test 30-60 minutes between steps.

### Fix 1 — Disable virtio-net offloads in guest (highest yield, ~5 min)

Addresses checksum offload bugs (RHEL bz 490266, Ubuntu LP 1629053).

```bash
# Guest — immediate, reversible
sudo ethtool -K ens3 tx off rx off tso off gso off gro off lro off

# Verify
ethtool -k ens3 | grep -E 'tx-check|gso|gro|tso|large-receive'
```

**Persistent (legacy `/etc/network/interfaces`):**

```bash
# /etc/network/interfaces.d/ens3-offload
post-up ethtool -K ens3 tx off rx off tso off gso off gro off lro off
```

### Fix 2 — Force cloudflared to HTTP/2 (bypasses UDP/QUIC NAT timeout class)

Default cloudflared uses QUIC over UDP/7844. UDP conntrack default = 30s stream, kills tunnel. Forcing HTTP/2 keeps a single long-lived TCP established flow (5-day conntrack timeout).

```yaml
# /etc/cloudflared/config.yml
tunnel: <tunnel-id>
credentials-file: /etc/cloudflared/<id>.json
protocol: http2    # was: quic (default)
```

```bash
sudo systemctl restart cloudflared
```

Confirm active protocol:

```bash
journalctl -u cloudflared --since "1 min ago" | grep -i protocol
```

If drops stop after this change → root cause confirmed as UDP/QUIC path (NAT timeout or virtio-spec #212 GSO-over-UDP bug).

### Fix 3 — Disable offloads on virbr0 and vnet tap (host side)

Removes double-offload (host bridge + virtio). Proxmox community standard for virtual bridges.

```bash
# Host — find vnet interface for the VM
ip link | grep vnet

# Apply
sudo ethtool -K virbr0 tx off gso off tso off
sudo ethtool -K vnet0  tx off gso off tso off   # substitute actual name
```

**Persistent via udev (fires on each vnet creation):**

```bash
# /etc/udev/rules.d/99-vnet-offload.rules
ACTION=="add", SUBSYSTEM=="net", KERNEL=="vnet*", \
  RUN+="/sbin/ethtool -K %k tx off gso off tso off"
```

```bash
sudo udevadm control --reload-rules
```

### Fix 4 — MSS clamping (PMTU black hole through NAT)

virbr0 MASQUERADE can swallow ICMP frag-needed, breaking PMTU discovery for large bursts.

```bash
# Host — add to FORWARD chain
sudo iptables -t mangle -A FORWARD -p tcp --tcp-flags SYN,RST SYN \
    -j TCPMSS --clamp-mss-to-pmtu

# Verify rule is in place
sudo iptables -t mangle -L FORWARD -nv
```

**Persistent via netfilter-persistent:**

```bash
sudo apt install netfilter-persistent
sudo netfilter-persistent save
```

### Fix 5 — conntrack UDP timeout extension

If protocol must remain QUIC and Fix 2 is not acceptable:

```bash
# Host — extend UDP stream timeout (seconds); persist in /etc/sysctl.d/99-conntrack.conf
sudo sysctl -w net.netfilter.nf_conntrack_udp_timeout=300
sudo sysctl -w net.netfilter.nf_conntrack_udp_timeout_stream=600
```

### Fix 6 — vhost-net CPU pinning (eliminates IRQ jitter)

Pin vhost-net kernel thread to dedicated host cores not shared with guest vCPUs. Prevents SMT migration → batch queue stalls.

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

Also set multiqueue to match vCPU count in the interface XML: `<driver name='vhost' queues='8'/>`, then in guest: `sudo ethtool -L ens3 combined 8`.

---

## Escape Hatches

Use when Fixes 1-6 do not resolve drops after 24+ hours of testing.

### macvtap (removes host bridge layer entirely)

VM traffic bypasses virbr0 and hits the physical NIC directly.
**Limitation:** host-to-VM communication breaks (macvtap design restriction).

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

Reference: https://wiki.libvirt.org/TroubleshootMacvtapHostFail.html

### Linux bridge to physical NIC (full routable IP on physical network)

Removes NAT entirely. VM gets a routable IP in the physical LAN — eliminates conntrack overhead.

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

### SR-IOV VF passthrough (highest stability, requires NIC + BIOS support)

Passes a virtual function of the physical NIC directly into the VM. Removes virtio entirely — no offload bugs, no vhost-net jitter, no host kernel involvement in data path.

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

Reference: https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/virtualization_host_configuration_and_guest_installation_guide/sect-virtualization_host_configuration_and_guest_installation_guide-sr_iov-how_sr_iov_libvirt_works

---

## Gotchas

- **Issue:** virtio-net offload bugs reported as "fixed" in older changelogs but still trigger on bridge/NAT paths in Linux 6.x — RHEL bugzilla 490266 remains open as of 2025. virtio-spec #212 added `VIRTIO_NET_F_GUEST_UDP_TUNNEL_GSO` via bits >64, but the `VIRTIO_NET_CTRL_GUEST_OFFLOADS_SET` control path is 64-bit: tunneled UDP/QUIC is directly in the ambiguity zone. -> **Fix:** always disable offloads explicitly; do not assume kernel version implies safety.

- **Issue:** QUIC tunnel (cloudflared default) drops every 2-3 minutes on NAT even when TCP connections from the same guest are stable for hours. `nf_conntrack_udp_timeout = 30s` by default; if QUIC keepalive interval exceeds this, the NAT entry expires and the next packet is treated as a new untracked flow → edge closes the connection. `conntrack -E -e DESTROY` shows the UDP entry being destroyed mid-session. -> **Fix:** `protocol: http2` in cloudflared config (Fix 2), or raise `nf_conntrack_udp_timeout_stream` to ≥ 600s (Fix 5).

- **Issue:** Disabling offloads on the guest NIC is not sufficient if the host virbr0 bridge still has `tx-checksumming on`. The bridge can re-enable offload on the path to the uplink. -> **Fix:** apply `ethtool -K virbr0 tx off gso off tso off` on the host in addition to the guest (Fix 3).

- **Issue:** macvtap `mode='bridge'` prevents host ↔ VM communication by design (hairpin forwarding disabled in macvlan driver). Services on the host that need to reach the VM IP will time out silently. -> **Fix:** add a second virtual NIC on virbr1 for host↔VM management; use macvtap only for external traffic. Or use a Linux bridge-to-physical NIC instead.

---

## See Also

- [[linux-server-administration]] — ethtool, sysctl persistence, systemd service units
- [[datacenter-network-design]] — PMTU discovery, ECMP, bridging vs routing tradeoffs
- [[monitoring-and-observability]] — conntrack metrics, interface drop counters, IRQ stats

**Source references:**
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
