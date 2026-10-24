---
title: "Onklaud 5"
category: projects
date: 2026-07-02
tags: [onklaud, onklaud-5-development, project]
aliases: ["Onklaud 5"]
level: 2
source_sha256: 62808b08818dca5f095e7d5cf36641767dc713d71b367d3f05fb70d0ab5e9f98
translation: machine
translated_at: '2026-10-24'
---
# Onklaud 5 {#onklaud-5}

**Ligne de développement :** `project:onklaud` · fil `onklaud-5-development`  
**Dernier événement :** 2026-07-02 · 1 événement daté depuis le 2026-07-02 · **Recherché le :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

Onklaud 5 : un outil d'orchestration en Python destiné aux développeurs qui veulent qu'un brouillon de code soit évalué par plusieurs modèles de langage plutôt que par un seul modèle.

- recherche des solutions connues dans une bibliothèque ou dans la bibliothèque standard avant la génération ;
- exécute des passes de revue avec Kimi et GLM, puis une boucle d'arbitrage et une porte de qualité locale ;
- accepte une clé OpenRouter et peut utiliser un point de terminaison local compatible OpenAI.

## Ligne de développement {#development-line}

- **2026-07-02 — Le 2026-07-02, Onklaud 5 a été relié à un dépôt GitHub public.** Le 2026-07-02, la ligne de développement d'Onklaud 5 incluait un lien vers le dépôt GitHub KorroAi/onklaud-5. Ce lien daté établit une référence publique du dépôt pour le projet, mais n'établit ni une version, ni un ensemble de fonctionnalités, ni une modification du code.

## Ce qui a changé {#what-changed}

2026-06-22 — la documentation actuelle indique que le projet a exécuté sa suite de tests de performance interne, avec 20 réussites sur 35 pour Ponytail et 29 sur 30 pour les vérifications du pipeline. 2026-07-02 — Onklaud 5 a été rendu disponible via le dépôt relié ; la copie de travail actuelle configure Kimi K2.7 Code et GLM 5.2, mais aucune étiquette ni aucun commit daté ne prouve que cet état exact existait à la date de l'événement.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-07-02, les praticiens doivent considérer KorroAi/onklaud-5 comme la référence publique identifiée d'Onklaud 5 et examiner son contenu avant de s'y fier.

1. Clonez le dépôt, copiez `.env.example` vers `.env`, puis définissez `OPENROUTER_API_KEY` pour les appels à Kimi et GLM.
  — <https://github.com/KorroAi/onklaud-5>
2. Exécutez `python test_pipeline.py` comme test de fumée local fourni avant de le connecter à un flux de travail.
  — <https://github.com/KorroAi/onklaud-5>
3. Vérifiez la configuration avec `python council.py status`, puis soumettez un brouillon avec `python council.py dual --type code --prompt "..." --draft-file file.py` ; utilisez `loop` pour le chemin plus long qui comprend la pré-conception, la double revue, la porte et l'arbitrage.
  — <https://github.com/KorroAi/onklaud-5>

## Bonnes pratiques {#best-practices}

- Considérez `test_pipeline.py` comme un test de fumée structurel, et non comme une preuve de bout en bout avec les modèles hébergés : son point d'entrée par défaut exécute des vérifications locales et n'appelle jamais une API. Ajoutez un canari d'API non sensible et votre propre suite de tests avant de vous fier à un résultat de revue.
  — <https://github.com/KorroAi/onklaud-5/blob/master/test_pipeline.py>
- N'acceptez pas une boucle de council dégradée comme une revue normale : sans `OPENROUTER_API_KEY`, le code avertit explicitement que le mode loop fonctionnera de manière dégradée ; les autres modes API renvoient une erreur.
  — <https://github.com/KorroAi/onklaud-5/blob/master/council.py>
- Vérifiez que votre usage en production respecte la condition de chiffre d'affaires ou d'effectif, ou obtenez une licence commerciale ; la BSL ne se convertit en MIT que le 2030-06-22.
  — <https://github.com/KorroAi/onklaud-5/blob/master/LICENSE>

## Remplacé par ce qui suit {#superseded-by-this}

- La recommandation de considérer le dépôt actuel comme un logiciel libre sous licence permissive est obsolète : la licence est BSL 1.1, avec des droits de production conditionnels jusqu'à sa date de conversion en MIT (constatée le 2026-09-05).

## Points encore inconnus {#still-unknown}

- Aucune étiquette, version publiée ou commit archivé daté du 2026-07-02 n'était disponible ; le dépôt actuel ne peut donc pas prouver son contenu à cette date.
- Les sources actuelles appellent le dépôt Onklaud 5, mais la licence désigne l'œuvre sous licence par v3.2 ; aucune correspondance documentée entre ces appellations n'a été trouvée.
- Les affirmations de 57,1 % de tâches résolues et de qualité sont auto-déclarées ; aucune reproduction indépendante n'a été trouvée.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/KorroAi/onklaud-5 | KorroAi/onklaud-5 — dépôt et README d'Onklaud 5 | 2026-09-05 |
| https://github.com/KorroAi/onklaud-5/blob/master/council.py | Onklaud 5 council.py | 2026-09-05 |
| https://github.com/KorroAi/onklaud-5/blob/master/test_pipeline.py | Onklaud 5 test_pipeline.py | 2026-09-05 |
| https://github.com/KorroAi/onklaud-5/blob/master/LICENSE | Onklaud 5 Business Source License 1.1 | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:onklaud`, fil `onklaud-5-development`, 1 événement daté du 2026-07-02 au 2026-07-02.
- **Note pratique :** À partir du 2026-07-02, les praticiens doivent considérer KorroAi/onklaud-5 comme la référence publique identifiée d'Onklaud 5 et examiner son contenu avant de s'y fier.
- **Confiance :** moyenne. Les remplacements datés font autorité pour ce qui est obsolète.
