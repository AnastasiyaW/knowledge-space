---
title: "Windows-Copilot-API"
category: projects
date: 2026-06-22
tags: [project, windows-copilot-api, windows-copilot-api-development]
aliases: ["Windows-Copilot-API"]
level: 2
source_sha256: 2e3b9ff587cb79dd9e98d7d55ea0c0d3f20eaec0db72e0164dc23a6a293a6f81
translation: machine
translated_at: '2026-10-24'
---
# Windows-Copilot-API {#windows-copilot-api}

**Ligne de développement :** `project:windows-copilot-api` · fil `windows-copilot-api-development`  
**Dernier événement :** 2026-06-22 · 1 événement daté depuis le 2026-06-22 · **Recherche effectuée le :** 2026-09-06 · niveau de confiance : élevé

## Présentation {#what-it-is}

Windows-Copilot-API est un pont multiplateforme non officiel. Il transforme une session Copilot grand public authentifiée en appels Python ou en point de terminaison de chat local compatible OpenAI.

- Chat Python, streaming et identifiants de conversation
- Points de terminaison locaux `/v1/chat/completions` et `/v1/models`
- Connexion par navigateur et session locale persistée

## Ligne de développement {#development-line}

- **2026-06-22 — Le dépôt Windows-Copilot-API et le site Microsoft Copilot ont été liés.** Le 2026-06-22, des liens publics ont relié le dépôt GitHub Windows-Copilot-API au site web Copilot de Microsoft. Cela établit un point de référence public daté pour la ligne de développement du projet, mais n'établit ni une version publiée, ni un ensemble de fonctionnalités, ni une propriété, ni un statut de déploiement. Aucun texte source original ni aucune preuve indépendante corroborante n'a été fourni.

## Changements {#what-changed}

- 2026-06-22 — Windows-Copilot-API a ajouté un déploiement Docker, une limitation de débit, des corrections de gestion de l'hôte et du port, de la documentation de dépannage et une correction de la CLI. Le pont local/compatible OpenAI principal avait déjà été intégré le 2026-06-19.
- 2026-06-23 — Une mise à jour de correctifs et de diagnostic a été intégrée.
- 2026-06-24 — La connexion a été étendue aux comptes Google en plus des comptes Microsoft, et la gestion automatique de la clearance Cloudflare a été intégrée.

Le dépôt ne répertorie aucune release GitHub ; les commits, et non les numéros de version, constituent donc les repères historiques fiables.

## Mode d'emploi {#how-to-use-this}

1. Ne faites pas transiter une charge de travail Copilot grand public en production par ce projet : les conditions d'utilisation grand public interdisent d'utiliser des outils ou des programmes informatiques, tels que des bots ou des scrapers, pour accéder à Copilot.
  — <https://www.microsoft.com/en-us/microsoft-copilot/for-individuals/termsofuse>
2. Pour une intégration Microsoft 365 prise en charge, utilisez les API Microsoft 365 Copilot distinctes : obtenez les licences Microsoft 365 Copilot et les licences équivalentes E3/E5 requises, enregistrez une application Entra, acquérez un jeton utilisateur et appelez la surface d'API `/copilot` de Graph.
  — <https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/copilot-apis-overview>
3. Pour l'analyse historique du code, épinglez l'état du commit du 2026-06-22 ; n'attribuez pas à cette date le comportement ultérieur de connexion Google ou de clearance automatique.
  — <https://github.com/sums001/Windows-Copilot-API/commits/master/>

## Bonnes pratiques {#best-practices}

- Considérez l'accès grand public comme interdit plutôt que comme solution de repli en production. Microsoft interdit explicitement l'accès programmatique par bots ou scrapers à Copilot.
  — [Conditions d'utilisation de Microsoft Copilot](https://www.microsoft.com/en-us/microsoft-copilot/for-individuals/termsofuse)
- Ne traitez pas la branche mutable `master` comme un artefact de publication. Épinglez un SHA de commit, car le dépôt ne possède aucune release GitHub.
  — [Releases de Windows-Copilot-API](https://github.com/sums001/Windows-Copilot-API/releases)
- Lors de l'examen du fonctionnement historique, séparez les modifications ultérieures d'OAuth et de clearance automatique de l'état du 2026-06-22.
  — [Historique des commits de Windows-Copilot-API](https://github.com/sums001/Windows-Copilot-API/commits/master/)
- Choisissez les API Microsoft Graph Copilot sous licence lorsque nous exigeons une intégration d'entreprise prise en charge avec les données et la gouvernance de Microsoft 365.
  — [Présentation des API Microsoft 365 Copilot](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/copilot-apis-overview)

## Remplacé par {#superseded-by-this}

- 2026-06-12 — La recommandation d'utiliser ce pont avec Copilot grand public est remplacée. Les conditions explicites pour le grand public interdisent les outils, les programmes informatiques, les bots et les scrapers pour l'accès à Copilot.
- 2026-06-24 — Les consignes de configuration réservées aux comptes Microsoft sont remplacées. Le dépôt a mis à jour la connexion pour prendre en charge les comptes Microsoft et Google.
- 2026-06-24 — Les consignes de clearance Cloudflare antérieures à l'automatisation sont remplacées, pour les clients interactifs, par la gestion automatique de la clearance. L'utilisation en service sans interface dépend toujours d'une reconnexion hors bande dans un navigateur visible lorsque la clearance expire.

## Points encore inconnus {#still-unknown}

- La description « About » du dépôt annonce un accès à GPT-4 et GPT-5, mais son README détaillé expose un seul modèle générique `copilot`, sans sélecteur de modèle ; le modèle exact en amont ne peut pas être vérifié.
- Le README actuel est mutable et le dépôt ne possède aucune release GitHub ; le comportement actuel ne peut donc pas être rétrodaté au 2026-06-22 sans inspection spécifique à un commit.
- La vue d'historique de GitHub établit des dates calendaires, mais pas assez de détails d'horodatage ou de fuseau horaire pour ordonner précisément les plusieurs commits du 2026-06-22.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/sums001/Windows-Copilot-API | Dépôt Windows-Copilot-API | 2026-09-06 |
| https://copilot.microsoft.com/ | Microsoft Copilot | 2026-09-06 |
| https://github.com/sums001/Windows-Copilot-API/commits/master/ | Historique des commits de Windows-Copilot-API | 2026-09-06 |
| https://github.com/sums001/Windows-Copilot-API/blob/master/README.md | README de Windows-Copilot-API | 2026-09-06 |
| https://github.com/sums001/Windows-Copilot-API/commit/dfbe3a91112640db7ff991511cf00d3176d80d53 | Commit OAuth comptes Google + Microsoft | 2026-09-06 |
| https://github.com/sums001/Windows-Copilot-API/commit/878a2ff1ec5607b5c417a57a9ff0a7daa6e5b48e | Commit de clearance CF automatique | 2026-09-06 |
| https://github.com/sums001/Windows-Copilot-API/releases | Releases de Windows-Copilot-API | 2026-09-06 |
| https://www.microsoft.com/en-us/microsoft-copilot/for-individuals/termsofuse | Conditions d'utilisation de Microsoft Copilot | 2026-09-06 |
| https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/copilot-apis-overview | Présentation des API Microsoft 365 Copilot | 2026-09-06 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:windows-copilot-api`, fil `windows-copilot-api-development`, 1 événement daté du 2026-06-22 au 2026-06-22.
- **Note pratique :** voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est devenu obsolète.
