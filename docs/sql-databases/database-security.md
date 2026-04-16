---
title: Database Security
category: concepts
tags: [sql-databases, security, sql-injection, tls, encryption, roles, privileges, homomorphic-encryption]
---

# Database Security

Database security spans multiple layers: network access, authentication, authorization, encryption, and application-level query safety. SQL injection remains the most common attack vector.

## SQL Injection Prevention

```sql
-- VULNERABLE: string concatenation
query = "SELECT * FROM users WHERE name = '" + userInput + "'";
-- Input: ' OR 1=1 -- bypasses authentication

-- SAFE: parameterized queries (prepared statements)
-- PostgreSQL (Python psycopg2)
cursor.execute("SELECT * FROM users WHERE id = %s", [user_id])

-- MySQL (Node.js)
pool.query('SELECT * FROM users WHERE id = $1', [userId])

-- PHP PDO
$stmt = $pdo->prepare("SELECT * FROM users WHERE age > :age");
$stmt->execute(['age' => 25]);
```

**Always use prepared statements with parameter binding. Never concatenate user input into SQL strings.**

## Authentication and Access Control

### PostgreSQL TLS/SSL Setup
```bash
# Generate certificate
openssl req -new -x509 -days 365 -nodes -out server.crt -keyout server.key
chmod 600 server.key

# postgresql.conf
ssl = on
ssl_cert_file = 'server.crt'
ssl_key_file = 'server.key'

# pg_hba.conf - require SSL for remote connections
hostssl  all  all  0.0.0.0/0  scram-sha-256
```

SSL client modes: `disable`, `allow`, `prefer`, `require`, `verify-ca`, `verify-full`.

### Roles and Privileges
```sql
-- Create roles
CREATE ROLE app_readonly LOGIN PASSWORD 'pass';
CREATE ROLE app_readwrite LOGIN PASSWORD 'pass';

-- Grant minimum necessary permissions
GRANT CONNECT ON DATABASE mydb TO app_readonly;
GRANT USAGE ON SCHEMA public TO app_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_readonly;

GRANT CONNECT ON DATABASE mydb TO app_readwrite;
GRANT USAGE ON SCHEMA public TO app_readwrite;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_readwrite;
```

## Principle of Least Privilege

- Application user: minimum necessary permissions (not superuser)
- Separate read-only and read-write accounts
- Separate connection pooler credentials from admin credentials
- Never use superuser for application connections
- Audit logging for privileged operations

## Encryption

**At Rest:** Data files encrypted on disk. TDE (Transparent Data Encryption) in SQL Server/Oracle. `pgcrypto` extension in PostgreSQL. Protects against physical disk theft.

**In Transit:** TLS/SSL for all client-to-server and server-to-server communication. Performance impact mitigated by connection pooling (TLS handshake happens once).

**Homomorphic Encryption (HE):** Allows arithmetic on encrypted data without decryption. FHE enables encrypted DB queries, L7 routing without TLS termination, index building on encrypted data. Still orders of magnitude slower than plaintext - not production-ready. IBM FHE Toolkit for experimentation.

## Wire Protocol Security

PostgreSQL wire protocol: all data transmitted as plaintext without TLS. Password sent as MD5 hash or SCRAM-SHA-256 challenge. Always enable TLS for production.

```bash
psql "host=server sslmode=verify-full sslrootcert=ca.crt"
```

## Key Facts

- SCRAM-SHA-256 is the recommended authentication method (PG 10+)
- `pg_hba.conf` controls which hosts can connect and how they authenticate
- Network-level security: firewall rules, IP whitelisting, VPN
- `log_connections = on` and `log_disconnections = on` for audit trail
- Data checksums detect silent corruption but not malicious modification

## Gotchas

- MD5 authentication is deprecated - use SCRAM-SHA-256
- `pg_hba.conf` processed top-to-bottom, first match wins
- `host all all 0.0.0.0/0 trust` in pg_hba.conf = no authentication (disaster)
- Connection strings in code/config may contain plaintext passwords - use pgpass or environment variables
- FHE is 10,000-1,000,000x slower than plaintext operations - research only
- Never store connection passwords in version control

## See Also

- [[postgresql-configuration-tuning]] - pg_hba.conf and listen_addresses
- [[connection-pooling]] - credential management with poolers
- [[postgresql-ha-patroni]] - TLS between Patroni nodes
- [[replication-fundamentals]] - encrypted replication connections
