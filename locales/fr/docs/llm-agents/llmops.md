---
title: "LLMOps"
description: "Exploiter des systèmes de modèles de langage avec évaluations versionnées, portes de mise en production, reçus observables et télémétrie minimisant les données."
tags: [llm-agents, llmops, evaluation, observability, governance, cost-optimization]
level: 3
source_sha256: d8b7a97d0456a03381a10b688ed3721496c3b928ecca4c0df6437a791ef247f2
translation: machine
translated_at: '2026-10-24'
---
# LLMOps (septembre 2026) {#llmops-september-2026}

Contexte de version : les alias de modèles, le comportement des API, la tarification, les règles de cache, les contrôles de rétention et la sémantique des outils évoluent indépendamment les uns des autres. Traitez chaque modèle résolu, chaque prompt, chaque configuration de récupération, chaque politique d'outil et chaque jeu d'évaluation comme une entrée de release soumise à revue, et non comme une documentation permanente.

LLMOps désigne la discipline opérationnelle d'un workflow reposant sur un LLM. Son objectif n'est pas de collecter chaque requête dans un tableau de bord. Son objectif est de décider si un changement a amélioré une tâche réelle, de déployer ce changement en toute sécurité, et de reconstruire ou d'annuler un résultat lorsque quelque chose tourne mal.

## Définir l'unité de changement {#define-the-unit-of-change}

Une modification de prompt peut affecter la sécurité, la qualité, la latence et le coût tout autant qu'une modification de code. Placez le candidat complet dans un petit manifeste de release :

```json
{
  "release_id": "support-triage-2026-09-03.1",
  "task_contract": "support-triage/v3",
  "model_key": "approved-triage-model",
  "resolved_model_revision": "recorded-at-deploy",
  "prompt_revision": "sha256:...",
  "retrieval_revision": "catalog@17",
  "tool_policy_revision": "tools@9",
  "eval_suite_revision": "triage-evals@12",
  "data_policy_revision": "retention@5",
  "owner": "support-platform"
}
```

Le manifeste identifie un comportement sans copier dans le contrôle de version des secrets, des contenus clients complets ou un objet de SDK fournisseur. Stockez une référence protégée ou un condensat lorsque le rejeu nécessite des éléments d'entrée.

## Cycle de vie de la release {#release-lifecycle}

| Étape | Question | Preuves requises | Issue finale |
|---|---|---|---|
| Contrat de tâche | Que doit faire le workflow, et que ne doit-il jamais faire ? | schéma d'entrée/sortie, frontière d'autorisation, critères d'acceptation | périmètre approuvé ou rejeté |
| Référence | Que réalise la release actuelle ? | jeu d'évaluation représentatif figé et reçu de référence | base de comparaison |
| Candidat | Qu'est-ce qui a changé ? | un seul diff de manifeste relu et notes de migration | candidat évaluable |
| Évaluation hors ligne | A-t-il progressé sans casser les cas connus ? | vérifications déterministes, cas étiquetés et échantillon d'échecs relu | validé, suspendu ou rejeté |
| Staging ou exécution fantôme (shadow) | Fonctionne-t-il en sécurité dans des conditions réalistes ? | trace, contrôles de politique, preuves de latence et d'erreurs | prêt ou bloqué |
| Canari | Une route réelle et bornée préserve-t-elle le contrat ? | cohorte explicite, point de retour arrière, reçus terminaux | promouvoir ou annuler |
| Archivage | Un opérateur peut-il expliquer le résultat plus tard ? | références immuables de release, d'évaluation et de décision | enregistrement reproductible |

Ne promouvez pas un prompt apparemment meilleur simplement parce qu'une démonstration semble convaincante. Une décision de release exige une comparaison avec le même contrat de tâche et un enregistrement des cas qui échouent encore.

## Construire un contrat d'évaluation {#build-an-evaluation-contract}

Utilisez plusieurs formes de preuves, car elles détectent des erreurs différentes :

| Type de preuve | Idéal pour | Limite |
|---|---|---|
| Assertion déterministe | schémas, étiquettes exactes, permissions, champs interdits | ne peut pas évaluer chaque réponse sémantique |
| Jeu de référence étiqueté | issues de tâches connues et régressions | la couverture se limite aux données sélectionnées |
| Revue humaine | nuances, utilité, interprétation des politiques | nécessite une grille calibrée et un échantillonnage |
| Juge fondé sur un modèle | triage à grande échelle de critères bien définis | constitue un signal à auditer, non une autorité sans limite |
| Reçu de production | état terminal réel et échecs visibles par l'utilisateur | doit respecter la confidentialité et être échantillonné de façon sûre |

Les recommandations d'évaluation d'OpenAI illustrent des critères de test tels qu'une vérification de chaîne exacte par rapport à une étiquette de référence. Ce schéma est utile lorsque la tâche admet une réponse objective ; il ne remplace pas une revue humaine des issues ambiguës ou à fort impact. [Working with evals](https://developers.openai.com/api/docs/guides/evals)

Figez les entrées de test, la version de l'évaluateur et les seuils d'acceptation avant de comparer des candidats. Si un juge fondé sur un modèle change, traitez-le comme un changement de candidat distinct et calibrez-le sur des exemples relus.

## Tracer le travail sans créer de fuite de données {#trace-work-without-creating-a-data-leak}

Une tâche visible par l'utilisateur ou une tâche durable doit posséder un seul identifiant de trace. Les appels de modèle, la récupération, les appels d'outils, les approbations, les validateurs, les nouvelles tentatives et les transmissions deviennent des événements enfants. Émettez par défaut des références et des champs structurés, et non des prompts ou des sorties d'outils sans restriction.

```json
{
  "schema_version": "llmops-event/v1",
  "trace_id": "tr_01...",
  "release_id": "support-triage-2026-09-03.1",
  "operation": "model.complete",
  "outcome": "completed",
  "duration_ms": 842,
  "usage": {"input": 0, "output": 0},
  "input_ref": "protected:request/...",
  "output_ref": "protected:result/...",
  "tool_policy_revision": "tools@9",
  "attempt": 1
}
```

Un événement utile indique quelle release a été exécutée, quelle autorité a été utilisée, comment il s'est terminé, et où se trouvent les preuves contrôlées. Le projet de conventions sémantiques GenAI d'OpenTelemetry constitue une référence utile pour l'interopérabilité ; les champs propres à l'application doivent rester documentés et placés dans un espace de noms.[OpenTelemetry GenAI conventions](https://github.com/open-telemetry/semantic-conventions-genai)

## Faire de la sécurité et de l'autorisation des portes de release {#make-safety-and-authorization-release-gates}

Un modèle, ou son prompt, n'est pas une frontière d'autorité. Conservez l'autorisation, l'isolation des locataires, l'approbation des effets de bord et les invariants métier dans du code applicatif déterministe.

Pour chaque candidat, testez au minimum :

1. des entrées malformées, manquantes et adversariales ;
2. des arguments d'outil valides en JSON mais non autorisés ;
3. des instructions contradictoires intégrées dans un texte récupéré ou contrôlé par l'utilisateur ;
4. les chemins de livraison en double et de dépassement de délai pour les travaux à effets ;
5. le comportement de masquage et de rétention dans les traces et les entrées de l'évaluateur ;
6. un retour arrière connu et sûr vers le manifeste de release précédent.

Les [bonnes pratiques de sécurité d'OpenAI](https://developers.openai.com/api/docs/guides/safety-best-practices) constituent un point de départ propre au fournisseur, et non un substitut à une modélisation des menaces propre au produit.

## Piloter les coûts par des mesures, non par la tradition {#operate-costs-as-measurements-not-folklore}

Collectez, pour chaque release, l'usage rapporté par le fournisseur, les signaux de cache lorsqu'ils sont disponibles, la révision du modèle, la latence, le nombre de nouvelles tentatives, le nombre d'appels d'outils et l'issue de la tâche. Déterminez le prix uniquement à partir de la grille tarifaire en vigueur pour le modèle exact et le niveau de traitement exact, au moment de la planification ou de la facturation.

Utilisez un budget comme condition de release :

```text
quality and safety SLOs met
    AND measured workload cost is within the approved budget
    AND no unaccounted retry or tool side effect exists
        => candidate may advance
```

Un nombre de jetons plus faible n'est pas automatiquement une amélioration des coûts s'il augmente les nouvelles tentatives, reporte le travail vers un outil coûteux, ou réduit le taux de réussite des tâches.

## Pratique des incidents et des retours arrière {#incident-and-rollback-practice}

Un enregistrement d'incident doit relier la trace, l'identifiant de release, les références d'entrée et de sortie, les reçus externes et les constats de l'évaluateur. Sa première question est opérationnelle : une action externe a-t-elle eu lieu ? Sa seconde est causale : quelle entrée de release a modifié le comportement ?

Annulez en restaurant un manifeste précédemment vérifié, puis confirmez à l'exécution le modèle et la configuration résolus. N'annulez pas en devinant un ancien alias de modèle, un ancien texte de prompt ou une ancienne configuration de cache.

## Pièges {#gotchas}

- **Les moyennes masquent les queues de distribution néfastes.** Une latence moyenne ou un score moyen peut dissimuler une petite classe d'échecs catastrophiques. **Correction :** segmentez les évaluations et la télémétrie par tâche, locale, chemin d'outil, politique de locataire et état terminal.
- **Un LLM-juge ne se valide pas lui-même.** Un évaluateur peut dériver ou partager le même angle mort que le candidat. **Correction :** calibrez-le sur des cas relus par des humains et conservez les désaccords pour audit.
- **Les charges utiles de trace peuvent devenir un magasin de données parallèle.** Journaliser les prompts complets, les fichiers récupérés ou les sorties d'outils crée des risques de rétention et d'accès. **Correction :** émettez des références contrôlées, masquez tôt et appliquez une politique de rétention.
- **Un canari sans reçu de retour arrière est une expérience en production.** Une petite cohorte ne rend pas réversible un effet de bord inconnu. **Correction :** définissez la condition d'arrêt, la stratégie d'idempotence et la release de retour arrière avant que le trafic ne bascule.
- **Un alias de modèle n'est pas un enregistrement de reproductibilité.** Les fournisseurs peuvent mettre à jour les alias ou leur disponibilité. **Correction :** enregistrez le modèle et la configuration résolus, tels qu'observés par la release en exécution.

## Sources {#sources}

- [OpenAI : working with evals](https://developers.openai.com/api/docs/guides/evals)
- [OpenAI : Responses API reference](https://developers.openai.com/api/reference/cli/resources/responses/methods/create)
- [OpenAI : safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices)
- [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai)

## Voir aussi {#see-also}

- [[agent-evaluation]]
- [[agent-observability-dashboards]]
- [[llm-api-integration]]
- [[prompt-engineering]]
- [[token-optimization]]
- [[agent-security]]
