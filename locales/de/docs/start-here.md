---
title: Beginnen Sie mit der Aufgabe
description: "Der kurze Weg von einer technischen Aufgabe zu einem überprüfbaren Material der Wissensdatenbank."
---
# Beginnen Sie mit der Aufgabe {#_1}

Diese Seite hilft Ihnen, den kürzesten zuverlässigen Weg in die Wissensdatenbank zu finden. Sie brauchen dafür weder ein Konto noch eine lokale Installation, sondern ein konkretes Ziel: Finden Sie das Ausgangsmaterial, prüfen Sie die Version und lesen Sie die Einschränkungen, bevor Sie die Konfiguration kopieren.

## 1. Formulieren Sie das Ergebnis {#1}

Eine nützliche Anfrage beschreibt das erwartete Ergebnis und die Umgebung:

- „Einen Python-Dienst mit Rollback und Zustandsprüfung sicher ausrollen“;
- „Einen Ansatz für die kontrollierte Bearbeitung eines Bildes auswählen“;
- „Verstehen, warum ein Kafka-Consumer nach einem Rebalance Duplikate erzeugt“;
- „Einem Coding-Agenten einen überprüfbaren technischen Kontext geben“.

Wenn Ihnen bereits das Modell, die Bibliothek, der Fehler oder der Befehl bekannt ist, nutzen Sie die Suche auf der Website oder die [Übersicht der Wissensdatenbank](knowledge-base/index.md). Wenn Ihnen nur das Ergebnis bekannt ist, beginnen Sie mit der folgenden Route.

## 2. Wählen Sie die nächstliegende Route {#2}

| Ich brauche | Hier beginnen | Danach |
|---|---|---|
| Einen AI- oder Image-Workflow aufbauen | [Image Generation](image-generation/index.md) | Modell, Bearbeitung, LoRA, Workflow oder Infrastruktur |
| Einen Dienst oder ein Web-Produkt ausrollen | [Architecture](architecture/index.md) | [Python](python/index.md), [Web Frontend](web-frontend/index.md) und [DevOps](devops/index.md) |
| Daten übertragen, analysieren oder abfragen | [Data Engineering](data-engineering/index.md) | [BI & Analytics](bi-analytics/index.md), [SQL](sql-databases/index.md) oder [Data Science](data-science/index.md) |
| Mit LLMs oder autonomen Workflows arbeiten | [LLM & Agents](llm-agents/index.md) | [LLM Memory](llm-memory/index.md) und [Security](security/index.md) |
| Mit Sprache, Transkription oder synthetischer Stimme arbeiten | [Audio & Voice](audio-voice/index.md) | Modell, Latenz und mehrsprachiger Rollout |
| Bestehenden Code debuggen, testen oder verbessern | [Testing & QA](testing-qa/index.md) | Sprache oder Framework Ihres Projekts |

## 3. Lesen Sie das Material als Grundlage für Entscheidungen {#3}

1. Prüfen Sie zuerst Version, Datum und Geltungsbereich.
2. Suchen Sie den Ansatz oder die Konfiguration, die zu Ihrer Umgebung passen.
3. Lesen Sie den Abschnitt **Gotchas**, bevor Sie Befehle ausführen: Dort sind die nicht offensichtlichen Fehler des Happy Path zusammengefasst.
4. Öffnen Sie benachbarte Artikel nur, wenn sie für die nächste Entscheidung benötigt werden.

Eine Seite der Wissensdatenbank ist ein Ausgangspunkt für eine Entscheidung, kein Ersatz für Tests in Ihrer eigenen Infrastruktur.

## 4. Verwendung mit einem AI-Agenten {#4-ai-}

Geben Sie dem Agenten einen Link zum Material, das Zielergebnis und die Umgebung. Den vollständigen Vertrag für Agenten finden Sie im [separaten Leitfaden](for-llm-agents.md).

```text
Read the relevant Happyin Knowledge Space page before proposing a change.
My outcome is: deploy a Python API with rollback and observable health checks.
Use the version context and Gotchas from the source; tell me what must be verified locally.
```

## Wenn Material fehlt {#_2}

Die Wissensdatenbank bietet einen öffentlichen Rückmeldeweg (beschrieben im [Leitfaden für Agenten](for-llm-agents.md)). Eine Nachricht sollte die Seite oder das Thema, die Version bzw. Umgebung und die öffentliche Quelle nennen. Senden Sie darin keinen persönlichen Code, keine Tokens und keine Nutzerdaten.
