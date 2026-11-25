---
title: "Tutu MCP"
category: projects
date: 2026-06-18
tags: [project, tutu, tutu-mcp, tutu-mcp-development]
aliases: ["Tutu MCP"]
level: 2
source_sha256: 9cec33f279f135cf02b47cb8241816dbf75386e049bd11aae210dd346d6bcbbf
translation: machine
translated_at: '2026-10-24'
---
# Tutu MCP {#tutu-mcp}

**Ligne de développement :** `project:tutu-mcp` · fil `tutu-mcp-development`  
**Dernier événement :** 2026-06-18 · 1 événement daté depuis le 2026-06-18 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

Tutu MCP est un point de terminaison MCP en Streamable HTTP pour Claude, Claude Code, ChatGPT, OpenCode et les agents compatibles.

- Recherche de vols, de trains, de bus, de trains de banlieue et d'hôtels.
- Détails des chambres et avis des utilisateurs.
- Transfert vers le lien de checkout.

Le serveur sélectionne les options et transfère vers le checkout sans accepter de paiements. Vérifiez la commande finale sur la page Tutu avant tout paiement.

## Ligne de développement {#development-line}

- **2026-06-18 — Point de terminaison public de Tutu MCP mentionné.** Le 2026-06-18, une mise à jour du développement de Tutu MCP mentionnait le point de terminaison MCP public à l'adresse mcp.tutu.ru/mcp.

## Modifications {#what-changed}

- 2026-06-18 — ajout de la reconnaissance des trains de marque, y compris Lastochka et les voitures à deux étages.
- 2026-06-22 — Tutu a annoncé l'accès des agents IA à la recherche et à la réservation de vols, de trains, de bus, de trains de banlieue et d'hôtels.
- 2026-08-19 — 2026-08-21 — Tutu a organisé un hackathon autour du serveur : 71 équipes ont participé et 42 ont soumis des projets. Cela a élargi les scénarios frontend et agents sans modifier le contrat de point de terminaison confirmé.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-06-18, les praticiens devraient considérer https://mcp.tutu.ru/mcp comme le point de terminaison public de Tutu MCP à évaluer ou à intégrer, tout en vérifiant ses exigences de protocole et d'accès.

1. Ajoutez le point de terminaison `https://mcp.tutu.ru/mcp` comme MCP distant en Streamable HTTP, sans authentification.
  — <https://mcp.tutu.ru/mcp>
2. Dans Claude Code, exécutez `claude mcp add --transport http tutu https://mcp.tutu.ru/mcp`.
  — <https://mcp.tutu.ru/mcp>
3. Transmettez à l'agent les villes de départ et d'arrivée, les dates, le budget, le type de transport et les limites ; comparez les itinéraires par prix et par durée.
  — <https://github.com/chemisttt/tutu-mcp-kit/blob/main/docs/MCP.md>
4. Vérifiez les conditions finales et finalisez la réservation sur Tutu ; les applications tierces ne doivent pas accepter de paiement à la place de Tutu.
  — <https://github.com/chemisttt/tutu-mcp-kit>

## Bonnes pratiques {#best-practices}

- N'ouvrez pas le point de terminaison dans un navigateur comme une API : utilisez un proxy de même origine pour les clients navigateur afin que CORS ne bloque pas les requêtes.
  — <https://github.com/chemisttt/tutu-mcp-kit/blob/main/docs/MCP.md>
- Ne remplacez pas les offres par des données factices lorsque le MCP en production renvoie des résultats vides : affichez l'état vide ou diagnostiquez l'échec.
  — <https://github.com/chemisttt/tutu-mcp-kit>
- Pour les voyages en plusieurs parties, interrogez séparément les transports et les hôtels, dédoublonnez les résultats et construisez les liens de checkout uniquement à partir du `checkout_ref` renvoyé.
  — <https://github.com/chemisttt/tutu-mcp-kit/blob/main/docs/MCP.md>

## Remplacé par {#superseded-by-this}

- 2026-07-16 — l'enregistrement du panier des voyageurs et les liens de checkout à usage unique ont remplacé le flux dans lequel l'agent s'arrêtait sur la page de saisie des données. La date provient d'un message secondaire et doit être confirmée par une source primaire.

## Points encore inconnus {#still-unknown}

- Le schéma de réponse ne contient pas les champs `event_findings` et `new_events` ; les mises à jour de développement restent dans `what_changed` sans champs non documentés.
- Une source secondaire confirme la reconnaissance des trains de marque pour la mise à jour du 2026-06-18, mais sa date de publication n'était pas disponible.
- Aucune source primaire datée de Tutu n'a été trouvée pour les statuts de publication des 2026-06-23, 2026-07-01, 2026-07-08, 2026-07-09 et 2026-07-16 : ces dates restent donc une chronologie produit non confirmée.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://mcp.tutu.ru/mcp | Tutu MCP — ИИ спланирует поездку за вас | 2026-09-05 |
| https://companies.rbc.ru/news/Q1Aa56ondv/servis-puteshestvij-tutu-otkryil-bronirovanie-poezdok-cherez-ii-agentov/ | Сервис путешествий Туту открыл бронирование поездок через ИИ-агентов | 2026-09-05 |
| https://hackathon2026.tutu.ru/ | ИИ-хакатон — Туту MCP | 2026-09-05 |
| https://github.com/chemisttt/tutu-mcp-kit/blob/main/docs/MCP.md | tutu-mcp-kit: MCP operator guide | 2026-09-05 |
| https://github.com/chemisttt/tutu-mcp-kit | chemisttt/tutu-mcp-kit | 2026-09-05 |

## Brief pour agents {#agent-brief}

- **Sujet :** `project:tutu-mcp`, fil `tutu-mcp-development`, 1 événement daté, du 2026-06-18 au 2026-06-18.
- **Note pratique :** À partir du 2026-06-18, les praticiens devraient considérer https://mcp.tutu.ru/mcp comme le point de terminaison public de Tutu MCP à évaluer ou à intégrer, tout en confirmant indépendamment son protocole et ses exigences d'accès actuels.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
