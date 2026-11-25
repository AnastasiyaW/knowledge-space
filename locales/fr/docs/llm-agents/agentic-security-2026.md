---
title: "Sécurité des IA agentiques"
description: "Guide de modélisation des menaces et de contrôles pour les agents utilisant des outils, les intégrations MCP, la mémoire persistante et les effets irréversibles. Périmètre vérifié le 2026-09-03."
tags: [agent-security, mcp, prompt-injection, authorization, supply-chain, ai-safety]
level: 4
source_sha256: 31ad7c52408b2c52f339d524d26e144022aed1482ff69c185fe1c9fa9f8da13f
translation: machine
translated_at: '2026-10-24'
---
# Sécurité des IA agentiques {#agentic-ai-security}

**Périmètre vérifié : 2026-09-03.** La sécurité des agents est un problème de sécurité applicative à l'intérieur duquel se trouve un planificateur probabiliste. Ne vous fiez pas à un chiffre de taux d'attaque spectaculaire, à une CVE isolée ou à un filtre de prompts comme frontière de sécurité. Commencez par une modélisation des menaces, appliquez l'autorité en dehors du modèle, et conservez des justificatifs pour chaque effet externe.

L'OWASP Top 10 pour les agents met en évidence, parmi les classes de risques critiques, le détournement d'objectif, l'utilisation abusive d'outils, les abus d'identité et de privilèges, les vulnérabilités de la chaîne d'approvisionnement et l'exécution de code inattendue. [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/)

## Commencer par la modélisation des menaces {#threat-model-first}

Cartographiez les flux réels de données et d'autorité :

```text
untrusted input -> retrieval / context -> model planner -> tool request
                       |                    |              |
                    private data          memory         effect executor
                                                               |
                                                         external system
```

Pour chaque frontière, consignez le principal, la classification des données, l'action autorisée, l'expiration, l'événement d'audit et le chemin de reprise. Une architecture à haut risque combine les trois éléments suivants dans une même boucle non contrainte :

1. lit des données privées ;
2. traite des entrées influençables par un attaquant ;
3. peut effectuer une action externe.

La réponse consiste en une séparation et une médiation imposée, et non simplement en un prompt système plus robuste.

## Classes de risques principales {#core-risk-classes}

| Risque | Exemple | Frontière de contrôle |
|---|---|---|
| Détournement d'objectif / injection de prompt | une page web demande à l'agent de contourner la politique | étiqueter le contenu comme non fiable ; l'exécuteur d'outils ignore le texte du modèle comme source d'autorité |
| Utilisation abusive d'outils | le modèle sélectionne un outil valide pour une action métier invalide | schéma, autorisation, approbations et idempotence au niveau de l'exécuteur |
| Abus d'identité et de privilèges | jeton divulgué ou trop large atteignant un connecteur | identité de charge de travail, portées restreintes, validation de l'audience, révocation |
| Compromission de la chaîne d'approvisionnement | une dépendance ou un serveur MCP distant modifie son comportement | provenance, épinglage, revue, déploiement contrôlé |
| Exécution de code inattendue | l'entrée d'un outil atteint un shell ou un interpréteur | bac à sable, commandes en liste blanche, pas de montages ou d'identifiants étendus |
| Empoisonnement de la mémoire | un texte hostile devient une instruction durable | provenance des sources, politique d'écriture, historique des modifications consultable |
| Exfiltration de données | une lecture autorisée est encodée dans un appel sortant autorisé | contrôles de sortie et du graphe d'actions de bout en bout |

## Imposer la capacité, pas l'intention {#enforce-capability-not-intent}

L'agent peut proposer une action. Un service d'effets déterministe décide si elle a lieu :

```json
{
  "task_id": "research-044",
  "action": "create_draft",
  "resource_scope": "project:happyin-space",
  "arguments_digest": "sha256:...",
  "approval_ref": "approval:appr_01...",
  "idempotency_key": "research-044:v1",
  "expires_at": "2026-09-03T18:00:00Z"
}
```

Avant tout effet, vérifiez l'identité de l'appelant, l'audience du destinataire, la requête immuable, la portée, l'approbation, l'expiration et la réservation d'idempotence. Toute modification des arguments exige une nouvelle capacité. Un résultat inconnu est réconcilié à partir d'un justificatif du fournisseur avant toute nouvelle tentative.

Voir [[agent-safety-alignment]] pour un contrat concret de capacité et de rejeu atomique.

## Frontières de MCP {#mcp-boundaries}

MCP rend les outils découvrables ; il ne les rend pas fiables pour autant. Le protocole recommande aux hôtes de conserver le consentement de l'utilisateur et le contrôle sur l'accès aux données et l'invocation des outils, et indique que les descriptions d'outils doivent être considérées comme non fiables, sauf si elles proviennent d'un serveur de confiance. [MCP architecture](https://modelcontextprotocol.io/specification/latest/architecture) [MCP tools](https://modelcontextprotocol.io/specification/latest/server/tools)

Pour les serveurs MCP distants :

1. vérifiez l'identité du serveur et le transport avant de l'enregistrer ;
2. demandez la portée OAuth minimale et validez que les jetons sont destinés à cette ressource ;
3. conservez les identifiants des services en amont côté serveur plutôt que de les faire transiter ;
4. n'exposez que les outils requis pour le flux de travail en cours ;
5. exigez une approbation de l'utilisateur ou de la politique pour les appels à fort impact ;
6. journalisez l'appel d'outil, l'appelant, le condensat de la requête et le justificatif obtenu.

L'autorisation MCP exige une liaison à la ressource et à l'audience, et rejette le transfert de jetons (token passthrough) comme modèle général sûr. [MCP authorization](https://modelcontextprotocol.io/specification/latest/basic/authorization)

## La mémoire est une donnée, pas une politique {#memory-is-data-not-policy}

La mémoire persistante peut contenir des affirmations provenant des utilisateurs, des pages récupérées, des outils ou de sorties antérieures du modèle. Conservez la provenance et traitez chaque écriture comme une donnée :

| Champ | Rôle |
|---|---|
| référence de la source | identifier l'origine de l'affirmation |
| étiquette de confiance | distinguer affirmation utilisateur, politique approuvée et récupération non fiable |
| principal autorisant | indiquer qui a permis l'écriture |
| date d'expiration ou de revue | empêcher une instruction périmée de devenir une autorité permanente |
| historique des révisions | auditer les modifications et permettre un retour arrière sûr |

Ne transformez jamais une instruction récupérée en permission, en règle de routage ou en référence d'identifiant uniquement parce qu'elle figure dans un document d'apparence fiable.

## Matrice de tests de sécurité {#security-test-matrix}

Testez le flux de travail intégré, et non des prompts isolés :

- injections directes et indirectes dans les pages web, pièces jointes, enregistrements et sorties d'outils ;
- tentatives de récupération et de sortie inter-locataires ;
- arguments d'outils altérés et actions valides au regard du schéma mais invalides au regard de la politique ;
- approbations périmées, capacités expirées et incohérences identité/audience ;
- chemins de doublon et de perte de réponse pour la publication, la suppression ou le paiement ;
- simulation de dépendance ou de version de serveur compromise ;
- contrôles d'annulation, d'évasion du bac à sable, de sortie réseau et de caviardage des journaux.

Consignez la classe d'entrée de test, la révision de la politique, la décision attendue et les preuves. Une complétion de texte « sûre » ne prouve pas que l'exécuteur d'effets rejetterait un appel dangereux.

## Observabilité prête pour la gestion d'incidents {#incident-ready-observability}

Pour toute requête d'outil significative, conservez une trace caviardée contenant :

- les identifiants de tâche et de session ;
- l'appelant authentifié et la révision de la politique ;
- l'action normalisée et le condensat des arguments ;
- la décision d'approbation ou de refus ;
- la version de l'outil ou du serveur ;
- le justificatif externe ou l'état de réconciliation.

Protégez ces données : l'observabilité peut sinon créer le même chemin d'exposition de données que l'agent était censé éviter.

## Pièges courants {#gotchas}

- **Le filtrage des injections n'est pas un système de permissions.** Des instructions inédites peuvent échapper aux motifs textuels. **Correctif :** appliquez l'autorisation et la portée après que le modèle a proposé un appel.
- **Un bac à sable peut contenir une autorité étendue.** Des jetons montés et une sortie réseau permissive peuvent annuler l'isolation du système de fichiers. **Correctif :** minimisez simultanément les identifiants, les chemins, les processus et les destinations.
- **Un outil peut être sûr seul mais dangereux dans une chaîne.** Lire, encoder et envoyer peuvent exfiltrer des données sans qu'aucun outil soit « dangereux » en soi. **Correctif :** modélisez les chemins d'action de bout en bout et la politique de sortie.
- **La mémoire crée des attaques différées.** Une note empoisonnée peut influencer les sessions futures. **Correctif :** associez provenance, expiration et revue aux écritures en mémoire.
- **Une nouvelle tentative peut dupliquer le dommage.** Les délais d'attente masquent si le service externe a agi. **Correctif :** réservez l'idempotence avant l'effet et réconciliez avant de répéter.

## Sources {#sources}

- [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/)
- [Model Context Protocol architecture](https://modelcontextprotocol.io/specification/latest/architecture)
- [Model Context Protocol tools](https://modelcontextprotocol.io/specification/latest/server/tools)
- [Model Context Protocol authorization](https://modelcontextprotocol.io/specification/latest/basic/authorization)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

## Voir aussi {#see-also}

- [[agent-safety-alignment]]
- [[agent-security]]
- [[tool-use-patterns]]
- [[multi-agent-messaging]]
- [[social-media-mcp-tools]]
