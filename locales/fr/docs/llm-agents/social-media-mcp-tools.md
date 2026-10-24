---
title: "Outils MCP pour les réseaux sociaux"
description: "Une conception indépendante du fournisseur, centrée sur l'approbation, pour utiliser MCP afin de rédiger, valider et publier du contenu social sans traiter une publication sociale comme une action de chat réversible."
tags: [mcp, social-media, publishing, approvals, oauth, agents]
level: 3
source_sha256: 0caf158ad6bd548853db8aecd98b1768941a439fb7fc9366e5678c27cfcbf09f
translation: machine
translated_at: '2026-10-24'
---
# Outils MCP pour les réseaux sociaux {#social-media-mcp-tools}

**Périmètre vérifié : 2026-09-03.** Un serveur MCP pour les réseaux sociaux constitue une frontière d'intégration, et non une politique de publication. Les permissions des plateformes, leur versionnage, les règles relatives aux médias et les offres commerciales évoluent fréquemment ; cette page ne classe donc pas les fournisseurs et ne conserve pas de tarifs statiques. Elle définit plutôt un contrat sûr pour connecter un pipeline d'actualités ou de contenus de projet à une API de plateforme.

## Traiter la publication comme un effet externe {#treat-publication-as-an-external-effect}

Une réponse réussie du modèle n'est pas une publication. Séparez le flux de travail :

```text
source evidence -> editorial draft -> policy validation -> human approval
                -> platform-specific publish -> provider receipt -> reconciliation
```

L'agent peut préparer un brouillon et une proposition structurée. Seul le service d'effet peut utiliser les identifiants de la plateforme ou créer la publication, et il doit conserver la réponse du fournisseur qui identifie la ressource créée.

## Intention de publication minimale {#minimal-publish-intent}

Conservez dans l'application une intention indépendante de la plateforme, puis traduisez-la au niveau de l'adaptateur du fournisseur :

```json
{
  "intent_id": "social-044",
  "project_ref": "happyin-space",
  "platform": "linkedin",
  "account_ref": "organization:public-channel",
  "content_revision": "draft:2026-09-03.2",
  "media_refs": ["asset:cover-044"],
  "schedule_at": null,
  "approval_ref": "approval:appr_01...",
  "idempotency_key": "social-044:linkedin:v1",
  "expires_at": "2026-09-03T18:00:00Z"
}
```

L'exécuteur dérive la charge utile propre à la plateforme à partir de cette intention immuable et valide le compte actuel, les portées, les médias, l'audience et le moment de publication. Il n'accepte jamais une instruction libre du type « publie ceci partout » comme source d'autorité.

## Surface d'outils MCP {#mcp-tool-surface}

Exposez des verbes étroits plutôt qu'un seul outil général `social_admin` :

| Outil | Effet | Vérifications requises |
|---|---|---|
| `list_connected_accounts` | lecture | appelant et périmètre du compte |
| `create_draft` | écriture interne réversible | projet, références aux sources, schéma du contenu |
| `validate_publish` | contrôle préalable en lecture seule auprès du fournisseur | portée, médias, format, version actuelle de la plateforme |
| `publish_approved` | effet externe | approbation immuable, expiration, compte, idempotence |
| `get_publication_receipt` | lecture | identifiant de l'intention et périmètre de l'appelant |

Les descriptions et annotations des outils sont considérées comme non fiables, sauf si elles proviennent d'un serveur déjà approuvé par l'hôte. Les hôtes doivent permettre à un humain de refuser l'invocation d'un outil. [Outils MCP](https://modelcontextprotocol.io/specification/latest/server/tools)

## Frontière d'autorisation {#authorization-boundary}

Pour un MCP distant, utilisez le flux d'autorisation du protocole et valider les jetons pour la ressource visée. Le serveur MCP doit conserver les identifiants OAuth de la plateforme dans un coffre côté serveur ; le client MCP ne reçoit que le résultat dont il a besoin, jamais un jeton d'accès réutilisable vers la plateforme. [Autorisation MCP](https://modelcontextprotocol.io/specification/latest/basic/authorization)

Pour chaque compte connecté, enregistrez :

- la référence du compte de la plateforme et de son propriétaire ;
- les portées accordées et la date de leur vérification ;
- la version actuelle de l'API et les capacités de contenu ;
- les exigences de téléversement des médias et les limites de taille ;
- le comportement du fournisseur en matière de limitation de débit et de nouvelles tentatives ;
- les restrictions de politique ou de relecture ;
- la procédure de rotation et de révocation des identifiants.

Les valeurs exactes dépendent de chaque plateforme et doivent être revalidées au moment de la connexion. Par exemple, l'API Posts de LinkedIn exige actuellement des en-têtes de requête versionnés et des portées distinctes pour les membres et les organisations ; une création réussie renvoie un identifiant de publication attribué par le fournisseur. [API Posts de LinkedIn](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api)

## Approbation et idempotence {#approval-and-idempotency}

```text
draft -> reviewer approves exact content revision and account
      -> effect service reserves (intent_id, idempotency_key, content_revision)
      -> adapter creates one platform post
      -> record provider ID, response class, and final visibility
```

Une nouvelle tentative identique renvoie le reçu stocké. Réutiliser la clé d'idempotence avec un compte, une révision ou une liste de médias différents doit être rejeté avant la création d'une seconde publication. Si le réseau expire après l'appel au fournisseur, marquez l'état comme inconnu et réconciliez-le à partir du reçu du fournisseur ou d'une consultation sûre ; ne republiez pas par supposition.

## Porte de qualification des fournisseurs {#provider-qualification-gate}

Évaluez un connecteur géré ou auto-hébergé à partir de preuves actuelles, et non d'une grille tarifaire :

1. flux de transport et OAuth documentés ;
2. modèle explicite de comptes, de portées et de versions d'API ;
3. prise en charge de requêtes immuables ou de l'idempotence pour la publication ;
4. reçus de téléversement de médias, de création de publication et de consultation ;
5. responsable de la maintenance, provenance des versions et revue des dépendances ;
6. un canari en environnement de préproduction ou sur un compte de test ;
7. un parcours d'approbation humaine qui affiche le contenu sortant réel.

Aucun serveur communautaire ne doit recevoir des identifiants sociaux étendus simplement parce que le nom de son outil paraît restreint.

## Mode opératoire pour un portail d'actualités {#operating-pattern-for-a-news-portal}

Utilisez la fiche de connaissance du portail comme source de vérité :

| État du portail | Action sur les réseaux sociaux |
|---|---|
| Recherche collectée | aucune action sociale |
| Rédigé et sources relues | proposition de brouillon facultative |
| Approuvé pour publication | création d'une intention de publication par plateforme |
| Publié et vérifié | rattachement du reçu du fournisseur et de l'URL canonique |
| Corrigé ou remplacé | publication d'une nouvelle révision liée ; ne pas écraser l'historique en silence |

Cela maintient la provenance des actualités, les pages de projet et les dérivés sociaux reliés entre eux, sans que la diffusion sociale ne redéfinisse la vérité éditoriale.

## Pièges courants {#gotchas}

- **Le reçu d'un planificateur n'est pas un reçu de publication.** Il signifie seulement que le connecteur a accepté la tâche. **Correction :** réconciliez l'identifiant de la ressource chez le fournisseur et la visibilité constatée.
- **Le transport MCP n'accorde aucune autorité sur la plateforme.** Les portées OAuth et les rôles de compte restent à la frontière de la plateforme. **Correction :** validez-les dans l'adaptateur du fournisseur pour chaque effet.
- **Les métadonnées des outils peuvent être malveillantes ou obsolètes.** Une description rassurante ne constitue pas une garantie de sécurité. **Correction :** faites confiance à l'identité du serveur configuré et inspectez les schémas avant d'activer des outils à effet.
- **Les nouvelles tentatives peuvent dupliquer une publication.** Un délai d'attente ne permet pas de savoir si la plateforme a agi. **Correction :** réservez de façon atomique une clé d'idempotence et réconciliez les issues inconnues.
- **Les comparatifs de fournisseurs deviennent vite obsolètes.** Les tarifs, la couverture des plateformes et les permissions ne sont pas des faits documentaires stables. **Correction :** conservez un reçu de qualification daté pour chaque connecteur.

## Sources {#sources}

- [Outils du Model Context Protocol](https://modelcontextprotocol.io/specification/latest/server/tools)
- [Autorisation du Model Context Protocol](https://modelcontextprotocol.io/specification/latest/basic/authorization)
- [API Posts de LinkedIn](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api)

## Voir aussi {#see-also}

- [[agent-safety-alignment]]
- [[tool-use-patterns]]
- [[multi-agent-messaging]]
- [[agent-orchestration]]
