---
title: "Odysseus"
category: projects
date: 2026-06-01
tags: [odysseus, project]
aliases: ["Odysseus"]
level: 3
source_sha256: 36a4e91a28561f3062f0e30738352247b64666c485bce3e51ea51f1f52001784
translation: machine
translated_at: '2026-10-24'
---
# Odysseus {#odysseus}

**Ligne de développement :** `project:odysseus` · fil `odysseus`  
**Dernier événement :** 2026-06-01 · 1 événement daté depuis le 2026-06-01 · **Investigué le :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

Odysseus est un espace de travail auto-hébergé destiné aux utilisateurs qui souhaitent une interface de type ChatGPT ou Claude, avec des modèles locaux ou accessibles par API.

- Chat et agents : exécution d'outils, MCP, fichiers, shell, skills et mémoire.
- Recherche et documents : gère la recherche approfondie, la comparaison de modèles, les documents, le courriel, les notes, les tâches, le calendrier et un Cookbook de service de modèles.

## Ligne de développement {#development-line}

- **2026-06-01 — Dépôt GitHub d'Odysseus relié.** Le 2026-06-01, nous avons consigné des liens vers le dépôt GitHub pewdiepie-archdaemon/odysseus et son point de terminaison Git. Ce lien indique un emplacement source, mais nous n'avons pas vérifié le contenu du dépôt, l'état des versions ni les fonctionnalités.

## Changements {#what-changed}

- 2026-06-01 — Le projet recherchait des contributeurs pour les tests multiplateformes, la documentation, la revue de sécurité ainsi que la fiabilité du Cookbook et des modèles locaux. Un rapport sur les identifiants de première exécution, publié le même jour, a mis en évidence des difficultés lors de la prise en main.
- 2026-07-12 — Un commit sur `main` a porté le numéro de version du code à 1.0.2.
- 2026-08-25 — Un commit sur `main` a préparé un correctif d'image 1.0.3.

## Mode d'emploi {#how-to-use-this}

Au 2026-06-01, nous utilisons le dépôt GitHub d'Odysseus enregistré comme référence source, et nous vérifions séparément son état opérationnel.

1. Clonez `https://github.com/odysseus-dev/odysseus.git`. Utilisez `main` pour le code validé plutôt que la branche `dev` par défaut.
  — <https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/README.md>
2. Pour Docker, copiez `.env.example` vers `.env`, exécutez `docker compose up -d --build` et attendez que les conteneurs soient opérationnels (healthy).
  — <https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/website/setup.md>
3. Ouvrez `http://localhost:7000`, récupérez le mot de passe administrateur temporaire dans `docker compose logs odysseus`, puis modifiez-le dans les paramètres.
  — <https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/website/setup.md>
4. Pour Windows natif au lieu de Docker, exécutez `powershell -ExecutionPolicy Bypass -File .\launch-windows.ps1`. Configurez Ollama à l'adresse `http://localhost:11434/v1` pour un modèle local sous Windows.
  — <https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/website/setup.md>

## Bonnes pratiques {#best-practices}

- Utilisez `main` pour le code validé. Choisissez `dev` uniquement si vous souhaitez délibérément les dernières modifications.
  — <https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/README.md>
- Gardez l'authentification activée et le contournement pour localhost désactivé pour les déploiements accessibles par le réseau. Utilisez HTTPS et un proxy de confiance, un VPN ou une couche d'accès privé au-delà de localhost.
  — <https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/SECURITY.md>
- Gardez les ports des modèles et des services de support en interne. Protégez `.env`, les données, les journaux, les fichiers téléversés, les fichiers de session, les bases de données, les sauvegardes et les identifiants d'API.
  — <https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/SECURITY.md>
- Limitez l'accès au shell, au système de fichiers, au courriel, à MCP et au service de modèles aux administrateurs de confiance. Les outils shell et système de fichiers des agents ne disposent ni de bac à sable ni de filtrage des sorties.
  — <https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/THREAT_MODEL.md>
- Testez en conditions réelles le chemin exact (Docker, natif, WSL, GPU et fournisseur) avant de vous y fier. La couverture des installations à partir de zéro reste un élément prioritaire de la feuille de route.
  — <https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/ROADMAP.md>

## Éléments remplacés {#superseded-by-this}

- 2026-07-12 — La version 1.0.2 remplace la v1.0 comme version actuelle du code sur `main`, après le commit de mise à jour du numéro de version.
- 2026-08-25 — Un commit préparant un correctif d'image 1.0.3 remplace la 1.0.2 comme cible de développement actuelle sur `main`, mais ce n'est pas une version GitHub officielle (Release).
- 2026-09-05 — `odysseus-dev/odysseus` remplace `pewdiepie-archdaemon/odysseus` comme espace de noms canonique pour le clonage, via une redirection ; la date du transfert est inconnue.

## Points toujours inconnus {#still-unknown}

- Nous n'avons pas de date ni de conditions consignées pour le passage de `pewdiepie-archdaemon` à `odysseus-dev`. La redirection établit uniquement la route canonique actuelle.
- Nous ne disposons pas d'un instantané reconstituable du code au 2026-06-01 ; la documentation actuelle et les commits ultérieurs ne permettent donc pas de vérifier les capacités de juin.
- Nous n'avons trouvé aucune version GitHub officielle (Release) ni aucune version stable ou étiquette (tag) immuable publiée par le projet.
- Nous n'avons trouvé aucune documentation de première main en chinois simplifié, ni aucune preuve reproductible d'utilisation en chinois.
- Nous n'avons trouvé aucun identifiant de modèle de fondation intégré. Odysseus est une couche applicative qui nécessite un modèle local ou accessible par API configuré.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/pewdiepie-archdaemon/odysseus | GitHub - odysseus-dev/odysseus : espace de travail IA auto-hébergé. | 2026-09-05 |
| https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/README.md | README d'Odysseus (branche dev) | 2026-09-05 |
| https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/website/setup.md | Guide d'installation d'Odysseus (branche dev) | 2026-09-05 |
| https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/SECURITY.md | Politique de sécurité d'Odysseus (branche dev) | 2026-09-05 |
| https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/THREAT_MODEL.md | Modèle de menaces d'Odysseus (branche dev) | 2026-09-05 |
| https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/ROADMAP.md | Feuille de route d'Odysseus (branche dev) | 2026-09-05 |
| https://github.com/odysseus-dev/odysseus/discussions/551 | Who can help? · Discussion #551 | 2026-09-05 |
| https://github.com/odysseus-dev/odysseus/issues/395 | what kind of credentials does it expect on first run · Issue #395 | 2026-09-05 |
| https://github.com/odysseus-dev/odysseus/commits/main/ | Commits · odysseus-dev/odysseus · main | 2026-09-05 |
| https://github.com/odysseus-dev/odysseus/releases | Releases · odysseus-dev/odysseus | 2026-09-05 |

## Synthèse pour agents {#agent-brief}

- **Sujet :** `project:odysseus`, fil `odysseus`, 1 événement daté du 2026-06-01 au 2026-06-01.
- **Note pratique :** Au 2026-06-01, les praticiens peuvent utiliser le dépôt GitHub d'Odysseus enregistré comme référence d'emplacement source, tout en vérifiant séparément son contenu et son état opérationnel.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
