---
title: "Meta AI — Modèles d'IA générative"
category: organizations
tags: [cm3leon, generative-ai-models, meta-ai, meta_ai, organization]
aliases: ["Meta AI"]
level: 3
source_sha256: 2c05adfde07e14002b0a4c379a5a7f3ee4dac0117a94c1ef632c964509681ffe
translation: machine
translated_at: '2026-10-24'
---
# Meta AI — Modèles d'IA générative {#meta-ai-generative-ai-models}

**Ligne de développement :** `organization:meta-ai` · fil `generative-ai-models`  
**Événements :** 1 daté, 2023-07-17 → 2023-07-17 · **Recherche effectuée :** 2026-09-04 · confiance : moyenne

## Description {#what-it-is}

Meta AI est l'assistant de Meta destiné aux utilisateurs de WhatsApp, Instagram, Facebook, Messenger, de l'application Meta AI et de meta.ai.

- **Réponses web** — répond aux questions, recherche des contenus sur le web et les résume.
- **Plans et recherches** — établit des plans et mène des recherches.
- **Diapositives et médias** — les crée.
- **E-mail et agenda** — se connecte à ces services sur certains marchés.
- **Tâches récurrentes** — les exécute sur certains marchés.

Les fonctionnalités d'agent ne sont déployées que dans certains pays et sur certaines surfaces. Il s'agit de l'assistant produit de Meta, et non d'une version accessible aux utilisateurs du modèle de recherche CM3leon.

## Ligne de développement {#development-line}

- **2023-07-17 — Meta AI annonce CM3leon pour la génération de texte et d'images.** Un modèle de recherche publié fonctionne à la fois en texte vers image et en image vers texte. L'article fait état d'un FID de 4,88 en zero-shot sur MS-COCO et d'un calcul cinq fois moindre que les approches transformeurs comparables. Il s'agit de recherche, et non d'instructions pour accéder à l'actuel Meta AI.

## Évolutions {#what-changed}

La trajectoire de Meta AI va d'un projet de recherche multimodal distinct à un assistant grand public. Meta n'a pas confirmé de lien de succession directe entre CM3leon et l'assistant.

- 2023-07-17 — CM3leon : un modèle de recherche a été publié pour le texte vers image et l'image vers texte ; l'article fait état d'un FID de 4,88 en zero-shot sur MS-COCO et d'un calcul cinq fois moindre que les approches transformeurs comparables. Il s'agit de recherche, et non d'instructions pour accéder à l'actuel Meta AI.

- 2025-01-25 — La modification exacte n'est pas confirmée : l'événement n'a ni URL ni titre dans les documents disponibles.

- 2025-01-27 — Meta a commencé à déployer la mémoire dans les conversations personnelles et des réponses plus personnalisées aux États-Unis et au Canada ; la mémoire peut être supprimée.

- 2025-03-19 — Meta AI a commencé à se déployer dans 41 pays européens et 21 territoires d'outre-mer, d'abord sous forme de chat en six langues dans les applications de Meta.

- 2025-04-29 — Une application Meta AI distincte est apparue, basée sur Llama 4 et liée à meta.ai ; la voix, la génération d'images et la retouche d'images sont devenues disponibles dans la conversation.

- 2026-07 — Meta a indiqué déployer des fonctionnalités sur Muse Spark 1.1 : plans, connexions à l'e-mail et à l'agenda, diapositives, recherches et tâches récurrentes via l'application Meta AI et meta.ai, mais uniquement sur certains marchés.

## Comment l'utiliser {#how-to-use-this}

Au 2023-07-17, les praticiens qui suivent les capacités génératives de Meta AI devraient inclure CM3leon comme jalon de modèle texte-image et consulter sa documentation officielle avant de tirer des conclusions d'implémentation.

1. Ouvrez l'application Meta AI ou meta.ai, et vérifiez d'abord si la fonction nécessaire est disponible sur votre marché.
  — <https://about.fb.com/news/2026/07/meta-ai-muse-spark-doesnt-just-think-it-acts/amp/>
2. Pour une tâche unique, décrivez le résultat attendu et l'échéance : par exemple, un plan, une recherche, des diapositives ou un point quotidien.
  — <https://about.fb.com/news/2026/07/meta-ai-muse-spark-doesnt-just-think-it-acts/amp/>
3. Pendant que Meta AI prépare un rapport, un plan ou une présentation, ajustez directement dans la conversation l'objectif, le ton et les sections indésirables.
  — <https://about.fb.com/news/2026/07/meta-ai-muse-spark-doesnt-just-think-it-acts/amp/>
4. Dans une conversation de groupe prise en charge sur WhatsApp, Messenger ou Instagram, appelez l'assistant avec « @MetaAI », puis rédigez votre demande.
  — <https://about.fb.com/news/2025/03/europe-meet-your-newest-assistant-meta-ai/>
5. Pour une conversation entièrement privée, choisissez Chat incognito si ce mode est affiché dans votre interface.
  — <https://about.fb.com/news/2026/07/meta-ai-muse-spark-doesnt-just-think-it-acts/amp/>

## Bonnes pratiques {#best-practices}

- Définissez une tâche autonome comme un résultat plus un calendrier. Cette approche convient mieux aux points récurrents et aux rappels qu'une demande générale sans échéance.
  — <https://about.fb.com/news/2026/07/meta-ai-muse-spark-doesnt-just-think-it-acts/amp/>
- N'attendez pas en silence la réponse finale. Ajustez l'objectif, le ton et la longueur pendant que la tâche s'exécute.
  — <https://about.fb.com/news/2026/07/meta-ai-muse-spark-doesnt-just-think-it-acts/amp/>
- Vérifiez la région et la surface avant de lancer un flux de travail. Meta précise explicitement que les nouvelles fonctionnalités sont déployées de manière sélective.
  — <https://about.fb.com/news/2026/07/meta-ai-muse-spark-doesnt-just-think-it-acts/amp/>
- Pour une tâche de groupe, utilisez l'appel @MetaAI et non la mémoire personnelle. Meta a décrit la mémoire uniquement pour les conversations 1:1, et non pour les groupes.
  — <https://about.fb.com/news/2025/01/building-toward-a-smarter-more-personalized-assistant/>

## Remplacé par {#superseded-by-this}

- 2023-07-17 : considérer CM3leon comme la manière actuelle de travailler avec Meta AI est obsolète. Il s'agit d'un modèle de recherche, alors que l'assistant actuel est un produit grand public distinct.
- 2025-04-29 : considérer Meta AI uniquement comme un chatbot est obsolète sur les marchés pris en charge. En 2026-07, Meta indique qu'il gère des tâches, des plans, des recherches, des diapositives et certaines connexions.
- 2025-03-19 : la disponibilité du chat en Europe ne signifie pas le même jeu de fonctionnalités partout. Les capacités d'agent actuelles sont toujours décrites comme un déploiement sélectif.

## Points encore inconnus {#still-unknown}

- L'événement du 2025-01-25 n'a ni URL ni titre dans les documents disponibles ; son sujet exact et la modification concernée ne sont donc pas établis. La publication de Meta du 2025-01-27 est listée séparément et n'est pas considérée comme cet événement.
- CM3leon et le Meta AI actuel sont peut-être deux sujets distincts portant le même nom Meta : l'un est un modèle de recherche, l'autre un assistant grand public. Aucun élément ne montre que CM3leon ait été déployé dans Meta AI.
- Le jeu de fonctionnalités, les langues, les applications prises en charge et l'accès aux connexions e-mail et agenda dépendent du marché et du compte. Une connexion en direct à meta.ai depuis le navigateur de recherche n'a pas été confirmée.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://ai.meta.com/blog/generative-ai-text-images-cm3leon/ | Présentation de CM3leon, un modèle génératif plus efficace et à l'état de l'art pour le texte et les images | 2026-09-04 |
| https://about.fb.com/news/2025/01/building-toward-a-smarter-more-personalized-assistant/ | Vers un assistant plus intelligent et plus personnalisé | 2026-09-04 |
| https://about.fb.com/news/2025/03/europe-meet-your-newest-assistant-meta-ai/ | Europe, découvrez votre nouvel assistant : Meta AI | 2026-09-04 |
| https://about.fb.com/news/2025/04/introducing-meta-ai-app-new-way-access-ai-assistant/ | Présentation de l'application Meta AI : une nouvelle façon d'accéder à votre assistant IA | 2026-09-04 |
| https://about.fb.com/news/2026/07/meta-ai-muse-spark-doesnt-just-think-it-acts/amp/ | Meta AI ne se contente pas de réfléchir, il agit | 2026-09-04 |

## Synthèse pour agents {#agent-brief}

- **Sujet :** `organization:meta-ai`, fil `generative-ai-models`, 1 événement daté, 2023-07-17 → 2023-07-17.
- **Note pratique :** Au 2023-07-17, les praticiens qui suivent les capacités génératives de Meta AI devraient inclure CM3leon comme jalon de modèle texte-image et consulter sa documentation officielle avant de tirer des conclusions d'implémentation.
- **Confiance :** moyenne. Les éléments datés remplacés définissent ce qui est obsolète.
