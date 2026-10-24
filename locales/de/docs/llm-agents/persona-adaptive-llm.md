---
title: "Personalisierung in LLM-Systemen"
description: "Ein Entscheidungsrahmen für Profilfelder, Retrieval-Speicher und adapterbasierte Personalisierung mit Mandantenisolation, Evaluation, Einwilligung und Löschgrenzen."
tags: [personalization, llm, lora, peft, privacy, evaluation]
level: 3
source_sha256: db84ab10e1c4365be242dc846d3035c2cd9700d02cb6f1fd5dc5e9ebfccd22bd
translation: machine
translated_at: '2026-10-24'
---
# Personalisierung in LLM-Systemen {#personalization-in-llm-systems}

**Stand geprüft: 2026-09-03.** Personalisierung ist kein einzelnes Feature, und eine Persona ist kein verlässlicher Fakt über eine Person. Trenne explizite Präferenzen, abgerufenen Verlauf, Aufgabenzustand und Modellanpassungen, damit jede Komponente einen Verantwortlichen, eine Herkunftsangabe, eine Evaluationsmethode und einen Entfernungspfad hat.

Adapterbasierte Personalisierung kann nützlich sein, ist aber eine betriebliche und datenschutzrechtliche Entscheidung und kein Standardersatz für ein gut abgegrenztes Profil- und Retrieval-System.

## Die kleinste reversible Schicht wählen {#choose-the-smallest-reversible-layer}

| Bedarf | Beginne mit | Warum |
|---|---|---|
| Antwortformat oder Tonalität für eine Aufgabe | explizite Anfrage oder begrenzte Systemrichtlinie | temporär und leicht prüfbar |
| stabile Nutzerpräferenz | strukturiertes Profilfeld mit Quelle und Ablaufdatum | prüfbar und korrigierbar |
| faktischer früherer Kontext | herkunftsbewusstes Retrieval | Daten können unabhängig aktualisiert oder entfernt werden |
| wiederholtes Modellverhalten für eine definierte Population | evaluierter Adapter oder Fine-Tuning | erfordert Lineage, Rollout und Rollback |

Trainiere keinen Adapter pro Nutzer, nur weil einige Präferenzen existieren. Retrieval und strukturierte Konfiguration bieten meist einen klareren Korrektur- und Löschpfad.

## Den Personalisierungsdatensatz modellieren {#model-the-personalization-record}

Führe serverseitig einen Datensatz, der Beobachtung von Autorisierung trennt:

```json
{
  "subject_ref": "opaque-user-reference",
  "attribute": "preferred_explanation_style",
  "value": "short examples before detail",
  "source": "user-confirmed-setting",
  "confidence": "confirmed",
  "allowed_uses": ["response-formatting"],
  "review_at": "2026-12-01",
  "revocation_ref": "privacy-request-reference"
}
```

Die Anwendung, nicht das Modell, entscheidet, welche Felder für eine Anfrage zulässig sind. Lass niemals einen nicht vertrauenswürdigen Prompt beliebige Profilzeilen, Mandantendatensätze, Adapterpfade oder Trainingsartefakte auswählen.

## Was LoRA und PEFT tatsächlich leisten {#what-lora-and-peft-actually-provide}

Parameter-effizientes Feintuning hängt trainierbare Adapter an ein Basismodell, statt alle Basisparameter zu aktualisieren. Aktuelle PEFT-Werkzeuge können benannte Adapter laden, wechseln, aktivieren, deaktivieren und entfernen; die Kompatibilität hängt weiterhin vom Modell, Adaptertyp und der Laufzeitumgebung ab. [PEFT-Überblick](https://huggingface.co/docs/transformers/peft) [PEFT-Adapterverwaltung](https://huggingface.co/docs/peft/en/developer_guides/troubleshooting)

Dies ist eine Implementierungsfähigkeit, keine Garantie dafür, dass:

- ein Adapter eine Person korrekt abbildet;
- zwei Adapter sicher kombiniert werden können;
- ein zur Laufzeit ausgetauschter Adapter feste Latenz- oder Speicherkosten hat;
- das Löschen eines Profils auch jede aus dem Training stammende Wirkung entfernt;
- ein Checkpoint aus einer nicht vertrauenswürdigen Quelle sicher geladen werden kann.

Behandle Aussagen zur Modellanpassung als Hypothesen, die einen Evaluationsplan brauchen.

## Grenze des Serving {#serving-boundary}

vLLM kann benannte LoRA-Adapter auf einem unterstützten Basismodell bereitstellen und dokumentiert sowohl die Konfiguration beim Start als auch das dynamische Laden von Adaptern. Ausdrücklich warnt es davor, Laufzeit-Updates von Adaptern für nicht vertrauenswürdige Clients zu aktivieren. [vLLM LoRA-Adapter](https://docs.vllm.ai/en/stable/features/lora/) [vLLM-Sicherheitshinweise](https://docs.vllm.ai/en/stable/usage/security/)

Für einen Mehrmandanten-Dienst gilt:

1. Ordne einen authentifizierten Mandanten und eine genehmigte Richtlinie serverseitig einer auf einer Allowlist stehenden Adapter-Kennung zu;
2. fixiere die Revision des Basismodells, die Adapterkonfiguration, den Artefakt-Digest und das Evaluationsergebnis;
3. stelle Endnutzern nur Generierungsendpunkte bereit, keine Endpunkte zum beliebigen Laden von Adaptern;
4. isoliere administratives Laden von der Verarbeitung von Anfragen;
5. bewahre eine idempotente Deployment-Quittung und ein Rollback-Ziel auf;
6. weise einen unbekannten Adapter, ein nicht passendes Basismodell oder ein nicht verifiziertes Artefakt ab.

Dynamisches Laden ist eine Operation für vertrauenswürdige Administratoren, es sei denn, ein isoliertes und verifiziertes Design belegt das Gegenteil.

## Evaluation vor der Personalisierung {#evaluation-before-personalization}

Vergleiche die kleinstmöglichen praktikablen Ansätze anhand eines festen, einwilligungsbasierten Korpus:

| Dimension | Beispielhafte Belege |
|---|---|
| Aufgabennutzen | vorab festgelegter Abnahmetest oder verblindete Bewertungsmatrix |
| Präferenztreue | von Nutzern bestätigte Beispiele und Korrekturrate |
| Sicherheit | Tests auf mandantenübergreifenden Zugriff, Prompt-Injection und unautorisierte Profile |
| Datenschutz | Prüfung der Datenflüsse, Aufbewahrungsregel, Plan für Löschung und Neutraining |
| Betrieb | Latenz-, Speicher-, Fehler- und Rollback-Nachweise in der Zielumgebung |

Führe dieselbe Testsuite für das Basismodell, die Baseline aus Profil/Retrieval und das angepasste Modell aus. Eine Qualitätsverbesserung rechtfertigt keinen Datenschutz- oder Isolationsfehler.

## Datenlebenszyklus {#data-lifecycle}

Bevor Daten für eine Personalisierungsschicht erhoben werden, lege fest:

- den Zweck, die Rechtsgrundlage und die zulässigen Datenklassen für die jeweilige Rechtsordnung;
- wer jeden Datensatz einsehen, ändern, exportieren oder widerrufen darf;
- ob ein Adapter Daten enthält, die nach einem Widerruf ein Neutraining, Ersetzen oder Außerbetriebnahme erfordern;
- wie Backup- und Evaluationsdatensätze derselben Aufbewahrungsregel folgen;
- wie das System nachweisen wird, dass eine Entfernung oder ein Rollback abgeschlossen wurde.

Das Privacy Framework des NIST ist eine nützliche Referenz für das Risikomanagement, ersetzt aber keine rechtlichen oder fachspezifischen Anforderungen. [NIST Privacy Framework](https://www.nist.gov/privacy-framework)

## Wann ein Adapter gerechtfertigt ist {#when-an-adapter-is-justified}

Verwende einen gelernten Adapter nur, wenn alle der folgenden Bedingungen erfüllt sind:

1. das Verhalten ist stabil genug, um es zu definieren und zu evaluieren;
2. Baselines für Profil und Retrieval wurden gemessen und reichen nicht aus;
3. Einwilligung, Mandantenzuordnung, Herkunft und Löschverantwortung sind definiert;
4. das Artefakt hat ein fixiertes Basismodell und eine reproduzierbare Evaluation;
5. vor der Freigabe existieren ein Rollback- und ein Incident-Pfad.

Andernfalls belasse die Personalisierung in strukturierten, editierbaren Daten.

## Stolperfallen {#gotchas}

- **Ein Prompt nennt einen anderen Nutzer.** Er darf weder dessen Verlauf noch dessen Adapter auswählen. **Lösung:** Bindе die Auswahl außerhalb des Modells an die authentifizierte Mandantenrichtlinie.
- **Ein Adapter funktioniert im Notebook.** Das ist kein Nachweis für einen Mehrmandanten-Produktivbetrieb. **Lösung:** Teste Isolation, Speicher, Fehlerverhalten und Rollback in der tatsächlichen Serving-Umgebung.
- **Ein Laufzeit-Endpunkt akzeptiert beliebige Pfade.** Dadurch wird das Laden von Artefakten zu einem Code- und Supply-Chain-Risiko. **Lösung:** Verwende eine Allowlist, Artefaktverifikation und ausschließlich administratives Laden.
- **Eine Präferenz veraltet.** Ihre weitere Verwendung kann das System weniger hilfreich machen. **Lösung:** Speichere Quelle, Prüfdatum und Korrekturweg.
- **Ein Löschantrag erreicht nur die Profiltabelle.** Abgeleitete Adapter oder Evaluationskopien können bestehen bleiben. **Lösung:** Pflege ein Lineage-Inventar und verifiziere den vollständigen Löschablauf.

## Quellen {#sources}

- [Hugging Face PEFT in Transformers](https://huggingface.co/docs/transformers/peft)
- [Hugging Face PEFT-Adapterverwaltung](https://huggingface.co/docs/peft/en/developer_guides/troubleshooting)
- [vLLM LoRA-Adapter](https://docs.vllm.ai/en/stable/features/lora/)
- [vLLM-Sicherheitshinweise](https://docs.vllm.ai/en/stable/usage/security/)
- [NIST Privacy Framework](https://www.nist.gov/privacy-framework)

## Siehe auch {#see-also}

- [[agent-memory]]
- [[llm-fine-tuning-practical]]
- [[agentic-security-2026]]
- [[ai-adaptive-learning-systems]]
