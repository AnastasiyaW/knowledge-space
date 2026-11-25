---
title: "Fizgig: fizgig-v6-0-1-refmod-support — Fizgig V6 0 1 Refmod Support"
category: "projects"
date: 2026-10-17
tags: ["fizgig", "fizgig-v6-0-1-refmod-support", "project"]
aliases: ["Fizgig: fizgig-v6-0-1-refmod-support"]
level: 2
source_sha256: 6f9b45474dd30454c1c4092917adaa6f02f522c2bc2179577997bf952ea38b1d
translation: machine
translated_at: '2026-10-24'
---
# Fizgig: fizgig-v6-0-1-refmod-support — Fizgig V6 0 1 Refmod Support {#fizgig-fizgig-v6-0-1-refmod-support-fizgig-v6-0-1-refmod-support}

**Entwicklungslinie:** project:fizgig · Thread fizgig-v6-0-1-refmod-support  
**Letztes Ereignis:** 2026-10-17 · 1 datiertes seit 2026-10-17 · **Recherchiert:** 2026-10-19 · Konfidenz: mittel

## Was es ist {#what-it-is}

Fizgig ist eine Open-Source-Suite für LoRA-Training und Model-Fine-Tuning auf lokalen und Cloud-GPUs. Sie trainiert Charakter-LoRA-Adapter mit einer Isolationsmethode, sodass jede Identität klar getrennt bleibt, wenn mehrere Personen in einem Bild vorkommen.

- Multi-Identity-Training: mehrere Charaktere in einer einzigen Adapterdatei
- Differential Output Preservation: abgeleitet von den AI-Toolkit-Grundlagen
- Fused-Token-Klassenentkopplung: trennt eindeutige Subjekt-Trigger von allgemeinen Klassenbegriffen
- Synthetische Negativpaare: schützen Fremde im Hintergrund
- Unterstützung von Basismodellen: funktioniert mit Flow-Matching- und Diffusionsarchitekturen

Beim Training werden mindestens zwei unterschiedliche Subjekte benötigt. Sind diese vorhanden, vermischen sich Identitäten nicht, und nach der Generierung ist kein manuelles Inpainting nötig.

## Entwicklungslinie {#development-line}

- **2026-10-17 — Fizgig veröffentlicht LoRA Isolation für Multi-Identity-LoRA-Training.** Am 2026-10-17 kündigte ein Fizgig-Entwickler LoRA Isolation an. Damit werden zwei Identitäten in einem LoRA trainiert, und andere Personen im Bild bleiben klar getrennt. In einem berichteten Test auf Krea 2 sank die Ausbreitung von Fremdgesichtern von 48 von 50 auf 0 von 50. Die Ankündigung verlinkt die Release Notes zu v8.4.0 und das GitHub-Repository.
  - Der Fizgig-Entwickler Peter Neill (@shootthesound) beschrieb, wie LoRA Isolation aufgebaut ist. Es kombiniert Differential Output Preservation (DOP), abgeleitet von Ostris AI-Toolkit, Fused-Token-Klassenentkopplung und synthetische Fremd-Negativpaare. Über 50 Testgenerierungen auf Krea 2 zeigte er keinerlei Ausbluten von Fremdgesichtern. (2026-10-17) — <https://www.reddit.com/r/StableDiffusion/comments/1x8aplh/fizgig_lora_isolation_a_new_process_for_more/>
  - Release v8.4.0 fügt der Subjects-Karte im Training-Tab eine Einrichtung mit mehreren Subjektordnern hinzu. Sie automatisiert die Fusion der Trigger-Klassen-Tokens und die Einrichtung des Negativpaar-Trainings. (2026-10-17) — <https://github.com/shootthesound/Fizgig/releases/tag/v8.4.0>
  - Ein Videotutorial richtet zwei getrennte Subjektordner auf der Subjects-Karte ein. Es formatiert Captions mit eindeutigen Triggern und Klassendeskriptoren, sodass Fused-Tokens automatisch erzeugt werden. (2026-10-17) — <https://youtu.be/CNh4sN5vN_8>

## Was sich geändert hat {#what-changed}

Die Arbeit verlagerte sich von einfachem Charakter-Fine-Tuning zur Trennung mehrerer Subjektidentitäten, aufbauend auf Differential Output Preservation und Negativpaar-Training. Als Nächstes kam die automatisierte Fusion von Caption zu Token, zusammen mit der Unterstützung neuerer Open-Weights-Bildbackends.

## Anwendung {#how-to-use-this}

1. Lege Datensätze für mindestens zwei unterschiedliche Identitäten in getrennten Ordnern auf der Subjects-Karte im Training-Tab von Fizgig ab.
  — <https://github.com/shootthesound/Fizgig/releases/tag/v8.4.0>
2. Beginne jede Caption mit dem eindeutigen Trigger-Token, dann einem Komma, dann dem Klassendeskriptor (z. B. 'zwxem, a woman smiling'). Fizgig nutzt dies, um interne Fused-Tokens zu bilden.
  — <https://github.com/shootthesound/Fizgig>
3. Aktiviere LoRA Isolation in der Trainingskonfiguration. Sie kombiniert Differential Output Preservation mit automatischer Paarung synthetischer Fremdbilder.
  — <https://www.reddit.com/r/StableDiffusion/comments/1x8aplh/fizgig_lora_isolation_a_new_process_for_more/>
4. Verwende bei der Inferenz das Fused-Trigger-Token und beschreibe die anderen Subjekte in der Szene. Identitätsgrenzen bleiben erhalten, und Gesichter laufen nicht ineinander.
  — <https://www.reddit.com/r/StableDiffusion/comments/1x8aplh/fizgig_lora_isolation_a_new_process_for_more/>

## Bewährte Praktiken {#best-practices}

- Trainiere mindestens zwei unterschiedliche Charaktere gemeinsam, auch wenn du nur einen brauchst. Dadurch muss das Netzwerk Identitäts-Tokens von allgemeinen menschlichen Klassen-Tokens trennen.
  — <https://www.reddit.com/r/StableDiffusion/comments/1x8aplh/fizgig_lora_isolation_a_new_process_for_more/>
- Lasse das Trigger-Token weg, wenn du Hintergrundfiguren oder Menschenmengen promptest. Das Basismodell rendert dann seine standardmäßigen, unterschiedlichen Gesichter ohne Leckage.
  — <https://www.reddit.com/r/StableDiffusion/comments/1x8aplh/fizgig_lora_isolation_a_new_process_for_more/>
- Schreibe beim Training mit Negativ-Kompositen aus mehreren Personen die Captions in kausaler Reihenfolge, wobei die Deskriptoren der Fremden zuerst stehen.
  — <https://www.reddit.com/r/StableDiffusion/comments/1x8aplh/fizgig_lora_isolation_a_new_process_for_more/>

## Was Praktiker sagen {#what-practitioners-say}

- Praktiker berichten, dass die Multi-Identity-Isolation ein verbreitetes Problem behebt: Charakter-LoRAs überschreiben Gesichter im Hintergrund und Nebenfiguren in Gruppenszenen. (2026-10-17)
  — <https://www.reddit.com/r/StableDiffusion/comments/1x8aplh/fizgig_lora_isolation_a_new_process_for_more/>

## Dadurch abgelöst {#superseded-by-this}

- Der frühere Rat lautete, mit einzelnen Subjekten und generischen Klassen-Tokens wie 'man' oder 'woman' zu trainieren. In Prompts mit mehreren Personen führte das zu starkem Ausbluten von Gesichtern auf Fremde.
  — <https://www.reddit.com/r/StableDiffusion/comments/1x8aplh/fizgig_lora_isolation_a_new_process_for_more/>

## Weiterhin unbekannt {#still-unknown}

- Der Thread heißt fizgig-v6-0-1-refmod-support, das Ereignis und die geprüften Release Notes beziehen sich jedoch auf v8.4.0. Das Veröffentlichungsdatum und die Implementierungsdetails der Refmod-Unterstützung in Version 6.0.1 ließen sich aus den verfügbaren Suchergebnissen nicht ermitteln.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://www.reddit.com/r/StableDiffusion/comments/1x8aplh/fizgig_lora_isolation_a_new_process_for_more/ | Fizgig LoRA Isolation: A new process for multi-identity training without face bleeding | 2026-10-19 |
| https://github.com/shootthesound/Fizgig/releases/tag/v8.4.0 | Release v8.4.0: LoRA Isolation Support · shootthesound/Fizgig | 2026-10-19 |
| https://github.com/shootthesound/Fizgig | shootthesound/Fizgig: LoRA and fine-tuning studio | 2026-10-19 |
| https://youtu.be/CNh4sN5vN_8 | Fizgig LoRA Isolation Walkthrough and Multi-Subject Workflow | 2026-10-19 |
| https://youtu.be/8uW5NdL5b20 | Fizgig LoRA Training Tutorial: Preventing Face Bleed | 2026-10-19 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** project:fizgig, Thread fizgig-v6-0-1-refmod-support, 1 datiertes Ereignis 2026-10-17 → 2026-10-17.
- **Praktischer Hinweis:** Nutze die belegten Anwendungs- und Praxisabschnitte oben, mit ihren Grenzen.
- **Konfidenz:** mittel. Die datierten Ablösungen oben entscheiden, was veraltet ist.
