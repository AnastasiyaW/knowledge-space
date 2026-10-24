---
title: "Deepfake- und Dokumentenforensik"
category: concepts
tags: [security, deepfake, forensics, image-analysis, anti-fraud, document-forgery]
level: 3
source_sha256: 3fdcb85f11f638a8ffb08da5f8e9f07018cabf6973eadbc1017571912511bda5
translation: machine
translated_at: '2026-10-24'
---
# Deepfake- und Dokumentenforensik {#deepfake-and-document-forensics}

Erkennung und Analyse gefälschter Inhalte: Deepfake-Video- und Audiotechnologie sowie Erkennungsmethoden, Techniken zur Dokumentenfälschung und deren Verifikation, Bildforensik (ELA, Perceptual Hashing, Klon-Erkennung) und die Analyse von E-Mail-Spoofing.

## Wichtige Fakten {#key-facts}
- Moderne Stimmklonung erreicht eine Authentizität von ~99 % aus wenigen Minuten Audiomaterial
- Error Level Analysis (ELA) erkennt manipulierte Bildbereiche anhand von Unterschieden in den JPEG-Kompressionsartefakten
- Perceptual Hashing erzeugt für ähnliche Bilder ähnliche Hashwerte (anders als kryptografisches Hashing)
- SPF, DKIM und DMARC zusammen verhindern E-Mail-Spoofing; zur Verifikation sollten alle drei geprüft werden
- EXIF-Metadaten überstehen die meisten Bearbeitungen, werden aber von Social-Media-Plattformen entfernt
- Echtzeit-Deepfake-Tools für Videoanrufe sind inzwischen kommerziell verfügbar

## Deepfake-Technologie {#deepfake-technology}

### Komponenten {#components}
1. **Gesichtssynthese** - KI-Modelle, die auf das Gesicht des Ziels trainiert werden (hunderte bis tausende Fotos)
2. **Sprachsynthese** - Stimmklonung aus Audiosamples (~99 % Authentizität aus wenigen Minuten Audio)
3. **Lippensynchronisation** - Abgleich der generierten Sprache mit den Mundbewegungen im Gesicht

### Erkennungsmethoden {#detection-methods}
- **Blinzelanalyse** - frühe Deepfakes simulierten kein natürliches Blinzeln
- **Artefakte an Gesichtsgrenzen** - Übergänge, an denen das eingeblendete Gesicht auf den Hintergrund trifft
- **Audio-Video-Synchronisation** - subtile Abweichungen zwischen Mundbewegungen und Sprache
- **Frequenzanalyse** - von GANs erzeugte Bilder weisen erkennbare Muster im Frequenzbereich auf
- **Metadatenanalyse** - generierte Videos fehlen die erwarteten Kamerametadaten

## Dokumentenfälschung {#document-forgery}

### Arten gefälschter Dokumente {#types-of-forged-documents}
- Identitätsdokumente (Reisepässe, Führerscheine)
- Finanzdokumente (Kontoauszüge, Steuerbescheide, Rechnungen)
- Unternehmensdokumente (Arbeitsverträge, Gesellschaftsverträge)
- KYC-Verifikations-Selfies mit Dokumenten

### Verifikationsmethoden {#verification-methods}
- **EXIF-Metadaten** - Erstellungsdatum, verwendete Software, Geräteinformationen
- **Template-Abgleich** - Vergleich mit bekannten echten Dokumentvorlagen
- **Datenbankabgleich** - Prüfung der Dokumentnummern gegen amtliche Datenbanken
- **UV-/Hologramm-Prüfungen** - physische Verifikation gedruckter Dokumente

## Bildforensik {#image-forensics}

### Error Level Analysis (ELA) {#error-level-analysis-ela}
Erkennt manipulierte Bereiche durch die Analyse von JPEG-Kompressionsartefakten:
- Bild mit bekannter Qualitätsstufe erneut speichern
- Pixel für Pixel mit dem Original vergleichen
- Manipulierte Bereiche zeigen ein anderes Kompressionsniveau (heller in der ELA-Ausgabe)

### Perceptual Hashing {#perceptual-hashing}
- Bilder werden auf kompakte Hashwerte reduziert
- Ähnliche Bilder erzeugen ähnliche Hashes
- Einsatz zur Erkennung bekannter betrügerischer Dokumente und zum Abgleich mit Datenbanken
- Ermöglicht das Durchsuchen von Milliarden Bildern ohne manuelle Prüfung

### Weitere Techniken {#additional-techniques}
- **Klon-Erkennung** - Auffinden kopiert eingefügter Bereiche innerhalb eines Bildes
- **Licht- und Schattenanalyse** - inkonsistente Lichtquellen verraten Bildmontagen
- **Rauschanalyse** - verschiedene Kameras und Sensoren erzeugen unterschiedliche Rauschmuster
- **EXIF-Datenextraktion** - Kameramodell, GPS, Datum, Bearbeitungssoftware

## E-Mail-Forensik {#email-forensics}

### Header-Analyse {#header-analysis}
```sql
Received: chain   - traces routing path from sender to recipient
X-Originating-IP  - may reveal sender's real IP
Message-ID         - domain should match sender
Return-Path        - vs From: mismatches indicate spoofing
```

### Erkennung von Spoofing {#spoofing-detection}
- SPF-Eintrag auf Übereinstimmung prüfen (Envelope-Sender vs. Header-From)
- DKIM-Signatur kryptografisch verifizieren
- DMARC-Richtlinie auswerten
- Konsistenz der Header-Kette analysieren
- Auf Indikatoren für BEC (Business Email Compromise) prüfen

## Google-Betrugssignale {#google-anti-fraud-signals}
Googles einheitliches Vertrauensmodell über alle Dienste hinweg:
- Telefonnummer: Netzbetreibertyp (VoIP vs. Mobilfunk), Alter der Nummer, Wiederverwendungsmuster
- Geräte-Fingerprint und IP-Reputation bei der Registrierung
- Verhaltensmuster nach der Registrierung (menschliche vs. Bot-Aktivität)
- Kontoalter und Aktivitätshistorie

### Häufige Missbrauchsmuster {#common-abuse-patterns}
- Kontoverkauf (Wert steigt mit dem Alter, Telefonverifikation, Berechtigung für Dienste)
- Missbrauch von Cloud-Hosting (Testguthaben von 1 $ für Rechenressourcen)
- AdSense-Betrug (gefälschte Impressionen/Klicks)
- Gefälschte Unternehmen in Maps (SEO- und Reputationsmanipulation)

## Stolpersteine {#gotchas}
- Die Erkennung KI-generierter Inhalte ist ein Wettrüsten: Die Erkennungsmethoden haben zunehmend höhere Raten an falsch negativen Ergebnissen
- ELA funktioniert nur bei JPEG (verlustbehaftete Kompressionsartefakte), nicht auf PNG/BMP
- EXIF-Daten lassen sich trivial verändern oder entfernen; das Fehlen von EXIF ist kein Beweis für eine Fälschung
- Perceptual Hashing lässt sich durch ausreichend starke Bildtransformationen umgehen
- Ein bestandener SPF-Check verifiziert nur die Domain des Envelope-Senders, nicht den dem Benutzer angezeigten Header-From
- Deepfakes in Videoanrufen lassen sich erkennen, indem man die Person bittet, unerwartete Aktionen auszuführen (sich seitlich drehen, das Gesicht teilweise verdecken)

## Siehe auch {#see-also}
- [[osint-and-reconnaissance]] - Metadatenextraktion, Beweissicherung
- [[anti-fraud-behavioral-analysis]] - Verhaltensbasierte Betrugssignale
- [[browser-and-device-fingerprinting]] - Geräteidentifikation
- [[compliance-and-regulations]] - Datenschutz bei Ermittlungen
