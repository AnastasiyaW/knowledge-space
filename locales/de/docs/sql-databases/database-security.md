---
title: "Datenbanksicherheit"
category: concepts
tags: [sql-databases, security, sql-injection, tls, encryption, roles, privileges, homomorphic-encryption]
level: 3
source_sha256: 6d5f2d9684c76b295bbbb6b98f4e167cfaad7b5041e1825160d0df8cbc26a01f
translation: machine
translated_at: '2026-10-24'
---
# Datenbanksicherheit {#database-security}

Datenbanksicherheit umfasst mehrere Ebenen: Netzwerkzugriff, Authentifizierung, Autorisierung, Verschlüsselung und die Sicherheit von Abfragen auf Anwendungsebene. SQL-Injection bleibt der häufigste Angriffsvektor.

## Prävention von SQL-Injection {#sql-injection-prevention}

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

**Verwenden Sie immer Prepared Statements mit Parameterbindung. Verketten Sie niemals Benutzereingaben zu SQL-Strings.**

## Authentifizierung und Zugriffskontrolle {#authentication-and-access-control}

### PostgreSQL TLS/SSL-Einrichtung {#postgresql-tlsssl-setup}
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

SSL-Clientmodi: `disable`, `allow`, `prefer`, `require`, `verify-ca`, `verify-full`.

### Rollen und Berechtigungen {#roles-and-privileges}
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

## Prinzip der minimalen Berechtigungen {#principle-of-least-privilege}

- Anwendungsbenutzer: nur die notwendigen Berechtigungen (nicht Superuser)
- Getrennte Konten für Lese- und Schreibzugriff
- Zugangsdaten des Connection Poolers getrennt von Admin-Zugangsdaten verwalten
- Niemals Superuser für Anwendungsverbindungen verwenden
- Audit-Logging für privilegierte Operationen

## Verschlüsselung {#encryption}

**Im Ruhezustand (At Rest):** Datendateien sind auf dem Datenträger verschlüsselt. TDE (Transparent Data Encryption) in SQL Server/Oracle. Die Erweiterung `pgcrypto` in PostgreSQL. Schützt vor physischem Diebstahl von Datenträgern.

**Während der Übertragung (In Transit):** TLS/SSL für die gesamte Kommunikation zwischen Client und Server sowie zwischen Servern. Die Performance-Auswirkungen werden durch Connection Pooling abgemildert (der TLS-Handshake erfolgt nur einmal).

**Homomorphe Verschlüsselung (HE):** Ermöglicht Berechnungen auf verschlüsselten Daten ohne Entschlüsselung. FHE ermöglicht verschlüsselte DB-Abfragen, L7-Routing ohne TLS-Terminierung sowie den Aufbau von Indizes auf verschlüsselten Daten. Immer noch um Größenordnungen langsamer als Klartext – nicht produktionsreif. IBM FHE Toolkit für Experimente.

## Sicherheit des Wire-Protokolls {#wire-protocol-security}

PostgreSQL-Wire-Protokoll: Alle Daten werden ohne TLS im Klartext übertragen. Das Passwort wird als MD5-Hash oder per SCRAM-SHA-256-Challenge gesendet. Aktivieren Sie für Produktivsysteme immer TLS.

```bash
psql "host=server sslmode=verify-full sslrootcert=ca.crt"
```

## Wichtige Fakten {#key-facts}

- SCRAM-SHA-256 ist die empfohlene Authentifizierungsmethode (PG 10+)
- `pg_hba.conf` steuert, welche Hosts sich verbinden dürfen und wie sie sich authentifizieren
- Netzwerkseitige Sicherheit: Firewall-Regeln, IP-Whitelisting, VPN
- `log_connections = on` und `log_disconnections = on` für den Audit-Trail
- Datenprüfsummen erkennen stille Datenkorruption, aber nicht absichtliche Manipulation

## Stolperfallen {#gotchas}

- MD5-Authentifizierung ist veraltet – verwenden Sie SCRAM-SHA-256
- `pg_hba.conf` wird von oben nach unten verarbeitet, der erste Treffer gewinnt
- `host all all 0.0.0.0/0 trust` in pg_hba.conf = keine Authentifizierung (katastrophal)
- Verbindungszeichenfolgen in Code/Konfiguration können Klartext-Passwörter enthalten – verwenden Sie pgpass oder Umgebungsvariablen
- FHE ist 10.000- bis 1.000.000-mal langsamer als Klartextoperationen – nur für die Forschung
- Speichern Sie Verbindungspasswörter niemals in der Versionsverwaltung

## Siehe auch {#see-also}

- [[postgresql-configuration-tuning]] - pg_hba.conf und listen_addresses
- [[connection-pooling]] - Verwaltung von Zugangsdaten bei Poolern
- [[postgresql-ha-patroni]] - TLS zwischen Patroni-Knoten
- [[replication-fundamentals]] - verschlüsselte Replikationsverbindungen
