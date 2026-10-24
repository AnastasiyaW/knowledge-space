---
title: "xAI — Développement du modèle Grok"
category: organizations
tags: [grok-model-development, grok_4, grok_release, organization, xai]
aliases: ["xAI"]
level: 3
source_sha256: 492f986f56cf04ebed559de76b26664e1fabaf1c7d7d0ea04d849d19f7211519
translation: machine
translated_at: '2026-10-24'
---
# xAI — Développement du modèle Grok {#xai-grok-model-development}

**Ligne de développement :** `organization:xai` · fil `grok-model-development`  
**Événements :** 1 événement daté, 2025-07-08 → 2025-07-08 · **Recherche effectuée le :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

xAI développe Grok et fournit une API destinée aux équipes qui créent des flux de travail de chat, de programmation et d'agents.

Capacités :

- Grok 4.6 accepte du texte et des images et renvoie du texte ;
- Grok 4.6 prend en charge un raisonnement configurable ;
- Grok prend en charge l'appel de fonctions, la recherche Web/X et l'exécution de code ;
- les API Voice et Imagine sont distinctes.

Limite : Grok 4.6 dispose d'une fenêtre de contexte de 500k tokens ; en dessous de 200k tokens d'entrée, son prix API est de 2 $ / 0,50 $ / 6 $ par 1M de tokens d'entrée / d'entrée en cache / de sortie.

Pour une nouvelle intégration de texte ou de programmation, utilisez le modèle actuel plutôt que le slug Grok 4 d'origine.

## Ligne de développement {#development-line}

- **2025-07-08 — Jalon de développement de Grok 4 chez xAI.** Grok 4 et Grok 4 Heavy sont devenus disponibles pour les abonnés et dans l'API xAI, avec l'utilisation native d'outils et la recherche Web/X en temps réel.

## Évolutions {#what-changed}

2024-08-15 — « non censuré » est une étiquette de positionnement non vérifiée. Aucune publication officielle ne relie cette mention à une version de Grok, un point de terminaison, une politique ou un changement de disponibilité.

2025-07-08 — La publication sociale liée n'a pas pu être consultée. Le premier changement de produit confirmé date du 2025-07-09 : Grok 4 et Grok 4 Heavy sont devenus disponibles pour les abonnés et dans l'API xAI, avec l'utilisation native d'outils et la recherche Web/X en temps réel.

2026-05-15 — `grok-4-0709` et plusieurs anciens slugs Grok ont été retirés ; les appels vers l'ancien slug Grok 4 sont redirigés vers `grok-4.3`.

Au 2026-09-04, Grok 4.6 est disponible dans l'API depuis le 2026-08-12 et constitue le modèle par défaut actuel pour les travaux de programmation et de texte général.

## Mode d'emploi {#how-to-use-this}

Au 2025-07-08, les praticiens qui évaluent Grok de xAI devraient réexaminer leurs hypothèses de choix de modèle à partir du jalon Grok 4. Vérifiez les capacités et les conditions d'accès actuelles auprès des sources primaires avant de l'adopter.

1. Créez un compte xAI Console et ajoutez des crédits.
  — <https://docs.x.ai/developers/quickstart>
2. Créez une clé API et chargez-la via `XAI_API_KEY`.
  — <https://docs.x.ai/developers/quickstart>
3. Sélectionnez `grok-4.6` pour une nouvelle intégration de texte général ou de programmation ; utilisez un slug daté lorsque la cohérence des sorties est importante.
  — <https://docs.x.ai/developers/models>
4. Envoyez la première requête à l'API Responses avec le SDK xAI ou un client OpenAI pointant vers `https://api.x.ai/v1`.
  — <https://docs.x.ai/developers/quickstart>
5. Activez la recherche Web ou la recherche X lorsque la réponse dépend d'informations actuelles.
  — <https://docs.x.ai/developers/models>

## Bonnes pratiques {#best-practices}

- Épinglez un slug de modèle daté pour un comportement de production reproductible. Utilisez `-latest` uniquement si les mises à jour automatiques de modèle sont souhaitées.
  — <https://docs.x.ai/developers/models>
- Traitez les questions d'actualité comme un cas d'utilisation d'outils. Activez la recherche côté serveur plutôt que de vous fier à la date de coupure des données d'entraînement du modèle.
  — <https://docs.x.ai/developers/models>
- Pour les conversations répétées, utilisez une `prompt_cache_key` ou un `x-grok-conv-id` stable. Gardez le préfixe en ajout seul et surveillez `cached_tokens`.
  — <https://docs.x.ai/developers/advanced-api-usage/prompt-caching/best-practices>
- Dimensionnez en fonction à la fois des RPS et des TPM. Gérez les HTTP 429 avec un backoff exponentiel borné.
  — <https://docs.x.ai/developers/rate-limits>

## Remplacé par ceci {#superseded-by-this}

- 2026-05-15 — La cible de déploiement `grok-4-0709`, issue de l'ère 2025, est obsolète : xAI la retire et redirige les appels vers `grok-4.3` ; choisissez explicitement un remplacement pour maîtriser le raisonnement et le prix.
- 2026-08-12 — Les recommandations par défaut pour les nouveaux travaux de texte général et de programmation sont passées à `grok-4.6` ; cela ne retire pas en soi le modèle `grok-4.3`, toujours pris en charge.

## Points encore inconnus {#still-unknown}

- La référence du 2024-08-15 est une URL de recherche sur X, et non une note de version archivée ; elle n'a pas permis d'établir l'état « non censuré » revendiqué.
- L'URL de statut x.com du 2025-07-08 était inaccessible au moment de la relecture ; son libellé n'a donc pas été utilisé.
- Aucune publication officielle ni aucune page de documentation spécifique au modèle en chinois simplifié n'a été trouvée. Les sources porteuses de faits sont en anglais.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://x.ai/news/grok-4 | Grok 4 | SpaceXAI | 2026-09-04 |
| https://docs.x.ai/developers/migration/may-15-retirement | Retrait des modèles Grok le 15 mai 2026 | SpaceXAI Docs | 2026-09-04 |
| https://docs.x.ai/developers/release-notes | Notes de version | SpaceXAI Docs | 2026-09-04 |
| https://docs.x.ai/developers/models | Modèles Grok et tarifs | SpaceXAI Docs | 2026-09-04 |
| https://docs.x.ai/developers/grok-4-6 | Grok 4.6 | SpaceXAI Docs | 2026-09-04 |
| https://docs.x.ai/developers/quickstart | Démarrage rapide de l'API Grok : obtenir votre clé API | SpaceXAI Docs | 2026-09-04 |
| https://docs.x.ai/developers/advanced-api-usage/prompt-caching/best-practices | Bonnes pratiques et FAQ | SpaceXAI Docs | 2026-09-04 |
| https://docs.x.ai/developers/rate-limits | Limites de débit | SpaceXAI Docs | 2026-09-04 |

## Synthèse pour agents {#agent-brief}

- **Sujet :** `organization:xai`, fil `grok-model-development`, 1 événement daté 2025-07-08 → 2025-07-08.
- **Note pratique :** Au 2025-07-08, les praticiens qui évaluent Grok de xAI devraient réexaminer leurs hypothèses de choix de modèle à partir du jalon Grok 4. Vérifiez les capacités et les conditions d'accès actuelles auprès des sources primaires avant de l'adopter.
- **Confiance :** moyenne. Les entrées « remplacé par » ci-dessus font foi pour ce qui est obsolète.
