---
title: Database Security
category: techniques
tags: [security, database, mysql, postgresql, mongodb, encryption, access-control]
---

# Database Security

Database security for SQL and NoSQL: user privilege management, encryption at rest and in transit, auditing, backup security, cloud database security (RDS, Azure SQL), and Database Activity Monitoring.

## Key Facts
- Principle of least privilege: application accounts should NEVER have GRANT ALL or DBA privileges
- Separate read-only accounts for reporting/analytics from read-write application accounts
- Restrict `FILE` privilege (MySQL) to prevent `LOAD_FILE()` / `INTO OUTFILE` exploitation
- Restrict `xp_cmdshell` (MSSQL) to prevent OS command execution
- TDE (Transparent Data Encryption) encrypts database files on disk
- Cloud databases: provider manages patching/backups; customer manages access/encryption/network

## User Management and Privileges

### MySQL
```sql
CREATE USER 'appuser'@'localhost' IDENTIFIED BY 'strong_password';
GRANT SELECT, INSERT, UPDATE ON appdb.* TO 'appuser'@'localhost';
REVOKE DELETE ON appdb.* FROM 'appuser'@'localhost';
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'appuser'@'localhost';
```

### PostgreSQL
```sql
CREATE ROLE appuser WITH LOGIN PASSWORD 'strong_password';
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO appuser;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO appuser;
```

### MongoDB
```javascript
use admin
db.createUser({
    user: "appuser",
    pwd: "strong_password",
    roles: [{ role: "readWrite", db: "appdb" }]
})
```

## Encryption

### At Rest
- **TDE** (Transparent Data Encryption) - encrypts files on disk
- MySQL: InnoDB tablespace encryption
- PostgreSQL: `pgcrypto` for column-level encryption
- Full disk encryption as additional layer

### In Transit
```ini
# MySQL
require_secure_transport = ON

# PostgreSQL (postgresql.conf)
ssl = on
```
Always verify certificate authenticity on client side.

## Auditing
```sql
-- MySQL audit plugin
INSTALL PLUGIN audit_log SONAME 'audit_log.so';
SET GLOBAL audit_log_policy = 'ALL';
```

```ini
# PostgreSQL pgaudit (postgresql.conf)
shared_preload_libraries = 'pgaudit'
pgaudit.log = 'all'
```

## Database Activity Monitoring (DAM)
Real-time monitoring of all database access:
- Track queries, responses, schema changes
- Alert on suspicious activity (unusual queries, bulk export, privilege escalation)
- Compliance evidence (who accessed what, when)
- Products: Imperva, IBM Guardium, Oracle Audit Vault

## Backup Security
- Encrypt backups before storage (`gpg`, `openssl`, or native encryption)
- Store encryption keys separately from backups
- Test restore process regularly
- Restrict backup creation/restore permissions
- Apply retention policies (old backups still contain sensitive data)

## Cloud Database Security

### Managed Services (RDS, Azure SQL, Cloud SQL)
Provider handles: patching, backups, failover.
Customer handles: access control, encryption settings, network security.

### Network Security
- VPC/VNet private subnets (no public IP for databases)
- Security groups restricting inbound to application servers only
- VPC peering or Private Link for cross-VPC access
- SSL/TLS required for all connections

### IAM Integration
```json
{
    "Effect": "Allow",
    "Action": ["rds-db:connect"],
    "Resource": "arn:aws:rds-db:region:account:dbuser:dbi-resource-id/db_user"
}
```

## Gotchas
- Default MongoDB installation has no authentication enabled - always enable `security.authorization`
- Admin credentials in application connection strings = if app is compromised, database is fully compromised
- Database audit logs can grow very fast - configure rotation and retention
- Cloud "managed" does not mean "secure by default" - you still configure access and encryption
- Backup encryption keys must survive disasters - consider key escrow or HSM

## See Also
- [[sql-injection-deep-dive]] - injection attacks against databases
- [[secure-backend-development]] - ORM usage, parameterized queries
- [[compliance-and-regulations]] - data protection requirements
- [[cryptography-and-pki]] - encryption algorithms
