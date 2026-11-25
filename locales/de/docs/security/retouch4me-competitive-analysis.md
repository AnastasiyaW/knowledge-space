---
level: 3
source_sha256: 9e6a9298ff4e77417bebac5f660e6308bc43dd89935d73e4bf5cf3d2e3e2a9ab
translation: machine
translated_at: '2026-10-24'
---
# Retouch4me: Wettbewerbsanalyse {#retouch4me-competitive-analysis}

Datum: 2026-04-03
Kontext: Architektur- und Produktanalyse für die Entwicklung eines konkurrierenden Retusche-Produkts.

---

## Unternehmensprofil {#company-profile}

- **Juristische Person:** RELU OU (Estland, Tallinn, Vesivarava 50-201)
- **Gegründet:** 28. März 2021. Registrierungsnummer: 16194437
- **Gründer:** Oleg Sharonov (auch Autor von 3D LUT Creator)
- **Hintergrund:** professioneller Entwickler, begann mit virtuellen Synthesizern. 8 Jahre Retusche-Erfahrung und 2 Jahre Studium des Deep Learning
- **Umsatz:** 2,63 Mio. EUR (2023), CAGR 19 %
- **Nutzer:** in mehr als 70 Ländern
- **Finanzierung:** bootstrapped (keine externen Finanzierungsrunden gefunden)

---

## Produktlinie {#product-line}

### 13 Foto-Plugins {#13-photo-plugins}

Jedes Plugin ist ein eigenes neuronales Netz, das für eine bestimmte Retusche-Aufgabe trainiert wurde:

| Plugin | Aufgabe | Preis |
|--------|---------|-------|
| Heal | Entfernen von Hautunreinheiten und Pickeln | $124 |
| Dodge & Burn | Automatisiertes High-End-D&B | $149 |
| Skin Tone | Korrektur des Hauttons, Vereinheitlichung | $124 |
| Mattifier | Entfernen von Glanz und Glanzlichtern auf der Haut | $124 |
| Portrait Volumes | Hinzufügen von Tiefe und Volumen | $124 |
| Skin Mask | Erzeugen einer Hautmaske (Gesicht/Körper) | $124 |
| Eye Vessels | Entfernen roter Äderchen im Auge | $124 (Bundle) |
| Eye Brilliance | Verstärken von Augenglanz | $124 (Bundle) |
| White Teeth | Zähne aufhellen | $124 |
| Fabric | Entfernen von Stofffalten | $124 |
| Clean Backdrop | Bereinigen des Hintergrunds | $149 |
| Stray Hair | Entfernen einzelner Haare | $124 |
| Dust | Entfernen von Staub und Partikeln | $124 |

**Kostenlos:** Panel (Photoshop-Panel), Frequency Separation, Glasses Glare Removal (in Apex), Face Make Lifting (in Apex).

### 2 Video-Plugins {#2-video-plugins}

| Plugin | Aufgabe | Preis | Standard |
|--------|---------|-------|----------|
| Dust OFX | Entfernen von Staub und Partikeln im Video | $349 | OFX |
| Color Match OFX | Farbangleichung im Video | n/a | OFX |

OFX-Unterstützung: DaVinci Resolve 18+, Nuke, VEGAS Pro, Natron, Assimilate SCRATCH.

### Apex – Cloud-All-in-One {#apex-cloud-all-in-one}

Strategisches Flaggschiff. Enthält alle Plugins; die Inferenz läuft auf den Servern von Retouch4me (nur Cloud).
Funktioniert eigenständig und als Plugin (Photoshop, Lightroom, Affinity Photo).
Keine lokale Hardwareanforderung.

### Arams – Eigenständige App {#arams-standalone-app}

Alle Plugins in einer App, Stapelverarbeitung (unbegrenzt), integrierte Dateiverwaltung, kein Photoshop erforderlich.

---

## Preise {#pricing}

### Unbefristete Lizenz (lokale Plugins) {#perpetual-license-local-plugins}
- $124–149 pro Plugin, lebenslang gültig
- Kostenlose Updates auf unbegrenzte Zeit
- 3 Aktivierungen (1 aktiv + 2 Reserve)
- An die Hardware gebunden

### Cloud-Credits (Panel / Apex) {#cloud-credits-panel-apex}

| Paket | Preis | Pro Foto |
|-------|-------|----------|
| Testversion | Kostenlos | 20 Retuschen |
| 100 Retuschen | $20 (einmalig) | $0,20 |
| Basic | $20/Monat | 200 ($0,10) |
| Pro | $35/Monat | 500 ($0,07) |
| Business | $90/Monat | 1500 ($0,06) |

1 Credit = 1 heruntergeladenes retuschiertes Foto (es können beliebig viele Werkzeuge angewendet werden).

---

## Technische Architektur {#technical-architecture}

### Inferenz-Engine {#inference-engine}

**Zentrale Erkenntnis: Retouch4me verwendet eine proprietäre Inferenz-Engine.**

Aus Interviews mit Oleg Sharonov: Mehrere ML-Trainingsframeworks wurden ausprobiert, aber keines war für den Desktop-Einsatz innerhalb von Photoshop geeignet. Daher wurde eine eigene Engine für volle Kontrolle entwickelt.

- **NICHT ONNX, NICHT TensorFlow, NICHT PyTorch** für die Inferenz
- Eigene Engine mit **OpenCL** zur GPU-Beschleunigung
- CPU-Inferenz über Intel OpenCL 1.1+
- Voraussetzung: GPU mit mindestens 4 GB VRAM oder Intel-CPU mit OpenCL

### Architektur der neuronalen Netze {#neural-network-architecture}

- **CNN (Convolutional Neural Networks)** – Kern
- **Encoder-Decoder-Architekturen**
- **Partielle Faltungen** – zum Inpainting beschädigter Bereiche
- **Perzeptuelle Verlustfunktionen** – Optimierung auf perzeptuelle Metriken (Merkmale vortrainierter Netze), nicht pixelweiser L2
- Jedes Plugin ist ein eigenes Netz, trainiert auf „Vorher/Nachher“-Paaren von professionellen Retuscheuren

### Modellgrößen {#model-sizes}

- Heal-Installer: ca. 35–41 MB (Windows), ca. 20 MB (macOS)
- **Modelle im Installer enthalten** – kein separater Download der Gewichte
- Deutet auf kompakte CNNs hin (einige Zehn MB pro Modul)
- Für OpenCL-Inferenz optimiert

### Verarbeitungsmodi {#processing-modes}

**Auf dem Gerät (lokal):**
- Eigene OpenCL-Engine
- GPU oder CPU
- Benötigt mindestens 4 GB VRAM
- Nach der Aktivierung vollständig offline nutzbar

**Cloud-Retusche (Panel/Apex):**
- Inferenz auf den Servern von Retouch4me
- Server: `retoucher.hz.labs.retouch4.me`
- REST-API mit Task-Endpunkten
- Keine lokale Hardwareanforderung

---

## Cloud-API {#cloud-api}

**Basis-URL:** `https://retoucher.hz.labs.retouch4.me/api/v1/`

Wichtige Endpunkte:

| Endpunkt | Methode | Beschreibung |
|----------|---------|--------------|
| `/info/limits` | GET | Dateilimits (Formate, Größe, Auflösung) |
| `/retoucher/getFile/{id}` | GET | Verarbeitete Datei abrufen |
| Task-Erstellung | POST | Retusche-Task anlegen |
| Task-Status | GET | Status des Tasks abfragen |

**Limits:** PNG/JPG/JPEG, maximal 100 MB, maximal 250 Megapixel.

**Professioneller Modus:** `mode=professional`, `layers=1` → Der Server liefert ein ZIP-Archiv mit getrennten Ebenen zurück.

---

## Systemanforderungen {#system-requirements}

**Windows:** Win 7/10/11 x64, 6 GB RAM, CPU 1,2 GHz x64, GPU mit mindestens 4 GB VRAM und OpenCL ODER Intel-CPU mit OpenCL 1.1+. Empfohlen: RTX 3050 8 GB / RTX 4070 Ti 12 GB.

**macOS:** 10.14+ (10.15+ für neue Produkte), Mac ab Baujahr 2015 (Intel, M1–M4 nativ unterstützt).

---

## Lizenzierung und Schutz {#licensing-and-protection}

### Lizenzmodell {#license-model}
- 1 aktiver Schlüssel + 2 Reserveschlüssel (3 Aktivierungen insgesamt)
- An die Hardwarekonfiguration gebunden
- Maximal 2 gleichzeitig aktive Geräte
- Eine Hardwareänderung macht den Schlüssel ungültig; dann ist der Reserveschlüssel zu verwenden
- Zusätzlicher Schlüssel: nur über den Support, frühestens 6 Monate nach dem Kauf

### Mechanismus {#mechanism}
- Hardwaregebundene Aktivierung
- **Keine Selbstdeaktivierung** (kein Nutzer-Dashboard)
- Alte Aktivierungen können technisch nicht entfernt werden
- Bei einem Laptopwechsel: Neue Aktivierung über den Support anfordern

### Lage bei Raubkopien {#anti-piracy-state}

Aus russischsprachigen Foren (diakov.net, 4pda.to):
- „Behandelte“ (geknackte) Versionen existieren, bei denen die Prüfung deaktiviert ist
- Retouch4me führt viele Abstürze auf Raubkopien zurück
- Raubkopierte Versionen destabilisieren mitunter legitime Plugins, die daneben installiert sind
- Norton-Antivirus markiert die Plugins gelegentlich (vermutlich wegen der Schutz-Verschleierung)

---

## Schwachstellen (Wettbewerbschancen) {#weaknesses-competitive-opportunities}

### Hauptschwächen {#primary-weaknesses}

1. **Preis:** $124–149 pro Plugin. Komplette Suite = $1500+. Hohe Hürde für Fotografen in aufstrebenden Märkten.

2. **Fragmentierung:** 13 separate Plugins. Keine einheitliche Gesamtlösung (Apex ist nur in der Cloud verfügbar, kein Offline-Modus).

3. **Lizenz-UX (größte Beschwerde):** Hardwarebindung ohne Selbstdeaktivierung. Nutzer verlieren Aktivierungen bei Hardwarewechsel. Support muss kontaktiert werden. 6 Monate Wartezeit für zusätzliche Schlüssel. Hauptbeschwerde auf Trustpilot.

4. **Minimale Nutzersteuerung:** Ein einziger Stärkeregler. Keine regionsspezifische Steuerung, keine Masken, Voreinstellungen oder Feinabstimmung.

5. **Nur OpenCL:** Keine CUDA-spezifischen Optimierungen, keine Metal-Shader. ONNX Runtime würde CUDA/DirectML/CoreML/OpenVINO abdecken.

6. **Kein SDK/keine Einbettung:** Nur als Plugin oder API. Keine Möglichkeit, in eine eigene Pipeline eingebettet zu werden.

7. **Apex-Cloud-Bindung:** Apex funktioniert AUSSCHLIESSLICH über die Cloud, ohne Offline-Modus.

### Chancen in der technischen Architektur {#technical-architecture-opportunities}

| Ansatz von Retouch4me | Bessere Alternative |
|-----------------------|---------------------|
| Proprietäre OpenCL-Engine (erheblicher Aufwand) | ONNX Runtime (CUDA/DirectML/CoreML/OpenVINO) – schnellere Entwicklung und breitere Kompatibilität |
| Photoshop-Filter im selben Prozess | Out-of-Process-Daemon mit IPC (Absturzisolation) |
| 13 separate Plugins | Ein einziges Produkt mit abschaltbaren Modulen |
| Kein Nutzer-Dashboard | Portal zur Lizenz-Selbstverwaltung |

---

## Zusammenfassung der Wettbewerbspositionierung {#competitive-positioning-summary}

**Stärken von Retouch4me:** über 8 Jahre Marktpräsenz, Trainingsdaten von professionellen Retuscheuren, bewährte Qualität, unbefristete Lizenzen, von Fotografen bevorzugt, Expansion in den Videobereich.

**Ihre Schwachstellen (unsere Chance):**
1. Preis + Fragmentierung → ein einziges Produkt zu einem niedrigeren Preis
2. Lizenz-UX → Selbstverwaltungs-Dashboard, flexible Übertragung
3. Keine Feinabstimmung → Stärke pro Region, Ebenenmasken, Voreinstellungen
4. Kein SDK → einbettbare Bibliothek für eigene Pipelines
5. Nur OpenCL → ONNX Runtime für bessere GPU-Abdeckung
6. Reine Cloud bei Apex → einheitliche lokale und Cloud-Nutzung mit Offline-Fallback

---

## Stolperfallen {#gotchas}

- **Hardwaregebundene Aktivierung ohne Selbstdeaktivierung ist die größte UX-Beschwerde** auf Trustpilot. Das ist ein lösbares Problem (Implementierung eines Geräteverwaltungs-Dashboards) und ein starkes Unterscheidungsmerkmal.
- **Die OpenCL-Anforderung (mindestens 4 GB VRAM) begrenzt die Marktreichweite.** ONNX Runtime mit DirectML funktioniert auf jeder DX12-GPU (bis hin zu integrierten Grafikeinheiten bei einfacheren Modellen), und CoreML nutzt auf modernen Macs die Apple Neural Engine.
- **Raubkopien, die legitime Installationen destabilisieren,** deuten darauf hin, dass der Schutz mit dem Host-Prozess auf eine Weise interagiert, die Kollateralschäden verursacht. Eine saubere Out-of-Process-Architektur vermeidet das.
- **Norton-Markierungen der Plugins** belasten den Kundensupport. Bekannte Verschleierungstechniken lösen Heuristiken von Virenscannern aus. Es gilt, Schutzstärke und Rate falsch positiver Treffer abzuwägen.
- **„Kein Dashboard“ ist kein Sicherheitsmerkmal**, sondern ein UX-Versagen. Selbstdeaktivierung mit Geräte-Limits (z. B. 2 gleichzeitig, 5 Übertragungen pro Jahr) ist eindeutig besser: Sie senkt die Supportlast, verbessert die Zufriedenheit und schwächt den Schutz nicht spürbar.
- **Im Installer enthaltene Modelle (ca. 35–41 MB)** bedeuten, dass die Update-Häufigkeit durch vollständige Neuinstallationen begrenzt wird. Eine separate Modell-Download-Infrastruktur ermöglicht Modell-Updates ohne App-Updates.
