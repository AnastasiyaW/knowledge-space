---
title: Hier starten
description: "Ein aufgabenorientierter Einstieg in den Happyin Knowledge Space für Personen, die einen verlässlichen nächsten technischen Schritt brauchen."
---
# Hier starten {#start-here}

Nutzen Sie diese Seite, wenn Sie eine konkrete technische Aufgabe haben und den kürzesten verlässlichen Weg in die Wissensdatenbank suchen. Sie benötigen weder ein Konto noch eine lokale Installation: Suchen Sie, öffnen Sie eine Referenz und prüfen Sie deren Versionskontext und Fallstricke, bevor Sie sie anwenden.

## Bevor Sie beginnen {#before-you-start}

Bringen Sie ein konkretes Ziel mit, nicht eine breite Technologiebezeichnung. Gute Einstiegsfragen sind:

- „Wie liefere ich einen Python-Dienst mit einem sicheren Deployment-Pfad aus?"
- „Welcher Ansatz zur Bildgenerierung passt zu einer kontrollierten Bearbeitung?"
- „Warum verursacht dieses Kafka-Consumer-Rebalancing Duplikate?"
- „Wie gebe ich meinem Coding-Agenten vertrauenswürdigen Kontext?"

Wenn Sie bereits ein Werkzeug, ein Modell, eine Fehlermeldung oder einen Befehl kennen, verwenden Sie zuerst das Suchfeld. Wenn Sie nur das Ziel kennen, wählen Sie unten einen Pfad.

## 1. Die passendste Aufgabe wählen {#1-choose-the-closest-task}

| Ich benötige… | Hier starten | Dann weiter zu |
|---|---|---|
| Einen KI-/Bild-Workflow aufbauen oder erweitern | [Image Generation](image-generation/index.md) | Seiten zu Modellen, Bearbeitung, LoRA, Workflow oder Infrastruktur |
| Einen Dienst oder ein Web-Produkt entwickeln | [Architecture](architecture/index.md) | [Python](python/index.md), [Web Frontend](web-frontend/index.md) und [DevOps](devops/index.md) |
| Daten verschieben, analysieren oder abfragen | [Data Engineering](data-engineering/index.md) | [BI & Analytics](bi-analytics/index.md), [SQL & Databases](sql-databases/index.md) oder [Data Science](data-science/index.md) |
| Mit Sprachmodellen oder autonomen Workflows arbeiten | [LLM & Agents](llm-agents/index.md) | [LLM Memory](llm-memory/index.md) und [Security](security/index.md) |
| Mit Sprache, Transkription oder synthetischer Stimme arbeiten | [Audio & Voice](audio-voice/index.md) | Modellvergleich, Latenz und Hinweise zum mehrsprachigen Deployment |
| Bestehenden Code debuggen, testen oder verbessern | [Testing & QA](testing-qa/index.md) | der Abschnitt zur Sprache oder zum Framework Ihrer Codebasis |

## 2. Eine Seite als Entscheidungshilfe lesen {#2-read-a-page-as-a-decision-aid}

Jede Referenz ist bewusst dicht gehalten. Lesen Sie sie in dieser Reihenfolge:

1. Prüfen Sie Version, Datum und Geltungsbereich. Eine Empfehlung zu einem Modell oder Framework aus dem Jahr 2024 passt möglicherweise nicht zu einer Installation aus dem Jahr 2026.
2. Suchen Sie das Implementierungsmuster oder den Konfigurationsblock, der zu Ihrem Setup passt.
3. Lesen Sie **Gotchas**, bevor Sie Befehle kopieren. Dort stehen die Fehlerfälle, die das Happy-Path-Beispiel nicht zeigen kann.
4. Folgen Sie **See also** nur, wenn Sie die angrenzende Entscheidung benötigen; öffnen Sie nicht standardmäßig eine ganze Domäne.

Die Wissensdatenbank ist ein Ausgangspunkt für eine Entscheidung, keine Autorität, die das Testen in Ihrer eigenen Umgebung ersetzt.

## 3. Mit einem KI-Assistenten verwenden {#3-use-it-with-an-ai-assistant}

Geben Sie einem Agenten die relevante Seite oder bitten Sie ihn, das Repository zu durchsuchen, bevor er eine Lösung vorschlägt. Der [Agenten-Leitfaden](for-llm-agents.md) enthält einen kurzen Prompt, maschinenlesbare Indizes und den Feedback-Vertrag.

Wenn Sie einen Agenten zum Handeln auffordern, nennen Sie das Ziel, Ihre Umgebung und die Quellseite. Zum Beispiel:

```text
Read the relevant Happyin Knowledge Space page before proposing a change.
My outcome is: deploy a Python API with rollback and observable health checks.
Use the version context and Gotchas from the source; tell me what must be verified locally.
```

## 4. Die Antwort für die nächste Person nützlich halten {#4-keep-the-answer-useful-for-the-next-person}

Wenn ein Artikel fehlt, veraltet oder falsch ist, nutzen Sie den Feedback-Weg der Seite oder den [Beitragsleitfaden](contributing/index.md). Ein hilfreicher Bericht nennt den Artikel oder das Thema, das beobachtete Problem, die Version oder Umgebung und eine öffentliche Quelle, die die Korrektur stützt. Fügen Sie keinen privaten Code, keine Zugangsdaten und keine Nutzerdaten bei.

## Was als Nächstes kommt {#what-comes-next}

- Durchsuchen Sie die [vollständige Domänenübersicht](index.md#domains), wenn die Aufgabe mehrere Bereiche berührt.
- Lesen Sie den [Blog](blog/index.md) für kürzlich hinzugefügtes Material und Projektneuigkeiten.
- Nutzen Sie [For AI Agents](for-llm-agents.md), wenn der nächste Leser ein Coding-Assistent statt einer Person ist.
