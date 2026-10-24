---
title: "Sécurité des bases de données"
category: concepts
tags: [sql-databases, security, sql-injection, tls, encryption, roles, privileges, homomorphic-encryption]
level: 3
source_sha256: 6d5f2d9684c76b295bbbb6b98f4e167cfaad7b5041e1825160d0df8cbc26a01f
translation: machine
translated_at: '2026-10-24'
---
# Sécurité des bases de données {#database-security}

La sécurité des bases de données couvre plusieurs couches : l'accès réseau, l'authentification, l'autorisation, le chiffrement et la sécurité des requêtes au niveau applicatif. L'injection SQL reste le vecteur d'attaque le plus courant.

## Prévention de l'injection SQL {#sql-injection-prevention}

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

**Utilisez toujours des requêtes préparées avec liaison de paramètres. N'concaténez jamais les entrées utilisateur dans des chaînes SQL.**

## Authentification et contrôle d'accès {#authentication-and-access-control}

### Configuration TLS/SSL de PostgreSQL {#postgresql-tlsssl-setup}
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

Modes client SSL : `disable`, `allow`, `prefer`, `require`, `verify-ca`, `verify-full`.

### Rôles et privilèges {#roles-and-privileges}
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

## Principe du moindre privilège {#principle-of-least-privilege}

- Utilisateur applicatif : permissions minimales nécessaires (pas de superutilisateur)
- Séparer les comptes en lecture seule et en lecture-écriture
- Séparer les identifiants du pooler de connexions de ceux d'administration
- Ne jamais utiliser le superutilisateur pour les connexions applicatives
- Journalisation d'audit pour les opérations privilégiées

## Chiffrement {#encryption}

**Au repos :** fichiers de données chiffrés sur disque. TDE (Transparent Data Encryption) dans SQL Server/Oracle. Extension `pgcrypto` dans PostgreSQL. Protège contre le vol physique de disques.

**En transit :** TLS/SSL pour toutes les communications client-serveur et serveur-serveur. L'impact sur les performances est atténué par le pooling de connexions (la négociation TLS n'a lieu qu'une fois).

**Chiffrement homomorphe (HE) :** permet d'effectuer des calculs arithmétiques sur des données chiffrées sans les déchiffrer. Le FHE (chiffrement homomorphe complet) permet les requêtes sur bases chiffrées, le routage L7 sans terminaison TLS, et la construction d'index sur des données chiffrées. Il reste plusieurs ordres de grandeur plus lent que le clair, et n'est pas prêt pour la production. IBM FHE Toolkit pour l'expérimentation.

## Sécurité du protocole filaire {#wire-protocol-security}

Protocole filaire PostgreSQL : toutes les données sont transmises en clair sans TLS. Le mot de passe est envoyé sous forme de hash MD5 ou via un challenge SCRAM-SHA-256. Activez toujours TLS en production.

```bash
psql "host=server sslmode=verify-full sslrootcert=ca.crt"
```

## Points clés {#key-facts}

- SCRAM-SHA-256 est la méthode d'authentification recommandée (PG 10+)
- `pg_hba.conf` contrôle quels hôtes peuvent se connecter et comment ils s'authentifient
- Sécurité au niveau réseau : règles de pare-feu, liste blanche d'IP, VPN
- `log_connections = on` et `log_disconnections = on` pour la piste d'audit
- Les sommes de contrôle des données détectent la corruption silencieuse, mais pas la modification malveillante

## Pièges courants {#gotchas}

- L'authentification MD5 est obsolète : utilisez SCRAM-SHA-256
- `pg_hba.conf` est traité de haut en bas, la première correspondance l'emporte
- `host all all 0.0.0.0/0 trust` dans pg_hba.conf = aucune authentification (catastrophe)
- Les chaînes de connexion dans le code ou la configuration peuvent contenir des mots de passe en clair : utilisez pgpass ou des variables d'environnement
- Le FHE est 10 000 à 1 000 000 de fois plus lent que les opérations en clair : réservé à la recherche
- Ne stockez jamais de mots de passe de connexion dans un système de gestion de versions

## Voir aussi {#see-also}

- [[postgresql-configuration-tuning]] - pg_hba.conf et listen_addresses
- [[connection-pooling]] - gestion des identifiants avec les poolers
- [[postgresql-ha-patroni]] - TLS entre les nœuds Patroni
- [[replication-fundamentals]] - connexions de réplication chiffrées
