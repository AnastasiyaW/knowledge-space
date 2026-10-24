---
title: "Modèles de production LLM et agents (septembre 2026)"
category: techniques
tags: [llm-agents, production, evaluation, observability, human-in-the-loop]
level: 3
source_sha256: ec7ea06ab1c821d74787a99f1ee16d57c2ed68465790c9a18502731ace1b54f5
translation: machine
translated_at: '2026-10-24'
---
# Modèles de production LLM et agents (septembre 2026) {#production-llm-and-agent-patterns-september-2026}

Revu le 2026-09-03. Un système LLM en production est une application dotée de composants probabilistes. Rendez explicites dans le code applicatif l'autorité sur les données, les effets de bord, l'évaluation et la reprise ; n'essayez pas de les encoder uniquement dans la formulation du prompt.

## Plan de contrôle central {#core-control-plane}

| Préoccupation | Contrat de production |
|---|---|
| Entrée | Unité de travail typée, référence de source et politique de classification des données |
| Modèle | Configuration exacte du modèle/fournisseur et version du prompt |
| Outils | Liste d'autorisation, schéma, délai d'expiration, identité et politique d'effets de bord |
| État | Identifiant d'exécution, nombre de tentatives, point de reprise et clé d'idempotence |
| Sortie | Validation du schéma et critères d'acceptation propres à la tâche |
| Preuves | Reçus des outils, références de source, résultat du validateur, décision du relecteur |
| Exploitation | Trace, budget, catégorie d'erreur, responsable et procédure de retour arrière |

Le SDK OpenAI Agents distingue l'orchestration contrôlée par le code de l'orchestration contrôlée par le modèle. Utilisez le code lorsque la décision relève d'une politique, d'une autorisation, d'un budget ou d'une règle de routage déterministe. [Orchestration d'agents](https://openai.github.io/openai-agents-js/guides/multi-agent/)

## La recherche est un produit de données {#retrieval-is-a-data-product}

La recherche est pertinente lorsque la réponse doit être ancrée dans un contenu changeant ou propriétaire. Traitez-la comme un système distinct, avec ingestion, contrôle d'accès, versionnage des documents, évaluation de la recherche et vérification des citations.

| Question | Un contexte direct suffit lorsque | La recherche est nécessaire lorsque |
|---|---|---|
| Ensemble de sources | Il est restreint, connu et versionné | Il est volumineux, changeant ou propre à l'utilisateur |
| Autorité | Un seul artefact contrôlé fait référence | Plusieurs sources doivent être classées et traçables |
| Mode de défaillance | L'absence de contexte est évidente | Une recherche erronée ou obsolète peut induire en erreur sans signal |

Ne prétendez jamais qu'un résultat de recherche vectorielle fait autorité du seul fait qu'il a été récupéré. Enregistrez l'identité et la version de la source avec la réponse.

## Validation déterministe {#deterministic-validation}

Gardez les validateurs petits et propres à la tâche. Cet exemple Python 3.11+ valide un candidat qui doit citer une source connue et utiliser un statut autorisé.

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Candidate:
    status: str
    source_id: str
    summary: str


def validate(candidate: Candidate, allowed_sources: set[str]) -> list[str]:
    errors: list[str] = []
    if candidate.status not in {"draft", "approved"}:
        errors.append("invalid_status")
    if candidate.source_id not in allowed_sources:
        errors.append("unknown_source")
    if not candidate.summary.strip():
        errors.append("empty_summary")
    return errors


if __name__ == "__main__":
    item = Candidate("draft", "source-42", "Verified change summary.")
    print(validate(item, {"source-42"}))
```

Utilisez un évaluateur humain ou indépendant distinct pour le jugement éditorial, la revue de sécurité ou la correction sémantique, que un validateur déterministe ne peut pas mesurer.

## Les effets de bord exigent un état d'approbation {#side-effects-need-an-approval-state}

```text
PENDING -> GENERATED -> VALIDATED -> AWAITING_APPROVAL -> PUBLISHED
                       |                    |
                       v                    v
                     REJECTED             HELD
```

La publication, l'envoi d'e-mails, les paiements, la modification de données et les tickets externes doivent passer par un état d'approbation explicite. Une phrase générée par le modèle n'est jamais le reçu d'un effet de bord.

## Observabilité {#observability}

Tracez les workflows, les tours de modèle, les outils, les validateurs et les approbations sous un même identifiant d'exécution. Le projet de conventions sémantiques GenAI couvre les spans, métriques et événements pour les clients GenAI et MCP ; ajoutez des champs propres à l'application, préfixés par un espace de noms, pour l'identité de l'unité de travail et des preuves. [Conventions GenAI d'OpenTelemetry](https://github.com/open-telemetry/semantic-conventions-genai)

Questions minimales pour l'opérateur :

- Quelle exécution et quelle configuration ont produit cette sortie ?
- Quelles sources et quels outils l'ont influencée ?
- Un validateur ou un approbateur l'a-t-il acceptée ?
- Une action externe a-t-elle abouti, échoué ou reste-t-elle incertaine ?
- Peut-on rejouer la même unité de travail sans dupliquer un effet de bord ?

## Pièges {#gotchas}

- **Problème : collecter par défaut les prompts bruts et les résultats d'outils.** Les traces deviennent un second entrepôt de données sensibles. **Correction :** conservez par défaut des références et des métadonnées sur liste d'autorisation ; exigez une capture contrôlée pour les charges utiles complètes.
- **Problème : traiter un délai d'expiration comme un échec net.** L'action externe a peut-être abouti. **Correction :** persistez une clé d'idempotence et réconciliez le reçu du fournisseur avant de relancer.
- **Problème : laisser un modèle choisir une action de gouvernance.** Une instruction n'est pas un système de contrôle d'accès. **Correction :** appliquez les portes d'approbation, de budget et de publication dans du code déterministe.
- **Problème : considérer une réponse de modèle réussie comme prête pour la production.** Elle peut manquer de sources, de validation et de comportement de reprise. **Correction :** exigez un contrat d'acceptation testable et des preuves opérationnelles.

## Voir aussi {#see-also}

- [[agent-observability-dashboards]]
- [[agent-evaluation]]
- [[function-calling]]
- [[rag-pipeline]]
- [[tool-use-patterns]]

## Sources {#sources}

- [OpenAI Agents SDK : Agent orchestration](https://openai.github.io/openai-agents-js/guides/multi-agent/)
- [Conventions sémantiques GenAI d'OpenTelemetry](https://github.com/open-telemetry/semantic-conventions-genai)
- [Claude : How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)
