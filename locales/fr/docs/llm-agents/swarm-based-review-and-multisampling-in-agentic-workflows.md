---
title: "Revue indépendante et multiéchantillonnage pour les workflows d'agents"
description: "Générer des candidats indépendants, valider les preuves et sélectionner les sorties d'agents selon des critères d'acceptation explicites plutôt que des nombres de votes fixes ou la confiance du modèle."
tags: [llm-agents, multisampling, review, evaluation, evidence]
level: 4
source_sha256: 9c7fa4ad382325c6caa9181850efb5fcf20bbf2e77923bed7cca8dce834d3cbc
translation: machine
translated_at: '2026-10-24'
---
# Revue indépendante et multiéchantillonnage pour les workflows d'agents {#independent-review-and-multisampling-for-agent-workflows}

**Périmètre vérifié : 2026-09-04.** Plusieurs sorties d'agents peuvent révéler des modes de défaillance différents, mais ni un vote majoritaire ni la confiance d'un agent ne constituent une preuve qu'une sortie est correcte. Considérez le multiéchantillonnage comme un moyen borné de créer des candidats concurrents, et la revue comme une activité de vérification distincte, régie par un contrat d'acceptation nommé.

## Commencer par un contrat de tâche {#start-with-a-task-contract}

Avant de générer des alternatives, consignez ce que signifie « terminé » pour cette tâche. Un contrat utile rend les candidats comparables et empêche un essaim de revue de modifier silencieusement la demande.

```yaml
task_id: payment-retry-001
source_revision: immutable repository revision
deliverable: patch and test receipt
acceptance:
  - named test command passes
  - retry is idempotent
  - no production mutation during evaluation
authority:
  - repository read and local test only
escalation:
  - missing credential, production target, or unclear owner
```

Le contrat doit distinguer la réponse souhaitée des preuves qui peuvent la démontrer. Pour une réponse fondée sur des sources, les preuves peuvent être des sources primaires à jour. Pour une modification de code, elles peuvent être un diff, des tests déterministes et une revue indépendante. Pour une action externe, elles doivent inclure l'approbation et le reçu résultant.

## Séparer les candidats de la vérification {#separate-candidates-from-verification}

| Rôle | Travail autorisé | Sortie | Ne peut pas prouver à lui seul |
|---|---|---|---|
| générateur de candidats | proposer une réponse ou un correctif conforme au contrat | candidat et hypothèses citées | que la proposition fonctionne |
| collecteur de preuves | localiser les sources, exécuter les vérifications autorisées, conserver les reçus | ensemble de preuves | que les preuves satisfont chaque critère d'acceptation |
| vérificateur | comparer le candidat et les preuves au contrat | réussite, échec ou incertitude bornée | l'autorité de modifier la cible |
| sélecteur | choisir un candidat prouvé ou ne prendre aucune décision | justification de la sélection | la correction sans preuve du vérificateur |

L'indépendance doit être conçue à partir de chemins de preuve différents, et non à partir de noms de rôles théâtraux. Par exemple, un candidat peut tracer une frontière de flux de données pendant qu'un autre exécute le test d'acceptation énoncé. Si chaque agent reçoit le même brouillon, les mêmes outils et les mêmes hypothèses implicites, les erreurs deviennent corrélées, même si les prompts diffèrent.

## Choisir une règle d'agrégation adaptée à l'affirmation {#choose-an-aggregation-rule-that-fits-the-claim}

| Type d'affirmation | Règle privilégiée | Pourquoi un vote est insuffisant |
|---|---|---|
| calcul déterministe ou comportement de code | exécuter le validateur nommé | le résultat d'un test est plus fort qu'un consensus |
| affirmation factuelle sensible au temps | exiger des citations de sources primaires à jour | de nombreux agents peuvent répéter une source obsolète |
| choix de conception | comparer les compromis selon des contraintes explicites | il peut exister plus d'une réponse acceptable |
| préoccupation de sécurité | conserver l'union comme triage, puis confirmer chaque constat | des constats rares peuvent être précieux, mais un constat non vérifié n'est pas une vulnérabilité |
| action irréversible | exiger l'approbation déclarée et un reçu d'effet de bord | l'accord ne confère pas d'autorité |

Un sélecteur peut renvoyer « aucun candidat prouvé ». C'est un résultat sain lorsque les preuves manquent, que le contrat est ambigu, ou que les outils autorisés ne permettent pas d'inspecter la frontière concernée.

## Boucle de multiéchantillonnage bornée {#bounded-multisampling-loop}

1. Figer le contrat de tâche, la révision des entrées, la politique d'outils et la condition d'arrêt.
2. Générer des candidats indépendants qui varient de perspective de preuve ou d'approche d'implémentation.
3. Exécuter une validation déterministe avant de demander à un modèle de juger une prose portant sur cette validation.
4. Envoyer au vérificateur aveugle uniquement le candidat et l'ensemble de preuves nécessaires pour appliquer le contrat.
5. Sélectionner un candidat uniquement lorsque ses preuves requises sont présentes ; sinon, consigner l'écart, puis escalader ou arrêter.

Fixez un budget exprimé en termes observables par les opérateurs : nombre de candidats autorisés, durée, appels d'outils ou coût. Arrêtez tôt lorsque tous les critères sont prouvés, et arrêtez à la limite du budget lorsqu'ils ne le sont pas. N'augmentez pas silencieusement le nombre d'échantillons jusqu'à ce qu'une réponse préférée l'emporte.

## Registre de preuves {#evidence-record}

Conservez suffisamment d'informations pour qu'un relecteur ultérieur puisse reproduire la décision :

- identifiants de la tâche et des candidats ;
- révision de la source, version de configuration et jeu de données d'entrée ;
- commandes de validation exactes et codes de sortie ;
- URL des sources ou empreintes des artefacts ;
- outils refusés, approbations et reçus d'effets de bord externes ;
- justification de la sélection et incertitude non résolue.

Ce registre transforme un ensemble d'agents en workflow auditable. Il rend aussi possible l'évaluation de non-régression : une exécution future peut utiliser le même contrat et signaler quelle entrée, quel outil ou quelle source a changé.

## Les revues de sécurité exigent une confirmation {#security-reviews-need-confirmation}

Les agents orientés sécurité peuvent élargir le champ de recherche, mais leur sortie est une piste, non une décision de mise en production. Conservez le constat, la révision concernée, le chemin de déclenchement proposé et les preuves nécessaires pour le reproduire. Confirmez par la méthode la plus sûre disponible — inspection du code, jeu de test contrôlé ou environnement autorisé — avant de qualifier le constat de vulnérabilité ou de modifier un système de production. Évitez d'accorder à un agent de revue des droits supplémentaires sur le réseau, les identifiants ou le déploiement dans le seul but de rendre son résultat plus convaincant.

## Modes de défaillance courants {#common-failure-modes}

- **La majorité comme preuve :** l'accord peut amplifier une fausse prémisse partagée.
- **Bloc-notes mutable partagé :** les candidats suivants imitent le premier au lieu de le tester.
- **Débat sans limite :** davantage de messages remplacent un test d'acceptation manquant.
- **Confiance aveugle dans les scores de confiance :** la confiance n'est pas une garantie de correction calibrée.
- **Union de sécurité livrée comme un fait :** les constats de triage exigent une confirmation et une revue par le responsable.
- **Perte de provenance :** sans révision, jeu de données et reçu, un résultat futur ne peut pas être comparé honnêtement.

## Références {#references}

- [Documentation OpenAI Evals](https://platform.openai.com/docs/guides/evals) — définitions d'évaluations, exécutions et graders.
- [NIST AI RMF : Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) — un cadrage de gestion des risques pour les systèmes d'IA générative.
- [Claude Code subagents](https://code.claude.com/docs/en/subagents) — documentation actuelle sur les définitions de sous-agents délimitées et le travail délégué.
