---
level: 3
source_sha256: b8016176a882d5fff6bfe47510a31f5f2d3542fdf0dce56d3a7545b5c5da9d58
translation: machine
translated_at: '2026-10-24'
---
# Rechtlicher Rahmen gegen Piraterie: DMCA, Geschäftsgeheimnisse, EULA-Design {#anti-piracy-legal-framework-dmca-trade-secrets-eula-design}

Datum: 2026-04-03
Kontext: Desktop-ML-Inferenzprodukt. Rechtliche Mechanismen zum Schutz von Software und Modellgewichten vor unbefugter Nutzung und Verbreitung.

---

## Schutz von ML-Modellen als Geschäftsgeheimnisse {#trade-secrets-protection-for-ml-models}

### Was als Geschäftsgeheimnis qualifiziert {#what-qualifies-as-trade-secret}

Neuronale Netzwerkgewichte sind als Geschäftsgeheimnisse schutzfähig, wenn:
1. Der wirtschaftliche Wert aus der Geheimhaltung entsteht (Wettbewerber würden vom Zugang profitieren)
2. Angemessene Maßnahmen zur Wahrung der Geheimhaltung getroffen wurden
3. Sie nicht öffentlich offengelegt wurden

**DTSA (Defend Trade Secrets Act, USA):** Bundesrechtlicher zivilrechtlicher Anspruch. Ermöglicht einstweilige Verfügungen sowie Schadensersatz bei Rechtsverletzung (Misappropriation).

**Was „angemessene Maßnahmen" in der Praxis bedeutet:**
- Verschlüsselung der Gewichte auf dem Datenträger und bei der Übertragung (AES-256-GCM)
- Zugriffsbeschränkung: serverseitiges Schlüsselmaterial, gerätegebundene Lizenzierung
- NDA für alle Mitarbeiter und Auftragnehmer mit Modellzugriff
- Kennzeichnung von Modelldateien und Dokumentation als „Proprietär – Vertraulich"
- Audit-Logs, die dokumentieren, wer auf Modelldateien zugegriffen hat

**Was NICHT zu tun ist:**
- Unverschlüsselte Gewichte im Anwendungspaket ausliefern (zerstört den Geschäftsgeheimnis-Anspruch)
- Unbegrenzten Offline-Zugriff ohne jede serverseitige Verifizierung erlauben
- Rohe Gewichtsdateien auch unter NDA ohne Verschlüsselung weitergeben

### ONNX/PyTorch-Format = keine urheberrechtsfähige Struktur {#onnxpytorch-format-not-copyrightable-structure}

Modellgewichte im ONNX-/SafeTensors-Format: Das Dateiformat ist offen, die konkreten trainierten Gewichtswerte sind jedoch als „Compilation" urheberrechtlich geschützt oder als Geschäftsgeheimnisse schutzfähig. Die Architektur (Graphtopologie) ist eine Idee und nicht urheberrechtsfähig. Die konkreten trainierten Werte sind Ausdruck.

---

## DMCA-Umgehungsschutz (17 U.S.C. § 1201) {#dmca-anti-circumvention-17-usc-1201}

### Was er abdeckt {#what-it-covers}

Verbietet die Umgehung von „technischen Schutzmaßnahmen" (Technological Protection Measures, TPMs), die den Zugang zu urheberrechtlich geschützten Werken kontrollieren.

**Anwendbar auf:**
- Verschlüsselung von Modellgewichten (die Gewichte = urheberrechtlich geschütztes Werk + TPM = Verschlüsselung)
- Lizenzprüfsysteme, die den Zugang zu Softwarefunktionen steuern
- DRM, das Aktivierungscodes schützt

**Kritische Voraussetzung:** Der umgangene Schutz muss tatsächlich den Zugang zu einem urheberrechtlich geschützten Werk steuern. Eine Lizenzprüfung, die true/false zurückgibt, aber Inhalte nicht kryptografisch sperrt, bietet ein schwächeres DMCA-Argument. Ein verschlüsseltes Modell, bei dem der Schlüssel = Funktion(Lizenz) ist, bietet ein starkes DMCA-Argument.

### Durchsetzbarkeit {#enforceability}

**Starke Fälle (Lizenz-als-Daten-Architektur):**
- Modellgewichte sind verschlüsselt, der Schlüssel wird aus einer gültigen Lizenz abgeleitet → Umgehung ist eindeutig erforderlich, um auf die urheberrechtlich geschützten Gewichte zuzugreifen
- ONNX Runtime `CreateSessionFromArray` mit Entschlüsselung → die TPM steuert unmittelbar das urheberrechtlich geschützte Werk

**Schwache Fälle (boolesches Gate):**
- `if (isLicensed()) { run(); }` → Patchen der Prüfung ist ein Graubereich (einige Gerichte vertreten, dass dies keine „Zugangskontrolle" für das zugrunde liegende Werk darstellt)

**Praktische Durchsetzung:**
1. DMCA-Takedown an den Hosting-Provider (GitHub, Spiegelserver von RuTracker) – schnell, erfordert minimale Beweise
2. Unterlassungsaufforderung (Cease-and-Desist) an identifizierte Personen – wirksam bei kommerzieller Piraterie
3. Zivilklage – teuer, nur bei erheblicher kommerzieller Rechtsverletzung

### DMCA für digitale Wasserzeichen {#dmca-for-digital-watermarks}

§ 1202: Verbietet das Entfernen oder Verändern von „Copyright Management Information" (CMI). In Ausgabebildern eingebettete Wasserzeichen sind CMI, wenn sie den Rechteinhaber und die Lizenz identifizieren.

**Wasserzeichen-Payload zur DMCA-Unterstützung:**
```text
bits 0-31: license_id hash (ties output to specific license)
bits 32-47: timestamp (days since epoch)
bits 48-55: app version
bits 56-63: CRC-8
```

Mit dieser Payload ist die Erkennung der Entfernung von Wasserzeichen möglich. Tauchen piratierte Ausgaben ohne Wasserzeichen auf → Anspruch nach §1202 wegen vorsätzlicher Entfernung.

---

## EULA-Design für Anti-Piraterie-Maßnahmen {#eula-design-for-anti-piracy-measures}

### Verpflichtende Offenlegungen {#mandatory-disclosures}

Fernverwaltung und Kill-Switch erfordern eine Offenlegung in der EULA, um rechtlich haltbar zu sein:

```text
LICENSE COMPLIANCE AND REMOTE MANAGEMENT

The Software periodically communicates with our servers to:
(a) Verify your license status and activation count;
(b) Transmit a device identifier (hardware fingerprint) for license
    validation purposes;
(c) Deliver configuration updates and security parameters.

In cases of confirmed license violation, we may progressively limit
application functionality. Full functionality is restored immediately
upon valid license activation. We will not damage or delete your
personal data as part of any compliance action.

By installing or using the Software, you consent to this communication.
```

**Sony-Rootkit-Präzedenzfall (2005):** Installation eines DRM-Rootkits ohne Offenlegung → Vergleich mit 7,50 $ pro Disc sowie verpflichtende Rückrufaktion. Technische Schutzmaßnahmen immer offenlegen.

**WGA-Präzedenzfall (2006):** Nicht offengelegtes tägliches Phone-Home → Sammelklage → Microsoft entfernte es. Phone-Home-Verhalten muss offengelegt werden.

### Clickwrap vs. Browsewrap {#clickwrap-vs-browse-wrap}

**Clickwrap (für Durchsetzbarkeit erforderlich):** Nutzer aktiviert aktiv ein „Ich stimme zu"-Kontrollkästchen und muss die EULA durchscrollen. In den meisten US-Gerichten durchsetzbar.

**Browsewrap („Durch die Nutzung dieser Software stimmen Sie zu …"):** schwach, gegenüber Verbrauchern häufig nicht durchsetzbar. Nur als Ergänzung zu Clickwrap verwenden.

**Umsetzung:** EULA beim ersten Start mit einer eindeutigen Schaltfläche „Ich akzeptiere" anzeigen. Zeitstempel der Zustimmung und Hash-Wert der EULA-Version im persistenten Speicher ablegen. Bei Aktualisierung erneut anzeigen, falls sich die EULA geändert hat.

### Rechtsordnungsspezifische Überlegungen {#jurisdiction-considerations}

**EU – Verbraucherschutz:**
- Richtlinie über digitale Inhalte (2019/770), Art. 14 Abs. 2: erlaubt die Kündigung bei Vertragsverletzung mit „angemessener" Frist
- Richtlinie über unlautere Geschäftspraktiken: nicht offengelegte Verschlechterung = potenziell unlautere Praxis
- DSGVO: Geräte-Fingerprint + Nutzungsdaten = personenbezogene Daten → Datenschutzerklärung + Rechtsgrundlage (berechtigtes Interesse)

**Russland/GUS – eingeschränkte Durchsetzbarkeit:**
- Durchsetzung von Softwarelizenzen gegenüber Einzelnutzern praktisch begrenzt
- Durchsetzung im Unternehmens- und Geschäftsbereich über russische Gerichte möglich
- Praktische Strategie: gestufte Reaktion (Qualität reduzieren) statt rechtlicher Schritte

**China – eigenes Durchsetzungsregime:**
- Urheberrecht existiert, aber die praktische Durchsetzung für ausländische Softwareunternehmen ist schwierig
- China-spezifische Preisgestaltung und lokale Zahlungsmethoden in Betracht ziehen, um den wirtschaftlichen Anreiz zur Piraterie zu verringern
- Vertriebskanäle wie Weibo/WeChat sind schwerer zu überwachen als das offene Web

---

## Urheberrechtliche Registrierung {#copyright-registration}

Urheberrecht an Software und Modellgewichten registrieren, um Folgendes zu begründen:
- Gesetzlichen Schadensersatz (750–30.000 $ pro Werk; bis zu 150.000 $ bei vorsätzlicher Verletzung)
- Anspruch auf Anwaltskosten
- Vermutung der Rechtsgültigkeit

**Was zu registrieren ist:**
- Software-Binärdatei (als „Computerprogramm")
- Modellgewichte (als „Compilation" oder „architektonisches Werk")
- Registrierung vor der Rechtsverletzung, um Anspruch auf gesetzlichen Schadensersatz zu haben

**Gebühr für die US-Urheberrechtsregistrierung:** 45–65 $ pro Werk online. Innerhalb von 3 Monaten nach Veröffentlichung einreichen, um die volle Schadensersatzoption zu erhalten.

---

## Beweissicherung für die Durchsetzung {#evidence-preservation-for-enforcement}

### Beweiskette bei Wasserzeichen {#watermark-chain-of-custody}

```python
# When pirated output detected: preserve evidence
evidence_record = {
    'detected_at': datetime.utcnow().isoformat(),
    'image_hash': sha256(image_bytes).hex(),
    'watermark_payload': decoded_payload,
    'license_id': lookup_license(decoded_payload['license_id_hash']),
    'original_activation': get_activation_record(license_id),
    'detection_confidence': confidence,
    'detection_threshold': 0.85,
    'detector_version': '2.1.0',
    'source_url': piracy_url,
}
# Store immutably with timestamp server signature
```

Anforderungen an die Beweiskette für Rechtsstreitigkeiten:
- Zeitgestempelte Server-Logs (append-only Log-Speicher verwenden)
- Kryptografisch signierte Erkennungsprotokolle
- Sicherung der ursprünglichen rechtsverletzenden URLs/Inhalte (Screenshots + HTTP-Antwortmitschnitte)
- Aktivierungsprotokolle, die license_id mit dem Kauf verknüpfen

### Vorbereitung auf ein BSA-Audit {#bsa-audit-preparation}

Für die Durchsetzung bei kommerzieller bzw. Unternehmenspiraterie über die BSA:
1. Dokumentieren: Anzahl der Aktivierungen pro Lizenz, Geräte-Fingerprints der Aktivierungen, Daten
2. Beweise: Server-Logs, die zeigen, dass ein Gerät die lizenzierte Software nutzt → wasserzeichenmarkierte Ausgaben werden online gefunden
3. BSA-Einbindung: Die BSA hat von Mitgliedsunternehmen delegierte Befugnisse; kommerzielle Piraterie-Fälle dorthin verweisen

---

## Praktische Durchsetzungsstufen {#practical-enforcement-tiers}

| Verletzungsart | Reaktion | Mechanismus |
|----------------|----------|-------------|
| Private Nutzung durch Einzelne | Dulden oder gestuftes Abschalten | Kill-Switch Stufe 1–2 |
| Freiberufler mit raubkopierter Version (kommerziell) | DMCA-Takedown an den Ausgabe-Host + Kill-Switch | Wasserzeichenerkennung |
| Geschäftliche/Unternehmensnutzung | Weiterleitung an BSA-Audit + C&D-Schreiben | Anomalie bei der Lizenzanzahl |
| Weiterverbreiter gecrackter Versionen | DMCA-Takedown an den Host | URL-Überwachung |
| Crack-Entwickler (GitHub) | DMCA + C&D | GitHub-DMCA-Verfahren |

---

## Fallstricke {#gotchas}

- **Boolesches Gate ohne Verschlüsselung = schwacher DMCA-Anspruch.** Gerichte sind sich uneinig, ob das Patchen einer booleschen Lizenzprüfung eine „TPM" umgeht, die das urheberrechtlich geschützte Werk schützt. Lizenz-als-Daten (verschlüsselte Gewichte, entschlüsselt mit einem aus der Lizenz abgeleiteten Schlüssel) = eindeutige DMCA-TPM.
- **Kill-Switch ohne EULA-Offenlegung = unlautere Praxis (EU).** Eine Fernverschlechterung darf nicht ohne offengelegte Grundlage aktiviert werden. Das Sony-Rootkit ($7,50 pro Disc) und die WGA-Klage haben klare Präzedenzfälle geschaffen.
- **Ein Geschäftsgeheimnis erfordert tatsächliche Geheimhaltungsmaßnahmen.** Unverschlüsselte Gewichte im Anwendungspaket auszuliefern, zerstört den Status als Geschäftsgeheimnis. Verschlüsseln, beschränken und NDA abschließen ist Pflicht.
- **Gesetzlicher Schadensersatz erfordert rechtzeitige Registrierung.** Wird das Urheberrecht nach Entdeckung der Verletzung registriert, bleibt nur der tatsächliche Schaden (schwer nachweisbar). Vor der Auslieferung registrieren, um die Option des gesetzlichen Schadensersatzes zu haben.
- **Die chinesische Durchsetzung ist praktisch begrenzt.** Selbst gültige Urheberrechts- oder Geschäftsgeheimnisansprüche führen möglicherweise nicht zu einer Durchsetzungsmaßnahme. Preisstrategie und Wasserzeichen sind auf dem chinesischen Markt praktischer als rechtliche Durchsetzung.
- **Das Recht auf Löschung nach DSGVO gilt für Telemetrie.** Werden Geräte-Fingerprints zur Piraterieerkennung gehasht, muss ein Löschersuchen für dieses Gerät sämtliche Telemetrieeinträge löschen. Einen Löschendpunkt implementieren.

## Siehe auch {#see-also}
- [[remote-kill-switch]]
- [[watermarking-encrypted-models]]
- [[adobe-piracy-patterns]]
- [[piracy-economics]]
