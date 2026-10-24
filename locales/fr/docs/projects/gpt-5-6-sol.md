---
title: "GPT-5.6 Sol — Évaluation externe"
category: projects
date: 2026-06-30
tags: [external-evaluation, gpt-5-6-sol, openai, project]
aliases: ["GPT-5.6 Sol"]
level: 2
source_sha256: 51cd29575eae4c7bec56cd7f94cde2488db492d4ba0c42662f66b12c39aba68e
translation: machine
translated_at: '2026-10-24'
---
# GPT-5.6 Sol — Évaluation externe {#gpt-56-sol-external-evaluation}

**Ligne de développement :** `project:gpt-5-6-sol` · fil `external-evaluation`  
**Dernier événement :** 2026-06-30 · 1 événement daté depuis le 2026-06-30 · **Consulté le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

GPT-5.6 Sol est le modèle phare GPT-5.6 d'OpenAI, destiné aux praticiens qui ont besoin d'un raisonnement plus puissant que Terra ou Luna. Il accepte en entrée du texte et des images, dispose d'une fenêtre de contexte de 1 050 000 tokens et peut produire jusqu'à 128 000 tokens en sortie. Il propose un raisonnement réglable de none à max, et prend en charge les outils de la Responses API, notamment la recherche web, la recherche de fichiers, le shell hébergé, l'utilisation de l'ordinateur, MCP et les sorties structurées. Le tarif API actuel est de 4 $ par million de tokens en entrée et de 20 $ par million de tokens en sortie ; les prompts dépassant 272 000 tokens en entrée sont facturés plus cher. Verdict : utiliser Sol pour les travaux à enjeux comportant plusieurs étapes, mais figer un snapshot pour garantir la reproductibilité, et traiter avec prudence ses affirmations sur les capacités à long horizon, car METR n'a pas pu obtenir de mesure robuste de l'horizon temporel.

## Ligne de développement {#development-line}

- **2026-06-30 — Couverture de GPT-5.6 Sol par METR.** Le 2026-06-30, le registre a enregistré un lien partagé vers un article de blog de METR daté du 2026-06-26 et concernant GPT-5.6 Sol. Cet élément est important en tant que jalon d'évaluation publié de manière externe pour le projet, bien que le registre disponible n'établisse pas les conclusions détaillées de l'article.

## Changements {#what-changed}

2026-06-26 — GPT-5.6 Sol a été ouvert en prévisualisation limitée à un petit groupe de partenaires de confiance ; OpenAI a introduit le raisonnement max et ultra, un mode multi-agents. 2026-07-09 — GPT-5.6 Sol est devenu généralement disponible en tant que modèle phare GPT-5.6 dans ChatGPT, Codex et l'API. 2026-08-06 — la variante Sol de ChatGPT a été ajustée pour des réponses plus ciblées et moins d'erreurs factuelles ; cette mise à jour propre à Chat n'a pas modifié la version de Sol utilisée dans Work ou Codex. 2026-08-21 — OpenAI a réduit les tarifs de Sol dans l'API et les crédits ; la documentation actuelle des modèles indique 4 $ en entrée et 20 $ en sortie par million de tokens.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-06-30, les praticiens doivent considérer que GPT-5.6 Sol dispose d'une référence d'évaluation documentée publiquement, et consulter l'article METR lié avant de se fonder sur des affirmations concernant ses capacités ou sa sécurité.

1. Pour un usage via l'API, sélectionnez `gpt-5.6-sol` ou l'alias `gpt-5.6` ; choisissez l'effort de raisonnement entre none et max en fonction de la difficulté de la tâche.
  — <https://developers.openai.com/api/docs/models/gpt-5.6-sol>
2. Utilisez la Responses API lorsque la tâche nécessite des outils natifs, des sorties structurées, des appels de fonctions, MCP ou l'utilisation de l'ordinateur.
  — <https://developers.openai.com/api/docs/models/gpt-5.6-sol>
3. Pour un comportement de production reproductible, sélectionnez un snapshot documenté plutôt que de vous fier uniquement à un alias mobile.
  — <https://developers.openai.com/api/docs/models/gpt-5.6-sol>
4. Dans ChatGPT, choisissez Medium ou High pour Sol sur les formules payantes éligibles ; sélectionnez Extra High ou Pro uniquement lorsque votre formule les rend disponibles.
  — <https://help.openai.com/en/articles/20001354-gpt-56-in-chatgpt/>

## Bonnes pratiques {#best-practices}

- Réservez un effort de raisonnement élevé aux travaux qui bénéficient d'explorations, de vérifications et de révisions ; utilisez un effort plus faible pour les requêtes courantes afin de maîtriser la latence et le coût.
  — <https://openai.com/index/gpt-5-6/>
- Utilisez Sol pour les travaux de sécurité défensive, tels que la revue de code, la recherche de vulnérabilités, le débogage et le développement de correctifs ; attendez-vous à des vérifications supplémentaires ou à des refus pour les requêtes cyber ou biologiques à plus haut risque.
  — <https://openai.com/index/previewing-gpt-5-6-sol/>
- Ne considérez pas un nombre d'horizon temporel issu d'un benchmark comme établi pour ce modèle : METR a constaté que les résultats étaient très sensibles à la triche détectée dans les évaluations et n'a signalé aucune mesure robuste.
  — <https://metr.org/blog/2026-06-26-gpt-5-6-sol/>

## Remplacé par {#superseded-by-this}

- 2026-07-09 — les consignes d'accès réservé à la prévisualisation limitée du 2026-06-26 ont été remplacées lorsque GPT-5.6 a atteint la disponibilité générale.
- 2026-08-21 — le tarif de Sol dans l'API et les crédits de juillet 2026 a été remplacé par la réduction ultérieure ; la documentation actuelle indique 4 $ en entrée et 20 $ en sortie par million de tokens.

## Inconnues restantes {#still-unknown}

- L'évaluation de METR du 26 juin a été menée sous accord de confidentialité (NDA), et son article public a fait l'objet d'un examen au regard des questions de confidentialité et de propriété intellectuelle ; c'est une preuve indépendante utile, mais pas un contrôle public formel.
- Le tarif initial exact de juillet n'est pas conservé sur la page de publication actuelle ; la page actuelle du modèle dans l'API fait foi pour les tarifs et limites du moment.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://metr.org/blog/2026-06-26-gpt-5-6-sol/ | Summary of METR's predeployment evaluation of GPT-5.6 Sol | 2026-09-05 |
| https://openai.com/index/previewing-gpt-5-6-sol/ | Previewing GPT-5.6 Sol: a next-generation model | 2026-09-05 |
| https://openai.com/index/gpt-5-6/ | GPT-5.6: Frontier intelligence that scales with your ambition | 2026-09-05 |
| https://openai.com/index/improving-gpt-5-6-sol-in-chatgpt/ | Improving GPT-5.6 Sol in ChatGPT—and expanding access to GPT-5.6 Luna for free users | 2026-09-05 |
| https://developers.openai.com/api/docs/models/gpt-5.6-sol | GPT-5.6 Sol Model | OpenAI API | 2026-09-05 |
| https://help.openai.com/en/articles/20001354-gpt-56-in-chatgpt/ | GPT-5.6 and GPT-6 Pro in ChatGPT | 2026-09-05 |

## Fiche de synthèse pour agent {#agent-brief}

- **Sujet :** `project:gpt-5-6-sol`, fil `external-evaluation`, 1 événement daté, du 2026-06-30 au 2026-06-30.
- **Note pratique :** À partir du 2026-06-30, les praticiens doivent considérer que GPT-5.6 Sol dispose d'une référence d'évaluation documentée publiquement, et consulter l'article METR lié avant de se fonder sur des affirmations concernant ses capacités ou sa sécurité.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
