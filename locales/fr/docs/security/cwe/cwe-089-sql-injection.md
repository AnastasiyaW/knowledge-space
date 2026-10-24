---
description: "CWE-89 : injection SQL - des données non fiables modifient la structure de la requête. Vecteurs peu évidents : requêtes brutes ORM, identifiants dynamiques, chemins LIKE/JSON, resolvers GraphQL."
date: 2026-04-16
tags: [security, cwe, sql-injection, web, owasp, database]
level: Advanced
source_sha256: 9f10a2aef0ce2313b763035d7277f7c3f8fa8080795163a34686416341ee8e66
translation: machine
translated_at: '2026-10-24'
---
# CWE-89 : injection SQL {#cwe-89-sql-injection}

**Rang dans le CWE Top 25 :** 3 (2024). OWASP A03:2021.
**Portée de l'impact :** contournement d'authentification, extraction complète de la base, RCE via `xp_cmdshell` / `COPY TO PROGRAM` / UDF.

---

## Sémantique fonctionnelle {#functional-semantics}

SQL est un langage où les données sont du code : le parseur ne peut pas distinguer la structure de requête voulue de la structure injectée. La vulnérabilité existe à la frontière où une chaîne contenant du SQL est construite par concaténation ou interpolation de données non fiables. Le parseur de la base évalue la chaîne combinée comme une requête unique ; les jetons injectés modifient l'arbre syntaxique, et pas seulement les valeurs des données.

**Manipulation canonique de l'arbre syntaxique :**

```sql
-- Intended: SELECT * FROM users WHERE name = '<input>'
-- Input: ' OR '1'='1
-- Result:  SELECT * FROM users WHERE name = '' OR '1'='1'
--                                               ^^^^^^^^^^ injected predicate, always true
```

La distinction essentielle : les requêtes paramétrées transmettent la valeur *après* l'analyse syntaxique ; l'arbre syntaxique est donc figé, et les jetons SQL injectés sont traités comme de simples données littérales.

---

## Vecteurs d'injection peu évidents {#non-obvious-injection-vectors}

### 1. Requêtes brutes « d'échappatoire » des ORM {#1-orm-escape-hatch-raw-queries}

```python
# VULNERABLE: Django ORM raw() with f-string
def search_users(request):
    username = request.GET['q']
    users = User.objects.raw(f"SELECT * FROM auth_user WHERE username = '{username}'")
    # Equivalent to classic injection; ORM provides zero protection here
```

```python
# FIXED: parameterized raw query
def search_users(request):
    username = request.GET['q']
    users = User.objects.raw(
        "SELECT * FROM auth_user WHERE username = %s",
        [username]
    )
```

**Fonctions de requête brute des ORM qui contournent la paramétrisation (toutes nécessitent un examen manuel) :**
- Django : `Model.objects.raw()`, `connection.cursor().execute()` avec interpolation, `extra(where=)`, `RawSQL()`
- SQLAlchemy : `text()` avec `.format()` ou des f-strings, `engine.execute(string % values)`
- ActiveRecord : `where("name = '#{params[:name]}'")`
- Hibernate : `session.createNativeQuery(hql_string)` avec concaténation de chaînes
- GORM : `db.Raw("... " + userInput)`

### 2. Noms de tables et de colonnes dynamiques {#2-dynamic-table-and-column-names}

La paramétrisation ne s'applique qu'aux *valeurs*, pas aux identifiants (noms de tables, noms de colonnes, champs ORDER BY). Les identifiants ne peuvent pas être paramétrés en SQL standard.

```python
# VULNERABLE: dynamic ORDER BY column
def get_sorted_data(request):
    col = request.GET.get('sort', 'name')
    query = f"SELECT * FROM products ORDER BY {col}"  # injection via sort=1; DROP TABLE products--
    return db.execute(query)
```

```python
# FIXED: allowlist identifiers
ALLOWED_SORT_COLUMNS = {'name', 'price', 'created_at'}

def get_sorted_data(request):
    col = request.GET.get('sort', 'name')
    if col not in ALLOWED_SORT_COLUMNS:
        col = 'name'
    query = f"SELECT * FROM products ORDER BY {col}"  # col is now validated
    return db.execute(query)
```

**Remarque :** le fait de mettre les identifiants entre guillemets (backticks ou guillemets doubles) n'empêche PAS l'injection, car un attaquant peut fermer le guillemet. La liste blanche (allowlist) est la seule approche sûre pour les identifiants.

### 3. Injection de motifs LIKE {#3-like-pattern-injection}

```javascript
// VULNERABLE: Node.js with pg - LIKE wildcard injection
async function searchProducts(req, res) {
    const term = req.query.term;
    // Attacker sends: term = %  → returns all rows
    // Attacker sends: term = \%anything\%  → escaping manipulation
    const result = await pool.query(
        `SELECT * FROM products WHERE name LIKE '%${term}%'`
    );
}
```

Même avec la paramétrisation, les métacaractères LIKE (`%`, `_`) présents dans la *valeur* provoquent un déni de service (parcours complet de table) ou des résultats inattendus. Deux problèmes distincts :

```javascript
// FIXED: parameterize the whole pattern, escape LIKE metacharacters in value
async function searchProducts(req, res) {
    const term = req.query.term
        .replace(/\\/g, '\\\\')
        .replace(/%/g, '\\%')
        .replace(/_/g, '\\_');
    const result = await pool.query(
        'SELECT * FROM products WHERE name LIKE $1 ESCAPE \'\\\'',
        [`%${term}%`]
    );
}
```

### 4. Injection de chemins JSON/JSONB dans PostgreSQL {#4-postgresql-jsonjsonb-path-injection}

```python
# VULNERABLE: jsonb path in raw query
def filter_by_attr(conn, attr_name, value):
    query = f"SELECT * FROM items WHERE data->>'{attr_name}' = %s"
    # attr_name injection: ' OR 1=1 --  breaks out of jsonb operator context
    conn.execute(query, (value,))
```

```python
# FIXED: allowlist attr_name
ALLOWED_ATTRS = {'color', 'size', 'brand'}

def filter_by_attr(conn, attr_name, value):
    if attr_name not in ALLOWED_ATTRS:
        raise ValueError("Invalid attribute")
    query = f"SELECT * FROM items WHERE data->>{attr_name!r} = %s"
    conn.execute(query, (value,))
```

### 5. Resolvers GraphQL construisant des requêtes brutes {#5-graphql-resolvers-building-raw-queries}

```javascript
// VULNERABLE: GraphQL resolver constructing SQL
const resolvers = {
    Query: {
        user: async (_, { filter }) => {
            // filter = { field: "name", value: "alice' OR '1'='1" }
            const sql = `SELECT * FROM users WHERE ${filter.field} = '${filter.value}'`;
            return db.query(sql);
        }
    }
};
```

```javascript
// FIXED: parameterize and validate field name
const ALLOWED_FIELDS = new Set(['name', 'email', 'role']);

const resolvers = {
    Query: {
        user: async (_, { filter }) => {
            if (!ALLOWED_FIELDS.has(filter.field)) throw new Error('Invalid field');
            const sql = `SELECT * FROM users WHERE ${filter.field} = $1`;
            return db.query(sql, [filter.value]);
        }
    }
};
```

### 6. Injection de second ordre {#6-second-order-injection}

Des données stockées de manière sûre (correctement paramétrées) sont ensuite relues et intégrées sans échappement dans une nouvelle requête.

```sql
-- Registration: username 'admin'--  stored safely in DB
INSERT INTO users (username) VALUES ($1)  -- parameterized, safe

-- Password change: username retrieved from session, embedded into new query
SELECT * FROM users WHERE username = 'admin'--' AND password = 'x'
-- The -- comments out the password check
```

**Détection :** tracer tous les chemins où des données présentes en base sont lues puis utilisées pour construire une requête. La paramétrisation à l'écriture ne protège pas le chemin lecture-puis-utilisation.

---

## Conditions de déclenchement {#trigger-conditions}

| Vecteur | Déclencheur |
|---------|-------------|
| Paramètre de requête ou corps HTTP | Saisie utilisateur directe dans la requête |
| En-tête HTTP (User-Agent, Referer) | Journalisé en base via un INSERT brut |
| Cookie ou valeur de session | Récupéré et utilisé dans une requête |
| Champ du corps JSON | Champ extrait utilisé dans du SQL dynamique |
| Téléversement de fichier (nom de fichier) | Nom de fichier stocké ou interrogé sans paramétrisation |
| Réponse d'une API externe | Stockée puis utilisée pour une injection de second ordre |
| Champ `variables` de GraphQL | Tout champ transmis à du SQL dynamique |

---

## Heuristiques de détection {#detection-heuristics}

**Tracer : entrée HTTP → construction de la requête**

1. Identifier toutes les sources de saisie HTTP : `request.GET`, `request.POST`, `request.headers`, cookies, segments du chemin d'URL, champs du corps JSON.
2. Suivre chaque valeur à travers la pile d'appels.
3. Signaler tout point où la valeur (ou un dérivé) est concaténée ou interpolée dans une chaîne transmise à une fonction d'exécution SQL.
4. Vérifier en particulier : `cursor.execute(string)`, `raw()`, `text()`, les f-strings et appels à `.format()` dans la couche d'accès aux données, l'opérateur `+` appliqué à des chaînes dans des fonctions nommées `query`, `search`, `filter`, `find`, `fetch`.

**Motifs de code à fort signal :**

```python
# Python - flag any of these patterns
f"SELECT ... {user_var}"
"SELECT ... " + user_var
"SELECT ... %s" % user_var   # % formatting - NOT parameterized (different from %s as placeholder)
cursor.execute("SELECT ... '" + val + "'")
```

```javascript
// JavaScript - flag these
`SELECT ... ${userVal}`
"SELECT ... " + userVal
db.query("SELECT ... '" + val + "'")
```

```java
// Java - flag these
"SELECT * FROM t WHERE x = '" + input + "'"
stmt.execute(String.format("SELECT ... %s", input))
```

**Échappatoires spécifiques aux ORM à rechercher :**

```bash
# grep patterns for common ORMs
grep -rn "\.raw(" --include="*.py"
grep -rn "RawSQL(" --include="*.py"
grep -rn "extra(where" --include="*.py"
grep -rn "createNativeQuery" --include="*.java"
grep -rn "\.where(\".*#\{" --include="*.rb"    # Ruby string interpolation in ActiveRecord where
grep -rn "db\.Raw(" --include="*.go"
```

---

## Écosystèmes concernés {#affected-ecosystems}

| Écosystème | API de paramétrisation | Échappatoire courante |
|------------|------------------------|-----------------------|
| Python/Django | Placeholders `%s` dans `execute()` | `raw()`, `extra()`, `RawSQL()` |
| Python/SQLAlchemy | `bindparam()`, `:name` dans `text()` | `text()` avec `.format()` |
| Node.js/pg | Placeholders `$1` / `$2` | Template literals |
| Node.js/mysql2 | Placeholders `?` | Template literals |
| Java/JDBC | `?` dans `PreparedStatement` | `Statement.execute(string)` |
| PHP/PDO | `?` ou `:name` | `query()` avec concaténation |
| Ruby/ActiveRecord | `?` ou conditions sous forme de hash | Interpolation de chaînes dans `where()` |
| Go/database/sql | `?` ou `$1` | `db.Exec(string)` avec `+` |
| .NET/ADO.NET | `@param` dans `SqlParameter` | `SqlCommand` avec concaténation de chaînes |

---

## Gravité selon le SGBD {#database-specific-severity}

| SGBD | Escalade au-delà de l'accès aux données |
|------|------------------------------------------|
| MSSQL | `xp_cmdshell` → exécution de commandes système (si sysadmin) |
| PostgreSQL | `COPY TO PROGRAM` → exécution de commandes système (si superuser) |
| MySQL | `INTO OUTFILE` → écriture de fichiers dans la racine web ; chargement d'UDF |
| SQLite | Lecture de fichiers via `ATTACH DATABASE` ; escalade limitée |
| Oracle | `DBMS_SCHEDULER` → commandes système (si DBA) |

---

## Motifs de correction {#fixing-patterns}

| Motif | Remarques |
|-------|-----------|
| Requêtes paramétrées | Défense principale. Fonctionne pour tous les types de valeurs. |
| Procédures stockées | Efficaces si la procédure elle-même utilise la paramétrisation en interne |
| Liste blanche des identifiants | Obligatoire pour les tables, colonnes et ORDER BY ; la paramétrisation ne suffit pas |
| ORM avec API de requête sûre | Sûr par défaut ; auditer tous les équivalents de `raw()` |
| WAF (Web Application Firewall) | Défense en profondeur uniquement ; contournable, ne constitue pas un contrôle principal |
| Compte de base de données à privilèges minimaux | Limite le périmètre d'impact ; n'empêche pas l'injection |
| Suppression des messages d'erreur | Empêche l'énumération par injection aveugle ; ne constitue pas une correction |

---

## Pièges - indicateurs de faux positifs {#gotchas-false-positive-indicators}

- **Chaînes de requête constantes sans interpolation :** `db.execute("SELECT 1")` - aucune donnée utilisateur impliquée.
- **Paramètres entiers convertis avant la requête :** `id = int(request.GET['id'])` puis `f"WHERE id = {id}"` - la conversion en entier empêche l'injection de chaînes. Reste une mauvaise pratique ; préférer la paramétrisation.
- **Fonctions d'échappement utilisées correctement :** `pg_escape_string()`, `mysql_real_escape_string()` dans des contextes restreints - techniquement sûres pour les valeurs de type chaîne, mais ne protègent pas les identifiants et sont fragiles si le jeu de caractères est modifiable. Non recommandées, mais pas automatiquement un défaut.
- **Méthodes de construction de requêtes de l'ORM (non brutes) :** `User.objects.filter(name=value)` - paramétrisé par l'ORM ; ce n'est pas un défaut. Seuls `.raw()` et `.extra()` sont des échappatoires.
- **Code de test et fixtures :** requêtes en dur dans les fichiers de test avec des littéraux comme `'test_user'` - ce n'est pas un défaut.

---

## Voir aussi {#see-also}

- CWE-564 : Hibernate Injection - variante d'injection SQL spécifique à l'ORM
- CWE-943 : Improper Neutralization - catégorie parente de l'injection NoSQL (`$where` de MongoDB, etc.)
- CWE-116 : Encoding/Escaping - mécanisme de défense ; atténuation par échappement
- [[sql-injection-deep-dive]] - entrée existante de la base de connaissances avec des schémas d'exploitation plus approfondis
