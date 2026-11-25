---
title: "Datenbanksicherheit"
category: techniques
tags: [security, database, mysql, postgresql, mongodb, encryption, access-control]
level: 3
source_sha256: 3c1444decee2573c3e6e0295aa67845b438405d4384968ce87a01e037acbc31d
translation: machine
translated_at: '2026-10-24'
---
# Datenbanksicherheit {#database-security}

Datenbanksicherheit für SQL und NoSQL: Verwaltung von Benutzerprivilegien, Verschlüsselung im Ruhezustand und bei der Übertragung, Auditing, Sicherheit von Backups, Sicherheit von Cloud-Datenbanken (RDS, Azure SQL) sowie Database Activity Monitoring.

## Kernfakten {#key-facts}
- Prinzip der minimalen Berechtigungen: Anwendungskonten sollten NIEMALS GRANT ALL oder DBA-Privilegien besitzen
- Separate Konten mit reinem Lesezugriff für Reporting und Analytik, getrennt von Lese-Schreib-Konten der Anwendung
- `FILE`-Privileg einschränken (MySQL), um die Ausnutzung von `LOAD_FILE()` / `INTO OUTFILE` zu verhindern
- `xp_cmdshell` einschränken (MSSQL), um die Ausführung von Betriebssystembefehlen zu verhindern
- TDE (Transparent Data Encryption) verschlüsselt Datenbankdateien auf dem Datenträger
- Cloud-Datenbanken: Der Anbieter übernimmt Patching und Backups, der Kunde verwaltet Zugriff, Verschlüsselung und Netzwerk

## Benutzerverwaltung und Privilegien {#user-management-and-privileges}

### MySQL {#mysql}
```sql
CREATE USER 'appuser'@'localhost' IDENTIFIED BY 'strong_password';
GRANT SELECT, INSERT, UPDATE ON appdb.* TO 'appuser'@'localhost';
REVOKE DELETE ON appdb.* FROM 'appuser'@'localhost';
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'appuser'@'localhost';
```

### PostgreSQL {#postgresql}
```sql
CREATE ROLE appuser WITH LOGIN PASSWORD 'strong_password';
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO appuser;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO appuser;
```

### MongoDB {#mongodb}
```javascript
use admin
db.createUser({
    user: "appuser",
    pwd: "strong_password",
    roles: [{ role: "readWrite", db: "appdb" }]
})
```

## Verschlüsselung {#encryption}

### Im Ruhezustand {#at-rest}
- **TDE** (Transparent Data Encryption) - verschlüsselt Dateien auf dem Datenträger
- MySQL: Verschlüsselung von InnoDB-Tablespaces
- PostgreSQL: `pgcrypto` für die Verschlüsselung auf Spaltenebene
- Vollständige Festplattenverschlüsselung als zusätzliche Schicht

### Bei der Übertragung {#in-transit}
```ini
# MySQL
require_secure_transport = ON

# PostgreSQL (postgresql.conf)
ssl = on
```
Die Echtheit des Zertifikats ist immer auf Client-Seite zu prüfen.

## Auditing {#auditing}
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

## Database Activity Monitoring (DAM) {#database-activity-monitoring-dam}
Echtzeitüberwachung aller Datenbankzugriffe:
- Nachverfolgung von Abfragen, Antworten und Schemaänderungen
- Alarmierung bei verdächtigen Aktivitäten (ungewöhnliche Abfragen, Massenexporte, Rechteausweitung)
- Nachweise für Compliance (wer hat wann worauf zugegriffen)
- Produkte: Imperva, IBM Guardium, Oracle Audit Vault

## Sicherheit von Backups {#backup-security}
- Backups vor der Speicherung verschlüsseln (`gpg`, `openssl` oder native Verschlüsselung)
- Verschlüsselungsschlüssel getrennt von den Backups aufbewahren
- Wiederherstellungsprozess regelmäßig testen
- Berechtigungen zum Erstellen und Wiederherstellen von Backups einschränken
- Aufbewahrungsrichtlinien anwenden (alte Backups enthalten weiterhin sensible Daten)

## Sicherheit von Cloud-Datenbanken {#cloud-database-security}

### Managed Services (RDS, Azure SQL, Cloud SQL) {#managed-services-rds-azure-sql-cloud-sql}
Der Anbieter übernimmt: Patching, Backups, Failover.
Der Kunde übernimmt: Zugriffskontrolle, Verschlüsselungseinstellungen, Netzwerksicherheit.

### Netzwerksicherheit {#network-security}
- VPC/VNet mit privaten Subnetzen (keine öffentliche IP für Datenbanken)
- Security Groups, die eingehenden Verkehr nur von Anwendungsservern zulassen
- VPC Peering oder Private Link für VPC-übergreifenden Zugriff
- SSL/TLS für alle Verbindungen erforderlich

### IAM-Integration {#iam-integration}
```json
{
    "Effect": "Allow",
    "Action": ["rds-db:connect"],
    "Resource": "arn:aws:rds-db:region:account:dbuser:dbi-resource-id/db_user"
}
```

## Stolperfallen {#gotchas}
- Eine Standardinstallation von MongoDB hat keine Authentifizierung aktiviert - `security.authorization` immer aktivieren
- Administrator-Zugangsdaten in Verbindungszeichenfolgen der Anwendung bedeuten: Wenn die Anwendung kompromittiert wird, ist die Datenbank vollständig kompromittiert
- Datenbank-Auditprotokolle können sehr schnell anwachsen - Rotation und Aufbewahrung konfigurieren
- "Managed" bedeutet in der Cloud nicht "standardmäßig sicher" - Zugriff und Verschlüsselung müssen weiterhin konfiguriert werden
- Verschlüsselungsschlüssel für Backups müssen Katastrophen überdauern - Key Escrow oder HSM in Betracht ziehen

## Siehe auch {#see-also}
- [[sql-injection-deep-dive]] - Injection-Angriffe auf Datenbanken
- [[secure-backend-development]] - Verwendung von ORMs, parametrisierte Abfragen
- [[compliance-and-regulations]] - Anforderungen an den Datenschutz
- [[cryptography-and-pki]] - Verschlüsselungsalgorithmen
