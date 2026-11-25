---
title: "Sécurité des bases de données"
category: techniques
tags: [security, database, mysql, postgresql, mongodb, encryption, access-control]
level: 3
source_sha256: 3c1444decee2573c3e6e0295aa67845b438405d4384968ce87a01e037acbc31d
translation: machine
translated_at: '2026-10-24'
---
# Sécurité des bases de données {#database-security}

Sécurité des bases de données SQL et NoSQL : gestion des privilèges utilisateurs, chiffrement au repos et en transit, audit, sécurité des sauvegardes, sécurité des bases de données cloud (RDS, Azure SQL) et surveillance de l'activité des bases de données (Database Activity Monitoring).

## Points clés {#key-facts}
- Principe du moindre privilège : les comptes applicatifs ne doivent JAMAIS disposer de GRANT ALL ou de privilèges DBA
- Utiliser des comptes en lecture seule distincts pour le reporting et l'analytique, séparés des comptes applicatifs en lecture-écriture
- Restreindre le privilège `FILE` (MySQL) pour empêcher l'exploitation de `LOAD_FILE()` et `INTO OUTFILE`
- Restreindre `xp_cmdshell` (MSSQL) pour empêcher l'exécution de commandes système
- TDE (Transparent Data Encryption) chiffre les fichiers de base de données sur disque
- Bases de données cloud : le fournisseur gère les correctifs et les sauvegardes ; le client gère les accès, le chiffrement et le réseau

## Gestion des utilisateurs et des privilèges {#user-management-and-privileges}

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

## Chiffrement {#encryption}

### Au repos {#at-rest}
- **TDE** (Transparent Data Encryption) : chiffre les fichiers sur disque
- MySQL : chiffrement des tablespaces InnoDB
- PostgreSQL : `pgcrypto` pour le chiffrement au niveau des colonnes
- Chiffrement complet du disque comme couche supplémentaire

### En transit {#in-transit}
```ini
# MySQL
require_secure_transport = ON

# PostgreSQL (postgresql.conf)
ssl = on
```
Vérifier systématiquement l'authenticité du certificat côté client.

## Audit {#auditing}
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

## Surveillance de l'activité des bases de données (DAM) {#database-activity-monitoring-dam}
Surveillance en temps réel de tous les accès à la base de données :
- Suivi des requêtes, des réponses et des modifications de schéma
- Alertes sur les activités suspectes (requêtes inhabituelles, export massif, élévation de privilèges)
- Preuves de conformité (qui a accédé à quoi, et quand)
- Produits : Imperva, IBM Guardium, Oracle Audit Vault

## Sécurité des sauvegardes {#backup-security}
- Chiffrer les sauvegardes avant stockage (`gpg`, `openssl` ou chiffrement natif)
- Stocker les clés de chiffrement séparément des sauvegardes
- Tester régulièrement le processus de restauration
- Restreindre les permissions de création et de restauration des sauvegardes
- Appliquer des politiques de rétention (les anciennes sauvegardes contiennent toujours des données sensibles)

## Sécurité des bases de données cloud {#cloud-database-security}

### Services managés (RDS, Azure SQL, Cloud SQL) {#managed-services-rds-azure-sql-cloud-sql}
Le fournisseur prend en charge : les correctifs, les sauvegardes, le basculement.
Le client prend en charge : le contrôle d'accès, les paramètres de chiffrement, la sécurité réseau.

### Sécurité réseau {#network-security}
- Sous-réseaux privés VPC/VNet (pas d'IP publique pour les bases de données)
- Groupes de sécurité limitant les connexions entrantes aux seuls serveurs applicatifs
- VPC peering ou Private Link pour les accès inter-VPC
- SSL/TLS obligatoire pour toutes les connexions

### Intégration IAM {#iam-integration}
```json
{
    "Effect": "Allow",
    "Action": ["rds-db:connect"],
    "Resource": "arn:aws:rds-db:region:account:dbuser:dbi-resource-id/db_user"
}
```

## Pièges courants {#gotchas}
- L'installation par défaut de MongoDB n'active aucune authentification : activer systématiquement `security.authorization`
- Identifiants administrateur dans les chaînes de connexion applicatives : si l'application est compromise, la base de données l'est entièrement
- Les journaux d'audit des bases de données peuvent croître très rapidement : configurer la rotation et la rétention
- « Managé » ne signifie pas « sécurisé par défaut » : il faut toujours configurer les accès et le chiffrement
- Les clés de chiffrement des sauvegardes doivent survivre aux sinistres : envisager un séquestre de clés (key escrow) ou un HSM

## Voir aussi {#see-also}
- [[sql-injection-deep-dive]] - attaques par injection contre les bases de données
- [[secure-backend-development]] - utilisation des ORM, requêtes paramétrées
- [[compliance-and-regulations]] - exigences en matière de protection des données
- [[cryptography-and-pki]] - algorithmes de chiffrement
