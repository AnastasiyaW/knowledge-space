---
title: "Browser- und Geräte-Fingerprinting"
category: concepts
tags: [security, fingerprinting, canvas, webgl, anti-fraud, tracking, privacy]
level: 3
source_sha256: 3423d6d4bb174649600e279d686e8018e5a48d427c698bad65b9d1f01cbb6058
translation: machine
translated_at: '2026-10-24'
---
# Browser- und Geräte-Fingerprinting {#browser-and-device-fingerprinting}

Technische Fingerprinting-Methoden, die von Anti-Fraud-Systemen und Tracking eingesetzt werden: Canvas-Fingerprinting, WebGL, AudioContext, Schriftarten-Enumeration, Hardware-Signale, TCP/IP-Stack-Fingerprinting, WebRTC-Leaks und persistente Tracking-Mechanismen (Evercookies).

## Wichtige Fakten {#key-facts}
- Canvas-Fingerprinting nutzt Unterschiede bei GPU- und OS-Rendering, die für das menschliche Auge unsichtbar sind
- WebGL legt das GPU-Modell direkt über die Erweiterung `WEBGL_debug_renderer_info` offen
- AudioContext-Fingerprinting beruht auf Unterschieden in der Verarbeitung durch die Web Audio API
- TCP/IP-Stack-Fingerprinting (p0f) erkennt das Betriebssystem auch hinter einem VPN
- WebRTC-STUN-Anfragen können die echte IP-Adresse hinter einem VPN offenlegen
- Evercookies speichern Identifikatoren an mehr als 10 Orten, um das Löschen zu überstehen

## Canvas-Fingerprinting {#canvas-fingerprinting}
Der Browser rendert Text und Grafiken über `<canvas>` mithilfe der GPU und der Rendering-Bibliotheken des Betriebssystems. Unterschiedliche Kombinationen aus Hardware und Software erzeugen Unterschiede auf Pixelebene.

Ablauf: Bestimmten Text und geometrische Formen erzwungen rendern -> `toDataURL()` oder `getImageData()` -> Pixeldaten hashen.

Einflussfaktoren: GPU-Modell, Treiberversion, Schriftdarstellung des Betriebssystems (DirectWrite/CoreText/FreeType), Antialiasing, Subpixel-Rendering.

Umgehung: Anti-Detect-Browser fügen den Pixeldaten Rauschen hinzu. Konsistentes Rauschen ist entscheidend, denn zufälliges Rauschen bei jedem Aufruf wirkt verdächtig.

## WebGL-Fingerprinting {#webgl-fingerprinting}
- `UNMASKED_VENDOR_WEBGL` und `UNMASKED_RENDERER_WEBGL` legen die GPU direkt offen
- Weitere Parameter: maximale Texturgröße, maximale Viewport-Abmessungen, Shader-Präzision, unterstützte Erweiterungen
- In Kombination mit 3D-Rendering-Tests entsteht ein sehr eindeutiger Fingerprint

## AudioContext-Fingerprinting {#audiocontext-fingerprinting}
`OscillatorNode` -> `DynamicsCompressorNode` -> `AnalyserNode` -> verarbeiteten Audio-Buffer auslesen. Abweichungen bei Fließkommaberechnungen in der Audioverarbeitung zwischen Plattformen erzeugen eindeutige Signaturen.

## Schriftarten-Enumeration {#font-enumeration}
- Seitenkanal: Text in Kandidatenschriften gegen eine Ausweichschrift rendern und Breiten- bzw. Höhenunterschiede messen
- Schriftartensets sind stark aussagekräftig: Schriften aus Adobe Creative Suite unterscheiden sich von der Standardausstattung unter Windows
- Sprachspezifische Schriften verraten die Locale

## Hardware-Signale {#hardware-signals}
- `screen.width`, `screen.height`, `screen.colorDepth`, `devicePixelRatio`
- `navigator.hardwareConcurrency` (logische CPU-Kerne)
- `navigator.deviceMemory` (ungefährer Arbeitsspeicher in GB)
- Battery Status API (größtenteils veraltet bzw. eingeschränkt)
- Kalibrierungs-Offsets von Sensoren (Beschleunigungssensor, Gyroskop) sind gerätespezifisch
- `navigator.mediaDevices.enumerateDevices()` liefert Audio- und Video-Geräte-IDs

## Gerätekennungen auf Betriebssystemebene {#os-level-device-identifiers}
- **Windows**: Machine GUID (`HKLM\SOFTWARE\Microsoft\Cryptography\MachineGuid`), Seriennummern von Datenträgern, BIOS-UUID
- **Linux**: `/etc/machine-id`, `/var/lib/dbus/machine-id`
- **MAC-Adressen**: leicht zu fälschen, werden aber gesammelt, sofern verfügbar
- **TPM Endorsement Key**: hardwaregebunden, nicht fälschbar

## TCP/IP-Stack-Fingerprinting {#tcpip-stack-fingerprinting}
Implementierungsdetails des Betriebssystems werden über Pakete preisgegeben:
- Initialer TTL-Wert (Linux: 64, Windows: 128)
- TCP-Fenstergröße und Reihenfolge der Optionen
- Erzeugung der IP-ID-Sequenz
- Verhalten des Don't-Fragment-Bits

Tool: `p0f` - passive Betriebssystem-Erkennung. Funktioniert auch hinter einem VPN, weil die TCP-Parameter vom Quell-Betriebssystem stammen.

## WebRTC-Leaks {#webrtc-leaks}
ICE (Interactive Connectivity Establishment) sammelt Kandidaten-IP-Adressen:
- Öffentliche IP über die Antwort eines STUN-Servers
- Lokale/private IP aus den Netzwerkschnittstellen
- Auch hinter einem VPN können die echte IP oder der lokale Netzwerkbereich sichtbar werden

Gegenmaßnahme: WebRTC deaktivieren (`media.peerconnection.enabled = false` in Firefox), Browser-Erweiterungen.

## Persistentes Tracking (Evercookies) {#persistent-tracking-evercookies}
Identifikatoren werden an mehreren Orten gespeichert, um das Löschen zu überstehen:
- HTTP-Cookies, Flash LSOs, Silverlight-Speicher
- `localStorage`, `sessionStorage`, `IndexedDB`, Web SQL
- HTTP-ETags (cachebasiert)
- HSTS-Supercookies (Bits werden pro Subdomain kodiert)
- `window.name`, Favicon-Cache

Beim erneuten Besuch werden alle Speicherorte geprüft; ist einer davon erhalten geblieben, werden die anderen wiederhergestellt.

### Browser-Speicher {#browser-storage}
- `localStorage`: bleibt bestehen, bis es explizit gelöscht wird, 5-10 MB pro Origin
- `sessionStorage`: pro Tab, wird beim Schließen gelöscht
- `IndexedDB`: strukturiert, große Kapazität
- Cache API / Service Worker: bleiben über Sitzungen hinweg erhalten

### Cookie-Syncing {#cookie-syncing}
Werbenetzwerke synchronisieren Identifikatoren über Redirect-Ketten. ITP (Safari) und ETP (Firefox) schränken dies schrittweise ein.

## Fallstricke {#gotchas}
- Anti-Detect-Browser können die meisten Fingerprints verschleiern, eine konsistente Verschleierung über alle Vektoren hinweg ist jedoch äußerst schwierig
- Canvas-Rauschen, das sich bei jedem Aufruf ändert, ist verdächtiger als ein konsistenter Fingerprint
- Private- bzw. Inkognitomodus verhindert Fingerprinting NICHT, er löscht lediglich den Speicher
- Mehrere Fingerprint-Vektoren werden kombiniert: Wer einen blockiert, lässt Dutzende andere offen
- Der Tor Browser zielt gezielt auf die Einheitlichkeit des Fingerprints ab (alle Nutzer sehen identisch aus)

## Siehe auch {#see-also}
- [[anti-fraud-behavioral-analysis]] - Verhaltensmuster als Ergänzung zu Fingerprints
- [[tls-fingerprinting-and-network-identifiers]] - IP-Analyse, Geolokalisierung
- [[osint-and-reconnaissance]] - Nutzung von Fingerprint-Daten für Ermittlungen
- [[web-application-security-fundamentals]] - CSP, Cookies, Speicher
