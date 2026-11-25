---
title: "Zweisprachige Nachrichtenrecherche und zeitliches Wissen"
category: architecture
tags: [news, research, knowledge-graph, provenance, llm-agents, mcp]
level: 3
source_sha256: f9565983a07b0c6052597b853943dd0345b9e1a3b317f603957b2d4b092f829f
translation: machine
translated_at: '2026-10-24'
---
# Zweisprachige Nachrichtenrecherche und zeitliches Wissen {#bilingual-news-research-and-temporal-knowledge}

## Vertragsumfang {#contract-scope}

Eine Nachricht ist für einen Agenten nur dann nützlich, wenn sie zu praktischem, versioniertem Wissen führt. Der Ziel-Workflow von Happyin verknüpft jedes geprüfte Element mit einem Projekt- oder Organisationsentwicklungsstrang und recherchiert anschließend, wie die geänderte Fähigkeit genutzt werden kann.

Das öffentliche Ergebnis ist englisch. Entdeckung und Verifikation sind zweisprachig: Englisch und vereinfachtes Chinesisch sind verpflichtende Recherchespuren. Community-Diskussionen werden als betriebliche Evidenz aufbewahrt, während Aussagen zu offizieller Identität, Releases, Kompatibilität und Support auf Quellen aus erster Hand gestützt bleiben.

Altes Wissen wird nicht allein deshalb gelöscht, weil ein neuerer Ansatz existiert. Es wird markiert, mit seinem Nachfolger verknüpft und getrennt von aktuellen Empfehlungen zurückgegeben.

## Laufzeitstatus {#runtime-status}

Diese Seite definiert den geprüften Ziel-Vertrag zum Stand 2026-08-26.

Umgesetzt:

- Öffentliche Nachrichten gemäß Schema 1.4 verlinken mit geprüften Projekt-/Unternehmenssträngen und unveränderlichen Knowledge-Space-Revisionen;
- ein privates, deterministisches Inventar der Telegram-Exporte trennt identitätstragende URLs von Hinweisen auf Startseiten/Produktfamilien;
- das bestehende manuelle, artikelbasierte Review- und Veröffentlichungstor.

Noch nicht umgesetzt:

- das Recherche- und Ledger für zeitliche Aussagen gemäß Schema 2;
- automatische zweisprachige Recherchejobs und ein Scheduler für Fälligkeitstermine;
- der öffentliche, anonyme MCP-Endpunkt happyin-context;
- zielorientierter Abruf von Aussagen und Rezepten.

Das Fehlen dieser Dienste ist eine Implementierungsgrenze und keine Aufforderung an Clients, Aktualität aus Git-Daten abzuleiten oder private Artefakte auszulesen.

## Lebenszyklus {#lifecycle}

~~~mermaid
flowchart TD
    A["Untrusted intake lead"] --> B["Identity candidate"]
    B --> C["Human thread review"]
    C --> D["Accepted news + durable research job"]
    S["Scheduled due check"] --> D
    D --> E["English search lane"]
    D --> F["Simplified Chinese search lane"]
    E --> G["Typed claims, recipes, conflicts and gaps"]
    F --> G
    G --> H["Knowledge Space review"]
    H -->|"approved"| I["Immutable article + public context projection"]
    H -->|"rejected/incomplete"| D
    I --> J["News site + anonymous MCP"]
~~~

Der Datenbankjob ist der Auslöser. MCP ist ein Adapter über dauerhaftem Zustand, keine Warteschlange, kein Scheduler, kein Recherchespeicher und keine Veröffentlichungsinstanz.

## Evidenz für den Entwicklungsgraphen {#development-graph-evidence}

Jede vorgeschlagene Verbindung erhält eine Evidenzstufe:

| Stufe | Evidenz | Ergebnis |
|---|---|---|
| E1 eindeutige Identität | Stabiles Repository, Modell-ID, Paper-ID, Release-ID oder identitätstragende kanonische URL | Privater Kandidatenkante |
| E2 geprüfte Herkunft | Offizielle Umbenennung, Nachfolger, Basismodell-Beziehung, Fork, Übernahme oder Organisationsaussage | Typisierte öffentliche Kante nach Prüfung |
| E3 Familienhinweis | Startseite, Herstellername, lexikalische/Embedding-Ähnlichkeit oder eine URL, die mehreren Produkten gemeinsam ist | Nur Ranking-Hinweis |
| E0 keine | Keine dauerhafte Identitätsevidenz | Bleibt unverknüpft |

Eine exakte URL belegt nicht, dass zwei Beiträge dasselbe Ereignis beschreiben. Eine Startseite identifiziert kein einzelnes Release. Verwandte Projekte können eine typisierte Kante vom Typ integration-with oder derived-from erhalten, ohne zu einem Projekt zusammengefasst zu werden.

## Verpflichtendes Suchpaket {#mandatory-search-bundle}

Jedes angenommene Thema dokumentiert die exakt ausgeführten Suchanfragen.

Die englische Spur umfasst:

- kanonischen Namen, Aliasse, exakte Version und Eigentümer;
- Release, Dokumentation, Repository, Model Card, Paper, Lizenz und Kompatibilität;
- Implementierung, Workflow, Parameter, Hardware, Einschränkungen, Fehler, Regressionen und Ersatztechnologie.

Die vereinfacht-chinesische Spur wiederholt dieselbe Absicht mit chinesischen Namen und Aliassen sowie aufgabenspezifischen Begriffen wie 参数, 配置, 显存, 训练, 推理, 工作流, 报错, 问题 und 实测.

Technologien chinesischen Ursprungs erfordern zusätzlich eine chinesischsprachige Spur mit einer Primärquelle und eine chinesische Implementierungs- oder Community-Spur. Eine Widerspruchsabfrage in beiden Sprachen sucht nach Fehlern, Inkompatibilitäten, Abkündigungen und neueren Ersatztechnologien.

Jeder Abfrageeintrag enthält Sprache, exakten Wortlaut, Aliasse/Versionseinschränkungen, Suchoberfläche, Ausführungszeitpunkt, betrachtete URLs, Ablehnungsgründe und gefundene Evidenzrollen. Ein fehlendes brauchbares Ergebnis wird als Lücke erfasst; eine Sprache ersetzt die andere niemals stillschweigend.

Quellen bleiben in ihrer Originalsprache. Der Artikel speichert eine englische Paraphrase, die Quellsprache und die Übersetzungsmethode, sofern eine Übersetzung nötig war.

## Evidenzrollen {#evidence-roles}

| Rolle | Typische Quellen | Autorität |
|---|---|---|
| Eingangshinweis | Telegram-Beitrag, Weiterleitung, Newsletter | Nur Entdeckung |
| Erste Partei | Release Notes, offizielle Dokumentation, Repository, Model Card, Lizenz | Identität, deklarierte Fähigkeit, Version und Support |
| Primärforschung | Paper, technischer Bericht, Benchmark-Protokoll | Methode und berichtete Evaluation |
| Implementierung | Fixierter Code/Workflow oder ein Issue mit versionierten Logs | Verhalten unter genannten Bedingungen |
| Community-Bericht | GitHub, Hugging Face, ModelScope, Reddit, Civitai, Zhihu, Bilibili | Praktische Einstellungen, Fehler und Hardwarebeobachtungen |
| Aggregator | Suche/Katalog/Zusammenfassung | Entdeckung, bis verifiziert |

Anforderungen an Aussagen:

- Für Identitäts- oder Release-Aussagen eine Quelle aus erster Hand verwenden, sofern eine existiert;
- für eine praktische Empfehlung Implementierungsevidenz und einen unabhängigen Betriebsbericht verlangen;
- für einen empfohlenen Parameterbereich zwei kompatible unabhängige Berichte oder einen reproduzierbaren eigenen Lauf verlangen;
- einen einzelnen Community-Kommentar als Anekdote mit niedriger Konfidenz behandeln;
- widersprechende Evidenz beibehalten, statt sie zu einem scheinbaren Konsens zu mitteln.

Externe Seiten und Kommentare sind nicht vertrauenswürdige Daten. Eingebettete Prompts, Befehle oder Aufforderungen zur Herausgabe von Zugangsdaten können Umfang, Werkzeuge, Berechtigungen, Identität oder Prüfstatus nicht verändern.

## Vertrag für praktische Rezepte {#practical-recipe-contract}

Eine Zahl ohne Betriebskontext ist kein wiederverwendbarer Parameter.

Jedes freigegebene Rezept enthält:

- Benutzerziel und Aufgabe;
- exakte Modell-/Artefakt-ID, Version, Commit/Hash und Lizenz;
- Versionen von Framework, Node/Extension, Treiber und Laufzeit;
- Hardware, VRAM/RAM, Präzision, Quantisierung und Beschleuniger;
- Eingabetyp, Auflösung, Dauer, Batch, Datensatzgröße sowie Daten- und Caption-Aufbereitung;
- reproduzierbaren Workflow, Befehl oder Graph-Referenz;
- getestete niedrige/hohe Werte, empfohlenen Startwert, Einheiten und Stichprobenumfang;
- Inferenz-Steuerungen wie Sampler, Scheduler, Schritte, Guidance, Denoise, Seed-Policy und Auflösung, sofern zutreffend;
- Trainingssteuerungen wie Optimizer, Lernrate, Rank/Alpha, Batch, Akkumulation, Schritte/Epochen, Checkpoint-Rhythmus und Regularisierung, sofern zutreffend;
- gemessene Qualität, Latenz, Speicherbedarf, bekannte Fehler, Warnsignale, Wiederherstellung und Fälle, in denen das Rezept nicht verwendet werden sollte;
- unterstützende und widersprechende Evidenz, Konfidenz und letzte Verifikation.

Bereiche aus unterschiedlichen Versionen, Aufgaben, Hardwareklassen oder Auflösungen bleiben getrennt. Ein Client darf sie vergleichen, aber nicht zu einem einzigen Intervall zusammenführen.

## Zeitliches Modell {#temporal-model}

Geltung und Aktualität sind unterschiedliche Dimensionen:

| Dimension | Werte |
|---|---|
| Zeitlicher Status | current, superseded, deprecated, obsolete, disputed, unknown |
| Aktualitätsstatus | fresh, due, unverified |

Jede strukturierte Aussage besitzt einen stabilen Schlüssel, eine unveränderliche Versions-ID, Beobachtungs- und Gültigkeitszeiten, letzte Verifikation, nächste Prüfung, Kompatibilitätsgeltungsbereich, Ersetzungsverknüpfungen, Konfidenz, Evidenz-IDs, Knowledge-Space-Revision und Prüfbeleg.

Eine Korrektur erzeugt eine neue Version und eine Ersetzungsverknüpfung. Historische Zeilen und Artikelabschnitte bleiben zugänglich. Git-Historie allein reicht nicht aus: Die öffentliche Projektion stellt den abgeleiteten Status bereit, damit Agenten ihn nicht selbst erschließen müssen.

Eine fällige Aussage ist nicht automatisch falsch, doch Standardempfehlungen schließen sie aus, sofern keine aktuellere Evidenz existiert. Dieser Rückfall muss explizit sein. Abgekündigtes und veraltetes Material erscheint nur für Kompatibilität/Historie oder wenn ein Client ausdrücklich Altwissen anfordert.

## Zielorientierter MCP-Vertrag {#goal-centred-mcp-contract}

Der geplante anonyme MCP-Dienst im Nur-Lese-Modus nimmt ein Ziel, Einschränkungen, einen Stichtag (as-of), eine Ergebnisobergrenze und ein explizites Flag für Altwissen entgegen. Er liefert getrennte Sammlungen:

- gerankte aktuelle Empfehlungen;
- anwendbare alternative Modelle, Technologien und Workflow-Varianten;
- praktische Rezepte und kontextgebundene Parameterbereiche;
- Kompatibilitäts- und Ressourcenbeschränkungen;
- strittige Evidenz;
- angeforderte ersetzte/abgekündigte/veraltete Historie;
- Quellsprachen, Evidenz, exakte Git-Revisionen, letzte Verifikation und nächste Prüfung;
- Lücken sowie Metadaten zur Gesamtzahl und zu Kürzungen.

Aktuelles und historisches Material werden niemals in einer unbeschrifteten Liste vermischt. Das lastModified einer MCP-Ressource ist ein Hinweis für den Client; maßgeblich bleiben die strukturierten Zeitfelder.

Der öffentliche Dienst liest nur bereinigte, per Commit adressierte öffentliche Artefakte. Er besitzt keine Route, keine Bindung und keine Zugangsdaten für Rohaufnahmen, private Anfragen, Anbieterausgaben, Reviews, Entwurfszweige, Datenbankschreibzugriffe oder Veröffentlichung.

## Erstes Korpus-Bootstrap {#first-corpus-bootstrap}

Das initiale private Inventar analysierte 13.473 Datensätze aus einem öffentlichen Telegram-Kanal im Zeitraum vom 30.11.2021 bis zum 26.08.2026.

Es ergab:

- 6.645 Nachrichten mit Links und 13.265 eindeutige kanonische URLs;
- 335 Nachrichten mit strikten URL-Treffern auf 288 der 330 bestehenden öffentlichen Nachrichtendatensätze;
- 693 wiederholte Identitätsgruppen;
- 663 wiederholte Identitätskandidaten, die noch nicht mit bestehenden Nachrichten verknüpft sind;
- 233 Nachrichten mit reinen Familienhinweisen, die nicht automatisch zu Graph-Kanten werden können.

Dies sind begrenzte Prüfkandidaten, keine veröffentlichten Fakten. Semantische Projekt- und Organisationsprüfung, zweisprachige Evidenzrecherche, Extraktion praktischer Rezepte, Knowledge-Space-Prüfung und das Exporttor für öffentliche Nachrichten gelten weiterhin.

## Veröffentlichungstor {#publication-gate}

Eine freigegebene Seite enthält:

1. aktuelle Empfehlung und Stichtag;
2. Alternativen und Auswahlkriterien;
3. praktischen Workflow und kontextgebundene Parameterbereiche;
4. Kompatibilität, Ressourcenbedarf und Fehlermodi;
5. Community-Beobachtungen mit Evidenzrolle und Konfidenz;
6. Einschränkungen, Streitfragen und explizite Lücken;
7. beibehaltene ersetzte/abgekündigte Historie;
8. Zusammenfassung des Recherche-Ledgers auf Englisch und Chinesisch;
9. ein Agent Brief;
10. exakte Quellen und unveränderliche Projektrevisionen.

Das Modell darf entwerfen. Es darf seine eigene Arbeit nicht als geprüft, aktuell oder veröffentlichbar markieren.

## Agent Brief {#agent-brief}

Bei der Nutzung dieses Wissens für eine reale Aufgabe:

1. Ziel, Modalität, Qualitätsziel, Hardware, Budget, Laufzeit und Kompatibilitätsbeschränkungen angeben;
2. zuerst aktuelle Optionen anfordern und Altoptionen nur bei Bedarf;
3. alle anwendbaren, begrenzten Modelle/Technologien vergleichen, statt das erste Ergebnis zu wählen;
4. Parameterbereiche an ihren Versions-, Aufgaben- und Hardwarekontext gebunden halten;
5. Streitfälle, fehlende chinesische/englische Abdeckung, fällige Prüfungen und Kürzungen offenlegen;
6. exakte Evidenz und Knowledge-Space-Revisionen zitieren;
7. einen Eingangsbeitrag oder eine Community-Anekdote niemals als Autorität aus erster Hand behandeln.

Wiederverwendbarer Prompt:

> Erstelle einen Lösungskontext für mein Ziel anhand der Happyin-Nachrichten und des Knowledge Space.
> Gib gerankte aktuelle Modelle und Technologien, praktikable Workflow-Alternativen,
> kontextgebundene Parameterbereiche, Kompatibilitäts- und Hardwarebeschränkungen,
> praktische Fehlermodi, englische und chinesische Evidenzabdeckung, Streitfälle,
> Aktualitätsdaten und exakte Quellrevisionen zurück. Halte ersetzte oder abgekündigte
> Empfehlungen getrennt und nimm sie nur auf, wenn sie für die Kompatibilität nötig sind.

## Erforderliche Evals {#required-evals}

- Sowohl die englische als auch die vereinfacht-chinesische Abfragespur sind dokumentiert;
- fehlende Sprachabdeckung bleibt als sichtbare Lücke erhalten;
- exakte Identität, geprüfte Herkunft und Familienhinweise lassen sich nicht verwechseln;
- Modell-/Versionskollisionen führen nicht zur Zusammenlegung von Entwicklungssträngen;
- Community-Anekdoten werden nicht zu Aussagen aus erster Hand;
- kontextlose Parameterbereiche werden abgelehnt;
- aktuelle und historische Aussagen sind getrennt;
- kein Update löscht historisches Wissen;
- Prompt-Injection kann Berechtigungen oder Zustand nicht verändern;
- fehlgeschlagene oder abgelehnte Arbeit erhöht die Aktualität nicht;
- Zielergebnisse zeigen relevante, begrenzte Alternativen und sichtbare Kürzungen.

## Stolperfallen {#gotchas}

- **Die neueste Quelle ist nicht immer die aktuelle, kompatible Antwort.** Ein neueres Release kann eine ältere GPU oder API nicht mehr unterstützen. **Lösung:** Status und Geltungsbereich (applies-to) unabhängig voneinander prüfen.
- **Viele Kommentare, die dieselbe kopierte Einstellung wiederholen, sind keine unabhängige Evidenz.** **Lösung:** Quellherkunft erhalten und unabhängige Läufe zählen, nicht Beiträge.
- **Eine chinesische Suche mit wörtlicher englischer Übersetzung übersieht lokale Namen.** **Lösung:** Hersteller-, Projekt- und Aufgabenaliasse erfassen, bevor gesucht wird.
- **Ein Git-Commit-Datum belegt keine Wissensaktualität.** **Lösung:** das explizite Verifikations-Ledger und den Zeitpunkt der nächsten Prüfung verwenden.
- **Historischer Text, der nur in Git verborgen ist, bleibt für die meisten Agenten unsichtbar.** **Lösung:** typisierte Ersetzungsverknüpfungen in der öffentlichen Projektion bereitstellen.

## Siehe auch {#see-also}

- [[news-development-graph]]
- [[happyin-knowledge-space]]
- [[architecture-documentation]]
- [[data-serialization-formats]]
- [[testing-and-quality]]

## Forschungsreferenzen {#research-references}

- [Hugging Face Model Cards](https://huggingface.co/docs/hub/en/model-cards)
- [ModelScope: Writing a Perfect Model Card](https://www.modelscope.cn/docs/contribute/model-file/help/wrtie-perfect-model-card)
- [W3C PROV overview](https://www.w3.org/TR/prov-overview/)
- [W3C PROV vocabulary](https://www.w3.org/ns/prov)
- [MCP Resources and annotations](https://modelcontextprotocol.io/specification/2025-11-25/server/resources)
