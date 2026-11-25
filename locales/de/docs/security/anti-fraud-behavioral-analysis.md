---
title: "Anti-Fraud-Verhaltensanalyse"
category: concepts
tags: [security, anti-fraud, behavioral-analysis, keystroke-dynamics, payment-fraud]
level: 3
source_sha256: 1c58d1d3acbe0da6f45754ed9496a17b281181e724844539851532c9c457a26a
translation: machine
translated_at: '2026-10-24'
---
# Anti-Fraud-Verhaltensanalyse {#anti-fraud-behavioral-analysis}

Verhaltenssignale, die von Anti-Fraud-Systemen genutzt werden: Mausbewegungsmuster, Tastendynamik, Analyse des Sitzungszeitverhaltens, Erkennung von Zahlungsbetrug (Velocity Checks, BIN-Analyse, 3D Secure) sowie Signale aus sozialen Bewertungen.

## Key Facts {#key-facts}
- Mausbewegungskurven folgen bei Menschen bezierähnlichen Pfaden; Bots verwenden lineare Interpolation
- Tastendynamik (Haltezeit, Flugzeit) kann einzelne Nutzer auch ohne Zugangsdaten identifizieren
- Velocity Checks erkennen Betrugsmuster: mehrere Karten vom selben Gerät, geografisch unmögliche Abfolgen
- Die BIN (die ersten 6-8 Ziffern) verrät die ausstellende Bank, den Kartentyp, das Land und den Status als Privat- oder Firmenkunde
- 3D Secure verschiebt die Betrugshaftung vom Händler auf den Kartenaussteller
- Anti-Fraud-Scoring kombiniert Hunderte von Signalen – eine Auffälligkeit in einer beliebigen Dimension erhöht das Risiko

## Mausbewegungsmuster {#mouse-movement-patterns}
- **Geschwindigkeit und Beschleunigung**: Bots bewegen sich mit konstanter Geschwindigkeit; Menschen zeigen Mikrokorrekturen
- **Klickpräzision**: Menschen verfehlen Ziele leicht; Bots klicken exakte Koordinaten
- **Bewegungskurven**: Menschliche Pfade sind bezierähnlich; Bots verwenden lineare Interpolation
- **Leerlaufmuster**: natürliche Pausen versus vollständiges Fehlen von Bewegung
- **Scrollverhalten**: Geschwindigkeit, Richtungswechsel, Momentum

## Tastendynamik (Biometrie) {#keystroke-dynamics-biometrics}
Individuelle Tippmuster pro Nutzer:
- **Haltezeit (Dwell Time)** – wie lange jede Taste gedrückt bleibt
- **Flugzeit (Flight Time)** – Zeit zwischen dem Loslassen einer Taste und dem Drücken der nächsten
- **Tippgeschwindigkeit** – WPM und Konsistenz
- **Fehlermuster** – Häufigkeit der Rücktaste, typische Korrekturen
- **Digraph-/Trigraph-Zeiten** – Zeit zwischen bestimmten Buchstabenpaaren

Diese Biometrie erstellt im Laufe der Zeit Profile und kann Nutzer auch ohne Login-Daten identifizieren.

## Analyse des Sitzungszeitverhaltens {#session-timing-analysis}
- Zeit zwischen Seitenaufrufen
- Verweildauer auf Formularen vor dem Absenden (zu schnell = Bot, zu langsam = manueller Betrug)
- Navigationsmuster (Lesen von Inhalten versus direktes Springen zur Kasse)
- Sitzungsdauer und Wiederkehrmuster

## Erkennung von Zahlungsbetrug {#payment-fraud-detection}

### BIN-Analyse (Bank Identification Number) {#bin-bank-identification-number-analysis}
Die ersten 6-8 Ziffern verraten:
- Ausstellende Bank und Land
- Kartentyp: Kredit-, Debit-, Prepaid- oder virtuelle Karte
- Kartenmarke und Stufe (Standard/Gold/Platinum)
- Privat- versus Firmenkunde

Anwendungen im Anti-Fraud: Abgleich, ob das Rechnungsland mit dem BIN-Land übereinstimmt, Erkennung virtueller/Prepaid-Karten (höheres Betrugsrisiko), Velocity Checks pro BIN-Bereich.

### Velocity Checks {#velocity-checks}
- Anzahl der Transaktionen pro Karte in einem Zeitfenster
- Anzahl unterschiedlicher Karten vom selben Gerät oder derselben IP
- Muster bei Transaktionsbeträgen (kleine Testbuchungen vor großen)
- Geografische Geschwindigkeit (Transaktionen aus weit entfernten Orten in unmöglich kurzer Zeit)

### AVS (Address Verification System) {#avs-address-verification-system}
Abgleich der Rechnungsadresse mit den Daten des Kartenausstellers: Übereinstimmung von Hausnummer und Postleitzahl, Übereinstimmung des Landes zwischen Rechnungsadresse und BIN.

### 3D Secure (3DS) {#3d-secure-3ds}
- Der Karteninhaber authentifiziert sich über das Portal der Bank (Verified by Visa, Mastercard SecureCode)
- Verschiebt die Betrugshaftung vom Händler auf den Aussteller
- 3DS2: risikobasierte Authentifizierung – reibungsloser Ablauf (frictionless) für risikoarme Transaktionen

### Indikatoren für virtuelle und Prepaid-Karten {#virtualprepaid-card-indicators}
- Prepaid-Karten verfügen über keine Verifizierung der Rechnungsadresse
- Virtuelle Karten werden häufig in großen Mengen erzeugt
- Bekannte BIN-Bereiche für Prepaid-/virtuelle Produkte
- Begrenzte Transaktionshistorie für die Risikobewertung

## Signale aus sozialen Bewertungen {#social-rating-signals}
- Kontoalter und Aktivitätsmuster
- Konsistenz des Social-Media-Profils
- E-Mail-Domain (kostenlos versus Firmendomain)
- Validierung der Telefonnummer (VoIP versus Mobilfunknetz, Alter der Nummer)
- Verhaltenskonsistenz mit der angegebenen Identität

## Stolperfallen {#gotchas}
- Maus- und Tastaturanalysen lassen sich durch ausgefeilte Replay-Werkzeuge umgehen, die menschenähnliches Rauschen einspielen
- Velocity Checks müssen legitime Szenarien berücksichtigen (Firmenkarten mit mehreren Nutzern, gemeinsam genutzte IPs)
- VPN- und Proxy-Nutzer sind nicht zwangsläufig betrügerisch – übermäßig aggressive IP-Bewertung erzeugt Fehlalarme (false positives)
- 3DS-Reibung senkt die Conversion-Rate – Händler wägen Sicherheit gegen Umsatzverluste ab
- Verhaltensbiometrie wirft datenschutzrechtliche Fragen nach der DSGVO auf (biometrische Daten gelten als besondere Kategorie)

## Siehe auch {#see-also}
- [[browser-and-device-fingerprinting]] - Signale auf Geräteebene per Fingerprint
- [[tls-fingerprinting-and-network-identifiers]] - IP- und Netzwerkanalyse
- [[deepfake-and-document-forensics]] - Erkennung von Dokumentenfälschungen
- [[compliance-and-regulations]] - DSGVO-Implikationen für Verhaltenstracking
