---
title: "Lyria"
category: projects

tags: [lyria, lyria-development, project]
aliases: ["Lyria"]
level: 2
source_sha256: 03cca4b143d80a5686729addd2a6ca8d21a8c9ce1b7810efcff8d5a1287e532f
translation: machine
translated_at: '2026-10-24'
---
# Lyria {#lyria}

**Ligne de développement :** `project:lyria` · fil `lyria-development`  
**Dernier événement :** - · 0 daté depuis - · **Recherche effectuée :** 2026-09-05 · confiance : élevée

## Description {#what-it-is}

Lyria est le système de génération musicale de Google DeepMind, destiné aux créateurs et aux développeurs. Lyria 3.5 est disponible via Flow Music, Gemini, l'API Gemini, AI Studio et Google Vids.

- Des prompts textuels produisent de la musique et des paroles.
- Les pistes générées portent un tatouage SynthID.

Le discours produit actuel indique que les pistes peuvent aller de courts extraits jusqu'à trois minutes. Utilisez-le pour de la musique originale guidée par prompt, puis vérifiez chaque résultat avant toute publication.

## Ligne de développement {#development-line}

- L'événement daté n'a pas encore fait l'objet d'une rédaction ; les informations connues figurent dans les sections ci-dessous.

## Évolutions {#what-changed}

- 2026-02-18 — Lyria 3 a été intégré à l'application Gemini en version bêta, pour des pistes de 30 secondes guidées par texte ou par image.
- 2026-03-25 — Google a ouvert en préversion pour développeurs Lyria 3 et Lyria 3 Pro dans l'API Gemini et AI Studio. Le modèle Clip vise des ressources de 30 secondes, et Pro des morceaux allant jusqu'à environ trois minutes.
- 2026-07-29 — Lyria 3.5 a été lancé dans Google Flow Music, avec des améliorations annoncées sur la structure mélodique, le respect des paroles, l'expression et la prononciation vocales, ainsi que le contrôle du tempo et de la durée.
- 2026-07-30 — Le lancement lié à Flow Music correspond à Lyria 3.5, et non à un modèle Lyria distinct ni à un premier lancement. L'annonce principale de Google est datée du 2026-07-29, tandis que Google Corée a publié son annonce locale le 2026-07-30.
- 2026-09-04 — Lyria 3.5 est devenu disponible mondialement dans Gemini sur le web et sur mobile, ainsi que dans l'API Gemini, AI Studio et Google Vids.

## Mode d'emploi {#how-to-use-this}

Au 2026-07-30, ne considérez pas l'URL de Flow Music seule comme un événement de développement documenté de Lyria. Consultez la ressource liée et la publication sous-jacente avant de vous y fier.

1. Ouvrez Google Flow Music ou Gemini, connectez-vous et vérifiez que la fonctionnalité de génération musicale est disponible pour votre compte.
  — <https://www.flowmusic.app/>
2. Choisissez un genre et une orientation vocale ou instrumentale, puis précisez dans le prompt l'usage prévu, le tempo, la durée, l'instrumentation et l'orientation des paroles.
  — <https://blog.google/innovation-and-ai/products/gemini-app/better-tracks-lyria-gemini/>
3. Pour une intégration, utilisez l'API Gemini ou AI Studio. Utilisez le mode texte pour un brief de piste, ou le mode compositeur pour diriger des sections telles que l'intro, le couplet et le pont.
  — <https://blog.google/innovation-and-ai/technology/developers-tools/lyria-3-developers/>
4. Écoutez la piste générée et vérifiez qu'elle correspond au projet visé avant de l'utiliser.
  — <https://deepmind.google/models/lyria/>

## Bonnes pratiques {#best-practices}

- Décrivez des contrôles musicaux concrets — tempo, tonalité, dynamique, style vocal et progression par sections — plutôt que de vous fier uniquement à une étiquette de genre.
  — <https://blog.google/innovation-and-ai/technology/developers-tools/lyria-3-developers/>
- Utilisez l'option courte orientée extraits pour les prototypes rapides et les ressources destinées aux réseaux sociaux. Réservez la génération de morceaux complets aux travaux plus longs et structurés.
  — <https://blog.google/innovation-and-ai/technology/developers-tools/lyria-3-developers/>
- Traitez la musique générée comme une ébauche : vérifiez que la piste correspond au brief créatif avant publication.
  — <https://deepmind.google/models/lyria/>

## Remplacé par {#superseded-by-this}

- 2026-02-18 — La limite de 30 secondes des pistes de Lyria 3 dans l'application Gemini est remplacée, pour l'usage grand public actuel, par les options de pistes courtes ou plus longues de Lyria 3.5.
- 2026-07-29 — Les recommandations relatives à Lyria 3 sont remplacées là où Lyria 3.5 est disponible. Utilisez le modèle le plus récent pour de meilleures paroles, voix, musicalité et contrôle du tempo et de la durée.

## Points toujours inconnus {#still-unknown}

- Le schéma de réponse requis ne comporte ni champ event_findings ni champ new_events ; les ajouts datés et la correction sont donc conservés dans what_changed plutôt qu'émis dans des champs distincts.
- La page d'accueil de Flow Music n'a fourni aucun texte produit exploitable dans la page récupérée ; elle n'est incluse qu'en tant qu'URL produit fournie et surface d'accès actuelle.
- Les documents publics de Google ne fournissent ni scores de benchmark indépendants, ni inventaire public complet des données d'entraînement de Lyria 3.5.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://www.flowmusic.app/ | Google Flow Music | 2026-09-05 |
| https://blog.google/innovation-and-ai/models-and-research/google-labs/lyria-3-5/ | Introducing Lyria 3.5 in Google Flow Music | 2026-09-05 |
| https://blog.google/intl/ko-kr/company-news/technology/lyria-3-5-kr/ | Lyria 3.5 launch in Google Flow Music | 2026-09-05 |
| https://deepmind.google/models/model-cards/lyria-3-5/ | Lyria 3.5 Model Card | 2026-09-05 |
| https://blog.google/innovation-and-ai/products/gemini-app/better-tracks-lyria-gemini/ | Create your best tracks yet with Lyria 3.5 in Gemini | 2026-09-05 |
| https://blog.google/innovation-and-ai/products/gemini-app/lyria-3/ | A new way to express yourself: Gemini can now create music | 2026-09-05 |
| https://blog.google/innovation-and-ai/technology/developers-tools/lyria-3-developers/ | Build with Lyria 3, our newest music generation model | 2026-09-05 |
| https://deepmind.google/models/lyria/ | Lyria 3.5 | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:lyria`, fil `lyria-development`, 0 événement daté - → -.
- **Remarque pratique :** Au 2026-07-30, ne considérez pas l'URL de Flow Music seule comme un événement de développement documenté de Lyria. Consultez la ressource liée et la publication sous-jacente avant de vous y fier.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi quant à ce qui est obsolète.
