---
title: "Sécurité des données et des sessions de Claude Desktop"
description: "Utilisez les contrôles pris en charge pour l'export, le compte et les extensions plutôt que de vous fier aux éléments internes non versionnés du cache local pour la récupération des conversations ou la synchronisation entre appareils."
tags: [claude-desktop, data-export, privacy, extensions, troubleshooting]
level: 3
source_sha256: b45629cca63517bdb3b0ca57da0693decce068c03455fae92e2f40ed547f9ba4
translation: machine
translated_at: '2026-10-24'
---
# Sécurité des données et des sessions de Claude Desktop {#claude-desktop-data-and-session-safety}

**Périmètre vérifié : 2026-09-04.** Claude Desktop est une application liée à un compte, et non une API de fichiers de session locaux prise en charge. La documentation publique d'Anthropic fournit des contrôles pris en charge pour exporter les données du compte et des conversations, ainsi que pour gérer les extensions Desktop ; elle ne garantit pas de schéma stable sur disque pour les conversations, de chemin de cache, de bundle de machine virtuelle, ni de procédure de récupération inter-appareils par copie. [Exporter vos données Claude](https://support.claude.com/en/articles/9450526-export-your-claude-data) [Extensions Claude Desktop](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop)

## Privilégier d'abord les contrôles pris en charge {#use-supported-controls-first}

| Besoin | Voie prise en charge | Ne pas se fier à |
|---|---|---|
| conserver ou consulter l'historique des conversations | demander un export de données dans Paramètres → Confidentialité | l'extraction de fichiers de cache de l'application |
| déplacer un projet de code entre machines | Git, un dépôt distant et les artefacts propres au projet | la copie de l'état de l'application de bureau |
| partager une conversation précise | les contrôles de partage et de retrait de partage du produit | l'envoi de bases de données ou de fichiers de cache bruts |
| gérer les intégrations locales | Paramètres → Extensions ou les paquets d'extension approuvés | des dossiers de configuration non documentés |
| diagnostiquer une extension | l'état et les journaux des extensions dans l'application | la suppression de données de l'application sans rapport |

Les utilisateurs individuels peuvent demander un export depuis l'application web ou depuis Claude Desktop ; les propriétaires d'équipes et d'entreprises disposent de contrôles d'export organisationnels équivalents. Le lien de téléchargement obtenu est envoyé par e-mail et expire : traitez-le comme une donnée sensible. [Exporter vos données Claude](https://support.claude.com/en/articles/9450526-export-your-claude-data)

## Conserver la continuité du projet hors du client de chat {#keep-project-continuity-outside-the-chat-client}

Pour un travail qui doit survivre à un changement d'appareil, de compte ou de client, conservez l'état réel du projet dans son propre système :

```text
source and decisions     → Git-backed project files
running-job checkpoints  → service-owned durable storage
credentials              → approved secret store
chat history             → account export when needed
local extension settings → Claude Desktop or organization policy
```

Ne supposez pas qu'une conversation visible, la barre latérale de l'application et les fichiers temporaires locaux obéissent à la même politique de conservation ou de synchronisation. L'interface du produit et l'export du compte sont le moyen pris en charge de récupérer les données de conversation des utilisateurs ; les détails d'implémentation peuvent changer sans garantie de compatibilité.

## Procédure sûre de diagnostic en cas de conversation manquante {#a-safe-missing-conversation-triage}

Si l'historique semble absent ou si un client Desktop se comporte de manière inattendue :

1. notez la version de l'application, le système d'exploitation, le contexte du compte ou de l'espace de travail, et le symptôme exact visible par l'utilisateur ;
2. vérifiez si le même compte affiche l'état attendu dans l'interface Claude prise en charge ;
3. préservez le dépôt du projet et tout justificatif indépendant de tâche avant de dépanner le client ;
4. utilisez le support intégré au produit, les contrôles du compte ou une demande d'export de données pour les données historiques ;
5. recueillez un diagnostic expurgé et arrêtez-vous avant de supprimer ou de copier l'état de l'application ;
6. ne réinstallez, ne réinitialisez ou ne videz les données que selon les instructions de support actuelles du produit, et après avoir préservé les artefacts nécessaires.

Cette séquence distingue un problème d'affichage du client d'un problème lié au dépôt ou au flux de travail externe, sans inventer de procédure de récupération du système de fichiers.

## Les extensions Desktop forment une frontière distincte {#desktop-extensions-are-a-separate-boundary}

Les extensions Desktop peuvent connecter Claude Desktop à des outils et des données locaux. Anthropic documente l'installation via Paramètres → Extensions, un répertoire d'extensions et des paquets personnalisés ; les consignes actuelles décrivent aussi les contrôles organisationnels et les politiques de la plateforme. Considérez chaque extension comme du code ayant accès aux ressources que sa configuration autorise. [Serveurs MCP locaux sur Claude Desktop](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop)

Avant d'en activer une :

1. identifiez son éditeur, sa version, ses permissions et ses flux de données ;
2. privilégiez les paquets relus ou approuvés par l'organisation ;
3. utilisez les accès minimaux nécessaires au système de fichiers, au réseau et aux secrets ;
4. testez-la dans un espace de travail hors production ;
5. conservez le paquet, la version et l'enregistrement de l'approbation ;
6. supprimez-la ou révoquez-la par la voie de gestion prise en charge lorsque son usage prend fin.

Pour les déploiements Team et Enterprise, les politiques de l'organisation et de la machine peuvent contrôler la disponibilité des extensions et des répertoires Desktop. Un réglage local de l'utilisateur ne constitue pas nécessairement la politique effective. [Administration des extensions Desktop](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop)

## Confidentialité et partage {#privacy-and-sharing}

Les conversations sont privées par défaut, mais un lien de conversation partagée expose l'instantané sélectionné pour le partage. Consultez et révoquez les liens partagés via les contrôles de confidentialité du produit, plutôt que de supposer que la suppression d'un artefact local modifie une copie partagée. [Partager et retirer le partage de conversations](https://privacy.anthropic.com/en/articles/10593882-sharing-and-unsharing-chats)

Les exports de données et les bundles de diagnostic peuvent contenir des conversations, des métadonnées ou des informations de compte sensibles. Stockez-les dans un emplacement privé approuvé, limitez les accès, et évitez de les placer dans des dépôts, des tickets, des trackers d'incidents publics ou des prompts de modèles.

## Ce que cette page n'affirme pas {#what-this-page-does-not-claim}

Cette page ne prescrit volontairement ni nom de répertoire, ni type de base de données, ni image de VM, ni registre de sessions caché, ni recette de vidage de cache, ni bogue propre à une version, ni outil tiers de synchronisation. Ces affirmations exigeraient un contrat de prise en charge actuel ou une enquête reproductible et bornée ; à défaut, ce seraient des conseils de récupération dangereux.

## Pièges courants {#gotchas}

- **Un dossier de cache ressemble à un export.** Il peut être incomplet, chiffré, transitoire ou constituer un état interne privé. **Correction :** utilisez le contrôle d'export du produit pour l'historique des conversations.
- **Copier les données de l'application semble restaurer une machine.** Cela peut aussi copier des identifiants, casser une autre installation ou créer un état non pris en charge. **Correction :** utilisez Git pour le travail sur les projets et les contrôles de compte pris en charge pour les conversations.
- **Une réinitialisation sert de premier diagnostic.** Elle peut supprimer des éléments de preuve nécessaires au support. **Correction :** notez le symptôme et préservez d'abord les artefacts indépendants du projet.
- **Une extension est jugée fiable parce qu'elle s'installe en un clic.** La facilité d'installation ne vaut pas revue des permissions. **Correction :** vérifiez l'éditeur, la portée et la politique de l'organisation avant de l'activer.
- **Une conversation partagée est prise pour une sauvegarde privée.** Toute personne disposant du lien peut accéder à l'instantané. **Correction :** consultez et révoquez le partage via les contrôles de confidentialité.

## Sources {#sources}

- [Exporter vos données Claude](https://support.claude.com/en/articles/9450526-export-your-claude-data)
- [Premiers pas avec les serveurs MCP locaux sur Claude Desktop](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop)
- [Quand utiliser les connecteurs Desktop et Web](https://support.anthropic.com/en/articles/11725091-when-to-use-desktop-and-web-connectors)
- [Partager et retirer le partage de conversations](https://privacy.anthropic.com/en/articles/10593882-sharing-and-unsharing-chats)

## Voir aussi {#see-also}

- [[claude-code-ecosystem]]
- [[agent-memory]]
- [[context-engineering]]
- [[agentic-security-2026]]
