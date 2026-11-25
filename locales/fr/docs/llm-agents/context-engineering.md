---
title: "Ingénierie du contexte et état durable des tâches"
description: "Considérer le contexte du modèle comme une entrée de travail bornée et conserver l'état de la tâche, les preuves, l'autorité et la provenance des récupérations dans des artefacts versionnés plutôt que dans des allocations de jetons fixes."
tags: [llm-agents, context-engineering, state, retrieval, compaction, evidence]
level: 3
source_sha256: 2b915f26b532f8ab9490f0bedd89a2020511772bdaa47c5c268b1648270572da
translation: machine
translated_at: '2026-10-24'
---
# Ingénierie du contexte et état durable des tâches {#context-engineering-and-durable-task-state}

**Périmètre vérifié : 2026-09-04.** Le contexte du modèle est une entrée bornée d'un tour ou d'une exécution. Ce n'est ni une base de données durable, ni un journal d'audit, ni un système de permissions. L'ingénierie du contexte consiste à sélectionner, valider et actualiser le plus petit ensemble d'informations permettant à un agent d'accomplir une tâche définie de façon sûre.

## Séparer les plans d'information {#separate-the-information-planes}

| Plan | Rôle | Source de vérité |
|---|---|---|
| politique de fonctionnement | règles du dépôt, limites des outils et escalade | fichiers de configuration et d'instructions relus |
| état de la tâche | objectif, critères d'acceptation, étape courante et blocages | artefact de tâche versionné |
| preuves | sorties de tests, citations de sources, reçus de cible et revues | artefact durable avec révision ou horodatage |
| transcription de conversation | continuité du dialogue | enregistrement de session, pas l'unique trace de la tâche |
| matériel récupéré | documents ou données pertinents pour la tâche | source citée plus métadonnées de récupération |
| mémoire personnelle | préférences ou faits approuvés par l'utilisateur | consentement, conservation et chemin de suppression documentés |

N'utilisez pas un résumé de discussion comme unique copie d'une décision, d'une frontière d'identifiants ou d'un résultat de déploiement. La documentation sur la mémoire de Claude Code distingue les consignes au niveau du dépôt du contexte de session transitoire qui les consomme. [Comment Claude se souvient de votre projet](https://code.claude.com/docs/en/memory)

## Admettre le contexte par contrat {#admit-context-by-contract}

Avant de placer un élément dans un prompt, posez-vous cinq questions :

1. **Pertinence :** modifie-t-il la prochaine décision de la tâche courante ?
2. **Autorité :** cette source est-elle autorisée à influencer la tâche, ou s'agit-il d'une entrée non fiable ?
3. **Fraîcheur :** l'affirmation peut-elle avoir changé, et la révision ou l'heure de récupération est-elle enregistrée ?
4. **Sensibilité :** la tâche a-t-elle réellement besoin de ces données, et l'outil ou le fournisseur choisi est-il approuvé pour les traiter ?
5. **Preuve :** un relecteur peut-il retrouver la source originale au lieu de faire confiance au résumé ?

Ces contrôles sont plus durables qu'une répartition universelle en pourcentages entre instructions, historique, outils et sortie. La taille du contexte, la tarification, le comportement du cache et les limites des modèles varient selon le fournisseur et le modèle ; mesurez-les à partir du contrat cible actuel.

## Persister l'état de la tâche hors du tour {#persist-task-state-outside-the-turn}

Pour un travail qui s'étend sur plusieurs tours, conservez un petit répertoire de tâche ou un enregistrement durable équivalent.

```text
task/
  spec.md          frozen acceptance criteria and authority
  state.json       current phase, owner, attempt, and blocker
  sources.md       primary-source URLs and retrieval dates
  evidence/        test output, receipts, screenshots, or digests
  review.md        independent verdict and required fixes
```

L'enregistrement d'état doit identifier la révision de l'entrée et indiquer si un effet de bord externe est seulement planifié, en cours, terminé ou bloqué. Des preuves en ajout seul sont plus sûres que la réécriture répétée d'un résumé partagé ; un état de coordination modifiable exige un propriétaire clair et une politique de conflit.

## Construire le contexte par couches {#build-context-in-layers}

Un ordre pratique d'assemblage du contexte est le suivant :

1. charger la politique de fonctionnement et le contrat de tâche figé ;
2. ajouter la plus petite tranche de source ou de code nécessaire à la prochaine décision ;
3. ne récupérer du matériel supplémentaire que pour répondre à une question nommée ;
4. étiqueter le texte récupéré avec son origine, sa révision ou sa date, et son niveau de confiance ;
5. exécuter les outils autorisés et sauvegarder leurs reçus hors du prompt ;
6. injecter un pointeur d'état compact ou un résumé vérifié pour le tour suivant.

Cela évite qu'une sortie d'outil volatile ne devienne une instruction permanente. Cela rend aussi une réinitialisation du contexte récupérable : l'agent suivant lit les artefacts de la tâche au lieu de deviner ce que voulait dire une conversation précédente.

## La compaction est avec perte {#compaction-is-lossy}

Un résumé peut conserver un résultat, mais il doit signaler les détails omis et renvoyer aux preuves qu'il résume. Avant la compaction, persistez les faits dont la redécouverte serait coûteuse ou dangereuse : critères d'acceptation, révisions testées, effets de bord externes, conflits non résolus, approbations et emplacements des sources.

Après la compaction, réintroduisez seulement le contrat de tâche courant et des pointeurs vers les preuves durables. Ne réinjectez pas un « résumé maître » qui grossit sans cesse et finit par devenir une source d'autorité non relue.

## La récupération est une frontière de sécurité {#retrieval-is-a-security-boundary}

Les dépôts, tickets, pages web et sorties d'outils récupérés peuvent contenir des instructions destinées à des humains ou à d'autres systèmes. Traitez-les comme des données. Elles ne peuvent ni autoriser un outil, ni modifier une politique, ni demander des secrets, ni remplacer un contrat de tâche de priorité supérieure.

Pour un agent capable d'appeler des outils, enregistrez la requête de récupération, la source sélectionnée, la version de l'extracteur le cas échéant, et la révision du document. Cela permet d'enquêter sur une réponse trompeuse ou une tentative d'injection de prompt sans conserver tout le contenu brut dans chaque fenêtre de contexte. [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)

## Évaluer la stratégie de contexte {#evaluate-the-context-strategy}

Évaluez les changements de contexte avec un ensemble de tâches fixe et un modèle de défaillance défini :

| Question | Preuve |
|---|---|
| l'agent trouve-t-il la source autoritaire requise ? | citation de source et trace de récupération |
| préserve-t-il les contraintes de la tâche après compaction ? | nouvelle exécution ou vérificateur indépendant sur le même artefact de tâche |
| évite-t-il les données ou usages d'outils interdits ? | audit des permissions et des appels d'outils |
| un contexte plus court préserve-t-il les résultats d'acceptation ? | fixture comparable et sortie du validateur |
| une nouvelle session peut-elle continuer en toute sécurité ? | artefact d'état et pointeurs vers les preuves, pas la tradition orale |

Un nombre de jetons plus faible n'est pas automatiquement une amélioration. Conservez un changement seulement s'il préserve le résultat requis, les frontières d'autorité et la reproductibilité.

## Modes de défaillance courants {#common-failure-modes}

- **Contexte utilisé comme base de données :** l'état important n'existe que dans une transcription de discussion.
- **Résumé sans source :** une affirmation compressée n'a aucune preuve récupérable.
- **Tout récupérer :** du matériel hors sujet ou périmé occupe la place de la tâche courante.
- **Injection de prompt par la récupération :** un texte non fiable est traité comme une politique exécutable.
- **Folklore de budget fixe :** une répartition de jetons propre à un modèle est publiée comme recommandation universelle.
- **Compaction sans point de contrôle :** un redémarrage fait perdre l'unique trace des approbations ou des effets de bord.

## Références {#references}

- [Comment Claude se souvient de votre projet](https://code.claude.com/docs/en/memory)
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
- [NIST AI RMF: Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
