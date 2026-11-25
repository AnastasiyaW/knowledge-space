---
title: "Base44 — Superagent"
category: projects
date: 2026-03-31
tags: [base44, project, superagent]
aliases: ["Base44"]
level: 2
source_sha256: e7299b60e4563065346ac8967c6a04844a98e33293c2563a3c6461ccfcf76284
translation: machine
translated_at: '2026-10-24'
---
# Base44 — Superagent {#base44-superagent}

**Ligne de développement :** `project:base44` · fil `superagent`  
**Dernier événement :** 2026-03-31 · 1 événement daté depuis le 2026-03-31 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

Base44 est un backend géré et un créateur d'applications doté d'agents autonomes en arrière-plan.

- Applications et hébergement : création d'applications web avec hébergement géré et interfaces frontales personnalisées.
- Infrastructure backend : fourniture de bases de données, d'authentification des utilisateurs et de fonctions serveur.
- Superagents : exécution de workers persistants en arrière-plan, selon des planifications ou des événements entrants.
- Intégrations : connexion de services externes à la logique de l'espace de travail.

L'accès des agents dépend strictement des outils connectés et des permissions qui leur sont attribuées. La plateforme convient aux applications internes et aux automatisations bornées, mais les permissions d'intégration nécessitent une conception explicite.

## Ligne de développement {#development-line}

- **2026-03-31 — Référence à la page Superagent et à la documentation de Base44.** Base44 a ajouté des agents persistants connectés à Gmail, Calendar, Stripe, Slack, CRM et plus de 100 services. L'entreprise a testé la fonctionnalité auprès d'environ 20 % des utilisateurs avant son lancement. La documentation actuelle définit le modèle de fonctionnement : on configure l'agent dans le chat avec des connecteurs, des connaissances et une mémoire, puis on exécute des tâches planifiées ou des déclencheurs de connecteur.

## Ce qui a changé {#what-changed}

2026-03-31 — Base44 a fait passer les Superagents de la phase de test à la disponibilité générale. Ces agents persistants se connectent à Gmail, Calendar, Stripe, Slack, CRM et plus de 100 services. Base44 a testé la fonctionnalité auprès d'environ 20 % des utilisateurs avant la diffusion générale. La documentation décrit le flux de travail : on construit l'agent dans le chat, on lui attribue des connecteurs, des connaissances et une mémoire, puis on exécute des tâches planifiées ou des déclencheurs de connecteur.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-03-31, considérez la page intitulée Superagent de Base44 comme une piste de découverte et consultez la documentation officielle avant de choisir un flux de travail. Ne supposez pas un lancement ou un changement de fonctionnalité sans preuve complémentaire.

1. Créez un Superagent dans la section Superagents et décrivez la tâche précise dans le chat.
  — <https://docs.base44.com/superagents/creating-a-superagent>
2. Connectez l'outil requis via Brain → Integrations et définissez le mode minimal nécessaire : lecture seule ou gestion.
  — <https://docs.base44.com/superagents/creating-a-superagent>
3. Ajoutez des connaissances et des compétences, puis configurez une tâche planifiée ou un déclencheur de connecteur.
  — <https://docs.base44.com/Getting-Started/superagent>
4. Pour les applications dotées d'interfaces frontales personnalisées, installez la CLI, créez le backend et connectez le client SDK.
  — <https://docs.base44.com/developers/home>

## Bonnes pratiques {#best-practices}

- Commencez par une seule tâche récurrente et affinez le comportement de l'agent dans le chat en fonction des résultats observés.
  — <https://docs.base44.com/Getting-Started/superagent>
- Connectez d'abord les outils et accordez les permissions séparément ; utilisez la lecture seule plutôt que la gestion pour consulter des données.
  — <https://docs.base44.com/superagents/creating-a-superagent>
- Stockez les documents de référence dans Knowledge et les fichiers de travail dans Files ; ils constituent des périmètres de contexte distincts pour l'agent.
  — <https://docs.base44.com/Getting-Started/superagent>

## Remplacé par ceci {#superseded-by-this}

- 2026-03-31 — Base44 a dépassé la création d'applications en ajoutant les Superagents. Un Superagent opère sur l'ensemble de l'espace de travail, tandis qu'un agent d'application reste limité à une seule application.

## Points encore inconnus {#still-unknown}

- Aucune entrée de changelog officielle et datée de Base44 n'existe pour le 2026-03-31 ; une publication publique du fondateur confirme la date de lancement et la participation aux tests, mais ce n'est pas une note de version.
- Le format de réponse ne comporte pas de champs pour les constats d'événements et les nouveaux événements ; le fait du 2026-03-31 reste sous « Ce qui a changé ». Nous n'avons ajouté aucun nouvel événement daté sans source primaire fiable.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://www.linkedin.com/posts/maorshlomo_were-launching-base44-superagents-today-activity-7437524930801369088-xFcd | Présentation de Base44 Superagents : des agents IA pour tous | 2026-09-05 |
| https://docs.base44.com/Getting-Started/superagent | Créer un Superagent | 2026-09-05 |
| https://docs.base44.com/superagents/creating-a-superagent | Créer un Superagent | 2026-09-05 |
| https://docs.base44.com/developers/home | Plateforme développeur Base44 | 2026-09-05 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:base44`, fil `superagent`, 1 événement daté du 2026-03-31 au 2026-03-31.
- **Note pratique :** À partir du 2026-03-31, considérez la page intitulée Superagent de Base44 comme une piste de découverte et consultez la documentation officielle avant de choisir un flux de travail. Ne supposez pas un lancement ou un changement de fonctionnalité sans preuve complémentaire.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
