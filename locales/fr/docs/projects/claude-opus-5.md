---
title: "Claude Opus 5"
category: projects
date: 2026-07-24
tags: [claude-opus-5, claude-opus-5-development, claude_opus_5, project]
aliases: ["Claude Opus 5"]
level: 3
source_sha256: a6eadfd07a1d2dbd72793f6dc9c14186c76d74fc4974758fa3566deb8fa875a9
translation: machine
translated_at: '2026-10-24'
---
# Claude Opus 5 {#claude-opus-5}

**Ligne de développement :** `project:claude-opus-5` · fil `claude-opus-5-development`  
**Dernier événement :** 2026-07-24 · 1 événement daté depuis le 2026-07-24 · **Recherche effectuée le :** 2026-09-07 · confiance : élevée

## Présentation {#what-it-is}

Le modèle Opus actif d'Anthropic, destiné aux équipes qui développent des agents de programmation à exécution longue et des workflows d'entreprise.

- Tâches complexes de programmation, d'utilisation d'outils, de contexte long, de vision et de traitement de documents.
- Contexte de 1M de tokens et sortie maximale standard de 128K ; le plafond de 300K de l'API Batch n'est disponible qu'en bêta.
- 5 $ par million de tokens en entrée et 25 $ par million de tokens en sortie.

Utilisez-le lorsque votre propre évaluation justifie le coût en tokens de sortie et en latence.

## Ligne de développement {#development-line}

- **2026-07-24 — Anthropic a publié une annonce d'actualité sur Claude Opus 5.** Le 2026-07-24, Anthropic a publié un article d'actualité officiel dont le lien indique qu'il concerne Claude Opus 5. Les éléments disponibles ne permettent pas d'établir les capacités, la disponibilité, la tarification ou les détails techniques de cette annonce ; cette entrée d'historique n'enregistre donc que le jalon de développement daté.

## Changements {#what-changed}

2026-07-24 — Claude Opus 5 a été lancé sous le nom `claude-opus-5`, avec un contexte de 1M de tokens, une sortie maximale de 128K, une réflexion adaptative activée par défaut, 5 niveaux d'effort et des modifications d'outils en cours de conversation en bêta.  
2026-08-01 — Claude Opus 5 est devenu pris en charge dans l'aperçu de recherche Dreams.  
2026-08-05 — Claude Opus 4.1 a été retiré ; Anthropic a désigné Claude Opus 5 comme voie de migration.  
2026-08-19 — Claude Opus 5 est devenu compatible avec l'API Claude, avec le jeu d'outils d'utilisation de l'ordinateur (computer use) passé en GA et le jeu d'outils client d'utilisation du navigateur (browser use) récemment lancé.  
2026-08-20 — Ces jeux d'outils sont devenus disponibles pour Claude Opus 5 sur Google Cloud.  
2026-09-01 — L'API Claude a ajouté, en bêta, la modification de l'effort message par message pour Claude Opus 5, tout en préservant le cache de prompt.

## Mode d'emploi {#how-to-use-this}

1. Créez une requête Messages API avec `model="claude-opus-5"`, définissez `max_tokens` et envoyez l'historique complet des messages pour une conversation multi-tours.
  — <https://platform.claude.com/docs/en/claude_api_primer>
2. Lors de la migration d'une intégration Opus 4.8, sélectionnez les blocs de réponse par `type`, renvoyez les blocs de réflexion sans modification après les appels d'outils, et supprimez `thinking.disabled` avec `xhigh` ou `max`.
  — <https://platform.claude.com/docs/en/models/opus-5/whats-new-opus-5>
3. Commencez avec l'effort `high` par défaut, effectuez un balayage des niveaux d'effort sur vos propres évaluations, puis choisissez `low`, `medium`, `xhigh` ou `max` ; définissez un `max_tokens` élevé avec `xhigh` ou `max`.
  — <https://platform.claude.com/docs/en/build-with-claude/effort>
4. Pour 1 session Claude Code, lancez `claude --model claude-opus-5`.
  — <https://support.claude.com/en/articles/11940350-claude-code-model-configuration>

## Bonnes pratiques {#best-practices}

- Fournissez dès le départ la spécification complète de la tâche pour les travaux complexes, et délimitez explicitement le périmètre pour les travaux ciblés.
  — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5>
- Demandez la longueur de réponse visible dont vous avez besoin ; l'effort contrôle le volume de réflexion, et non de manière fiable la longueur de la réponse.
  — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5>
- Commencez à `high`, puis ne modifiez l'effort qu'après un balayage des niveaux d'effort sur vos propres évaluations ; abaissez-le lorsque la qualité se maintient, et réservez `xhigh` ou `max` aux travaux sensibles à la capacité.
  — <https://platform.claude.com/docs/en/build-with-claude/effort>
- Supprimez les instructions de vérification finale ou de sous-agent vérificateur héritées, sauf si la tâche les exige réellement ; avec Opus 5, elles peuvent entraîner une sur-vérification et un gaspillage de tokens.
  — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5>

## Remplacé par {#superseded-by-this}

- 2026-07-24 — L'hypothèse Opus 4.8 selon laquelle la réflexion adaptative est optionnelle et que `content[0]` est toujours du texte est obsolète pour Claude Opus 5 ; les blocs de réponse doivent être traités selon leur type.
- 2026-07-24 — `thinking: {"type": "disabled"}` avec `xhigh` ou `max` n'est plus une requête Claude Opus 5 valide ; elle renvoie une erreur HTTP 400.
- 2026-08-05 — `claude-opus-4-1-20250805` est retiré et renvoie désormais une erreur ; la cible de migration indiquée par Anthropic est Claude Opus 5.
- 2026-08-19 — Considérer `computer_toolset_20260801` comme une version bêta uniquement sur l'API Claude est obsolète ; le jeu d'outils est en GA, et les versions bêta antérieures restent disponibles.

## Points toujours inconnus {#still-unknown}

- Aucune source de cet ensemble n'établit les quotas propres à chaque compte, la capacité régionale ou la tarification contractuelle ; vérifiez la console cible ou le catalogue cloud avant le déploiement.
- Les affirmations de l'annonce de lancement concernant les benchmarks et l'accès anticipé n'ont pas été reproduites indépendamment ici.
- Aucune source officielle trouvée lors de cette recherche n'indique que Fable 5.1 retire ou remplace Claude Opus 5 ; la page actuelle du modèle indique toujours Opus 5 comme actif.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://www.anthropic.com/news/claude-opus-5 | Présentation de Claude Opus 5 | 2026-09-07 |
| https://platform.claude.com/docs/en/release-notes/overview | Notes de version de Claude Platform | 2026-09-07 |
| https://platform.claude.com/docs/en/models/opus-5/overview | Claude Opus 5 | 2026-09-07 |
| https://platform.claude.com/docs/en/models/opus-5/whats-new-opus-5 | Nouveautés de Claude Opus 5 | 2026-09-07 |
| https://platform.claude.com/docs/en/claude_api_primer | Introduction à l'utilisation de l'API Claude | 2026-09-07 |
| https://platform.claude.com/docs/en/build-with-claude/effort | Effort | 2026-09-07 |
| https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5 | Prompting Claude Opus 5 | 2026-09-07 |
| https://support.claude.com/en/articles/11940350-claude-code-model-configuration | Configuration du modèle Claude Code | 2026-09-07 |
| https://platform.claude.com/docs/zh-CN/release-notes/overview | Claude Platform 发布说明 | 2026-09-07 |

## Brief agent {#agent-brief}

- **Sujet :** `project:claude-opus-5`, fil `claude-opus-5-development`, 1 événement daté du 2026-07-24 au 2026-07-24.
- **Note pratique :** voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
