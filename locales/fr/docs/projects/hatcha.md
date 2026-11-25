---
title: "HATCHA — Référence du dépôt public"
category: projects
date: 2026-06-27
tags: [hatcha, project, public-repository-reference]
aliases: ["HATCHA"]
level: 2
source_sha256: b7f3dcb2c0a3bb9f437c160f094637a6c155916d1aa7b55836cd5a9f8a521b12
translation: machine
translated_at: '2026-10-24'
---
# HATCHA — Référence du dépôt public {#hatcha-public-repository-reference}

**Ligne de développement :** `project:hatcha` · fil `public-repository-reference`  
**Dernier événement :** 2026-06-27 · 1 événement daté depuis le 2026-06-27 · **Consulté le :** 2026-09-05 · confiance : moyenne

## Description {#what-it-is}

HATCHA est un reverse CAPTCHA open source de monday.com, destiné à Next.js et Express. Il émet un défi de calcul, ne conserve la réponse que côté serveur, signe le hash et l'expiration avec un jeton HMAC, puis renvoie un jeton de vérification.

- Cinq défis intégrés : exécuter des tâches de calcul pour la vérification d'agents.
- Composants React : fournir l'intégration côté client et les wrappers de providers.
- Gestionnaires serveur : router les requêtes de vérification dans Next.js et Express.
- Générateurs personnalisés : enregistrer des défis non standard.

Les défis intégrés sont limités à 30 secondes.

Cela constitue un filtre supplémentaire pour des scénarios réservés aux agents à faible risque, et non une preuve d'identité, d'autorité ou de sécurité de l'agent.

## Ligne de développement {#development-line}

- **2026-06-27 — Référence au dépôt GitHub de HATCHA.** Le monorepo se répartit en paquets core, React et serveur, avec des adaptateurs pour Next.js et Express.

## Ce qui a changé {#what-changed}

2026-06-27 — monday.com a publié HATCHA sous forme de projet public sous licence MIT. Le monorepo se répartit en paquets core, React et serveur, avec des adaptateurs pour Next.js et Express.

## Mode d'emploi {#how-to-use-this}

Nous pouvons considérer le dépôt GitHub de HATCHA comme la source d'implémentation depuis la référence du 2026-06-27. Vérifiez son contenu et l'état de ses versions avant de vous appuyer sur une fonctionnalité particulière.

1. Installer les paquets React et serveur : `npm install @mondaycom/hatcha-react @mondaycom/hatcha-server`.
  — <https://github.com/mondaycom/HATCHA>
2. Créer un gestionnaire de route Next.js avec `createHatchaHandler` et transmettre un `HATCHA_SECRET` serveur unique.
  — <https://github.com/mondaycom/HATCHA>
3. Encapsuler l'application dans `HatchaProvider`, importer les styles et appeler `requestVerification` avant l'action cible réservée aux agents.
  — <https://usehatcha.dev/>
4. Vérifier le jeton de vérification émis côté serveur avant d'autoriser l'action protégée ; ne pas exposer le défi ni la réponse comme secrets côté client.
  — <https://github.com/mondaycom/HATCHA>

## Bonnes pratiques {#best-practices}

- Placer HATCHA devant des workflows réservés aux agents à faible risque, des démos ou des bacs à sable, mais conserver une authentification, une autorisation, des journaux d'audit, des contrôles anti-abus et des plafonds de dépense distincts pour les actions sur les données ou les opérations financières.
  — <https://news.lavx.hu/article/monday-com-releases-hatcha-a-reverse-captcha-for-ai-agents>
- Garder `HATCHA_SECRET` strictement côté serveur, utiliser une valeur robuste et définir des limites de débit en complément d'un modèle de menace explicite.
  — <https://news.lavx.hu/article/monday-com-releases-hatcha-a-reverse-captcha-for-ai-agents>
- Enregistrer un générateur de défi personnalisé pour les cas d'usage non standard, tout en conservant la vérification côté serveur et une durée de vie (TTL) bornée.
  — <https://github.com/mondaycom/HATCHA>

## Éléments remplacés {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Points inconnus {#still-unknown}

- Le dépôt ne publie aucune GitHub Release ; les sources primaires n'identifient pas le commit ni la version exacts correspondant au 2026-06-27.
- Aucun billet de changelog primaire n'est daté du 2026-06-27 ; les détails reposent sur une publication du 2026-06-26 et la documentation actuelle, ce qui laisse les évolutions ultérieures non confirmées.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/mondaycom/HATCHA | GitHub — mondaycom/HATCHA | 2026-09-05 |
| https://usehatcha.dev/ | HATCHA — Reverse CAPTCHA pour agents IA | 2026-09-05 |
| https://news.lavx.hu/article/monday-com-releases-hatcha-a-reverse-captcha-for-ai-agents | Monday.com publie HATCHA, un reverse CAPTCHA pour agents IA | 2026-09-05 |
| https://developer-community.monday.com/ai-category-25/welcoming-agents-to-the-ecosystem-5206 | Welcoming Agents to the Ecosystem | 2026-09-05 |
| https://developer.monday.com/api-reference/docs/build-on-monday-with-ai | Build on monday.com with AI | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:hatcha`, fil `public-repository-reference`, 1 événement daté du 2026-06-27 au 2026-06-27.
- **Note pratique :** Nous pouvons considérer le dépôt GitHub de HATCHA comme la source d'implémentation depuis la référence du 2026-06-27, tout en vérifiant son contenu et l'état de ses versions avant de nous appuyer sur une fonctionnalité particulière.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
