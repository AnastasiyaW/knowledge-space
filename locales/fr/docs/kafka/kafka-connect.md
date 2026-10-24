---
title: "Kafka Connect"
category: concepts
tags: [kafka, connect, source, sink, connector, smt, debezium, distributed, worker, task]
level: 4
source_sha256: 10c1374eda9c6f9982c5e62b846ae88bd9938725569d8c7ba41f41d6e5315287
translation: machine
translated_at: '2026-10-24'
---
# Kafka Connect {#kafka-connect}

Kafka Connect est un framework de streaming de données entre Kafka et des systèmes externes (bases de données, index de recherche, systèmes de fichiers, stockage cloud) à l'aide de connecteurs enfichables, avec tolérance aux pannes intégrée, répartition des tâches et gestion des offsets.

## Points clés {#key-facts}

- Fait partie d'Apache Kafka : fournit un runtime pour les plugins de connecteurs
- **Connecteurs source** : extraient les données des systèmes externes vers les topics Kafka
- **Connecteurs sink** : envoient les données des topics Kafka vers les systèmes externes
- **Connector** = coordinateur ; détermine le nombre de tâches, répartit le travail et reçoit la configuration depuis les workers
- **Task** = élément qui déplace réellement les données ; s'exécute dans son propre thread Java ; le connector découpe un job en plusieurs tasks pour le parallélisme
- **Worker** = processus conteneur pour les connectors et les tasks ; gère les requêtes REST, le stockage de la configuration et la réaffectation des tasks
- **Converter** = transforme entre tableaux d'octets et le format de données interne de Connect
- **SMT (Single Message Transform)** = transformations légères par message
- **Dead Letter Queue** = topic pour les messages en échec (connecteurs sink uniquement)
- Le mode distribué stocke les configurations, les offsets et les statuts dans des topics Kafka internes : `connect-configs`, `connect-offsets`, `connect-status`

## Patterns {#patterns}

### Exécuter Kafka Connect {#running-kafka-connect}

```bash
bin/connect-distributed.sh config/connect-distributed.properties
```

Propriétés clés :
```properties
bootstrap.servers=broker1:9092,broker2:9092
group.id=connect-cluster
plugin.path=/opt/connectors
key.converter=org.apache.kafka.connect.json.JsonConverter
value.converter=org.apache.kafka.connect.json.JsonConverter
rest.host.name=0.0.0.0
rest.port=8083
```

### API REST {#rest-api}

```bash
# List connector plugins
curl http://localhost:8083/connector-plugins | jq

# Create connector
curl -X POST http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  --data-binary "@connector-config.json"

# List / Status / Delete
curl http://localhost:8083/connectors
curl http://localhost:8083/connectors/{name}/status
curl -X DELETE http://localhost:8083/connectors/{name}

# Pause / Resume / Restart
curl -X PUT http://localhost:8083/connectors/{name}/pause
curl -X PUT http://localhost:8083/connectors/{name}/resume
curl -X POST http://localhost:8083/connectors/{name}/restart
curl -X POST http://localhost:8083/connectors/{name}/tasks/{id}/restart
```

### Connecteur source JDBC (PostgreSQL) {#jdbc-source-connector-postgresql}

```json
{
  "name": "postgres-source",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
    "connection.url": "jdbc:postgresql://localhost:5432/db",
    "table.whitelist": "clients,orders",
    "mode": "timestamp",
    "timestamp.column.name": "modified_date",
    "topic.prefix": "postgres."
  }
}
```

### Source CDC Debezium (WAL PostgreSQL) {#debezium-cdc-source-postgresql-wal}

```json
{
  "name": "postgres-cdc",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "localhost",
    "database.port": "5432",
    "database.user": "debezium",
    "database.password": "secret",
    "database.dbname": "mydb",
    "topic.prefix": "cdc",
    "plugin.name": "pgoutput"
  }
}
```

### SMT intégrées {#built-in-smts}

| SMT | Rôle |
|-----|---------|
| `Cast` | Modifier les types de champs |
| `MaskField` | Masquer les données sensibles |
| `Filter` | Supprimer ou conserver des messages selon une condition |
| `Flatten` | Aplatir les structures imbriquées |
| `InsertField` | Ajouter des champs (par exemple, horodatage, nom du topic) |
| `InsertHeader` | Ajouter des headers de message |
| `ReplaceField` | Renommer ou supprimer des champs |
| `TimestampConverter` | Convertir les formats d'horodatage |
| `TimestampRouter` | Router vers un topic selon l'horodatage |
| `RegexRouter` | Router vers un topic selon une correspondance par expression régulière |
| `ExtractField` | Extraire un seul champ d'un message complexe |

### Configuration de la Dead Letter Queue {#dead-letter-queue-configuration}

```json
{
  "errors.tolerance": "all",
  "errors.deadletterqueue.topic.name": "dlq-connector-errors",
  "errors.deadletterqueue.topic.replication.factor": 3,
  "errors.deadletterqueue.context.headers.enable": true
}
```

- `errors.tolerance=none` (par défaut) : une erreur provoque l'échec immédiat de la task
- `errors.tolerance=all` : les erreurs sont ignorées silencieusement, sauf si une DLQ est configurée

### Développement d'un connecteur personnalisé {#custom-connector-development}

```java
// Source Connector
public class MySourceConnector extends SourceConnector {
    public Class<? extends Task> taskClass() { return MySourceTask.class; }
    public List<Map<String, String>> taskConfigs(int maxTasks) { /* split work */ }
    public void start(Map<String, String> props) { }
    public void stop() { }
}

public class MySourceTask extends SourceTask {
    public List<SourceRecord> poll() { /* read from source, return records */ }
}

// Sink Connector
public class MySinkTask extends SinkTask {
    public void put(Collection<SinkRecord> records) { /* write to target */ }
}
```

### Mode autonome ou distribué {#standalone-vs-distributed}

| Mode | Cas d'usage | Tolérance aux pannes |
|------|----------|----------------|
| **Standalone** | Développement, tests | Aucune (processus unique) |
| **Distributed** | Production | Basculement automatique, rééquilibrage des tasks |

## Pièges à éviter {#gotchas}

- **L'échec d'une task ne déclenche PAS de rééquilibrage** : les tasks en échec doivent être redémarrées manuellement via l'API REST
- **L'échec d'un worker déclenche un rééquilibrage** : les tasks sont redistribuées vers les workers actifs restants
- **La DLQ ne fonctionne que pour les connecteurs sink** : les connecteurs source n'ont pas de mécanisme de DLQ
- **Converter incompatible = corruption silencieuse des données** : vérifiez que le producteur et Connect utilisent le même format de sérialisation
- **Gestion des schémas dans les connecteurs personnalisés** : utilisez `SchemaBuilder.struct()` pour définir les schémas d'enregistrements ; les enregistrements transportent leur schéma pour les consommateurs en aval
- **Polling JDBC vs CDC** : le source JDBC interroge la base à l'aide d'horodatages (avec un délai) ; Debezium lit le WAL pour une capture en temps réel (sans délai, sans charge supplémentaire sur la base)

## Voir aussi {#see-also}

- [[schema-registry]] - gestion des schémas pour les connecteurs Avro/Protobuf
- [[transactional-outbox]] - le CDC comme alternative au pattern outbox explicite
- [[ksqldb]] - ksqlDB peut créer et gérer des connecteurs via SQL
- [[kafka-monitoring-and-tuning]] - supervision des clusters Connect
- [Documentation Apache Kafka Connect](https://kafka.apache.org/documentation/#connect)
- [Confluent Hub - Marketplace de connecteurs](https://www.confluent.io/hub/)
