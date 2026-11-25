---
level: 3
source_sha256: 7f593b474a6c7994271c09232ee021bec791d459c427824f2f37a67e51ce8a7a
translation: machine
translated_at: '2026-10-24'
---
# Claude Mythos Leak und KI-Lieferkettensicherheit {#claude-mythos-leak-and-ai-supply-chain-security}

Der unbefugte Zugriff auf die Claude Mythos Preview (April 2026) gilt als Referenzfall für Schwachstellen in der KI-Lieferkette. Der Vorfall zeigte das Muster des „verketteten Lecks“, bei dem Metadaten eines Anbieters die gezielte Ausnutzung wertvoller Ressourcen eines anderen ermöglichen.

## Modellfähigkeiten und Cybersicherheitsfunktionen {#model-capabilities-and-cybersecurity-features}
Mythos ist ein Frontier-Modell mit emergenten Fähigkeiten im autonomen offensiven Sicherheitsbereich. Anders als frühere Generationen beruht seine Sicherheitskompetenz auf Emergenz und nicht auf spezialisiertem Fine-Tuning.

- **Zero-Day-Erkennung:** Autonome Identifikation von Schwachstellen in kompiliertem und Quellcode ohne Eingabeaufforderungen mit menschlicher Beteiligung (Human-in-the-Loop).
- **Exploit-Verkettung:** Fähigkeit, mehrere unterschiedliche Memory-Corruption-Primitive zu einem funktionsfähigen RCE-Exploit zu verketten.
- **CVE-2026-4747:** Ein bemerkenswerter Fund, bei dem es sich um eine 17 Jahre alte Remote-Code-Execution-Schwachstelle im FreeBSD-Kernel handelt. Der Fund wird öffentlich der modellgestützten Erkennung zugeschrieben.

## Verketteter Angriffsvektor über die Lieferkette {#chained-supply-chain-attack-vector}
Der Einbruch folgte einer mehrstufigen Aufklärungs- und Ausnutzungsstrategie, die sich gegen das Ökosystem von Drittanbietern richtete und nicht gegen den primären Perimeter des Labors.

### Vorhersagbare Ressourcenbenennung {#predictable-resource-naming}
Ein vorgelagerter Leak bei einem sekundären Trainingspartner legte interne URL-Konventionen offen. Dadurch konnten Angreifer den Speicherort unveröffentlichter Modellgewichte gezielt erraten. Im Ergebnis wurde die Logik von **Insecure Direct Object References (IDOR)** auf die Infrastruktur zur Modellbereitstellung übertragen.

### Übernahme von Zugangsdaten {#credential-hijacking}
Der Zugriff wurde über gemeinsam genutzte Konten von Auftragnehmern und API-Schlüssel abgeschlossen. Der Angriff erfolgte am Tag der Ankündigung der eingeschränkten Vorschau. Dies zeigt, dass das Zeitfenster einer „begrenzten Freigabe“ häufig unmittelbar für eine Kompromittierung der Lieferkette anfällig ist.

```json
{
  "incident_type": "Supply Chain Breach",
  "target_model": "Claude Mythos Preview",
  "vector_a": "Metadata leakage (URL conventions)",
  "vector_b": "Contractor credential theft",
  "attributed_cve": "CVE-2026-4747"
}
```

## Defensive Rahmenwerke: Project Glasswing {#defensive-frameworks-project-glasswing}
Project Glasswing ist ein Konsortium aus Infrastrukturanbietern (Amazon, Cisco, Microsoft, Linux Foundation), das Modelle in defensiven Kontexten testen soll.

- **Behebung von Schwachstellen:** Modelle werden eingesetzt, um kritische Infrastruktur-Codebasen vor der allgemeinen Freigabe zu scannen.
- **Telemetrie und Zuordnung:** Erfassung von „KI-entdeckten“ im Vergleich zu „menschlich entdeckten“ Fehlern, um die sich verschiebenden Vorteile in der defensiven Sicherheit zu messen.
- **Frühe Prüfergebnisse:** Während der ersten Glasswing-Prüfphase wurden etwa 40 wahrscheinliche CVEs identifiziert.

## Historischer Kontext von KI-Modell-Leaks {#historical-context-of-ai-model-leaks}
| Jahr | Modell | Primärer Fehlermodus |
|------|--------|----------------------|
| 2023 | LLaMA 1 | Leak durch Forscher (Verbreitung über 4chan) |
| 2024 | Miqu-1-70b | Clientseitiger Fehler durch einen übereifrigen Mitarbeiter |
| 2026 | Mythos | Verkettete Lieferkette (Metadaten + Zugangsdaten von Auftragnehmern) |

## Fallstricke {#gotchas}
- **Problem:** Verwendung vorhersagbarer Benennungskonventionen für Modell-API-Endpunkte (z. B. `lab-models-prod-mythos-v1`). → **Lösung:** Für interne Ressourcen zufällige UUIDs und kryptografisch gesalzene Hashes verwenden, um eine Entdeckung über Metadaten-Leaks zu verhindern.
- **Problem:** Verlass auf „begrenzte Vorschauen“ ohne isolierte VPCs für Partner. → **Lösung:** Architekturen für „Bring Your Own Model“ (BYOM) implementieren, bei denen die Gewichte in der Laborumgebung verbleiben und nur über eingeschränktes VPC-Peering zugänglich sind.
- **Problem:** Gemeinsam genutzte Zugangsdaten von Auftragnehmern für Fine-Tuning-Umgebungen. → **Lösung:** Hardwaregebundene mTLS-Token erzwingen und API-Schlüssel strikt auf bestimmte CIDR-Bereiche und Modellversionen beschränken.

## Siehe auch {#see-also}
- [[security-solutions-architecture]]
- [[authentication-and-authorization]]
- [[threat-modeling]]
- [[network-security-and-protocols]]
- [[secure-backend-development]]
