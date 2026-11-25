---
title: "OpenSandbox"
category: projects

tags: [opensandbox, opensandbox-development, opensandbox-group/opensandbox, project]
aliases: ["OpenSandbox"]
level: 2
source_sha256: cbb2d4a6dcf06b1628ab9fe3c6123196a3ff03be63e3071d014065e69443612b
translation: machine
translated_at: '2026-10-24'
---
# OpenSandbox {#opensandbox}

**Ligne de développement :** `project:opensandbox` · fil `opensandbox-development`  
**Dernier événement :** - · 0 daté depuis · **Consulté le :** 2026-09-08 · confiance : moyenne

## Description {#what-it-is}

OpenSandbox fournit des environnements isolés pour les agents IA, sur Docker et Kubernetes.

- SDK multi-langages, une CLI `osb` et un serveur MCP
- API de cycle de vie, de commandes et de fichiers sur Docker et Kubernetes
- Politique de sortie réseau par sandbox, proxy Credential Vault et choix optionnels de runtime sécurisé

L'exécution locale nécessite Docker et Python 3.10+ ; l'API de cycle de vie se lie à `0.0.0.0` par défaut. Utilisez-le comme couche d'exécution pour les charges de travail des agents, mais sécurisez le plan de contrôle et la politique réseau sortante avant de l'exposer.

## Ligne de développement {#development-line}

- La ligne datée n'est pas encore rédigée ; ce qui est connu figure dans les sections ci-dessous.

## Évolutions {#what-changed}

Développement d'OpenSandbox : 2026-03-03 — le paquet `opensandbox-server` 0.1.5 a été publié, ce qui montre la distribution du paquet avant la référence projet d'août. 2026-03-22 — PyPI indique `opensandbox-server` 0.1.8 comme retiré (yanked) pour incompatibilité. 2026-08-15 — la référence projet datée identifie OpenSandbox, mais n'établit pas à elle seule une fonctionnalité ou une version étiquetée. 2026-08-19 — chart Helm 0.2.2, version de l'application 0.2.2, livré sous forme de paquet tout-en-un contrôleur et serveur. 2026-08-26 — `opensandbox-server` 0.2.3 a été publié et `execd` 1.1.0 a ajouté des fonctionnalités optionnelles d'initialisation, de durcissement et de hooks de cycle de vie ; la topologie classique est restée celle par défaut.

## Mode d'emploi {#how-to-use-this}

1. Pour une utilisation locale, installez Docker et Python 3.10+, générez la configuration d'exemple Docker avec `uvx opensandbox-server init-config ~/.sandbox.toml --example docker`, puis lancez `uvx opensandbox-server`.
  — <https://github.com/opensandbox-group/OpenSandbox>
2. Installez `opensandbox-cli`, configurez son domaine, son protocole et sa clé API, créez une sandbox avec un délai d'expiration explicite, vérifiez son état de santé, exécutez la charge de travail, puis arrêtez la sandbox.
  — <https://github.com/opensandbox-group/OpenSandbox/blob/main/cli/README.md>
3. Pour un client de programmation compatible MCP, installez `opensandbox-mcp` et configurez son processus stdio avec le domaine, le protocole et la clé API d'OpenSandbox.
  — <https://github.com/opensandbox-group/OpenSandbox/blob/main/sdks/mcp/sandbox/python/README.md>
4. Pour la topologie Kubernetes tout-en-un, installez la version officielle 0.2.2 du chart Helm dans le namespace `opensandbox-system`.
  — <https://github.com/opensandbox-group/OpenSandbox/releases/tag/helm%2Fopensandbox%2F0.2.2>

## Bonnes pratiques {#best-practices}

- Définissez une clé API serveur non vide avant toute exposition en production ; une clé vide désactive les contrôles et exige une confirmation explicite du démarrage non sécurisé.
  — <https://github.com/opensandbox-group/OpenSandbox/blob/main/server/configuration.md>
- Créez les sandboxes avec proxy d'identifiants en définissant une politique réseau explicite, et transmettez les charges Credential Vault par fichier ou par stdin plutôt que par options en clair sur la ligne de commande.
  — <https://github.com/opensandbox-group/OpenSandbox/blob/main/cli/README.md>
- Utilisez des délais d'expiration explicites pour les sandboxes et arrêtez-les après la charge de travail ; une demande de pause est asynchrone, il faut donc interroger l'état jusqu'à ce qu'il atteigne Paused.
  — <https://github.com/opensandbox-group/OpenSandbox/blob/main/cli/README.md>
- Résolvez les images de release vers des digests immuables et vérifiez leur signature Cosign ainsi que leur attestation de provenance, plutôt que de vous fier à des tags mutables.
  — <https://github.com/opensandbox-group/OpenSandbox/blob/main/docs/community/release-verification.md>

## Remplacé par ceci {#superseded-by-this}

- {"claim":"`opensandbox-server` 0.1.8 est une version serveur utilisable.","obsolete_since":"2026-03-22","source_url":"https://pypi.org/project/opensandbox-server/"}

## Inconnues restantes {#still-unknown}

- L'événement fourni ne contient qu'une URL de projet ; la fonctionnalité ou l'affirmation visée pour le 2026-08-15 ne peut donc pas être retrouvée.
- Aucune note de version publiée par le projet et datée exactement du 2026-08-15 n'a été trouvée ; le détail Helm du même jour est un ticket d'anomalie, non une annonce de version.
- Le guide actuel de vérification mentionne une identité historique de dépôt `alibaba/OpenSandbox` pour les artefacts antérieurs à la migration, mais ne date pas la migration de l'organisation.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://github.com/opensandbox-group/OpenSandbox | README du dépôt OpenSandbox | 2026-09-08 |
| https://pypi.org/project/opensandbox-server/0.1.5/ | opensandbox-server 0.1.5 sur PyPI | 2026-09-08 |
| https://pypi.org/project/opensandbox-server/ | opensandbox-server sur PyPI | 2026-09-08 |
| https://github.com/opensandbox-group/OpenSandbox/issues/1529 | Ticket #1529 : écart de publication du chart Helm tout-en-un | 2026-09-08 |
| https://github.com/opensandbox-group/OpenSandbox/releases/tag/helm%2Fopensandbox%2F0.2.2 | Chart Helm opensandbox 0.2.2 (App v0.2.2) | 2026-09-08 |
| https://github.com/opensandbox-group/OpenSandbox/releases/tag/docker%2Fexecd%2Fv1.1.0 | Version 1.1.0 de components/execd | 2026-09-08 |
| https://github.com/opensandbox-group/OpenSandbox/blob/main/cli/README.md | README de la CLI OpenSandbox | 2026-09-08 |
| https://github.com/opensandbox-group/OpenSandbox/blob/main/server/configuration.md | Référence de configuration du serveur OpenSandbox | 2026-09-08 |
| https://github.com/opensandbox-group/OpenSandbox/blob/main/sdks/mcp/sandbox/python/README.md | Serveur MCP Sandbox d'OpenSandbox | 2026-09-08 |
| https://github.com/opensandbox-group/OpenSandbox/blob/main/docs/community/release-verification.md | Vérification des releases d'OpenSandbox | 2026-09-08 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:opensandbox`, fil `opensandbox-development`, 0 événement daté - → -.
- **Note pratique :** voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
