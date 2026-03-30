---
title: Database Security, Roles, and Access Control
category: reference
tags: [sql, security, roles, privileges, grant, revoke, rls, pg-hba, authentication, postgresql, mysql]
---

# Database Security, Roles, and Access Control

Database security encompasses authentication (who can connect), authorization (what they can do), and data protection (row-level security, encryption). Both PostgreSQL and MySQL use role-based access control with GRANT/REVOKE.

## Key Facts

- **Roles** (PostgreSQL) - unified concept for users and groups. A role with LOGIN is a user; without LOGIN is a group. MySQL uses separate USER and ROLE concepts (MySQL 8.0+)
- **pg_hba.conf** - PostgreSQL's connection authentication config. Controls which hosts can connect, which databases, which authentication method (md5, scram-sha-256, cert, trust)
- **GRANT/REVOKE** - assign or remove privileges on database objects. Privileges: SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER, CREATE, CONNECT, USAGE
- **Row-Level Security (RLS)** - PostgreSQL feature for row-level access control via policies. Transparent to applications. MySQL does not have native RLS
- **SCRAM-SHA-256** (PostgreSQL 10+) - recommended authentication method, replacing MD5
- **Default privileges** - set automatic grants for future objects with `ALTER DEFAULT PRIVILEGES`
- See [[views-and-materialized-views]] for security barrier views
- See [[postgresql-configuration-tuning]] for connection security settings

## Patterns

### PostgreSQL role management

```sql
-- Create application role
CREATE ROLE app_user WITH LOGIN PASSWORD 'secure_password';

-- Create read-only role (group)
CREATE ROLE readonly;
GRANT CONNECT ON DATABASE mydb TO readonly;
GRANT USAGE ON SCHEMA public TO readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT ON TABLES TO readonly;

-- Assign group role to user
GRANT readonly TO analyst_user;

-- Create application-specific role
CREATE ROLE app_readwrite;
GRANT CONNECT ON DATABASE mydb TO app_readwrite;
GRANT USAGE, CREATE ON SCHEMA public TO app_readwrite;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_readwrite;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO app_readwrite;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_readwrite;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT USAGE ON SEQUENCES TO app_readwrite;
```

### pg_hba.conf authentication

```
# TYPE  DATABASE  USER         ADDRESS           METHOD

# Local connections
local   all       postgres                       peer
local   all       all                            scram-sha-256

# Remote connections
host    mydb      app_user     10.0.0.0/8        scram-sha-256
host    all       all          0.0.0.0/0          reject

# SSL-required connections
hostssl mydb      app_user     0.0.0.0/0          scram-sha-256

# Replication
host    replication replicator  10.0.1.0/24       scram-sha-256
```

### Row-Level Security (PostgreSQL)

```sql
-- Enable RLS on table
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Policy: users see only their own documents
CREATE POLICY user_documents ON documents
    FOR ALL
    USING (owner_id = current_setting('app.user_id')::INT);

-- Multi-tenant isolation
CREATE POLICY tenant_isolation ON orders
    FOR ALL
    USING (tenant_id = current_setting('app.tenant_id')::INT)
    WITH CHECK (tenant_id = current_setting('app.tenant_id')::INT);

-- Set context in application connection
SET app.tenant_id = '42';
-- Now all queries on orders are automatically filtered by tenant_id = 42
```

### MySQL user and privilege management

```sql
-- Create user
CREATE USER 'app_user'@'10.0.%' IDENTIFIED BY 'secure_password';

-- Grant privileges
GRANT SELECT, INSERT, UPDATE, DELETE ON mydb.* TO 'app_user'@'10.0.%';

-- MySQL 8.0+ roles
CREATE ROLE 'app_readonly';
GRANT SELECT ON mydb.* TO 'app_readonly';
GRANT 'app_readonly' TO 'analyst'@'%';
SET DEFAULT ROLE 'app_readonly' TO 'analyst'@'%';

-- Revoke
REVOKE INSERT, UPDATE ON mydb.* FROM 'app_user'@'10.0.%';

-- View grants
SHOW GRANTS FOR 'app_user'@'10.0.%';
```

## Gotchas

- **PostgreSQL: table owner bypasses RLS** - the table owner and superusers are NOT subject to RLS policies by default. Use `ALTER TABLE ... FORCE ROW LEVEL SECURITY` to apply policies to the owner
- **Default PUBLIC grants** - PostgreSQL grants CONNECT on databases and USAGE on public schema to PUBLIC role by default. For strict security: `REVOKE ALL ON DATABASE mydb FROM PUBLIC;`
- **pg_hba.conf order matters** - first matching rule wins. Put more specific rules before general ones
- **MySQL user@host** - MySQL treats `'user'@'localhost'` and `'user'@'%'` as different users. This causes confusing access issues. Always specify host explicitly
- **ALTER DEFAULT PRIVILEGES** - only affects FUTURE objects created by the specified role. Existing objects need explicit GRANT
- **Password in connection string** - avoid hardcoding passwords. Use `.pgpass` file (PostgreSQL), `mysql_config_editor` (MySQL), or environment variables

## See Also

- [[views-and-materialized-views]] - security barrier views for additional protection
- [[postgresql-configuration-tuning]] - authentication and SSL settings
- [PostgreSQL client authentication](https://www.postgresql.org/docs/current/auth-pg-hba-conf.html)
- [PostgreSQL row security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [MySQL access control](https://dev.mysql.com/doc/refman/8.0/en/access-control.html)
