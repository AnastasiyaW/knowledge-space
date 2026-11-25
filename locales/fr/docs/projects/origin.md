---
title: "Origin — Hébergement de code"
category: projects
date: 2026-08-19
tags: [code-hosting, cursor, origin, project]
aliases: ["Origin"]
level: 3
source_sha256: 97e865b7b96e512d7f0b1f143265e5d8cfd458c79dc705617459c7dc9792e70d
translation: machine
translated_at: '2026-10-24'
---
# Origin — Hébergement de code {#origin-code-hosting}

**Ligne de développement :** `project:origin` · fil `code-hosting`  
**Dernier événement :** 2026-08-19 · 1 événement daté depuis le 2026-08-19 · **Recherche effectuée le :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

Origin est la forge Git en bêta anticipée de Cursor, destinée aux utilisateurs payants de Cursor.

- Dépôts natifs : héberger le code avec Origin comme source de vérité.
- Miroir GitHub : mettre en miroir des dépôts tant que GitHub reste la source de vérité.
- Recherche et navigation dans le code : rechercher et inspecter le code du dépôt.
- Revue de pull requests : examiner les diffs et les vérifications avant la fusion.
- Connexions d'agents : connecter les agents cloud et les automatisations aux dépôts.

Utilisez-le pour des workflows de code natifs à Cursor ou pour un miroir GitHub, mais considérez que son API et ses contrats de bêta sont susceptibles de changer.

## Ligne de développement {#development-line}

- **2026-08-19 — Origin a atteint une étape de développement de l'hébergement de code.** Dépôts natifs, miroir GitHub, navigation dans le code, pull requests et agents Cursor ; la page de lancement elle-même est datée du 2026-08-17.

## Ce qui a changé {#what-changed}

- 2026-08-19 — Origin est entré dans le déploiement de la bêta anticipée : dépôts natifs, miroir GitHub, navigation dans le code, pull requests et agents Cursor ; la page de lancement elle-même est datée du 2026-08-17.
- 2026-08-26 — L'API publique a ajouté les labels de dépôt et les annotations des check runs ; la structure des payloads des webhooks de relecteurs a changé.
- 2026-08-27 — La spécification de l'API est devenue plus adaptée à la génération de code et a ajouté des échéances facultatives pour les check runs.
- 2026-08-28 — Les échéances dépassées ont commencé à faire passer les check runs en cours à l'état expiré (`timed_out`) ; l'API a ajouté les archives tar des dépôts et la liste des fichiers de comparaison.
- 2026-08-29 — La prise en charge de l'API a été étendue aux relecteurs demandés, aux fils de revue résolubles, aux commentaires en ligne et aux commentaires de revue atomiques.
- 2026-09-01 — Des webhooks de suppression de dépôt et de mise à jour des métadonnées ont été ajoutés.
- 2026-09-02 — Les endpoints de liste des check suites et des check runs ne renvoient plus que la dernière tentative, ce qui masque les relances remplacées dans les listes habituelles.
- 2026-09-03 — La liste des check runs et des commentaires de pull request a reçu des filtres pour l'interrogation incrémentale.
- 2026-09-04 — Le `slug` de l'application a été retiré des métadonnées d'acteur de l'API et des webhooks ; les intégrations doivent utiliser l'`id` de l'application et le `displayName` facultatif.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-08-19, les praticiens qui évaluent des workflows d'hébergement de code devraient inclure Origin dans leurs recherches, tout en vérifiant ses capacités exactes et sa disponibilité dans la documentation primaire.

1. Vérifiez que votre compte a accès à Origin, réservez un espace de noms pour la base de code et choisissez-le avec soin : il ne peut pas être renommé pendant la bêta.
  — <https://cursor.com/docs/origin>
2. Créez un dépôt natif depuis Codebase → New, sélectionnez la visibilité Internal ou Private, puis copiez son URL de clonage.
  — <https://cursor.com/docs/origin/create-repository>
3. Authentifiez-vous avec la CLI d'Origin, clonez le dépôt ou ajoutez le remote Git HTTPS standard, puis poussez votre branche.
  — <https://cursor.com/docs/origin/git>
4. Pour un dépôt GitHub existant, utilisez Sync from GitHub ; Origin devient un miroir, et GitHub reste l'référence pour les pushes.
  — <https://cursor.com/docs/origin/mirror-github>
5. Ouvrez une pull request après avoir poussé une branche, examinez les vérifications et les diffs, demandez des relecteurs, puis fusionnez une fois la revue et la CI validées.
  — <https://cursor.com/docs/origin/pull-requests>
6. Attachez des agents cloud Cursor ou des automatisations lorsque vous voulez que les agents clonent, créent des branches, committent, poussent ou ouvrent des pull requests sur le dépôt.
  — <https://cursor.com/docs/origin/integrations>

## Bonnes pratiques {#best-practices}

- Traitez un dépôt synchronisé avec GitHub comme un miroir : les Issues GitHub, la configuration des Actions et les secrets ne sont pas copiés dans Origin, et GitHub reste la source de vérité.
  — <https://cursor.com/docs/origin/mirror-github>
- Choisissez l'espace de noms avant d'activer Origin ; les espaces de noms de bêta ne peuvent pas être modifiés ni mis à jour après leur réservation.
  — <https://cursor.com/docs/origin>
- Pour les intégrations, régénérez le code à partir de la spécification OpenAPI actuelle et migrez la gestion de l'identité des applications de `slug` vers `id` plus `displayName` facultatif.
  — <https://cursor.com/docs/api/origin/changelog>
- Interrogez les nouveaux commentaires de pull request avec les filtres `since` ou `until` plutôt que de parcourir à répétition tout l'historique des commentaires.
  — <https://cursor.com/docs/api/origin/changelog>

## Remplacé par ce qui suit {#superseded-by-this}

- 2026-08-27 — La règle selon laquelle un `deadlineAt` expiré ne modifie pas l'état d'un check run a été remplacée le 2026-08-28 : les check runs en cours expirés se terminent désormais en `timed_out`.
- 2026-09-02 — Les intégrations qui s'appuient sur les endpoints de liste pour exposer chaque tentative de check sont obsolètes : les réponses de liste habituelles ne conservent que la dernière tentative ; récupérez un ID précis pour les tentatives remplacées.
- 2026-09-04 — Les intégrations utilisant le `slug` de l'application comme identifiant d'acteur sont obsolètes ; utilisez l'`id` de l'application et le `displayName` facultatif.

## Points encore inconnus {#still-unknown}

- La date d'événement fournie est le 2026-08-19, mais la page de lancement principale de Cursor est datée du 2026-08-17 ; nous retenons le 2026-08-19 comme date d'événement.
- Aucune preuve indépendante d'usage en production d'Origin n'a été trouvée ; la disponibilité des fonctionnalités est documentée comme déployée par étapes et en bêta anticipée. La plupart des changements postérieurs au lancement relevés sont des modifications d'API plutôt qu'un récit daté de sorties produit.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://cursor.com/changelog/origin-code-hosting | Origin Code Hosting · Cursor | 2026-09-05 |
| https://cursor.com/docs/origin | Origin | Cursor Docs | 2026-09-05 |
| https://cursor.com/docs/origin/create-repository | Create an Origin repository | Cursor Docs | 2026-09-05 |
| https://cursor.com/docs/origin/git | Clone, Push & Pull | Cursor Docs | 2026-09-05 |
| https://cursor.com/docs/origin/mirror-github | Mirror a GitHub repository | Cursor Docs | 2026-09-05 |
| https://cursor.com/docs/origin/pull-requests | Pull requests | Cursor Docs | 2026-09-05 |
| https://cursor.com/docs/origin/integrations | Origin integrations | Cursor Docs | 2026-09-05 |
| https://cursor.com/docs/api/origin/changelog | Origin API Changelog | Cursor Docs | 2026-09-05 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:origin`, fil `code-hosting`, 1 événement daté du 2026-08-19 au 2026-08-19.
- **Note pratique :** À partir du 2026-08-19, les praticiens qui évaluent des workflows d'hébergement de code devraient inclure Origin dans leurs recherches, tout en vérifiant ses capacités exactes et sa disponibilité dans la documentation primaire.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
