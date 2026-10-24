---
title: "Claude Mythos"
category: projects

tags: [claude-mythos, claude-mythos-security-findings, claude_mythos_security_findings, project]
aliases: ["Claude Mythos"]
level: 3
source_sha256: 881b9c435411d28add32e46b68dc44d222dd0e249fa83bbdb00721871cd684cf
translation: machine
translated_at: '2026-10-24'
---
# Claude Mythos {#claude-mythos}

**Ligne de développement :** `project:claude-mythos` · fil `claude-mythos-security-findings`  
**Dernier événement :** - · 0 daté depuis · **Recherché le :** 2026-09-05 · confiance : moyenne

## Description {#what-it-is}

Gamme de modèles d'Anthropic accessible uniquement sur invitation, réservée aux défenseurs cyber approuvés et aux équipes de logiciels critiques.

- Analyse les bases de code appartenant à l'organisation pour détecter des vulnérabilités contextuelles et proposer des correctifs.
- Accès direct réservé aux partenaires approuvés de Project Glasswing.
- Alimente les analyses de Claude Security sans exposer d'accès direct au modèle.

## Ligne de développement {#development-line}

- La ligne datée n'a pas encore fait l'objet d'un compte rendu ; les éléments connus figurent dans les sections ci-dessous.

## Évolutions {#what-changed}

- 2026-04-07 — Anthropic a annoncé Claude Mythos Preview et Project Glasswing. La version Preview a été réservée aux partenaires de lancement et à plus de 40 organisations d'infrastructures critiques, pour des travaux défensifs et non pour une diffusion générale.
- 2026-04-10 — Les recommandations datées d'Anthropic identifient le modèle comme Claude Mythos Preview et présentent cette étape comme une directive opérationnelle postérieure au lancement, et non comme une deuxième sortie de modèle. L'IA réduit les délais de découverte de vulnérabilités et d'exploitation ; Anthropic recommande de combler au plus vite le retard de correctifs et de traiter en priorité les entrées KEV.
- 2026-06-09 — Claude Mythos 5 (`claude-mythos-5`) a remplacé la version Preview pour les participants éligibles de Glasswing. Il repose sur le même modèle de base que Fable 5, sans les garde-fous cyber pour les utilisateurs approuvés ; les limites documentées sont un contexte de 1 M, une sortie de 128 K, et 10 $ / 50 $ par million de tokens en entrée / sortie.
- 2026-08-21 — La bêta publique de Claude Security pour Enterprise a commencé à exécuter des analyses de dépôts sur Mythos 5, en renvoyant des résultats et des correctifs suggérés sans requête directe adressée à Mythos.
- 2026-08-31 — Claude Mythos 5.1 a été désigné comme Covered Model à disponibilité limitée pour les partenaires approuvés.
- 2026-09-01 — Claude Mythos 5.1 est devenu le modèle Mythos actuel à accès direct, toujours accessible uniquement sur invitation via Project Glasswing.

## Mode d'emploi {#how-to-use-this}

À la date du 2026-04-10, n'apportez aucune modification opérationnelle sur la base de cette ligne tant que nous n'avons pas récupéré et examiné la publication ou la source sous-jacente.

1. Activez Claude Security dans les paramètres de l'organisation, sous Claude Enterprise.
  — <https://support.claude.com/en/articles/14661296-use-claude-security>
2. Connectez un compte GitHub autorisé, puis sélectionnez dans Claude Security un dépôt GitHub.com ou GitHub Enterprise Server appartenant à l'organisation.
  — <https://support.claude.com/en/articles/14661296-use-claude-security>
3. Lancez l'analyse, puis examinez pour chaque résultat la catégorie CWE, la gravité, le niveau de confiance, le chemin de reproduction et le correctif suggéré.
  — <https://claude.com/blog/bringing-claude-mythos-5-to-more-defenders>
4. Ouvrez un correctif proposé dans Claude Code, puis faites-le relire, tester et approuver par une personne avant mise en œuvre.
  — <https://claude.com/blog/bringing-claude-mythos-5-to-more-defenders>
5. Pour un usage direct de Mythos 5.1, obtenez l'approbation de Project Glasswing auprès de l'équipe de compte d'Anthropic, d'AWS ou de Google Cloud ; utilisez l'identifiant de modèle `claude-mythos-5-1` uniquement une fois l'accès accordé.
  — <https://platform.claude.com/docs/en/models/mythos-5-1/overview>

## Bonnes pratiques {#best-practices}

- Ne lancez d'analyses que sur le code appartenant à l'organisation ou sur lequel elle dispose des droits nécessaires.
  — <https://support.claude.com/en/articles/14661296-use-claude-security>
- Considérez les analyses comme des éléments probabilistes, et non comme un substitut à la validation ; les paramètres de gravité ne sont pas configurables.
  — <https://support.claude.com/en/articles/14661296-use-claude-security>
- Corrigez les systèmes exposés sur Internet dans les 24 heures suivant la disponibilité d'un exploit ; traitez d'abord les entrées KEV et hiérarchisez le reste de la file avec EPSS.
  — <https://claude.com/blog/preparing-your-security-program-for-ai-accelerated-offense>
- N'envoyez un rapport de vulnérabilité qu'après vérification humaine ; incluez le chemin de code vulnérable, une reproduction exécutable, un correctif proposé, et signalez le recours à l'IA.
  — <https://claude.com/blog/preparing-your-security-program-for-ai-accelerated-offense>
- Commencez le tri des alertes par IA en accès en lecture seule, et mesurez l'accord avec un relecteur humain avant d'étendre l'automatisation.
  — <https://claude.com/blog/preparing-your-security-program-for-ai-accelerated-offense>

## Remplacé par {#superseded-by-this}

- 2026-06-09 — Claude Mythos Preview est déprécié ; les utilisateurs éligibles ont été migrés vers Claude Mythos 5.
- 2026-09-01 — Claude Mythos 5 n'est plus la cible actuelle à accès direct ; les partenaires éligibles doivent migrer vers Claude Mythos 5.1.
- 2026-08-21 — Les requêtes directes ne sont plus nécessaires pour Mythos : Claude Security renvoie des résultats défensifs bornés sans exposer le modèle.

## Points encore inconnus {#still-unknown}

- L'entrée du 2026-04-10 ne comporte ni URL ni texte ; son affirmation exacte ne peut donc pas être rapprochée de façon concluante des recommandations datées d'Anthropic.
- La documentation actuelle indique Mythos 5 pour les analyses Claude Security et Mythos 5.1 pour l'accès direct des partenaires ; elle ne confirme pas que Claude Security soit passé à la version 5.1.
- Aucune procédure publique en libre-service pour l'accès direct à Mythos 5.1 n'est documentée.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://www.anthropic.com/research/mythos-preview | Évaluation des capacités de cybersécurité de Claude Mythos Preview | 2026-09-05 |
| https://www.anthropic.com/glasswing | Project Glasswing : sécuriser les logiciels critiques à l'ère de l'IA | 2026-09-05 |
| https://claude.com/blog/preparing-your-security-program-for-ai-accelerated-offense | Préparer votre programme de sécurité à une offensive accélérée par l'IA | 2026-09-05 |
| https://www.anthropic.com/news/claude-fable-5-mythos-5 | Claude Fable 5 et Claude Mythos 5 | 2026-09-05 |
| https://platform.claude.com/docs/en/models/mythos-5/overview | Claude Mythos 5 - Documentation de la plateforme Claude | 2026-09-05 |
| https://claude.com/blog/bringing-claude-mythos-5-to-more-defenders | Ouvrir les capacités de cybersécurité de Claude Mythos 5 à davantage de défenseurs | 2026-09-05 |
| https://platform.claude.com/docs/en/models/mythos-5-1/overview | Claude Mythos 5.1 - Documentation de la plateforme Claude | 2026-09-05 |
| https://support.claude.com/en/articles/14661296-use-claude-security | Utiliser Claude Security | 2026-09-05 |
| https://support.claude.com/en/articles/15425695-covered-models | Covered Models | 2026-09-05 |
| https://platform.claude.com/docs/en/about-claude/model-deprecations | Dépréciations de modèles - Documentation de la plateforme Claude | 2026-09-05 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:claude-mythos`, fil `claude-mythos-security-findings`, 0 événement daté - → -.
- **Remarque pratique :** À la date du 2026-04-10, n'apportez aucune modification opérationnelle sur la base de cette ligne tant que la publication ou la source sous-jacente n'a pas pu être récupérée et examinée.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
