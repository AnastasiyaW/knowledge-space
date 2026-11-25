---
title: "Kafka-Sicherheit"
category: reference
tags: [kafka, security, ssl, tls, sasl, acl, authentication, authorization, encryption]
level: 3
source_sha256: 409dee3543a2b589f5164f04e51cf44465474b66b812b948e94aa52e69ab0981
translation: machine
translated_at: '2026-10-24'
---
# Kafka-Sicherheit {#kafka-security}

Die Sicherheit von Kafka umfasst drei Ebenen: Verschlüsselung (SSL/TLS für Daten bei der Übertragung), Authentifizierung (SASL zur Identitätsprüfung) und Autorisierung (ACLs zur Zugriffskontrolle).

## Wichtige Fakten {#key-facts}

- Drei Sicherheitsebenen: **Verschlüsselung** (SSL/TLS), **Authentifizierung** (SASL), **Autorisierung** (ACLs)
- Broker-Listener unterstützen: PLAINTEXT, SSL, SASL_PLAINTEXT, SASL_SSL
- SASL-Mechanismen: PLAIN, SCRAM-SHA-256/512, GSSAPI (Kerberos), OAUTHBEARER
- SASL/SCRAM wird für die meisten Deployments empfohlen
- ACLs werden über das CLI-Tool `kafka-acls.sh` verwaltet
- ACLs greifen pro Topic, Consumer Group, Cluster und Transactional ID
- Der KRaft-Modus erfordert `kafka.security.authorizer.AclAuthorizer` (nicht den veralteten `SimpleAclAuthorizer`)
- SSL/TLS deaktiviert Zero-Copy-Übertragung (Daten müssen im Userspace verschlüsselt werden)
- Das Zertifikatsmanagement ist der komplexeste operative Aspekt der Kafka-Sicherheit

## Muster {#patterns}

### SASL/PLAIN-Authentifizierung einrichten {#saslplain-authentication-setup}

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

### SSL/TLS-Einrichtung (Überblick) {#ssltls-setup-high-level}

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

### ACL-Verwaltung {#acl-management}

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

### ACL über die Admin API {#acl-via-admin-api}

```java
admin.createAcls(List.of(new AclBinding(
    new ResourcePattern(ResourceType.TOPIC, "orders", PatternType.LITERAL),
    new AccessControlEntry("User:alice", "*", AclOperation.WRITE, AclPermissionType.ALLOW)
)));
```

### Verschlüsselung ruhender Daten (Data-at-Rest) {#data-at-rest-encryption}

- Kafka verschlüsselt ruhende Daten nicht nativ
- Ansatz „Recht auf Vergessenwerden“: Daten mit pro Benutzer eigenen Schlüsseln verschlüsseln und den Schlüssel löschen, um die Daten unlesbar zu machen
- Die physischen Daten bleiben auf der Festplatte, können aber nicht entschlüsselt werden
- Alternative: Verschlüsselung auf Dateisystemebene verwenden (dm-crypt, LUKS)

## Fallstricke {#gotchas}

- **SSL deaktiviert Zero-Copy** - erhebliche Auswirkungen auf die Performance; den Durchsatz vor und nach der Aktivierung von SSL messen
- **Zertifikatsdokumentation ist oft unvollständig** - praktische Erfahrung ist unerlässlich; die SSL-Einrichtung ist die häufigste Ursache für Probleme beim Deployment
- **ACL-Änderungen erfordern einen Broker mit konfiguriertem Authorizer** - entweder `kafka.security.authorizer.AclAuthorizer` (KRaft) oder `kafka.security.auth.SimpleAclAuthorizer` (Legacy mit ZooKeeper)
- **Vor der KRaft-Migration von SimpleAclAuthorizer zu AclAuthorizer wechseln** - die beiden sind nicht kompatibel
- **Client-Keystore/Truststore getrennt vom Broker verwalten** - Clients benötigen eigene Zertifikate; Broker-Keystores nicht gemeinsam nutzen

## Siehe auch {#see-also}

- [[broker-architecture]] - Listener-Konfiguration, ACL-Aspekte bei der KRaft-Migration
- [[kafka-cluster-management]] - Best Practices für den operativen Betrieb in Bezug auf Sicherheit
- [Apache Kafka Sicherheitsdokumentation](https://kafka.apache.org/documentation/#security)
