---
title: Kafka Security
category: reference
tags: [kafka, security, ssl, tls, sasl, acl, authentication, authorization, encryption]
---

# Kafka Security

Kafka security covers three layers: encryption (SSL/TLS for data in transit), authentication (SASL for identity verification), and authorization (ACLs for access control).

## Key Facts

- Three security layers: **encryption** (SSL/TLS), **authentication** (SASL), **authorization** (ACLs)
- Broker listeners support: PLAINTEXT, SSL, SASL_PLAINTEXT, SASL_SSL
- SASL mechanisms: PLAIN, SCRAM-SHA-256/512, GSSAPI (Kerberos), OAUTHBEARER
- SASL/SCRAM recommended for most deployments
- ACLs managed via `kafka-acls.sh` CLI tool
- ACLs enforce per topic, consumer group, cluster, transactional ID
- KRaft mode requires `kafka.security.authorizer.AclAuthorizer` (not the legacy `SimpleAclAuthorizer`)
- SSL/TLS disables zero-copy transfer (data must be encrypted in userspace)
- Certificate management is the most complex operational aspect of Kafka security

## Patterns

### SASL/PLAIN Authentication Setup

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

### SSL/TLS Setup (High-Level)

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

### ACL Management

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

### ACL via Admin API

```java
admin.createAcls(List.of(new AclBinding(
    new ResourcePattern(ResourceType.TOPIC, "orders", PatternType.LITERAL),
    new AccessControlEntry("User:alice", "*", AclOperation.WRITE, AclPermissionType.ALLOW)
)));
```

### Data-at-Rest Encryption

- Kafka does not natively encrypt data at rest
- "Right to be forgotten" approach: encrypt data with per-user keys, delete the key to make data unreadable
- Physical data remains on disk but cannot be decrypted
- Alternative: use filesystem-level encryption (dm-crypt, LUKS)

## Gotchas

- **SSL disables zero-copy** - significant performance impact; measure throughput before and after enabling SSL
- **Certificate documentation is often incomplete** - hands-on practice essential; SSL setup is the most common source of deployment issues
- **ACL changes require broker configured with authorizer** - either `kafka.security.authorizer.AclAuthorizer` (KRaft) or `kafka.security.auth.SimpleAclAuthorizer` (legacy ZK)
- **Switch from SimpleAclAuthorizer to AclAuthorizer before KRaft migration** - they are not compatible
- **Client keystore/truststore separate from broker** - clients need their own certificates; don't share broker keystores

## See Also

- [[broker-architecture]] - listener configuration, KRaft migration ACL considerations
- [[kafka-cluster-management]] - operational security best practices
- [Apache Kafka Security Documentation](https://kafka.apache.org/documentation/#security)
