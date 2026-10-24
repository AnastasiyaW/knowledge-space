---
title: "Sécurité de Kafka"
category: reference
tags: [kafka, security, ssl, tls, sasl, acl, authentication, authorization, encryption]
level: 3
source_sha256: 409dee3543a2b589f5164f04e51cf44465474b66b812b948e94aa52e69ab0981
translation: machine
translated_at: '2026-10-24'
---
# Sécurité de Kafka {#kafka-security}

La sécurité de Kafka repose sur trois couches : le chiffrement (SSL/TLS pour les données en transit), l'authentification (SASL pour la vérification de l'identité) et l'autorisation (ACL pour le contrôle d'accès).

## Points clés {#key-facts}

- Trois couches de sécurité : **chiffrement** (SSL/TLS), **authentification** (SASL), **autorisation** (ACL)
- Les listeners des brokers prennent en charge : PLAINTEXT, SSL, SASL_PLAINTEXT, SASL_SSL
- Mécanismes SASL : PLAIN, SCRAM-SHA-256/512, GSSAPI (Kerberos), OAUTHBEARER
- SASL/SCRAM recommandé pour la plupart des déploiements
- ACL gérées via l'outil en ligne de commande `kafka-acls.sh`
- Les ACL s'appliquent par topic, par consumer group, par cluster et par transactional ID
- Le mode KRaft nécessite `kafka.security.authorizer.AclAuthorizer` (et non l'ancien `SimpleAclAuthorizer`)
- SSL/TLS désactive le transfert zero-copy (les données doivent être chiffrées dans l'espace utilisateur)
- La gestion des certificats est l'aspect opérationnel le plus complexe de la sécurité de Kafka

## Modèles {#patterns}

### Mise en place de l'authentification SASL/PLAIN {#saslplain-authentication-setup}

```properties
# server.properties (broker)
listeners=SASL_PLAINTEXT://0.0.0.0:9092
security.inter.broker.protocol=SASL_PLAINTEXT
sasl.mechanism.inter.broker.protocol=PLAIN
sasl.enabled.mechanisms=PLAIN

# JAAS config for broker
listener.name.sasl_plaintext.plain.sasl.jaas.config=\
  org.apache.kafka.common.security.plain.PlainLoginModule required \
  username="admin" password="admin-secret" \
  user_admin="admin-secret" \
  user_alice="alice-secret" \
  user_bob="bob-secret";
```

```properties
# client.properties
security.protocol=SASL_PLAINTEXT
sasl.mechanism=PLAIN
sasl.jaas.config=\
  org.apache.kafka.common.security.plain.PlainLoginModule required \
  username="alice" password="alice-secret";
```

### Mise en place de SSL/TLS (vue d'ensemble) {#ssltls-setup-high-level}

```bash
# 1. Generate CA key and certificate
openssl req -new -x509 -keyout ca-key -out ca-cert -days 365

# 2. Generate broker keystore
keytool -keystore kafka.server.keystore.jks -alias localhost \
  -genkey -keyalg RSA -validity 365

# 3. Sign broker certificate with CA
keytool -keystore kafka.server.keystore.jks -alias localhost \
  -certreq -file cert-request
openssl x509 -req -CA ca-cert -CAkey ca-key \
  -in cert-request -out cert-signed -days 365

# 4. Import CA and signed cert into keystore
keytool -keystore kafka.server.keystore.jks -alias CARoot \
  -import -file ca-cert
keytool -keystore kafka.server.keystore.jks -alias localhost \
  -import -file cert-signed

# 5. Create truststore with CA cert
keytool -keystore kafka.server.truststore.jks -alias CARoot \
  -import -file ca-cert
```

```properties
# Broker SSL config
listeners=SSL://0.0.0.0:9093
ssl.keystore.location=/var/kafka/ssl/kafka.server.keystore.jks
ssl.keystore.password=keystorepass
ssl.key.password=keypass
ssl.truststore.location=/var/kafka/ssl/kafka.server.truststore.jks
ssl.truststore.password=truststorepass
```

### Gestion des ACL {#acl-management}

```bash
# Grant write permission
kafka-acls.sh --bootstrap-server localhost:9092 \
  --add --allow-principal User:alice \
  --operation Write --topic orders

# Grant read permission
kafka-acls.sh --bootstrap-server localhost:9092 \
  --add --allow-principal User:bob \
  --operation Read --topic orders \
  --group my-consumer-group

# List ACLs
kafka-acls.sh --bootstrap-server localhost:9092 \
  --list --topic orders

# Remove ACL
kafka-acls.sh --bootstrap-server localhost:9092 \
  --remove --allow-principal User:alice \
  --operation Write --topic orders
```

### ACL via l'API d'administration {#acl-via-admin-api}

```java
admin.createAcls(List.of(new AclBinding(
    new ResourcePattern(ResourceType.TOPIC, "orders", PatternType.LITERAL),
    new AccessControlEntry("User:alice", "*", AclOperation.WRITE, AclPermissionType.ALLOW)
)));
```

### Chiffrement des données au repos {#data-at-rest-encryption}

- Kafka ne chiffre pas nativement les données au repos
- Approche « droit à l'oubli » : chiffrer les données avec des clés propres à chaque utilisateur, puis supprimer la clé pour rendre les données illisibles
- Les données physiques restent sur le disque, mais ne peuvent plus être déchiffrées
- Alternative : utiliser le chiffrement au niveau du système de fichiers (dm-crypt, LUKS)

## Pièges à éviter {#gotchas}

- **SSL désactive le zero-copy** : impact significatif sur les performances ; mesurez le débit avant et après l'activation de SSL
- **La documentation sur les certificats est souvent incomplète** : la pratique concrète est indispensable ; la configuration SSL est la source la plus courante de problèmes de déploiement
- **Les modifications d'ACL nécessitent un broker configuré avec un authorizer** : soit `kafka.security.authorizer.AclAuthorizer` (KRaft), soit `kafka.security.auth.SimpleAclAuthorizer` (ZooKeeper, legacy)
- **Passer de SimpleAclAuthorizer à AclAuthorizer avant la migration vers KRaft** : ils ne sont pas compatibles
- **Keystore/truststore du client distincts de ceux du broker** : les clients ont besoin de leurs propres certificats ; ne partagez pas les keystores des brokers

## Voir aussi {#see-also}

- [[broker-architecture]] - configuration des listeners, considérations sur les ACL lors de la migration vers KRaft
- [[kafka-cluster-management]] - bonnes pratiques de sécurité opérationnelle
- [Documentation de sécurité Apache Kafka](https://kafka.apache.org/documentation/#security)
