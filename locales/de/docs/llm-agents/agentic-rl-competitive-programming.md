---
title: "Agentic RL für kompetitive Programmierung"
category: patterns
tags: [llm-agents, reinforcement-learning, competitive-programming, code-generation, self-improvement, verification]
level: 3
source_sha256: e67f496f86cf2f4875d6113004431ee337dad7bc78f59e02200bff3811367288
translation: machine
translated_at: '2026-10-24'
---
# Agentic RL für kompetitive Programmierung {#agentic-rl-for-competitive-programming}

GrandCode (2026) erreicht Grandmaster-Niveau bei Problemen der kompetitiven Programmierung, indem es eine agentische Schleife mit Reinforcement Learning kombiniert. Die zentrale Erkenntnis: Klassisches RL trainiert eine Policy auf Trajektorien, kompetitive Programmierung erfordert jedoch mehrstufiges Schlussfolgern, Selbstkorrektur und externe Verifikation – genau das agentische Muster. Der Ansatz erreicht den Rang IGM (International Grandmaster) auf Codeforces und übertrifft damit alle bisherigen KI-Systeme.

## Kernarchitektur {#core-architecture}

Der Agent arbeitet in einer Schleife **generieren → ausführen → bewerten → verbessern** statt in einem einmaligen Generierungsdurchlauf:

```python
# Simplified agentic RL loop (pseudocode)
def solve(problem: str, time_budget: int) -> str:
    solution = initial_draft(problem)
    for step in range(time_budget):
        result = run_tests(solution)           # external verifier
        if result.all_pass:
            return solution
        feedback = analyze_failures(result)    # step-level reward signal
        solution = refine(solution, feedback)  # policy update via RL
    return best_so_far
```

Die Policy wird mit **Process Reward** (Korrektheit auf Schrittebene) statt mit **Outcome Reward** (nur finaler Bestanden/Nicht-bestanden) trainiert. Dies ist auf Grandmaster-Schwierigkeit entscheidend, denn bei einer spärlichen Belohnung liefert ein einziger falscher Schritt in einer 50-schrittigen Herleitung gar kein Signal.

## Warum agentisches RL one-shot-Generierung übertrifft {#why-agentic-rl-beats-one-shot-generation}

| Ansatz | Pass@1 bei schweren Problemen | IGM-Benchmark |
|---|---|---|
| GPT-4o (direkt) | ~8 % | Nein |
| o3-mini (Chain-of-Thought) | ~23 % | Nein |
| GrandCode (agentisches RL) | ~61 % | Ja |

Die Lücke entsteht, weil schwierige kompetitive Probleme Folgendes erfordern:

- **Testgetriebene Iteration** – Teillösungen einreichen und beobachten, welche Tests fehlschlagen
- **Entdeckung von Randfällen** – der externe Judge deckt Eingaben auf, die das Modell nicht in Betracht gezogen hat
- **Multi-Hypothesen-Suche** – verschiedene algorithmische Ansätze parallel ausprobieren

Eine One-shot-Generierung kann sich von einer falschen Algorithmuswahl nicht erholen. Eine agentische Schleife kann zurückgehen und neu ansetzen.

## Verifikation als Trainingssignal {#verification-as-the-training-signal}

Die entscheidende Infrastrukturkomponente sind **günstige, deterministische Verifizierer**. Kompetitive Programmierung verfügt über perfekte Verifizierer (Judge-Testfälle). Die RL-Schleife funktioniert nur, weil:

1. jede Zwischenlösung exakt bewertet werden kann,
2. die Bewertung schnell ist (Millisekunden pro Testfall),
3. Teilpunkte aussagekräftig sind (Anteil bestandener Tests = Belohnung).

```python
# Process reward model
def step_reward(partial_solution: str, test_cases: list) -> float:
    passed = sum(run_test(partial_solution, t) for t in test_cases)
    return passed / len(test_cases)   # 0.0 → 1.0 dense signal
```

Deshalb ist kompetitive Programmierung eine ideale Domäne für RL-Training: Das Belohnungssignal, das RL bei offenen Aufgaben schwer macht, steht hier kostenlos zur Verfügung.

## Memory Intelligence Agent (MIA) Pattern {#memory-intelligence-agent-mia-pattern}

Eine separate Arbeitslinie (ECNU-SII/MIA) adressiert einen verwandten Engpass: Bei **Deep-Research**-Aufgaben muss der Agent Informationen über Dutzende von Tool-Aufrufen hinweg zusammenführen. Ohne explizites Speichermanagement verliert er frühere Erkenntnisse, sobald der Kontext sich füllt.

MIA führt ein strukturiertes Arbeitsgedächtnis ein, das der Agent explizit liest und schreibt:

```python
# MIA-style memory operations (conceptual)
memory = WorkingMemory()

# During research loop
finding = web_search(query)
memory.store(key=topic_hash(finding), value=summarize(finding))

# When forming final answer
relevant = memory.retrieve(query=current_subtask, top_k=5)
answer = synthesize(relevant + current_context)
```

Die gemessene Verbesserung: etwa 40 % weniger „wiederholte Suchen“ (der Agent entdeckt Informationen erneut, die er bereits gefunden hat) sowie spürbare Genauigkeitsgewinne bei Multi-Hop-Recherche-Benchmarks.

## Verbindung zum Proof-Loop-Pattern {#connecting-to-proof-loop-pattern}

Sowohl GrandCode als auch MIA realisieren dasselbe zugrunde liegende Muster:

```text
spec_freeze → build → evidence → fresh_verify → fix → verify_again
```

- **GrandCode**: Spezifikation = Problemstellung; Evidenz = Testergebnisse; frischer Verifizierer = Judge
- **MIA**: Spezifikation = Forschungsfrage; Evidenz = Inhalte des Gedächtnisses; frischer Verifizierer = Synthesschritt

Der Unterschied zu Reflexionstechniken aus [[agent-self-improvement]] liegt darin, dass GrandCode **externe Ground Truth** (Judge-Tests) verwendet und keine selbst eingeschätzte Qualität. Der Verifizierer liegt außerhalb der Policy, die optimiert wird. Dadurch kann das Modell seine eigene Bewertungsmetrik nicht manipulieren.

## Implementierungsbeschränkungen {#implementation-constraints}

- **Verfügbarkeit des Verifizierers ist der Engpass**: Der Ansatz lässt sich direkt auf jede Domäne mit günstiger deterministischer Verifikation übertragen (Unit-Tests, formale Beweiser, SQL-Query-Validatoren). Auf offene Generierungsaufgaben ohne separates Reward-Modell lässt er sich nicht übertragen.
- **Explorationskosten skalieren mit der Problemschwierigkeit**: Grandmaster-Probleme erfordern 50–200 Verfeinerungsschritte, einfache Probleme 1–3. Das Budget entsprechend planen.
- **RL benötigt Trajektoriendaten**: Um Grandmaster-Niveau zu erreichen, war Training auf etwa 500.000 Trajektorien kompetitiver Programmierung mit annotierten Zwischenbelohnungen nötig. Das ist kein Fine-Tuning auf Lösungen, sondern Training auf dem gesamten Lösungsprozess.

## Stolperfallen {#gotchas}

- **Spärliche Belohnung macht RL bei schweren Problemen unbrauchbar**: Bewertet man nur die finale Einreichung, ist das Gradientensignal für eine zu 90 % korrekte Lösung identisch mit dem für eine zu 0 % korrekte. Die Testsuite-Bestehensrate als dichte Belohnung verwenden.
- **Testleckage macht Ergebnisse ungültig**: Enthalten die Trainingstrajektorien Probleme aus dem Evaluationsset, ist die gemeldete Leistung überhöht. Die Aufteilung von Training und Evaluation muss auf Problemebene geprüft werden, nicht nur auf Lösungsebene.
- **Selbst erzeugte Testfälle sind schwach**: Modelle neigen dazu, Tests zu erzeugen, die ihre eigenen Lösungen bestehen. Externe Judges mit zurückgehaltenen Testfällen oder adversarial erzeugte Randfälle verwenden.
- **Speicher ohne Vergessen verschlechtert sich**: MIA-artiger Speicher sammelt über lange Sitzungen Rauschen an. Veralterungsabbau oder periodische Konsolidierung implementieren, damit die Abrufqualität nach mehr als 50 Schreibvorgängen nicht absinkt.

## Siehe auch {#see-also}

- [[agent-self-improvement]]
- [[agent-memory]]
- [[swarm-based-review-and-multisampling-in-agentic-workflows]]
- [[adaptive-patterns-for-autonomous-agents]]
