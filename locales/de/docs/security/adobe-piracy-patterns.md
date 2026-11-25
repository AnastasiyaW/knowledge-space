---
level: 3
source_sha256: 1b62d63d7fca393a30ec7162cfe902fc736ceeffa5acdb3b77a5db4fb4d84f89
translation: machine
translated_at: '2026-10-24'
---
# Adobe-Piraterie-Muster: Angriffskategorien und Lehren für den ML-Schutz {#adobe-piracy-patterns-attack-categories-and-lessons-for-ml-protection}

Datum: 2026-04-03
Kontext: Defensive Sicherheitsforschung. Analyse von Adobe-Angriffsmustern, um einen besseren Schutz für ML-Produkte zu entwerfen.

---

## Architektur von Adobe Genuine Software (AGS) {#adobe-genuine-software-ags-architecture}

AGS = Hintergrunddienst, der die Echtheit installierter Adobe-Anwendungen prüft.

**Was geprüft wird:**
- Seriennummer / Lizenztyp
- Integrität der Binärdateien (Hashes der ausführbaren Dateien)
- Gültigkeit der Aktivierung über den Server

**Schwachstellen:**
- Eigenständiger Prozess - kann beendet oder blockiert werden
- Periodische statt kontinuierlicher Prüfungen
- Serverkommunikation durch die hosts-Datei blockierbar
- Anfällig für DLL-Substitution

**Speicherort der Lizenzdaten:** `<user>/AppData/Roaming/Adobe/`

**Wichtige Endpunkte:**
- `lcs-cops.adobe.io` - Feature Restricted Licensing
- `lm.licenses.adobe.com` - Lizenzvalidierung
- `activate.adobe.com` - Aktivierung

**Offline-Kulanzzeitraum:**
- Jahresabonnement: 99 Tage offline
- Monatsabonnement: 30 Tage
- **Kritische Schwachstelle:** Der 99-Tage-Kulanzzeitraum bedeutet, dass eine einzige erfolgreiche Aktivierung die App offline lange genug funktionsfähig hält, um dauerhafte Patches anzuwenden.

**Wirksamster Adobe-Schutz:** Firefly (KI-Funktionen) läuft serverseitig. Serverseitige Berechnungen können nicht raubkopiert werden. Das ist die architektonische Lehre.

---

## Angriffskategorie 1: DLL-Austausch {#attack-category-1-dll-replacement}

**Mechanismus:** Ersetzen von `amtlib.dll` (Lizenz-DLL) durch eine modifizierte Version, die bei allen Abfragen „Lizenz gültig“ zurückgibt.

**Angriffsweg von AMTEmu (2013-2019):**
1. `amtlib.dll` im App-Verzeichnis finden
2. Durch gepatchte DLL ersetzen
3. Die gepatchte DLL liefert bei allen Lizenzprüfungen `true`
4. Ergebnis: dauerhafte Aktivierung

**Warum es jahrelang funktionierte:**
- Eine einzige DLL war für die gesamte Lizenzlogik verantwortlich
- Boolesches Gate - die DLL gab true/false zurück, und ein dauerhaftes `true` umging alles
- Adobe hat die Architektur jahrelang nicht geändert

**Lehre:** Lizenzlogik NIEMALS in einem einzigen Modul bündeln. Prüfungen über Dutzende Stellen verteilen. Inline-Prüfungen statt Aufrufen einer separaten „Lizenz“-Funktion.

---

## Angriffskategorie 2: Manipulation der hosts-Datei {#attack-category-2-hosts-file-modification}

```markdown
127.0.0.1 lcs-cops.adobe.io
127.0.0.1 lm.licenses.adobe.com
127.0.0.1 activate.adobe.com
127.0.0.1 genuine.adobe.com
# ... dozens more Adobe domains
```

GitHub-Repositories pflegen aktualisierte Blockierlisten für Adobe-Hosts. Sie blockieren jegliche Serverkommunikation.

**Lehren:**
- Sich nicht allein auf DNS-Namen verlassen; Certificate Pinning verwenden
- Manipulation der hosts-Datei erkennen (DNS-Auflösung mit bekannter IP vergleichen)
- IP-Fallback zusätzlich zu DNS verwenden
- Steganografische Kommunikation nutzen (Abschaltsignal in CDN-Headern/Gewichten)
- Nicht übermäßig aggressiv vorgehen - Unternehmensfirewalls betreffen auch legitime Nutzer

---

## Angriffskategorie 3: Binary-Patching {#attack-category-3-binary-patching}

**Mechanismus:**
1. Binärdatei disassemblieren (IDA Pro, Ghidra, OllyDbg)
2. Bedingten Sprung nach der Lizenzprüfung finden
3. `JNZ` → `JMP` (unbedingt) ersetzen oder den Aufruf durch NOPs ersetzen

```asm
; Original
call license_check
test eax, eax
jnz  failure_path    ; jump if license invalid

; Patched
call license_check
test eax, eax
nop                  ; always falls through to success
nop
```

**Techniken:**
- NOP-Injection
- Umkehrung bedingter Sprünge
- Erzwingen des Vergleichsergebnisses
- IAT-Hooking (Ersetzen von Adressen in der Import Address Table)

**GenP (2019 bis heute):** Quelloffener AutoIt-Patcher, von der Community gepflegt. Er sucht bei jeder Aktualisierung nach charakteristischen Byte-Sequenzen der Lizenzprüfung.

Warum GenP trotz Updates weiterhin funktioniert: Die Struktur der Lizenzprüfungslogik ändert sich nicht grundlegend. `if (license_valid) { run } else { block }` - es bleibt bei einem einzigen Bit. GenP findet für jede Version neue Muster.

**Grundlegendes Problem des „booleschen Gates“:**
```c
if (isLicensed()) {
    enableFeatures();
}
```
Unabhängig von der Komplexität von isLicensed() ist das Ergebnis 1 Bit (wahr/falsch). Eine gepatchte Anweisung umgeht alles.

**Lehre: Die Lizenz muss DATEN sein, kein Boolescher Wert:**
- Der Lizenzschlüssel enthält Parameter, die für den Algorithmus erforderlich sind
- Ohne korrekten Schlüssel liefert der Algorithmus Unsinn statt einer Sperrmeldung
- Kein einzelnes `if (licensed)`, das gepatcht werden könnte
- Beispiel: HKDF-abgeleitete Modellgewichte ([[hkdf-personalized-weights]]), verschlüsseltes Modell ([[watermarking-encrypted-models]])

---

## Angriffskategorie 4: Gefälschter lokaler Lizenzserver {#attack-category-4-fake-local-license-server}

**Mechanismus:** Ein lokaler Server emuliert die Antworten des Adobe-Servers. Der Angreifer leitet den Verkehr über die hosts-Datei oder einen Proxy um und sendet gefälschte Antworten mit „Lizenz gültig“.

**Vorteil gegenüber Binary-Patching:** Es werden keine Dateien auf dem Datenträger verändert - das ist schwerer zu erkennen.

**Lehren:**
- Serverantworten müssen kryptografisch signiert sein (Ed25519)
- Gegenseitiges TLS (Mutual TLS)
- Die Antwort muss DATEN enthalten, die für die Berechnung benötigt werden (nicht nur „OK“)
- Selbst mit einem gefälschten Server kann ein Angreifer kein Ed25519-signiertes Schlüsselmaterial fälschen

---

## Angriffskategorie 5: Vorgepatchte Installer (Repacks) {#attack-category-5-pre-patched-installers-repacks}

**Mechanismus:** Veränderte Installer, auf die bereits Patches angewendet wurden. Creative Cloud ist nicht erforderlich.

**Warum sich das schwer verhindern lässt:** Kann die App ohne Serverbindung eigenständig laufen, sind Repacks unvermeidlich.

**Lehren:** Eine serverabhängige Architektur ist die einzige verlässliche Verteidigung gegen Repacks. Erfordert die Kernfunktionalität eine Live-Validierung am Server, die kryptografisches Material zurückliefert, sind Repacks nutzlos.

---

## Angriffskategorie 6: Ausnutzung des Kulanzzeitraums {#attack-category-6-grace-period-exploitation}

**Mechanismus:** Legal aktivieren → Kulanzzeitraum abwarten → Binärdatei patchen → dauerhaft weiterarbeiten (die gecachte Lizenz im Kulanzzeitraum funktioniert nach dem Patch offline unbegrenzt).

**Lehren für offline betriebene ML-Anwendungen:**
- Modell verschlüsselt; Entschlüsselungsschlüssel = Funktion aus Hardware-ID + Lizenz + Zeitstempeln
- Ohne serverseitige Verifikation lässt sich das Modell nicht entschlüsseln
- Selbst eine gecachte Lizenz erfordert eine periodische Neuableitung des Verschlüsselungsschlüssels

---

## Effektive Adobe-Schutzmaßnahmen (zum Übernehmen) {#adobes-effective-defenses-to-copy}

### Mehrere unabhängige Prüfpunkte {#multiple-independent-verification-points}
AGS (Hintergrunddienst) + Prüfungen in der Anwendung + Prüfungen der CC-Desktop-App. Selbst wenn einer umgangen wird, arbeiten die anderen weiter.

Für ML-Produkte: Prüfungen über den Code verteilen. Nicht ein einziges `if (licensed)`, sondern Dutzende Prüfpunkte in verschiedenen Modulen.

### Serverseitige Feature-Steuerung {#server-side-feature-gating}
Generative KI (Firefly) läuft AUSSCHLIESSLICH auf Adobe-Servern. Serverseitige Berechnungen lassen sich nicht raubkopieren. Sie erzeugen Generative Credits - serverseitige Abrechnung, die nicht gefälscht werden kann.

Für ML-Produkte: Vollständig serverseitig ist am besten, aber nicht immer praktikabel. Hybrid: Das Material zur Schlüsselentschlüsselung kommt vom Server, das gespeicherte Modell ist ohne dieses Material nutzlos.

### Laufende Updates brechen alte Cracks {#continuous-updates-breaking-old-cracks}
Jedes Update kann bestehende Patches unbrauchbar machen. Dadurch entstehen Zeitfenster, in denen die Raubkopie nicht funktioniert. Piraten müssen ihre Cracks ständig aktualisieren.

### Abonnement und Cloud-Funktionen als Mehrwert {#subscription-cloud-features-as-value-add}
Cloud-Speicher, Schriften, Bibliotheken und Zusammenarbeit funktionieren nur mit aktivem Abonnement. Eine Raubkopie ist eine verstümmelte Version. Der Umsatz wuchs von 4,2 Mrd. $ auf 21,5 Mrd. $ (2011-2024). 37 Mio. CC-Abonnenten.

### Abgestufte Reaktion statt harter Sperre {#graduated-response-vs-hard-block}
Adobes Reaktion auf GenP 3.x: Warnungen, Funktionseinschränkungen, gezielte Sperren. Nicht das Unbrauchbarmachen jeder gepatchten Installation (das würde Gelegenheitsnutzer vertreiben).

---

## Zu vermeidende Adobe-Fehlschläge {#adobes-ineffective-defenses-to-avoid}

### Eine einzige DLL für die gesamte Lizenzierung (amtlib.dll) {#single-dll-for-all-licensing-amtlibdll}
Ein Austausch bedeutet vollständige Umgehung. Inzwischen behoben, aber die Lehre bleibt: nie zentralisieren.

### Vorhersehbare DNS-Namen {#predictable-dns-names}
20 Domains in der hosts-Datei blockieren - erledigt. Stattdessen Pinning, steganografische Kanäle und IP-Fallback verwenden.

### Boolesches Gate überall {#boolean-gate-everywhere}
Muster: `if (isLicensed())` → durch NOP immer knackbar. Lösung: Die Lizenz ist eine Entschlüsselungszutat.

### Langer Offline-Kulanzzeitraum {#long-offline-grace-period}
99 Tage Kulanz = 99 Tage für Piraten, um dauerhafte Patches anzuwenden. Für ML-Produkte: periodische Neuableitung der Schlüssel aus Serverdaten.

---

## Angriffsfläche von Photoshop-Plugins {#photoshop-plugin-attack-surface}

**CEP-Erweiterungen (veraltet):** JavaScript-Minifizierung bietet keinen echten Schutz. Minifiziertes JS lässt sich leicht deobfuskieren.

**UXP-Plugins:** Der Code wird vor der Veröffentlichung im Marketplace von Adobe geprüft, aber die direkte Installation (`.ccx`) umgeht diese Prüfung.

**Lizenzprüfung bei Plugins:** In der Regel eine HTTP-Anfrage an den Server des Anbieters beim Start (ca. 0,3 s Prüfung). Leicht zu umgehen, indem ein lokaler Proxy ein gefälschtes „OK“ zurückgibt, wenn die Antwort nicht kryptografisch signiert ist.

**Lehre für Plugin-Entwickler:** Signierung der Antworten ist Pflicht. Enthält die Lizenzantwort nur `{"valid": true}`, emuliert ein lokaler Fake-Server dies trivial.

---

## Durchsetzungsstrategie {#enforcement-strategy}

**BSA (Business Software Alliance) + Adobe:**
- Prüfungsaufforderungen an Unternehmen
- Selbstauskunft erforderlich
- Vergleiche typischerweise 100.000 $ und mehr bei gewerblicher Nutzung
- Unternehmen muss Lizenzen erwerben, nicht lizenzierte Kopien vernichten und künftigen Prüfungen zustimmen

**Strategie der „Piraterie-Toleranz“:**
- Studierende nutzen Raubkopien → lernen → bekommen Jobs → Unternehmen kaufen Firmenlizenzen
- Einzelnutzer werden größtenteils in Ruhe gelassen (sie bleiben im Ökosystem)
- Gewerbliche und unternehmerische Piraterie wird konsequent verfolgt
- Weiterverbreiter erhalten Takedowns

**Zeitleiste:**
- 1990er: SafeDisc/SecuROM (in ca. einer Woche geknackt)
- 2013: Start des CC-Abonnements; die ersten Cracks erschienen 2 TAGE später
- 2019 ff.: AGS + Cloud-gesperrte Funktionen
- 2022: GenP-Mustererkennung in CC 23.x
- 2024 ff.: Neural Filters/Firefly auf Serverseite verlagert

---

## Vergleiche mit anderen Kreativsoftware-Ökosystemen {#creative-software-ecosystem-comparisons}

### Autodesk (AutoCAD, Maya) {#autodesk-autocad-maya}
- Online-Lizenzierung seit 2017 (Offline-Seriennummer abgeschafft)
- Eingebettete Berichterstattung: automatische Telemetrie zu Installationen mit eindeutigen IDs
- Seriendatenbank: Eingabe einer geleakten Seriennummer löst eine Prüfungseinladung aus
- Die Cracking-Gruppe MAGNiTUDE hat den Network Licensing Mechanism (NLM) gehackt - stellt einen gecrackten NLM bereit, der in vielen Repacks verwendet wird
- Lehre: Telemetrie mit eindeutigen Installations-IDs ermöglicht Erkennung, wirft aber Datenschutzfragen auf

### Maxon (Cinema 4D) {#maxon-cinema-4d}
- Prüft jede Projektdatei auf eine Signatur der offiziellen Quelle
- Fehlende oder ungültige Signatur blockiert die Datei
- Lehre: Lizenzinformationen IN die Ausgabedateien einbetten (Output-Wasserzeichen) - verarbeitete Dateien tragen eine Lizenz-ID

### Foundry (Nuke) {#foundry-nuke}
- RLM (Reprise License Manager): schwimmende Lizenz, gebunden an die Server-System-ID
- Gecrackte RLM-Server emulieren legitime Antworten - ein Standardangriff auf schwimmende Lizenzen
- Foundry ist für aggressive rechtliche Verfolgung bekannt: Drohungen mit Forderungen in Höhe von zehntausenden Dollar
- Lehre: Gegenseitiges TLS und Certificate Pinning schützen vor der Emulation gefälschter Server

### Topaz Photo AI {#topaz-photo-ai}
- Modelle gespeichert im Format `.tz`/`.tz2`, heruntergeladen von `models-bal.topazlabs.com`
- **Kritischer Fehler:** Modell-URLs sind ohne Authentifizierung erreichbar - rund 180 Modelle (über 100 GB) wurden abgegriffen und öffentlich auf GitHub gelistet
- Modelle unverschlüsselt - direkt nutzbar
- Bewertung: 2/10 für den Modellschutz. Einzige echte Verteidigung: Die Abhängigkeit von Cloud-Updates bricht gecrackte Versionen
- Sep. 2025: Umstellung auf reines Abonnement ($199/Jahr Standard, $599/Jahr Pro), was zu massivem Nutzerprotest führte

### Retouch4me {#retouch4me}
- Hardware-gebundene Schlüssel (3 Aktivierungen beim Kauf)
- Eigenständige Versionen mit lokalen Modellen - gecrackte Versionen auf Torrent-Seiten gefunden (Modelle erfolgreich extrahiert)
- Cloud-Version (2024): 8/10 Schutz - serverseitige Inferenz ist nicht raubkopierbar
- Strategie: Umstellung auf die Cloud als Reaktion auf Piraterie

### Luminar Neo (Skylum) {#luminar-neo-skylum}
- Kontobasiert, für die Aktivierung ist eine Internetverbindung zwingend erforderlich
- Die EULA gewährt ausdrücklich das Recht, die Lizenz „jederzeit, ohne Entschädigung und ohne vorherige Ankündigung einzuschränken, auszusetzen oder zu beenden“
- Massiv raubkopiert: gecrackte Versionen auf dutzenden Seiten, in nahezu aktuellen Versionen

## Russisch-/GUS-Piraterie-Ökosystem {#russiancis-piracy-ecosystem}

**RuTracker.org:** 15,5 Mio. aktive Nutzer, 2,59 Mio. Torrents, 6,2 Petabyte. In Russland, Großbritannien, Australien und weiteren Ländern gesperrt. Über VPN erreichbar.

**m0nkrus-Muster:** Übernimmt offizielle Installer → wendet GenP-Patches an → verpackt als eigenständige Version (ohne CC, ohne Adobe-ID). Neue Adobe-Versionen erscheinen innerhalb von Tagen bis Wochen. Automatisierter Workflow.

Lehren:
- Läuft eine App eigenständig ohne Serverbindung, sind Repacks unvermeidlich
- CDN-Modell + benutzerspezifisches Aktivierungs-Blob verhindert die Verbreitung von Repacks

## Stolpersteine {#gotchas}

- **Der Umsatz wuchs 5-fach trotz (oder wegen) Piraterie.** Adobes Strategie der „Piraterie-Toleranz“ ist bewusst gewählt - kostenlose Präsenz bei Studierenden schafft künftige zahlende Kunden. Nicht jede Piraterie ist reiner Verlust.
- **Selbst nach Architekturverbesserungen funktioniert GenP weiter.** Der von der Community gepflegte Mustererkenner passt sich neuen Binärmustern an. Nur serverseitige Funktionen sind wirklich piraterieresistent.
- **Der Kulanzzeitraum kann für die UX nicht null sein.** 99 Tage sind extrem; 7-30 Tage sind das richtige Gleichgewicht zwischen Nutzerfreundlichkeit (Reisen, Netzwerkprobleme) und Sicherheit.
- **Aggressiver Schutz vor Raubkopien schadet zuerst legitimen Nutzern.** Unternehmensfirewalls blockieren den Rückruf an den Server → Support-Tickets. Bei Netzwerkausfällen eine geordnete Funktionseinschränkung statt harter Sperren vorsehen.
- **Signierte Antworten sind nicht verhandelbar.** Der Fake-Server-Angriff (Kategorie 4) macht alle unsignierten Serverantworten wertlos. Die Ed25519-Verifikation muss Teil jeder Lizenzprüfung mit Serverkommunikation sein.
- **Der GenP-Quellcode wurde 2023 veröffentlicht.** Die Open-Source-Community pflegt weiterhin Forks. „Sicherheit durch Verschleierung“ von Binärmustern hat eine begrenzte Lebensdauer; die architektonische Verteidigung (Lizenz = Daten) ist dauerhaft.
- **Topaz-Modell-URL-Leck:** Ungeschütztes CDN = vollständige Modellextraktion ohne jede Umgehung der Lizenz. Modelle verschlüsseln UND Download-Anfragen authentifizieren - beides ist nötig.
- **Eigenständig lauffähige Apps werden geknackt.** Die eigenständige Retouch4me-Version wurde trotz Hardware-Bindung geknackt; die Cloud-Version blieb verschont. Bei ML-Apps mit On-Device-Inferenz muss die Verteidigungstiefe über reine Lizenzprüfungen hinausgehen.
