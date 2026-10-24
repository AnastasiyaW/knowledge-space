---
level: 2
source_sha256: 64f5a98626c89e7aa3b1118807baa79542f52fccbc1d48436125f18f8c96ab18
translation: machine
translated_at: '2026-10-24'
---
# Architecture de surveillance des tâches OIS multi-environnements {#ois-multi-environment-task-monitoring-architecture}

L'infrastructure OIS repose sur un déploiement monorepo uniforme entre les environnements de staging et de production (RU et EN). Bien que les chemins de code soient identiques, les environnements sont isolés par des hôtes de base de données, des identifiants S3 et des instances Redis distincts. La surveillance des tâches sur ces environnements nécessite d'agréger les données de deux magasins d'état distincts : PostgreSQL pour la persistance et Redis pour l'état d'exécution en temps réel.

## Sources de données et parité des environnements {#data-sources-and-environment-parity}

Chaque environnement exécute les mêmes images de services (`oisgold/<service>`). Les différences entre environnements relèvent strictement de la configuration (variables d'environnement).

- **Persistance en base de données :** PostgreSQL stocke les métadonnées des tâches dans la table `chat_message`.
- **État de la file en temps réel :** Redis BullMQ gère le cycle de vie d'exécution des jobs sur cinq niveaux de priorité.
- **API d'administration :** Montée sous `/api/chat/admin/`, protégée par le middleware `checkAdmin`, qui exige un JWT ou un cookie de session avec `role: 'admin'`.

## Persistance de l'état basée sur les messages PostgreSQL {#postgresql-message-based-state-persistence}

Le système n'utilise pas de table `tasks` dédiée. Les tâches sont des lignes `chat_message` spécialisées, identifiées par un blob JSON dans le champ `text`.

### Détection des tâches et dérivation du statut {#task-detection-and-status-derivation}

Une ligne est considérée comme une tâche si le champ `text` est un objet JSON contenant un tableau `items`. Le statut n'est pas stocké dans une colonne, mais dérivé dynamiquement à partir des propriétés JSON : `done`, `stopped`, `canceled` et `items[].output`.

```sql
-- Query to identify active (not-done) tasks across all environments
SELECT id, chat_id, created_at, text
FROM chat_message
WHERE text LIKE '{%' 
  AND text::jsonb ? 'items'
  AND coalesce((text::jsonb->>'done')::boolean, false) = false
  AND coalesce((text::jsonb->>'stopped')::boolean, false) = false
  AND coalesce((text::jsonb->>'canceled')::boolean, false) = false
ORDER BY created_at DESC;
```

## Gestion des files Redis BullMQ {#redis-bullmq-queue-management}

Les états des jobs en temps réel (`waiting`, `active`, `delayed`, `paused`, `failed`) résident dans BullMQ. OIS utilise cinq files spécifiques pour gérer les différents niveaux de priorité et les tâches système.

| File | Niveau de priorité | Utilisateurs cibles / Cas d'usage |
|---|---|---|
| `image-high` | Élevé | Offres Enterprise et Corporate |
| `image-medium` | Moyen | Utilisateurs Standard et Pro |
| `image-low` | Faible | Utilisateurs du plan gratuit |
| `main` | Système | Facturation, webhooks et envoi d'e-mails |
| `dead-letter` | N/A | Jobs relancés (10 tentatives, backoff exponentiel) |

### Identification des jobs {#job-identification}

Les jobs BullMQ transportent une charge utile dans `job.data` qui inclut `{messageId, inputFileId}`. Ces métadonnées sont essentielles pour croiser les jobs Redis avec les lignes PostgreSQL afin de détecter les tâches « orphelines » (lignes en base marquées comme en file d'attente mais sans job Redis correspondant).

## Stratégie d'agrégation : le pattern Collector {#aggregation-strategy-the-collector-pattern}

Pour fournir une vue unifiée sans modifier les services de production, un agrégateur en mode pull (Collector) est mis en place.

1. **Abonnement Redis :** les Collectors utilisent `QueueEvents` de BullMQ pour écouter en temps réel les événements `waiting`, `active` et `completed`.
2. **Interrogation PostgreSQL :** une interrogation périodique (30 à 60 s) identifie les tâches orphelines et met à jour l'état du tableau de bord unifié.
3. **Frontière de confiance interne :** l'agrégateur doit idéalement s'exécuter dans le VPC ou utiliser des JWT de service de longue durée pour contourner les exigences habituelles en matière de cookie de session.

## API d'actions d'administration {#administrative-action-api}

Les opérateurs gèrent les jobs bloqués ou en échec via les endpoints `/api/chat/admin/tasks`.

### Relance et récupération {#restart-and-recovery}

- **Relance groupée :** `POST /tasks/restart` avec `messageIds[]` remet en file tous les fichiers non terminés des messages spécifiés.
- **Relance ciblée :** `POST /tasks/restart-file` cible un seul `inputFileId`.
- **Récupération depuis la DLQ :** `POST /tasks/dlq/retry` supprime les métadonnées de la DLQ et renvoie le job dans sa file d'origine.

### Arrêt et limitation {#stopping-and-throttling}

- **Arrêter la tâche :** `POST /tasks/stop` marque la ligne en base avec `stopped=true` et supprime le job de Redis, tout en conservant les sorties existantes.
- **Mise en pause de la file :** `Queue.pause()` est disponible via l'API BullMQ, mais nécessite un endpoint d'administration personnalisé pour activer ou désactiver l'exécution d'un niveau de priorité complet (par exemple, mettre en pause `image-low` en période de forte charge).

## Pièges courants {#gotchas}

- **Problème :** le statut de la tâche est masqué dans le JSON → **Solution :** utiliser un index `jsonb` ou une vue PostgreSQL pour éviter les parcours séquentiels lors du filtrage de milliers de lignes.
- **Problème :** des événements Redis peuvent être manqués pendant une indisponibilité du collector → **Solution :** effectuer systématiquement un instantané complet de PostgreSQL et un parcours de la file Redis (`getJobs`) au démarrage du collector pour resynchroniser l'état.
- **Problème :** la mise en pause par job de BullMQ n'est pas native dans OIS → **Solution :** utiliser l'endpoint `/tasks/stop` ; il suspend effectivement le travail en retirant le job de la file et permet une `restart` ultérieure.
- **Problème :** expiration du cookie d'authentification → **Solution :** pour les moniteurs de longue durée, utiliser un JWT Bearer signé avec la clé privée de l'environnement plutôt que le cookie de session d'un opérateur humain.

## Voir aussi {#see-also}

- [[monitoring-and-observability]]
- [[docker-fundamentals]]
- [[microservices-patterns]]
- [[runpod-production]]
