---
title: "Tableaux de bord d'observabilité des agents"
description: "Contrats de traces, vues de tableau de bord et télémétrie minimisant les données pour les systèmes à outils et multi-agents ; revue du 2026-09-03."
level: 3
source_sha256: b79e8a8f26cf69b6498bac22401dc7d84c5ce9435e6c926b8f4ee8d1f1432878
translation: machine
translated_at: '2026-10-24'
---
# Tableaux de bord d'observabilité des agents {#agent-observability-dashboards}

Revue du 2026-09-03. Un tableau de bord d'observabilité répond à quatre questions opérationnelles : quel travail a été exécuté, quelle autorité a agi, quels outils ou modèles ont été impliqués, et quelles preuves rendent le résultat fiable. Il ne doit pas dépendre d'un hook d'IDE particulier ni d'un nom d'événement propre à un fournisseur.

## Commencer par un contrat de trace {#start-with-a-trace-contract}

Utilisez une trace pour un workflow visible par l'utilisateur ou un élément de travail durable. Chaque appel de modèle, appel d'outil, transfert (handoff), validateur et approbation devient un span ou un événement enfant.

```json
{
  "schema_version": "agent-trace/v1",
  "timestamp": "2026-09-03T14:10:31.442Z",
  "trace_id": "tr_01J...",
  "span_id": "sp_01J...",
  "parent_span_id": "sp_01J-parent",
  "run_id": "run_01J...",
  "operation": "tool.fetch_source",
  "actor": { "kind": "agent", "id": "researcher@2026-09-03" },
  "outcome": "ok",
  "duration_ms": 184,
  "input_ref": "source:42",
  "output_ref": "artifact:claim-set-42",
  "tool": { "name": "fetch_source", "policy_id": "research-readonly-v2" },
  "attributes": { "attempt": 1, "environment": "production" }
}
```

Ne placez pas de secrets, de prompts utilisateur bruts, de jetons d'accès ni de sorties d'outils non restreintes dans la charge utile par défaut de l'événement. Stockez une référence contrôlée ou un condensat (digest) lorsque le rejeu l'exige.

## Taxonomie minimale des spans {#minimum-span-taxonomy}

| Opération | Parent | Champs requis | Preuve de succès |
|---|---|---|---|
| Workflow | Aucun | identifiant d'exécution, objectif, propriétaire, état terminal | reçu terminal |
| Tour d'agent | Workflow | version agent/configuration, modèle, références d'entrée/sortie | sortie validée ou erreur |
| Appel d'outil | Tour d'agent | politique d'allowlist, nom de l'outil, référence des arguments, échéance | reçu de l'outil |
| Transfert (handoff) | Tour d'agent | propriétaire source/cible, motif de routage, référence de contexte | transfert accepté |
| Validateur | Workflow | version des critères, résultat, référence des constats | rapport réussite/échec |
| Approbation | Workflow | identité du relecteur, périmètre, décision | reçu d'approbation |

Le projet de conventions sémantiques GenAI d'OpenTelemetry couvre les spans, métriques et événements pour les clients GenAI et MCP. Utilisez ses conventions lorsqu'elles correspondent ; conservez les champs propres à l'application dans un espace de noms et documentez-les. [Conventions GenAI d'OpenTelemetry](https://github.com/open-telemetry/semantic-conventions-genai)

## Émettre un événement structuré {#emit-a-structured-event}

Cet exemple Python 3.11+ sans dépendance écrit un événement JSON par ligne sur la sortie standard. Un collecteur de production peut transmettre la même enveloppe à un point de terminaison OTLP, une file d'attente ou une base de données.

```python
from __future__ import annotations

import json
from datetime import UTC, datetime
from time import perf_counter
from uuid import uuid4


def emit(operation: str, trace_id: str, started: float, outcome: str) -> None:
    event = {
        "schema_version": "agent-trace/v1",
        "timestamp": datetime.now(UTC).isoformat(),
        "trace_id": trace_id,
        "span_id": f"sp_{uuid4().hex}",
        "operation": operation,
        "outcome": outcome,
        "duration_ms": round((perf_counter() - started) * 1000, 2),
        "attributes": {"environment": "development"},
    }
    print(json.dumps(event, separators=(",", ":"), sort_keys=True))


def main() -> None:
    trace_id = f"tr_{uuid4().hex}"
    started = perf_counter()
    try:
        # Replace with a bounded model or tool invocation.
        result = "validated"
        emit("agent.generate_summary", trace_id, started, "ok")
        print(result)
    except Exception:
        emit("agent.generate_summary", trace_id, started, "error")
        raise


if __name__ == "__main__":
    main()
```

## Vues de tableau de bord qui guident les décisions {#dashboard-views-that-drive-decisions}

| Vue | Question principale | Données nécessaires |
|---|---|---|
| Liste des exécutions | Quel travail est bloqué, en échec ou en attente d'approbation ? | état terminal, propriétaire, ancienneté, nombre de tentatives |
| Arbre de trace | Où le temps ou l'autorité ont-ils changé de mains ? | spans parent/enfant, durée, transferts |
| Registre des outils | Quelle capacité a causé un échec ou un pic de coût ? | politique de l'outil, résultat de l'outil, référence des arguments |
| File des validateurs | Quels candidats peuvent être publiés en toute sécurité ? | version des critères, verdict, référence des preuves |
| Vue budgétaire | Quel workflow dépasse son allocation ? | unités modèle/outil, imputation des coûts, concurrence |
| Vue incident | Cette exécution peut-elle être rejouée ou réconciliée ? | clé d'idempotence, reçu externe, catégorie d'erreur |

Évitez les graphiques de vanité. Un graphique de jetons sans identité de workflow ne permet pas à un opérateur de savoir à quelle tâche utilisateur ou à quel changement de production il correspond.

## Conception du pipeline {#pipeline-design}

```text
application / workflow controller
        |
        v
structured trace emitter
        |
        v
collector with schema validation and redaction
        |
        +--> durable event store
        |
        +--> OpenTelemetry-compatible backend
        |
        v
operator dashboard and alerts
```

Le collecteur est une frontière de confiance. Il valide la forme des événements, attribue l'horodatage d'ingestion, applique l'échantillonnage et la caviardage (redaction), et rejette les charges utiles malformées. Instrumentez vos propres frontières de workflow et d'outils plutôt que de supposer qu'un client tiers émet tous les événements dont vos équipes d'exploitation ont besoin.

Le SDK OpenAI Agents expose un traçage intégré avec des spans de trace, d'agent, de tour, de génération, de fonction, de garde-fou (guardrail) et de transfert (handoff). Un adaptateur peut enrichir ces spans avec vos références d'élément de travail et de preuve, plutôt que de remplacer leur hiérarchie de traces. [Traçage du SDK OpenAI Agents](https://openai.github.io/openai-agents-js/guides/tracing/)

## Échantillonnage, rétention et confidentialité {#sampling-retention-and-privacy}

| Classe de données | Politique par défaut | Escalade |
|---|---|---|
| Identifiants et temporisation | Conserver pendant la fenêtre opérationnelle | Agréger après la fenêtre |
| Texte des prompts/sorties | Ne pas conserver par défaut | Capture sur option, caviardée, à accès contrôlé |
| Arguments/résultats d'outils | Stocker des références ou des champs autorisés | Capture complète uniquement pour un débogage approuvé |
| Charges utiles d'erreur | Caviarder avant stockage | Enregistrement d'incident sécurisé à durée limitée |

Définissez la rétention selon la finalité. Le rejeu de débogage, l'analyse produit, l'imputation des coûts et les preuves d'audit ont des exigences d'accès et de suppression différentes. Vérifiez le comportement réel de stockage du backend de traçage que vous déployez ; les affirmations de l'interface du tableau de bord ne constituent pas une politique de rétention des données.

## Conditions d'alerte {#alert-conditions}

Alertez sur les transitions qui exigent une action, et non sur le volume brut d'événements :

- une exécution dépasse son échéance ou son budget ;
- un outil à effets de bord a un résultat inconnu ;
- le taux d'échec des validateurs évolue après une mise en production d'agent ou de configuration ;
- une file d'approbation dépasse son objectif d'ancienneté ;
- un collecteur rejette des événements ou perd l'accusé de réception de son stockage durable.

Chaque alerte doit renvoyer vers un identifiant de trace, un propriétaire, une référence de preuve et une action de runbook.

## Pièges {#gotchas}

- **Problème : journaliser par défaut les prompts bruts et les résultats d'outils.** La télémétrie devient une fuite de données secondaire et un magasin de rejeu coûteux. **Solution :** journalisez des références, des empreintes et des métadonnées autorisées ; ne capturez les charges utiles complètes que selon une politique documentée et à accès contrôlé.
- **Problème : réutiliser un même ID de span entre les tentatives.** Le tableau de bord ne peut pas distinguer une nouvelle tentative de l'appel initial incertain. **Solution :** conservez l'identité de la trace et de l'élément de travail, mais créez un nouveau span et un nouveau numéro de tentative pour chaque nouvel essai.
- **Problème : considérer les événements d'une bibliothèque cliente comme la trace complète du système.** Les approbations, les mises en file d'attente et les reçus externes se produisent souvent en dehors du SDK. **Solution :** instrumentez les frontières du contrôleur de workflow et corrélez les spans du fournisseur avec l'identifiant d'exécution durable.
- **Problème : alerter sur le seul nombre de jetons.** Un volume élevé peut être légitime ; un délai silencieux sur un effet de bord est plus urgent. **Solution :** alertez sur la violation d'une politique, d'un état ou d'un objectif de niveau de service.

## Voir aussi {#see-also}

- [[llmops]]
- [[agent-orchestration]]
- [[multi-agent-systems]]
- [[multi-session-coordination]]

## Sources {#sources}

- [OpenTelemetry GenAI Semantic Conventions](https://github.com/open-telemetry/semantic-conventions-genai)
- [OpenAI Agents SDK : Tracing](https://openai.github.io/openai-agents-js/guides/tracing/)
- [OpenAI Agents SDK : Agent Orchestration](https://openai.github.io/openai-agents-js/guides/multi-agent/)
