---
title: Kafka Security
category: reference
tags: [kafka, security, ssl, sasl, acl, encryption, authentication, authorization]
---

# Kafka Security

Kafka ships with zero security by default - all connections are PLAINTEXT, no authentication, no authorization. Production deployments require three layers: **encryption** (SSL/TLS for data in transit), **authentication** (SASL or mTLS to prove identity), and **authorization** (ACLs or RBAC to control access). This entry covers the complete stack from certificate generation through audit logging.

## Listener Configuration

### Listener Types

Listeners define how clients and brokers connect. Each listener binds a name to a protocol on a specific port.

```properties
# Format: listener_name://host:port
listeners=PLAINTEXT://0.0.0.0:9092,SSL://0.0.0.0:9093,SASL_SSL://0.0.0.0:9094
```

| Protocol | Transport | Authentication | Production Use |
|----------|-----------|----------------|----------------|
| `PLAINTEXT` | Unencrypted | None | Never in prod |
| `SSL` | TLS encrypted | Optional client cert (mTLS) | Yes |
| `SASL_PLAINTEXT` | Unencrypted | SASL | Never in prod |
| `SASL_SSL` | TLS encrypted | SASL | Yes (most common) |

### advertised.listeners

What clients actually connect to. Must be resolvable from the client's network. Distinct from `listeners` (which is the bind address).

```properties
# Broker binds to all interfaces but advertises the external hostname
listeners=PLAINTEXT://0.0.0.0:9092,SSL://0.0.0.0:9093
advertised.listeners=PLAINTEXT://broker1.internal:9092,SSL://broker1.example.com:9093
```

Common multi-listener pattern - internal + external access:

```properties
listeners=INTERNAL://0.0.0.0:9092,EXTERNAL://0.0.0.0:9093
advertised.listeners=INTERNAL://broker1.internal:9092,EXTERNAL://broker1.public.com:9093
listener.security.protocol.map=INTERNAL:SASL_PLAINTEXT,EXTERNAL:SASL_SSL
inter.broker.listener.name=INTERNAL
```

### listener.security.protocol.map

Maps custom listener names to security protocols. Required when using non-standard listener names.

```properties
listener.security.protocol.map=INTERNAL:SASL_PLAINTEXT,EXTERNAL:SASL_SSL,CONTROLLER:SASL_SSL
```

Without this mapping, Kafka assumes the listener name IS the protocol name. So `listeners=SSL://...` works without a map, but `listeners=BROKER://...` requires an explicit mapping.

### Multiple Listeners - Complete Example

```properties
# 3 listeners: internal plaintext, external SSL, controller (KRaft)
listeners=INTERNAL://0.0.0.0:9092,EXTERNAL://0.0.0.0:9093,CONTROLLER://0.0.0.0:9094
advertised.listeners=INTERNAL://10.0.1.5:9092,EXTERNAL://kafka.example.com:9093
listener.security.protocol.map=INTERNAL:SASL_PLAINTEXT,EXTERNAL:SASL_SSL,CONTROLLER:SASL_SSL

# Inter-broker communication uses INTERNAL listener
inter.broker.listener.name=INTERNAL

# KRaft controller listener (not advertised to clients)
controller.listener.names=CONTROLLER
controller.quorum.voters=1@ctrl1:9094,2@ctrl2:9094,3@ctrl3:9094

# SASL config per listener
sasl.mechanism.inter.broker.protocol=SCRAM-SHA-512
listener.name.internal.sasl.enabled.mechanisms=SCRAM-SHA-512
listener.name.external.sasl.enabled.mechanisms=SCRAM-SHA-512,OAUTHBEARER
listener.name.controller.sasl.enabled.mechanisms=SCRAM-SHA-512
```

## SSL/TLS Encryption

### Keystore vs Truststore

| Store | Contains | Purpose |
|-------|----------|---------|
| **Keystore** | Private key + signed certificate | Proves this broker/client's identity |
| **Truststore** | CA certificate(s) | Validates the other party's certificate |

Each broker needs its own keystore (unique cert) but can share the same truststore (same CA).

### Step 1: Create Certificate Authority (CA)

```bash
# Generate CA private key and self-signed certificate
openssl req -new -x509 \
  -keyout ca-key \
  -out ca-cert \
  -days 365 \
  -subj "/CN=KafkaCA/OU=Kafka/O=MyOrg" \
  -passout pass:ca-password

# Verify CA cert
openssl x509 -in ca-cert -noout -subject -dates
```

### Step 2: Generate Broker Keystore and CSR

```bash
BROKER_HOST=broker1.example.com
BROKER_ID=1

# Generate keypair in PKCS12 keystore
keytool -genkey \
  -keyalg RSA \
  -keysize 2048 \
  -keystore server.keystore.jks \
  -alias $BROKER_HOST \
  -validity 365 \
  -storetype pkcs12 \
  -storepass keystore-password \
  -keypass keystore-password \
  -dname "CN=$BROKER_HOST,OU=Kafka,O=MyOrg,L=City,ST=State,C=US" \
  -ext "SAN=dns:$BROKER_HOST,dns:localhost,ip:10.0.1.$BROKER_ID"

# Export CSR
keytool -keystore server.keystore.jks \
  -alias $BROKER_HOST \
  -certreq \
  -file server.csr \
  -storepass keystore-password
```

The `-ext SAN=...` is critical - without Subject Alternative Names, hostname verification will fail.

### Step 3: Sign the Certificate with CA

```bash
# Sign the CSR
openssl x509 -req \
  -CA ca-cert \
  -CAkey ca-key \
  -in server.csr \
  -out server-cert-signed \
  -days 365 \
  -CAcreateserial \
  -passin pass:ca-password \
  -extensions v3_req \
  -extfile <(printf "[v3_req]\nsubjectAltName=DNS:$BROKER_HOST,DNS:localhost,IP:10.0.1.$BROKER_ID")

# Import CA cert into keystore (must be imported BEFORE the signed cert)
keytool -keystore server.keystore.jks \
  -alias CARoot \
  -importcert \
  -file ca-cert \
  -storepass keystore-password \
  -noprompt

# Import signed cert into keystore
keytool -keystore server.keystore.jks \
  -alias $BROKER_HOST \
  -importcert \
  -file server-cert-signed \
  -storepass keystore-password \
  -noprompt
```

### Step 4: Create Truststores

```bash
# Server truststore (trusts the CA)
keytool -keystore server.truststore.jks \
  -alias CARoot \
  -importcert \
  -file ca-cert \
  -storepass truststore-password \
  -noprompt

# Client truststore (same CA cert)
keytool -keystore client.truststore.jks \
  -alias CARoot \
  -importcert \
  -file ca-cert \
  -storepass truststore-password \
  -noprompt
```

### Step 5: Broker SSL Configuration

```properties
# server.properties
listeners=SSL://0.0.0.0:9093
advertised.listeners=SSL://broker1.example.com:9093

# Keystore (broker's identity)
ssl.keystore.location=/etc/kafka/ssl/server.keystore.jks
ssl.keystore.password=keystore-password
ssl.key.password=keystore-password
ssl.keystore.type=PKCS12

# Truststore (who to trust)
ssl.truststore.location=/etc/kafka/ssl/server.truststore.jks
ssl.truststore.password=truststore-password
ssl.truststore.type=JKS

# Inter-broker encryption
security.inter.broker.protocol=SSL

# Client certificate authentication
ssl.client.auth=required          # required | requested | none

# Hostname verification
ssl.endpoint.identification.algorithm=https  # set to empty string to disable

# TLS version and ciphers
ssl.enabled.protocols=TLSv1.3,TLSv1.2
ssl.protocol=TLSv1.3
ssl.cipher.suites=TLS_AES_256_GCM_SHA384,TLS_CHACHA20_POLY1305_SHA256
```

`ssl.client.auth` modes:
- `none` - server presents cert, client does not (one-way TLS)
- `requested` - server requests client cert but does not require it
- `required` - mutual TLS (mTLS) - both sides present certificates

### Step 6: Client SSL Configuration

```properties
# client-ssl.properties
security.protocol=SSL
ssl.truststore.location=/etc/kafka/ssl/client.truststore.jks
ssl.truststore.password=truststore-password

# For mTLS (ssl.client.auth=required on broker):
ssl.keystore.location=/etc/kafka/ssl/client.keystore.jks
ssl.keystore.password=client-keystore-password
ssl.key.password=client-keystore-password
```

### Verify SSL

```bash
# Test connectivity
openssl s_client -connect broker1.example.com:9093 -tls1_3

# Test with Kafka CLI tools
kafka-topics.sh --list \
  --bootstrap-server broker1.example.com:9093 \
  --command-config client-ssl.properties

kafka-console-producer.sh \
  --bootstrap-server broker1.example.com:9093 \
  --topic test \
  --producer.config client-ssl.properties
```

### Automation Script - Full PKI Setup

```bash
#!/bin/bash
set -euo pipefail

CA_PASS="ca-secret"
STORE_PASS="store-secret"
VALIDITY=365
BROKERS=("broker1.example.com" "broker2.example.com" "broker3.example.com")

# 1. CA
openssl req -new -x509 -keyout ca-key -out ca-cert \
  -days $VALIDITY -subj "/CN=KafkaCA" -passout pass:$CA_PASS

for i in "${!BROKERS[@]}"; do
  HOST="${BROKERS[$i]}"
  echo "=== Generating certs for $HOST ==="

  # 2. Keystore
  keytool -genkey -keyalg RSA -keysize 2048 \
    -keystore "$HOST.keystore.jks" -alias "$HOST" \
    -validity $VALIDITY -storetype pkcs12 \
    -storepass $STORE_PASS -keypass $STORE_PASS \
    -dname "CN=$HOST" -ext "SAN=dns:$HOST"

  # 3. CSR
  keytool -keystore "$HOST.keystore.jks" -alias "$HOST" \
    -certreq -file "$HOST.csr" -storepass $STORE_PASS

  # 4. Sign
  openssl x509 -req -CA ca-cert -CAkey ca-key \
    -in "$HOST.csr" -out "$HOST-signed.pem" \
    -days $VALIDITY -CAcreateserial -passin pass:$CA_PASS

  # 5. Import chain into keystore
  keytool -keystore "$HOST.keystore.jks" -alias CARoot \
    -importcert -file ca-cert -storepass $STORE_PASS -noprompt
  keytool -keystore "$HOST.keystore.jks" -alias "$HOST" \
    -importcert -file "$HOST-signed.pem" -storepass $STORE_PASS -noprompt

  # 6. Truststore
  keytool -keystore "$HOST.truststore.jks" -alias CARoot \
    -importcert -file ca-cert -storepass $STORE_PASS -noprompt
done

# Client truststore
keytool -keystore client.truststore.jks -alias CARoot \
  -importcert -file ca-cert -storepass $STORE_PASS -noprompt

echo "Done. Files: *.keystore.jks, *.truststore.jks, client.truststore.jks"
```

## SASL Authentication

### SASL/PLAIN

Username/password in JAAS config. Credentials stored in plaintext - always use over SSL (`SASL_SSL`).

**Broker JAAS:**

```
// kafka_server_jaas.conf
KafkaServer {
    org.apache.kafka.common.security.plain.PlainLoginModule required
    username="admin"
    password="admin-secret"
    user_admin="admin-secret"
    user_producer1="producer1-secret"
    user_consumer1="consumer1-secret";
};
```

- `username`/`password` - credentials this broker uses for inter-broker auth
- `user_<name>="<password>"` - credentials the broker accepts from clients

```properties
# server.properties
listeners=SASL_SSL://0.0.0.0:9094
security.inter.broker.protocol=SASL_SSL
sasl.mechanism.inter.broker.protocol=PLAIN
sasl.enabled.mechanisms=PLAIN
# + all SSL keystore/truststore properties
```

```bash
# Start broker with JAAS config
export KAFKA_OPTS="-Djava.security.auth.login.config=/etc/kafka/kafka_server_jaas.conf"
kafka-server-start.sh config/server.properties
```

**Client JAAS (inline in properties):**

```properties
# client-sasl.properties
security.protocol=SASL_SSL
sasl.mechanism=PLAIN
ssl.truststore.location=/etc/kafka/ssl/client.truststore.jks
ssl.truststore.password=truststore-password
sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required \
    username="producer1" \
    password="producer1-secret";
```

**Limitation**: adding/removing users requires editing the JAAS file and restarting all brokers. For dynamic user management, use SCRAM.

### SASL/SCRAM-SHA-256 and SCRAM-SHA-512

Salted Challenge Response Authentication Mechanism. Credentials stored in ZooKeeper or KRaft metadata - can add/remove users without broker restart.

**Create SCRAM credentials:**

```bash
# ZooKeeper mode
kafka-configs.sh --zookeeper localhost:2181 \
  --alter --add-config 'SCRAM-SHA-512=[password=alice-secret]' \
  --entity-type users --entity-name alice

# KRaft mode
kafka-configs.sh --bootstrap-server localhost:9092 \
  --alter --add-config 'SCRAM-SHA-512=[password=alice-secret]' \
  --entity-type users --entity-name alice \
  --command-config admin.properties

# List SCRAM credentials
kafka-configs.sh --bootstrap-server localhost:9092 \
  --describe --entity-type users --entity-name alice \
  --command-config admin.properties

# Delete SCRAM credentials
kafka-configs.sh --bootstrap-server localhost:9092 \
  --alter --delete-config 'SCRAM-SHA-512' \
  --entity-type users --entity-name alice \
  --command-config admin.properties
```

**Broker config:**

```properties
listeners=SASL_SSL://0.0.0.0:9094
sasl.enabled.mechanisms=SCRAM-SHA-512
sasl.mechanism.inter.broker.protocol=SCRAM-SHA-512
security.inter.broker.protocol=SASL_SSL
```

```
// kafka_server_jaas.conf (SCRAM)
KafkaServer {
    org.apache.kafka.common.security.scram.ScramLoginModule required
    username="admin"
    password="admin-secret";
};
```

**Client config:**

```properties
security.protocol=SASL_SSL
sasl.mechanism=SCRAM-SHA-512
ssl.truststore.location=/etc/kafka/ssl/client.truststore.jks
ssl.truststore.password=truststore-password
sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
    username="alice" \
    password="alice-secret";
```

**SCRAM-SHA-256 vs SCRAM-SHA-512**: SHA-512 is stronger hash but both are safe. SHA-512 preferred unless constrained by client library support.

### SASL/GSSAPI (Kerberos)

Enterprise authentication via Kerberos KDC. Each broker and client gets a Kerberos principal.

**Prerequisites:**
- Kerberos KDC running and accessible
- Service principal for each broker: `kafka/broker1.example.com@EXAMPLE.COM`
- Keytab files generated for each principal

```bash
# Create Kerberos principals (on KDC)
kadmin.local -q "addprinc -randkey kafka/broker1.example.com@EXAMPLE.COM"
kadmin.local -q "addprinc -randkey kafka/broker2.example.com@EXAMPLE.COM"
kadmin.local -q "addprinc -randkey kafkaproducer@EXAMPLE.COM"

# Export keytabs
kadmin.local -q "xst -k /etc/kafka/kafka_broker1.keytab kafka/broker1.example.com@EXAMPLE.COM"
kadmin.local -q "xst -k /etc/kafka/kafka_producer.keytab kafkaproducer@EXAMPLE.COM"
```

**Broker JAAS:**

```
KafkaServer {
    com.sun.security.auth.module.Krb5LoginModule required
    useKeyTab=true
    storeKey=true
    keyTab="/etc/kafka/kafka_broker.keytab"
    principal="kafka/broker1.example.com@EXAMPLE.COM";
};
```

```properties
# server.properties
sasl.enabled.mechanisms=GSSAPI
sasl.mechanism.inter.broker.protocol=GSSAPI
sasl.kerberos.service.name=kafka
security.inter.broker.protocol=SASL_SSL
```

**Client JAAS:**

```properties
sasl.mechanism=GSSAPI
sasl.kerberos.service.name=kafka
sasl.jaas.config=com.sun.security.auth.module.Krb5LoginModule required \
    useKeyTab=true \
    storeKey=true \
    keyTab="/etc/kafka/kafka_producer.keytab" \
    principal="kafkaproducer@EXAMPLE.COM";
```

### SASL/OAUTHBEARER

Token-based authentication using OAuth 2.0. Two implementations:

**1. Unsecured (development only):**

```properties
sasl.enabled.mechanisms=OAUTHBEARER
sasl.oauthbearer.token.endpoint.url=     # empty = unsecured
listener.name.sasl_ssl.oauthbearer.sasl.login.callback.handler.class=\
  org.apache.kafka.common.security.oauthbearer.internals.unsecured.OAuthBearerUnsecuredLoginCallbackHandler
listener.name.sasl_ssl.oauthbearer.sasl.server.callback.handler.class=\
  org.apache.kafka.common.security.oauthbearer.internals.unsecured.OAuthBearerUnsecuredValidatorCallbackHandler
```

**2. Production with OIDC provider (Kafka 3.1+):**

```properties
# server.properties
sasl.enabled.mechanisms=OAUTHBEARER
sasl.mechanism.inter.broker.protocol=OAUTHBEARER

# Token validation
listener.name.sasl_ssl.oauthbearer.sasl.server.callback.handler.class=\
  org.apache.kafka.common.security.oauthbearer.OAuthBearerValidatorCallbackHandler
listener.name.sasl_ssl.oauthbearer.sasl.oauthbearer.jwks.endpoint.url=\
  https://idp.example.com/.well-known/jwks.json
listener.name.sasl_ssl.oauthbearer.sasl.oauthbearer.expected.audience=kafka-cluster
listener.name.sasl_ssl.oauthbearer.sasl.oauthbearer.expected.issuer=\
  https://idp.example.com

# Token acquisition (for inter-broker)
listener.name.sasl_ssl.oauthbearer.sasl.login.callback.handler.class=\
  org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginCallbackHandler
sasl.oauthbearer.token.endpoint.url=https://idp.example.com/oauth/token
sasl.jaas.config=org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required \
    clientId="kafka-broker" \
    clientSecret="broker-secret" \
    scope="kafka";
```

**Client config (OIDC):**

```properties
security.protocol=SASL_SSL
sasl.mechanism=OAUTHBEARER
sasl.login.callback.handler.class=\
  org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginCallbackHandler
sasl.oauthbearer.token.endpoint.url=https://idp.example.com/oauth/token
sasl.jaas.config=org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required \
    clientId="my-app" \
    clientSecret="my-app-secret" \
    scope="kafka";
ssl.truststore.location=/etc/kafka/ssl/client.truststore.jks
ssl.truststore.password=truststore-password
```

### Multiple SASL Mechanisms

A single listener can accept multiple SASL mechanisms. Clients specify which one they use.

```properties
# Broker accepts both SCRAM and OAUTHBEARER on the same listener
sasl.enabled.mechanisms=SCRAM-SHA-512,OAUTHBEARER
# Inter-broker uses SCRAM
sasl.mechanism.inter.broker.protocol=SCRAM-SHA-512
```

### Per-Listener SASL Configuration

Different listeners can have different SASL settings:

```properties
listener.security.protocol.map=INTERNAL:SASL_PLAINTEXT,EXTERNAL:SASL_SSL
# Internal: only SCRAM
listener.name.internal.sasl.enabled.mechanisms=SCRAM-SHA-512
# External: SCRAM + OAUTHBEARER
listener.name.external.sasl.enabled.mechanisms=SCRAM-SHA-512,OAUTHBEARER
# External: custom OAUTHBEARER callbacks
listener.name.external.oauthbearer.sasl.server.callback.handler.class=\
  org.apache.kafka.common.security.oauthbearer.OAuthBearerValidatorCallbackHandler
```

## ACL Authorization

### Enabling ACLs

```properties
# ZooKeeper mode
authorizer.class.name=kafka.security.authorizer.AclAuthorizer

# KRaft mode
authorizer.class.name=org.apache.kafka.metadata.authorizer.StandardAuthorizer

# Superusers (bypass all ACLs)
super.users=User:admin;User:kafkabroker

# Allow access when no ACLs are defined (DANGEROUS in prod, useful during migration)
allow.everyone.if.no.acl.found=false
```

### ACL Model

Every ACL entry follows the pattern:

```
Principal P is [Allowed|Denied] Operation O from Host H
on Resource R matching ResourcePattern RP
```

**Resource Types:**

| Resource | Operations | Example |
|----------|-----------|---------|
| `Topic` | Read, Write, Create, Delete, Describe, Alter, DescribeConfigs, AlterConfigs | `--topic orders` |
| `Group` | Read, Describe, Delete | `--group my-consumer-group` |
| `Cluster` | Create, ClusterAction, Describe, Alter, DescribeConfigs, AlterConfigs, IdempotentWrite | `--cluster` |
| `TransactionalId` | Describe, Write | `--transactional-id my-tx-id` |
| `DelegationToken` | Describe | `--delegation-token` |

**Resource Pattern Types:**
- `LITERAL` (default) - exact match: `--topic orders` matches only topic `orders`
- `PREFIXED` - prefix match: `--topic orders --resource-pattern-type prefixed` matches `orders`, `orders-v2`, `orders.retry`

### kafka-acls.sh Operations

```bash
# Grant write on a specific topic
kafka-acls.sh --bootstrap-server localhost:9094 \
  --command-config admin.properties \
  --add \
  --allow-principal User:producer1 \
  --operation Write \
  --topic orders

# Grant read on topic + consumer group
kafka-acls.sh --bootstrap-server localhost:9094 \
  --command-config admin.properties \
  --add \
  --allow-principal User:consumer1 \
  --operation Read \
  --topic orders \
  --group order-processors

# Producer shorthand (Write + Describe + Create on topic)
kafka-acls.sh --bootstrap-server localhost:9094 \
  --command-config admin.properties \
  --add \
  --allow-principal User:producer1 \
  --producer \
  --topic orders

# Consumer shorthand (Read on topic + Read on group)
kafka-acls.sh --bootstrap-server localhost:9094 \
  --command-config admin.properties \
  --add \
  --allow-principal User:consumer1 \
  --consumer \
  --topic orders \
  --group order-processors

# Prefix-based ACL (all topics starting with "orders")
kafka-acls.sh --bootstrap-server localhost:9094 \
  --command-config admin.properties \
  --add \
  --allow-principal User:producer1 \
  --operation Write \
  --topic orders \
  --resource-pattern-type prefixed

# Deny from specific host
kafka-acls.sh --bootstrap-server localhost:9094 \
  --command-config admin.properties \
  --add \
  --deny-principal User:producer1 \
  --deny-host 192.168.1.100 \
  --operation Write \
  --topic orders

# Idempotent producer (requires cluster-level IdempotentWrite)
kafka-acls.sh --bootstrap-server localhost:9094 \
  --command-config admin.properties \
  --add \
  --allow-principal User:producer1 \
  --producer \
  --topic orders \
  --idempotent

# Transactional producer
kafka-acls.sh --bootstrap-server localhost:9094 \
  --command-config admin.properties \
  --add \
  --allow-principal User:tx-producer \
  --operation Write --operation Describe \
  --transactional-id my-tx-id

# List all ACLs
kafka-acls.sh --bootstrap-server localhost:9094 \
  --command-config admin.properties \
  --list

# List ACLs for specific topic
kafka-acls.sh --bootstrap-server localhost:9094 \
  --command-config admin.properties \
  --list --topic orders

# Remove ACL
kafka-acls.sh --bootstrap-server localhost:9094 \
  --command-config admin.properties \
  --remove \
  --allow-principal User:producer1 \
  --operation Write \
  --topic orders
```

### ACL Precedence Rules

1. If a resource has **no ACLs** and `allow.everyone.if.no.acl.found=false`, access is **denied** (except superusers)
2. **Deny** ACLs take precedence over **Allow** ACLs
3. If a user has an explicit **Allow** and no matching **Deny**, access is **allowed**
4. `User:*` matches all users (wildcard principal)

### Minimum ACLs for Common Patterns

**Simple producer:**
```
User:producer1 -> Write, Describe on Topic:orders
```

**Idempotent producer:**
```
User:producer1 -> Write, Describe on Topic:orders
User:producer1 -> IdempotentWrite on Cluster
```

**Transactional producer:**
```
User:producer1 -> Write, Describe on Topic:orders
User:producer1 -> Write, Describe on TransactionalId:my-tx
User:producer1 -> Write, Describe on Group (for offsets commit in EOS)
```

**Consumer:**
```
User:consumer1 -> Read, Describe on Topic:orders
User:consumer1 -> Read on Group:my-group
```

**Kafka Streams application:**
```
User:streams-app -> Read, Write, Create, Describe on Topic (internal topics auto-created)
User:streams-app -> Read on Group:streams-app-id
User:streams-app -> Write, Describe on TransactionalId:streams-app-id (if EOS)
```

**Kafka Connect:**
```
User:connect -> Read, Write, Create on Topic (config, offset, status topics)
User:connect -> Read on Group:connect-cluster
User:connect -> Read, Write on Topic (connector source/sink topics)
User:connect -> Create on Cluster (for internal topics)
```

## RBAC (Confluent Platform)

Confluent RBAC extends Kafka ACLs with role-based access control, centralized in Confluent's Metadata Service (MDS).

### Predefined Roles

| Role | Scope | Permissions |
|------|-------|-------------|
| `SystemAdmin` | Cluster | Full access to all resources |
| `ClusterAdmin` | Cluster | Manage cluster, brokers, topics |
| `SecurityAdmin` | Cluster | Manage role bindings |
| `Operator` | Cluster | View configs, manage consumer groups |
| `ResourceOwner` | Resource | Full control of specific resource |
| `DeveloperRead` | Resource | Read from topic/group |
| `DeveloperWrite` | Resource | Write to topic |
| `DeveloperManage` | Resource | Create/delete topics |

### Enabling RBAC

```properties
# server.properties
authorizer.class.name=io.confluent.kafka.security.authorizer.ConfluentServerAuthorizer
confluent.authorizer.access.rule.providers=CONFLUENT,ZK_ACL

# MDS configuration
confluent.metadata.server.listeners=https://0.0.0.0:8090
confluent.metadata.server.advertised.listeners=https://mds.example.com:8090

# LDAP integration
ldap.java.naming.provider.url=ldap://ldap.example.com:389
ldap.java.naming.security.principal=cn=admin,dc=example,dc=com
ldap.java.naming.security.credentials=ldap-password
ldap.search.base=dc=example,dc=com
ldap.user.search.filter=(uid={0})
ldap.group.search.filter=(member={0})
```

### Role Binding with confluent CLI

```bash
# Grant DeveloperWrite on topic "orders" to user alice
confluent iam rbac role-binding create \
  --principal User:alice \
  --role DeveloperWrite \
  --resource Topic:orders \
  --kafka-cluster-id $CLUSTER_ID

# Grant DeveloperRead on consumer group
confluent iam rbac role-binding create \
  --principal User:alice \
  --role DeveloperRead \
  --resource Group:order-processors \
  --kafka-cluster-id $CLUSTER_ID

# Grant ClusterAdmin to ops team group
confluent iam rbac role-binding create \
  --principal Group:ops-team \
  --role ClusterAdmin \
  --kafka-cluster-id $CLUSTER_ID

# List role bindings
confluent iam rbac role-binding list \
  --principal User:alice \
  --kafka-cluster-id $CLUSTER_ID

# Delete role binding
confluent iam rbac role-binding delete \
  --principal User:alice \
  --role DeveloperWrite \
  --resource Topic:orders \
  --kafka-cluster-id $CLUSTER_ID
```

### RBAC for Schema Registry and Connect

```bash
# Schema Registry: grant subject read
confluent iam rbac role-binding create \
  --principal User:alice \
  --role DeveloperRead \
  --resource Subject:orders-value \
  --kafka-cluster-id $CLUSTER_ID \
  --schema-registry-cluster-id $SR_CLUSTER_ID

# Connect: grant connector management
confluent iam rbac role-binding create \
  --principal User:alice \
  --role ResourceOwner \
  --resource Connector:jdbc-source \
  --kafka-cluster-id $CLUSTER_ID \
  --connect-cluster-id $CONNECT_CLUSTER_ID
```

## Audit Logging

### Built-in Kafka Logging

```properties
# log4j.properties - authorization decisions
log4j.logger.kafka.authorizer.logger=INFO, authorizerAppender
log4j.appender.authorizerAppender=org.apache.log4j.RollingFileAppender
log4j.appender.authorizerAppender.File=/var/log/kafka/kafka-authorizer.log
log4j.appender.authorizerAppender.MaxFileSize=256MB
log4j.appender.authorizerAppender.MaxBackupIndex=10
log4j.appender.authorizerAppender.layout=org.apache.log4j.PatternLayout
log4j.appender.authorizerAppender.layout.ConversionPattern=[%d] %p %m (%c)%n

# Request logging (all API calls)
log4j.logger.kafka.request.logger=WARN, requestAppender
log4j.appender.requestAppender=org.apache.log4j.RollingFileAppender
log4j.appender.requestAppender.File=/var/log/kafka/kafka-request.log
```

Log output for authorization:

```
[2026-03-30 10:15:32] INFO Principal = User:producer1 is Allowed Operation = Write
  from host = 10.0.1.50 on resource = Topic:LITERAL:orders (kafka.authorizer.logger)

[2026-03-30 10:15:33] INFO Principal = User:unknown is Denied Operation = Read
  from host = 192.168.1.200 on resource = Topic:LITERAL:orders (kafka.authorizer.logger)
```

### Confluent Audit Logs

Confluent Platform provides structured audit logging to a dedicated Kafka topic:

```properties
# server.properties
confluent.security.event.logger.enable=true
confluent.security.event.logger.destination.admin.topic=confluent-audit-log-events
confluent.security.event.logger.exporter.class=\
  io.confluent.security.auth.provider.ConfluentSecurityEventLogger

# Route audit events
confluent.security.event.router.config={
  "routes": {
    "crn:///kafka=*/topic=orders": {
      "produce": { "allowed": "confluent-audit-log-events", "denied": "confluent-audit-log-events" },
      "consume": { "allowed": "", "denied": "confluent-audit-log-events" }
    }
  },
  "defaultTopics": {
    "allowed": "",
    "denied": "confluent-audit-log-events"
  }
}
```

Audit event structure (JSON):

```json
{
  "id": "a1b2c3",
  "source": "crn:///kafka=cluster1",
  "type": "io.confluent.kafka.server/authorization",
  "time": "2026-03-30T10:15:32Z",
  "data": {
    "authenticationInfo": {
      "principal": "User:producer1"
    },
    "authorizationInfo": {
      "granted": true,
      "operation": "Write",
      "resourceType": "Topic",
      "resourceName": "orders",
      "patternType": "LITERAL"
    },
    "requestMetadata": {
      "clientAddress": "10.0.1.50"
    }
  }
}
```

## ZooKeeper Security

When using ZooKeeper mode (legacy), secure ZooKeeper communication separately.

### ZooKeeper SASL/Digest

```
// zookeeper_jaas.conf
Server {
    org.apache.zookeeper.server.auth.DigestLoginModule required
    user_super="admin-secret"
    user_kafka="kafka-secret";
};
```

```properties
# zookeeper.properties
authProvider.sasl=org.apache.zookeeper.server.auth.SASLAuthenticationProvider
requireClientAuthScheme=sasl
```

**Broker-to-ZooKeeper JAAS:**

```
// kafka_server_jaas.conf - add Client section
Client {
    org.apache.zookeeper.server.auth.DigestLoginModule required
    username="kafka"
    password="kafka-secret";
};
```

### ZooKeeper TLS (ZooKeeper 3.5+)

```properties
# zookeeper.properties
secureClientPort=2182
ssl.keyStore.location=/etc/zookeeper/ssl/zk.keystore.jks
ssl.keyStore.password=zk-keystore-pass
ssl.trustStore.location=/etc/zookeeper/ssl/zk.truststore.jks
ssl.trustStore.password=zk-truststore-pass

# Kafka broker connection
zookeeper.connect=zk1:2182,zk2:2182,zk3:2182
zookeeper.ssl.client.enable=true
zookeeper.clientCnxnSocket=org.apache.zookeeper.ClientCnxnSocketNetty
zookeeper.ssl.keystore.location=/etc/kafka/ssl/kafka-zk.keystore.jks
zookeeper.ssl.keystore.password=keystore-pass
zookeeper.ssl.truststore.location=/etc/kafka/ssl/kafka-zk.truststore.jks
zookeeper.ssl.truststore.password=truststore-pass
```

## Java Client Configuration (Programmatic)

### Producer with SASL_SSL

```java
Properties props = new Properties();
props.put("bootstrap.servers", "broker1:9094,broker2:9094");
props.put("security.protocol", "SASL_SSL");
props.put("sasl.mechanism", "SCRAM-SHA-512");
props.put("sasl.jaas.config",
    "org.apache.kafka.common.security.scram.ScramLoginModule required " +
    "username=\"producer1\" password=\"producer1-secret\";");
props.put("ssl.truststore.location", "/etc/kafka/ssl/client.truststore.jks");
props.put("ssl.truststore.password", "truststore-password");
props.put("ssl.endpoint.identification.algorithm", "https");

// Standard producer settings
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("acks", "all");

KafkaProducer<String, String> producer = new KafkaProducer<>(props);
```

### Spring Boot Configuration

```yaml
# application.yml
spring:
  kafka:
    bootstrap-servers: broker1:9094,broker2:9094
    security:
      protocol: SASL_SSL
    properties:
      sasl.mechanism: SCRAM-SHA-512
      sasl.jaas.config: >
        org.apache.kafka.common.security.scram.ScramLoginModule required
        username="myapp" password="${KAFKA_PASSWORD}";
    ssl:
      trust-store-location: classpath:client.truststore.jks
      trust-store-password: ${TRUSTSTORE_PASSWORD}
    producer:
      acks: all
    consumer:
      group-id: my-app-group
      auto-offset-reset: earliest
```

## Gotchas

- **SSL disables zero-copy transfer.** With SSL enabled, Kafka cannot use `sendfile()` for disk-to-network transfer. Expect 20-30% throughput reduction. Benchmark before and after.

- **`ssl.endpoint.identification.algorithm` defaults to `https`** since Kafka 2.0. If your certs don't have proper SANs matching the advertised hostname, connections fail with `SSLHandshakeException`. Set to empty string only in dev, never in prod.

- **SCRAM users must exist before broker startup.** In KRaft mode, at least the inter-broker SCRAM user must be created during cluster formatting. In ZK mode, create users in ZK before starting brokers.

- **SASL/PLAIN sends passwords in cleartext.** The PLAIN mechanism name is misleading - it does NOT encrypt. Always pair with SSL transport (`SASL_SSL`). The "PLAIN" refers to the SASL mechanism, not the transport.

- **No ACLs = no access** when the authorizer is enabled (except for superusers). During ACL migration, temporarily set `allow.everyone.if.no.acl.found=true`, add ACLs, then flip to `false`. Missing this locks out all clients.

- **Inter-broker protocol is configured separately.** Setting client-facing listener to `SASL_SSL` does NOT encrypt broker-to-broker traffic. You must explicitly set `security.inter.broker.protocol=SASL_SSL`.

- **KRaft uses a different authorizer class.** `AclAuthorizer` is for ZooKeeper mode; `StandardAuthorizer` is for KRaft. Using the wrong one prevents broker startup.

- **Deny ACLs override Allow.** If a user matches both an Allow and a Deny ACL, Deny wins. This is useful for blacklisting specific hosts but can cause confusing access denials if not tracked.

- **Certificate renewal requires rolling restart.** Kafka does not hot-reload SSL certificates. Plan for rolling restarts when renewing certs. Some deployments use short-lived certs with automated renewal scripts.

- **JAAS config via `-Djava.security.auth.login.config` is JVM-global.** If running multiple Kafka components (broker + Connect) in the same JVM (don't), use the inline `sasl.jaas.config` property instead.

- **OAUTHBEARER token refresh.** Kafka clients automatically refresh tokens before expiry, but if the token endpoint is slow or unreachable, connections fail. Set `sasl.login.retry.backoff.ms` and `sasl.login.retry.backoff.max.ms` for resilience.

- **Kafka Connect and Schema Registry need their own security config.** They are separate JVM processes with separate `security.protocol`, `sasl.jaas.config`, and SSL properties. Each needs its own ACLs/RBAC bindings.

## Quick Reference

**Certificate generation sequence:**

```
1. openssl req -new -x509           -> CA key + cert
2. keytool -genkey                  -> broker keystore with keypair
3. keytool -certreq                 -> CSR from broker keystore
4. openssl x509 -req                -> sign CSR with CA
5. keytool -importcert (CA)         -> CA cert into keystore
6. keytool -importcert (signed)     -> signed cert into keystore
7. keytool -importcert (CA)         -> CA cert into truststore(s)
```

**Security protocol decision tree:**

```
Need encryption? --no--> PLAINTEXT (dev only)
  |yes
  Need auth? --no--> SSL (encryption only, or mTLS)
    |yes
    --> SASL_SSL
        Which SASL mechanism?
          Internal users, static --> PLAIN (simple, restart to change users)
          Internal users, dynamic --> SCRAM-SHA-512 (add/remove without restart)
          Enterprise/AD/LDAP --> GSSAPI/Kerberos
          Cloud/microservices --> OAUTHBEARER
```

**Key kafka-acls.sh flags:**

| Flag | Purpose |
|------|---------|
| `--add` / `--remove` / `--list` | ACL operation |
| `--allow-principal` / `--deny-principal` | Target user (`User:name`) |
| `--allow-host` / `--deny-host` | Restrict to IP address |
| `--operation` | Permission (Read, Write, Create, Delete, Describe, Alter, etc.) |
| `--topic` / `--group` / `--cluster` | Resource type |
| `--transactional-id` | Transactional resource |
| `--producer` / `--consumer` | Shorthand for common permission sets |
| `--idempotent` | Include IdempotentWrite on Cluster |
| `--resource-pattern-type` | `literal` (default) or `prefixed` |

## See Also

- [[broker-architecture]] - listener configuration, inter-broker communication, KRaft setup
- [[kafka-connect]] - securing connectors, Connect worker security properties
- [[kafka-cluster-operations]] - rolling restarts for cert renewal, SCRAM user management
