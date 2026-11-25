---
title: "Bots gérés Telegram"
description: "Guide de production sur le modèle manager-bot de Telegram : création, rotation des tokens, paramètres d'accès, isolation de l'état et reçus de cycle de vie."
tags: [telegram, bot-api, managed-bots, security, deployment]
level: 3
source_sha256: 8754df886567939fdadb542cba4bdace4b4a8a746ac0dac9e34f2dca2ae1d56c
translation: machine
translated_at: '2026-10-24'
---
# Bots gérés Telegram {#telegram-managed-bots}

**Périmètre vérifié : 2026-09-04.** Les Managed Bots de Telegram permettent à un manager bot de créer et d'exploiter un bot au nom de son propriétaire. Cette fonctionnalité est arrivée dans la Bot API 9.6 ; l'API actuelle continue de documenter son flux de création, ses méthodes de gestion des tokens, ses paramètres d'accès et ses types de mises à jour. Il s'agit d'une fonctionnalité de plan de contrôle de Telegram, et non d'un système complet de multi-location applicative ou d'isolation des données. [Bot API changelog](https://core.telegram.org/bots/api-changelog) [Managed Bots guide](https://core.telegram.org/bots/features#managed-bots)

## Ce que fournit Telegram {#what-telegram-provides}

Le manager est un bot ordinaire dont le Bot Management Mode est activé dans BotFather. Un utilisateur suit un lien profond newbot, confirme un nom de bot et un nom d'utilisateur suggérés modifiables, et Telegram envoie au manager une mise à jour **managed_bot**. Cette mise à jour contient un objet **ManagedBotUpdated** avec le propriétaire et le bot géré. Le manager peut ensuite obtenir son token via **getManagedBotToken**. [Managed Bots guide](https://core.telegram.org/bots/features#managed-bots) [Bot API objects](https://core.telegram.org/bots/api#managedbotupdated)

Telegram documente également :

- **replaceManagedBotToken**, qui révoque l'ancien token et renvoie un nouveau token ;
- **getManagedBotAccessSettings** et **setManagedBotAccessSettings**, qui exposent et modifient la politique d'accès du bot ;
- les mises à jour ultérieures de bot géré lorsque le token ou le propriétaire d'un bot géré change.

Ces capacités identifient et contrôlent le bot Telegram. Elles ne partitionnent pas votre base de données, votre stockage d'objets, votre compte auprès du fournisseur de modèles, vos analyses ni les accès des opérateurs. Définissez ces frontières explicitement.

## Topologie de production {#production-topology}

Utilisez un plan de contrôle manager et un runtime locataire distinct :

```text
owner confirms bot creation
        |
manager bot receives managed_bot update
        |
control plane records owner, bot id, lifecycle version
        |
secret store retains the token; application reads it by bot id
        |
tenant runtime processes that bot's updates under an authenticated tenancy
```

La clé de routage doit être un enregistrement de bot côté serveur, et non un identifiant de chat ou un champ de prompt fourni par l'utilisateur. Rattachez chaque mise à jour entrante au bot géré qui l'a reçue, puis résolvez son propriétaire et ses ressources autorisées en dehors du modèle.

## Enregistrer l'événement de création {#register-the-creation-event}

Les noms de méthodes des bibliothèques varient ; gardez donc le contrat de cycle de vie indépendant d'un SDK particulier :

```python
# Pseudocode: validate the webhook before parsing an update.
def register_managed_bot(update, telegram_api, registry):
    managed = update.get("managed_bot")
    if not managed:
        return

    owner_id = managed["user"]["id"]
    bot_id = managed["bot"]["id"]
    token = telegram_api.get_managed_bot_token(user_id=owner_id)

    registry.upsert(
        bot_id=bot_id,
        owner_id=owner_id,
        token_secret_ref=store_secret(token),
        lifecycle_event_id=update["update_id"],
    )
```

Persistez l'identifiant de mise à jour ou une autre clé d'idempotence avant de provisionner un worker. Telegram indique que les identifiants de mise à jour permettent d'ignorer les doublons et de rétablir l'ordre ; un webhook peut aussi être relancé par Telegram. [Update](https://core.telegram.org/bots/api#update) [Webhooks](https://core.telegram.org/bots/api#setwebhook)

Ne renvoyez, ne journalisez, ne committez et ne placez jamais un token de bot géré dans une transcription de tâche. Traitez la récupération, le remplacement et l'amorçage du worker comme des opérations de manipulation de secrets.

## Recevoir les mises à jour en toute sécurité {#receiving-updates-safely}

Pour chaque bot géré, choisissez un mode de distribution : long polling ou webhook. Telegram les documente comme mutuellement exclusifs. Un webhook doit utiliser HTTPS et un secret token unique ; Telegram envoie la valeur correspondante dans l'en-tête X-Telegram-Bot-Api-Secret-Token. [Getting updates](https://core.telegram.org/bots/api#getting-updates) [setWebhook](https://core.telegram.org/bots/api#setwebhook)

Avant de répartir une mise à jour :

1. vérifiez le transport et le secret du webhook ;
2. résolvez l'enregistrement du bot géré à partir du point d'entrée ou du runtime authentifié ;
3. dédupliquez l'identifiant de mise à jour et enregistrez le reçu de distribution ;
4. chargez uniquement la politique locataire, l'état de conversation, les outils et les secrets de ce bot ;
5. appliquez les contrôles d'autorisation et de débit avant tout appel au modèle ou à un service externe ;
6. conservez un événement d'audit expurgé contenant l'identifiant du bot, la référence du propriétaire, l'action et le résultat.

N'annoncez pas de limite de débit statique pour un produit à bots gérés. Les limites et le comportement de distribution relèvent de la Bot API et de la FAQ actuelles de Telegram, et peuvent évoluer ; testez le schéma exact des appels sortants et observez les réponses de l'API. [Bot API FAQ](https://core.telegram.org/bots/faq)

## L'isolation est un contrat applicatif {#isolation-is-an-application-contract}

Utilisez un bot géré lorsqu'une identité Telegram distincte et un cycle de vie propre au propriétaire sont utiles. Appliquez malgré tout la frontière applicative :

| Couche | Isolation requise |
|---|---|
| Identifiants Telegram | une référence de secret par bot géré ; reçu de rotation |
| État applicatif | clé locataire ou bot sur chaque lecture et écriture |
| Fichiers et recherche | stockage namespacé et autorisation au moment de la récupération |
| Outils | liste d'autorisation sélectionnée selon la politique du propriétaire authentifié |
| Facturation et quotas | comptage rattaché au même enregistrement locataire côté serveur |
| Opérations | piste d'audit et retour arrière d'incident par bot |

Des tokens distincts ne suffisent pas à prouver que le Worker A ne peut pas récupérer les données du Worker B.

## Cycle de vie et suppression {#lifecycle-and-deletion}

Traitez une mise à jour de bot géré comme un événement pouvant créer, faire tourner ou transférer une propriété. Ne récupérez et ne remplacez le secret que par l'API documentée ; réconciliez le nouvel état de cycle de vie avant de reprendre la distribution. **replaceManagedBotToken** révoque le token courant, mais ne supprime ni vos enregistrements locataires, ni vos fichiers, ni votre historique de modèle. [Token methods](https://core.telegram.org/bots/api#getmanagedbottoken)

Un workflow de suppression demandée par le propriétaire doit disposer de son propre reçu :

1. authentifiez le propriétaire selon la politique actuelle du bot et de l'application ;
2. désactivez l'ingestion et révoquez ou faites tourner le token, selon le cas ;
3. supprimez l'accès du locataire aux données, aux tâches et aux intégrations ;
4. appliquez la politique de conservation et de suppression applicable au contenu stocké ;
5. enregistrez l'action accomplie sans conserver le token ni le contenu des messages.

N'inventez pas de fonctionnalité Telegram pour l'effacement légal, la suppression des sauvegardes ou la révocation inter-services. Ces responsabilités restent celles de votre système.

## Points de vigilance {#gotchas}

- **Une mise à jour de création est traitée deux fois.** Les relances peuvent provisionner des workers en double. **Correctif :** rendez l'enregistrement idempotent sur l'identifiant de mise à jour et l'identifiant du bot géré.
- **Un prompt choisit un bot ou un locataire.** Cela permet une sélection de données inter-locataires. **Correctif :** résolvez le bot et le propriétaire à partir de l'entrée authentifiée, et non à partir de la sortie du modèle.
- **Un token apparaît dans un journal de diagnostic.** Il accorde un accès à l'API. **Correctif :** expurgez les secrets, stockez une référence et faites tourner le token rapidement en cas de fuite suspectée.
- **Un token a été roté mais l'ancien worker continue de répondre.** La configuration locale est désormais périmée. **Correctif :** arrêtez l'ancienne ingestion, rechargez le nouveau secret et conservez un reçu de santé positif.
- **Un propriétaire perd l'accès.** Le contrôle Telegram peut changer alors que l'état applicatif subsiste. **Correctif :** consommez les mises à jour de cycle de vie et définissez une politique documentée de suspension et de rétablissement.

## Sources {#sources}

- [Telegram Bot API changelog](https://core.telegram.org/bots/api-changelog)
- [Telegram Managed Bots guide](https://core.telegram.org/bots/features#managed-bots)
- [Telegram Bot API : updates, webhooks et méthodes de bots gérés](https://core.telegram.org/bots/api)
- [Telegram Bot API FAQ](https://core.telegram.org/bots/faq)

## Voir aussi {#see-also}

- [[multi-agent-messaging]]
- [[agent-deployment]]
- [[tool-use-patterns]]
- [[agentic-security-2026]]
