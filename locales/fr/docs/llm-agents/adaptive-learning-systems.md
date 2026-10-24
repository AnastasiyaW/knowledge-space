---
title: "Systèmes d'apprentissage adaptatif avec des LLM"
description: "Une architecture bornée pour l'état de l'apprenant, la planification déterministe, la génération de contenu, l'évaluation et la confidentialité"
level: 3
source_sha256: 762ce577fe2100b38d73409bfef469b34aeb3d76e9eb86753b083c7a64b024f3
translation: machine
translated_at: '2026-10-24'
---
# Systèmes d'apprentissage adaptatif avec des LLM (septembre 2026) {#adaptive-learning-systems-with-llms-september-2026}

Contexte de version : les modèles d'apprenant, les programmes d'études et les algorithmes de planification sont des politiques propres au domaine. Traitez leurs versions, leurs données de calibration et leurs règles de confidentialité comme des artefacts déployables ; ne les intégrez pas uniquement dans un prompt de LLM.

Un LLM peut générer des explications et des exercices, mais il ne doit pas être la source de vérité pour les graphes de prérequis, les dossiers des apprenants, la planification des révisions ni les décisions d'évaluation à fort enjeu.

## Quatre couches bornées {#four-bounded-layers}

```text
Curriculum model  -> concepts, prerequisites, approved objectives
Learner model     -> evidence-backed estimates and review history
Scheduler         -> deterministic next-review and workload policy
Generation layer  -> explanations, examples, feedback, and exercise candidates
```

Cette séparation rend le système testable : le programme d'études et la planification peuvent être rejoués sans appel au modèle, tandis que la génération peut être évaluée par rapport à un état de l'apprenant connu.

## Contrat des événements d'apprentissage {#learner-event-contract}

Stockez les interactions observées, et non des affirmations non fondées telles que `the learner understands algebra`.

```json
{
  "event_id": "evt_01J...",
  "learner_id": "pseudonymous-id",
  "concept_id": "fractions.addition",
  "activity_revision": "fractions-v5",
  "submitted_at": "2026-09-03T18:00:00Z",
  "result": "incorrect",
  "attempt_count": 2,
  "evidence_ref": "encrypted://assessment/...",
  "consent_policy": "education-data-v2"
}
```

Une mise à jour de l'état de l'apprenant est une transformation versionnée d'événements. Enregistrez la révision du modèle ou de la règle, la confiance, l'horodatage et la plage d'événements source.

## Planification en dehors du LLM {#scheduling-outside-the-llm}

Le planificateur détermine quand un élément est dû. Anki documente FSRS comme un algorithme de planification distinct, qui estime la probabilité de rappel et utilise un paramètre de rétention souhaitée ; c'est un bon exemple de la raison pour laquelle la planification doit être déterministe et auditable de manière indépendante.

```python
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ReviewDecision:
    concept_id: str
    due_at: datetime
    scheduler_revision: str
    reason: str


def next_activity(decision: ReviewDecision) -> dict[str, str]:
    return {
        "concept_id": decision.concept_id,
        "scheduler_revision": decision.scheduler_revision,
        "reason": decision.reason,
    }
```

Le LLM peut recevoir cette activité sélectionnée ainsi que le contexte de l'apprenant limité au strict nécessaire. Il ne doit pas choisir une autre date d'échéance ni réécrire silencieusement l'état de maîtrise.

## Contrat de génération {#generation-contract}

Utilisez le modèle pour proposer du contenu, puis validez-le par rapport aux contraintes du programme d'études :

| Entrée | Validateur |
|---|---|
| Concept et ensemble de prérequis | Service de programme d'études |
| Bande de difficulté | Politique calibrée |
| Format de l'exercice | Validateur de schéma |
| Matériel source factuel | Validateur de récupération et de citations |
| Retour visible par l'apprenant | Politique de sécurité et de ton |
| Clé de réponse | Vérificateur déterministe ou grille de notation validée |

Pour les retours ouverts, indiquez que le résultat constitue une aide. Ne présentez pas un retour généré comme une note vérifiée, sauf si une politique d'évaluation l'autorise explicitement.

## Suivi des connaissances {#knowledge-tracing}

Le suivi des connaissances (knowledge tracing) prédit les performances futures à partir de séquences d'interactions. C'est un estimateur, et non un fait concernant un apprenant.

Commencez par une base de référence transparente et mesurez la calibration sur des historiques d'apprenants mis de côté. N'utilisez une boîte à outils de recherche comme pyKT qu'après avoir vérifié que sa représentation des données, sa stratégie de découpage et sa licence conviennent au produit. Le choix d'implémentation doit être justifié par une amélioration mesurée par rapport à la base de référence.

## Contexte et confidentialité {#context-and-privacy}

Le contexte du modèle ne doit contenir que ce qui est nécessaire à l'activité en cours :

- identifiants autorisés de l'apprenant et du programme d'études en cours ;
- concept, objectif et politique de difficulté sélectionnés ;
- résumé récent des retours pertinent pour l'activité ;
- matériel source approuvé et contraintes d'évaluation.

Gardez hors du prompt les historiques bruts, les données personnellement identifiables et les conversations sans rapport. Définissez les politiques de conservation, de suppression, de revue des accès et d'exportation avant de collecter les événements d'apprentissage.

## Porte d'évaluation {#evaluation-gate}

Évaluez le système dans son ensemble, et non seulement la prose générée :

1. Le parcours du programme d'études respecte les prérequis.
2. Le planificateur produit des résultats reproductibles pour une même séquence d'événements.
3. Les estimations de l'état de l'apprenant sont calibrées sur des historiques mis de côté.
4. Les exercices générés respectent l'objectif et le schéma de réponse.
5. Les retours ne divulguent pas de données protégées et ne formulent pas d'affirmations non étayées.
6. La charge de travail et les résultats d'apprentissage sont suivis dans le cadre d'un protocole d'étude approuvé.

## Pièges courants {#gotchas}

- **Le texte de tutorat généré n'est pas un modèle de l'élève.** Une explication sûre d'elle peut être erronée quant au niveau de compétence. **Correctif :** dérivez l'état de l'apprenant à partir de transformations versionnées d'événements et exposez la confiance ou l'incertitude.
- **La planification dans un prompt n'est pas reproductible.** Un même historique peut donner des conseils de révision différents. **Correctif :** exécutez la planification sous forme de code déterministe et transmettez l'activité choisie au modèle.
- **Les fuites de données futures invalident l'évaluation.** Découper au hasard des interactions chronologiques permet aux performances ultérieures de révéler la réponse. **Correctif :** découpez par apprenant et par frontière temporelle avant l'ajustement ou le réglage.
- **Les données éducatives sont sensibles.** Les journaux de conversation riches peuvent contenir des informations sur l'identité, un handicap ou l'évaluation. **Correctif :** minimisez le contexte du prompt et appliquez des politiques explicites de conservation et d'accès.

## Sources {#sources}

- [Manuel d'Anki : FSRS](https://docs.ankiweb.net/deck-options.html#fsrs)
- [Projet FSRS pour Anki](https://github.com/open-spaced-repetition/fsrs4anki)
- [Boîte à outils de suivi des connaissances pyKT](https://github.com/pykt-team/pykt-toolkit)

## Voir aussi {#see-also}

- [[agent-memory]]
- [[rag-pipeline]]
- [[embeddings]]
- [[agent-evaluation]]
