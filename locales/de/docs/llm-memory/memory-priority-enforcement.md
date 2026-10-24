---
level: 3
source_sha256: 65091d694c862a03524c0eee6423a6c58f9eeaa2171460b9cf7e6d1a01aa424a
translation: machine
translated_at: '2026-10-24'
---
# Durchsetzung der Speicherpriorität {#memory-priority-enforcement}

Muster zur Aufteilung des Agentenspeichers in eine Stufe, die immer geladen wird (kritisch), und eine Stufe, die bei Bedarf geladen wird (Referenz), ergänzt um mechanische Durchsetzung der wichtigsten Regeln. Konvergenz von 8 unabhängigen Domänen auf dasselbe Prinzip.

## Kernprinzip {#core-principle}

Wenn das Vergessen einer Regel irreversible Folgen hat → immer laden.  
Alles andere → bei Bedarf laden.

Dies ist keine Performance-Optimierung, sondern eine Sicherheitseigenschaft: Kritischer Kontext muss Kontextkompaktierung, lange Sitzungen und nachlassende Aufmerksamkeit überstehen.

## Kriterien für „immer laden“ vs. „bei Bedarf“ {#always-vs-on-demand-criteria}

**Immer laden** (es genügt eines der folgenden Kriterien):
1. **Irreversible Folgen** – Vergessen führt zu Datenverlust, finanziellem Schaden, Produktionsausfall oder Sicherheitsvorfall
2. **Sitzungsübergreifende Invarianten** – Regeln, die unabhängig von der Aufgabe nie verletzt werden dürfen („niemals ohne Bestätigung löschen“, „niemals eine Produktions-GPU verwenden, ohne die Zuteilung zu prüfen“)
3. **Benutzerprofil / Präferenzen** – Kommunikationsstil, Expertise-Niveau, Werkzeugpräferenzen

**Bei Bedarf** (laden, sobald das Thema relevant wird):
- Details aktiver Projekte (werden geladen, wenn an diesem Projekt gearbeitet wird)
- Referenzmaterial und Methodiken
- Historische Informationen und frühere Vorfälle
- Spezifische Werkzeugintegrationen, die nicht im Tagesgeschäft verwendet werden

## Boeing-Regel – „Immer laden“ kurz halten {#boeing-rule-keep-always-load-short}

Luftfahrt-„Memory Items“ (Notverfahren, die aus dem Gedächtnis ausgeführt werden, ohne Checkliste):
- Typisch: 3–4 Punkte pro Notverfahren
- Maximum: ca. 10 Punkte (gilt als hoch)
- Über 10: Checklisten-Ermüdung → kritische Punkte werden unter Stress vergessen

**Für Agentenspeicher:** Der Abschnitt „immer laden“ sollte höchstens 10–15 Einträge umfassen. Darüber fallen wichtige Punkte in die Zone „Lost in the Middle“.

**Lost in the Middle (Liu et al. 2023, arxiv 2307.03172):** Die Leistung von LLMs folgt einer U-förmigen Kurve in Abhängigkeit von der Position im Kontext. Elemente am Anfang oder Ende erhalten die höchste Aufmerksamkeit, Elemente in der Mitte werden deutlich schwächer. Bei 36 Einträgen für „immer laden“ belegen kritische Regeln im langen Kontext die Plätze 5–35, also genau den geschwächten Bereich.

## IAEA-Zwei-Schichten-Prinzip {#iaea-two-layer-principle}

Aus dem Defense-in-Depth-Konzept von IAEA INSAG-10: Kritische Sicherheitsbarrieren müssen unabhängig und redundant sein. Die Durchsetzung kritischen Verhaltens über eine einzige Schicht (eine Regel) scheitert bei gemeinsamer Ursache (Kontextdruck, Kompaktierung, Ablenkung).

**Umsetzung:**
- Regel in CLAUDE.md/Speicher (beschreibt WARUM und WIE)
- Mechanische Durchsetzung durch Hook/Skript (wird unabhängig vom Kontextzustand ausgeführt)

**Beispiele funktionierender Paare:**
```text
Documentation integrity:
  Rule → "validate file references"
  Hook → SessionStart → validate_config.py (runs every session, blocks on drift)

Handoff reminder:
  Rule → "write handoff before ending long sessions"
  Hook → Stop → remind_handoff.py (blocks session end if no recent handoff)

Supply chain defense:
  Rule → "delay fresh packages"
  Enforcement → .npmrc min-release-age=7 (mechanically applied to every install)
```

**Prüfung beim Hinzufügen einer neuen kritischen Regel:** „Kann diese Regel umgangen werden, indem man vergisst, den Speicher zu lesen?“  
Falls ja → sie braucht einen Hook, nicht nur eine Regel.

## MemGPT-Zwei-Stufen-Architektur {#memgpt-two-tier-architecture}

```text
Core memory    ← in-context, fixed-size, agent can read/write via tool calls
               ← User profile, current task state, active invariants

Archival memory ← searchable database, paged in on-demand
                ← Historical context, past projects, reference materials
```

**Wesentliche Eigenschaft:** Der Agent entscheidet explizit, was aus dem Archiv in den Kernspeicher geladen wird. Dadurch bleibt der Kernspeicher klein und fokussiert, während die vollständige Historie erhalten bleibt.

**Für dateibasierte Systeme:**  
Abschnitt `MEMORY.md Always Load` = Kernspeicher  
Abschnitt `MEMORY.md On Demand` = Archivindex  
Die tatsächlichen Dateien für den bedarfsabhängigen Abruf = Archivspeicher

## Tabelle zur Domänenkonvergenz {#domain-convergence-table}

| Domäne | Kritisch / immer | Referenz / bei Bedarf | Durchsetzungsmechanismus |
|--------|------------------|-----------------------|--------------------------|
| LLM-Kontext (Liu 2023) | Anfang / Ende des Kontexts | Mitte (Aufmerksamkeit nimmt ab) | Position im Prompt |
| MemGPT | Kernspeicher (fest) | Archiv (ausgelagert) | Tool-Aufrufe zum Nachladen |
| Luftfahrt | Memory Items (3–10) | Checklisten (dokumentiert) | Training + Wiederholung |
| Neurowissenschaft | Prozedurales Gedächtnis (Striatum) | Episodisch (Hippocampus) | Neuronale Architektur |
| Kognitionspsychologie | Arbeitsgedächtnis (4±1 Chunks) | Langzeitgedächtnis (unbegrenzt) | Aufmerksamkeit / Wiederholung |
| Nukleare Sicherheit (INSAG-10) | 5-stufige Schutzbarrieren | Verfahren / Handbücher | Physische Redundanz |
| Linux-Syslog | EMERG/ALERT → Konsole | DEBUG → Ringpuffer | `console_loglevel` |
| Kubernetes | Admission-Webhook-Richtlinien | API-Server-Logs | Webhook-Abfangung |

Alle 8 Domänen konvergieren auf: **kleine kritische Menge + große Referenzmenge + mechanische Durchsetzung für die kritische Menge.**

## Verwaltung veralteter Speicherinhalte {#memory-staleness-management}

Speichereinträge sollten ein Feld `created: YYYY-MM-DD` enthalten. Veralterung nach Typ:

| Typ | Veraltet nach | Prüfung bei Verwendung |
|-----|---------------|------------------------|
| `project` | 30 Tage | Vor Verwendung prüfen, wenn älter |
| `reference` (IPs, Pfade, Ports) | 7 Tage | Bei infrastrukturbezogenen Einträgen immer prüfen |
| `feedback` | Stabil (Benutzerpräferenzen ändern sich selten) | Niedrige Priorität |
| `user` | Sehr stabil | Nur prüfen, wenn ein größerer Kontextwechsel vermutet wird |

## Muster zur automatischen Speicherextraktion {#automatic-memory-extraction-pattern}

Nach Sitzungen in den Speicher übernehmen:
1. **Fähigkeiten** – neu entdeckte Workflows, Werkzeuge, Integrationen
2. **Korrekturen** – vom Benutzer korrigierte Vorgehensweisen (→ feedback-Speicher)
2. **Berechtigungen** – neu erlaubte Befehle (→ Einstellungen)
4. **Fehler-Fix-Paare** – Symptom → Ursache → Lösung (→ Stolperfallen)
5. **Entscheidungen** – Architekturentscheidungen mit Begründung (→ DECISIONS.md oder Speicher)

Zur Sortierung getaggt: `[DECISION]`, `[GOTCHA]`, `[REUSE]`, `[DEFER]`

## Stolperfallen {#gotchas}

- **Problem:** Der Abschnitt „immer laden“ wächst unbegrenzt, weil neue Regeln hinzugefügt werden, ohne alte zu entfernen. → **Lösung:** Boeing-Regel bei jeder Überprüfung anwenden: Überschreitet der Abschnitt 15 Einträge, eine Sichtung nach dem Kriterium irreversibler Folgen durchführen. Die meisten „nett zu wissen“-Punkte gehören in die bedarfsabhängige Stufe.
- **Problem:** Eine Regel im Speicher verhindert eine Aktion zu Sitzungsbeginn, wird aber nach einer Kontextkompaktierung mitten in der Sitzung vergessen. → **Lösung:** Für jede Regel, die über die gesamte Sitzung gelten muss (z. B. „Produktion nicht ändern“), einen Hook erstellen, der bei jedem relevanten Tool-Aufruf prüft – nicht nur zu Sitzungsbeginn.
- **Problem:** Der bedarfsabhängige Speicher wird zu einem unstrukturierten Sammelsurium, wodurch das Wiederfinden unzuverlässig wird. → **Lösung:** Wiki-Links `[[filename]]` verwenden, um einen navigierbaren Graphen aufzubauen. Speicherinhalte zu Projekt X sollten auf die Infrastruktur, auf der es läuft, die verwendeten Werkzeuge und die angewandte Methodik verlinken.
- **Problem:** Vor Jahren angelegte Speichereinträge verweisen auf Dateipfade, Server-IPs oder Ports, die nicht mehr existieren. → **Lösung:** Ein SessionStart-Hook (z. B. `validate_config.py`) durchsucht den Speicher nach absoluten Pfaden und prüft deren Existenz. Abweichungen werden gemeldet, bevor die Sitzung auf veraltete Daten zugreift.

## Siehe auch {#see-also}

- [[context-window-management]]
- [[memory-architectures]]
- [[session-persistence]]
- [[knowledge-graph-memory]]
