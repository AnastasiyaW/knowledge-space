---
description: "CWE-89: SQL-Injection - nicht vertrauenswürdige Daten verändern die Abfragestruktur. Nicht offensichtliche Angriffsvektoren: rohe ORM-Abfragen, dynamische Bezeichner, LIKE-/JSON-Pfade, GraphQL-Resolver."
date: 2026-04-16
tags: [security, cwe, sql-injection, web, owasp, database]
level: Advanced
source_sha256: 9f10a2aef0ce2313b763035d7277f7c3f8fa8080795163a34686416341ee8e66
translation: machine
translated_at: '2026-10-24'
---
# CWE-89: SQL-Injection {#cwe-89-sql-injection}

**CWE Top 25 Rang:** 3 (2024). OWASP A03:2021.
**Auswirkungen:** Umgehung der Authentifizierung, vollständiger Datenbank-Dump, RCE über `xp_cmdshell`/`COPY TO PROGRAM`/UDF.

---

## Funktionale Semantik {#functional-semantics}

SQL ist eine Sprache, in der Daten zugleich Code sind: Der Parser kann nicht unterscheiden, ob eine Struktur der Abfrage beabsichtigt oder eingeschleust ist. Die Schwachstelle entsteht an der Stelle, an der ein SQL-haltiger String durch Verketten oder Interpolieren nicht vertrauenswürdiger Daten aufgebaut wird. Der Datenbank-Parser wertet den kombinierten String als eine einzige Abfrage aus; eingeschleuste Tokens verändern dabei den Parse-Baum und nicht nur die Datenwerte.

**Klassische Manipulation des Parse-Baums:**

```sql
-- Intended: SELECT * FROM users WHERE name = '<input>'
-- Input: ' OR '1'='1
-- Result:  SELECT * FROM users WHERE name = '' OR '1'='1'
--                                               ^^^^^^^^^^ injected predicate, always true
```

Der entscheidende Unterschied: Parametrisierte Abfragen übergeben den Wert *nach* dem Parsen. Der Parse-Baum ist damit fixiert, und eingeschleuste SQL-Tokens werden als literale Zeichenkettendaten behandelt.

---

## Nicht offensichtliche Injection-Vektoren {#non-obvious-injection-vectors}

### 1. Rohe Abfragen als „Escape Hatch“ im ORM {#1-orm-escape-hatch-raw-queries}

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

**ORM-Funktionen für rohe Abfragen, die die Parametrisierung umgehen (alle erfordern manuelle Prüfung):**
- Django: `Model.objects.raw()`, `connection.cursor().execute()` mit Interpolation, `extra(where=)`, `RawSQL()`
- SQLAlchemy: `text()` mit `.format()` oder f-Strings, `engine.execute(string % values)`
- ActiveRecord: `where("name = '#{params[:name]}'")`
- Hibernate: `session.createNativeQuery(hql_string)` mit String-Konkatenation
- GORM: `db.Raw("... " + userInput)`

### 2. Dynamische Tabellen- und Spaltennamen {#2-dynamic-table-and-column-names}

Parametrisierung betrifft nur *Werte*, nicht Bezeichner (Tabellennamen, Spaltennamen, ORDER-BY-Felder). Bezeichner lassen sich in Standard-SQL nicht parametrisieren.

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

**Hinweis:** Das Quoting von Bezeichnern mit Backticks oder doppelten Anführungszeichen verhindert keine Injection, da ein Angreifer das Anführungszeichen schließen kann. Für Bezeichner ist eine Allowlist der einzig sichere Ansatz.

### 3. LIKE-Muster-Injection {#3-like-pattern-injection}

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

Auch mit Parametrisierung verursachen LIKE-Metazeichen (`%`, `_`) im *Wert* DoS (vollständiger Tabellenscan) oder unerwartete Ergebnisse. Dabei sind zwei Aspekte getrennt zu betrachten:

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

### 4. Injection in PostgreSQL-JSON-/JSONB-Pfaden {#4-postgresql-jsonjsonb-path-injection}

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

### 5. GraphQL-Resolver, die rohe Abfragen erstellen {#5-graphql-resolvers-building-raw-queries}

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

### 6. Second-Order-Injection {#6-second-order-injection}

Daten werden korrekt parametrisiert gespeichert, später aber ausgelesen und ungeschützt in eine neue Abfrage eingebettet.

```sql
-- Registration: username 'admin'--  stored safely in DB
INSERT INTO users (username) VALUES ($1)  -- parameterized, safe

-- Password change: username retrieved from session, embedded into new query
SELECT * FROM users WHERE username = 'admin'--' AND password = 'x'
-- The -- comments out the password check
```

**Erkennung:** Verfolge alle Pfade, auf denen datenbankseitig gespeicherte Daten gelesen und anschließend beim Aufbau einer Abfrage verwendet werden. Die Parametrisierung beim Schreiben schützt den Pfad „lesen, dann verwenden“ nicht.

---

## Auslösebedingungen {#trigger-conditions}

| Vektor | Auslöser |
|--------|----------|
| HTTP-Query-Parameter/Body | Direkte Benutzereingabe in die Abfrage |
| HTTP-Header (User-Agent, Referer) | Über rohes INSERT in die Datenbank geschrieben |
| Cookie-/Session-Wert | Ausgelesen und in einer Abfrage verwendet |
| Feld im JSON-Body | Extrahiertes Feld in dynamischem SQL verwendet |
| Datei-Upload (Dateiname) | Dateiname ohne Parametrisierung gespeichert oder abgefragt |
| Antwort einer externen API | Gespeichert und anschließend per Second-Order-Injection verwendet |
| GraphQL-`variables` | Beliebiges Feld, das an dynamisches SQL übergeben wird |

---

## Erkennungsheuristiken {#detection-heuristics}

**Verfolgung: HTTP-Eingabe → Aufbau der Abfrage**

1. Identifiziere alle HTTP-Eingabequellen: `request.GET`, `request.POST`, `request.headers`, Cookies, URL-Pfadsegmente, Felder im JSON-Body.
2. Verfolge jeden Wert durch den Aufrufstapel.
3. Markiere jede Stelle, an der der Wert (oder eine davon abgeleitete Größe) in einen String verkettet oder interpoliert wird, der an eine Funktion zur Datenbankausführung übergeben wird.
4. Prüfe gezielt: `cursor.execute(string)`, `raw()`, `text()`, f-Strings/`.format()`-Aufrufe innerhalb der Datenbankschicht, den `+`-Operator auf Strings in Funktionen mit Namen wie `query`, `search`, `filter`, `find`, `fetch`.

**Muster mit hoher Aussagekraft im Code:**

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

**ORM-spezifische Escape Hatches, nach denen gesucht werden sollte:**

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

## Betroffene Ökosysteme {#affected-ecosystems}

| Ökosystem | Parametrisierungs-API | Üblicher Escape Hatch |
|-----------|----------------------|-----------------------|
| Python/Django | `%s`-Platzhalter in `execute()` | `raw()`, `extra()`, `RawSQL()` |
| Python/SQLAlchemy | `bindparam()`, `:name` in `text()` | `text()` mit `.format()` |
| Node.js/pg | `$1`/`$2`-Platzhalter | Template-Literale |
| Node.js/mysql2 | `?`-Platzhalter | Template-Literale |
| Java/JDBC | `PreparedStatement` mit `?` | `Statement.execute(string)` |
| PHP/PDO | `?` oder `:name` | `query()` mit Konkatenation |
| Ruby/ActiveRecord | `?` oder Hash-Bedingungen | String-Interpolation in `where()` |
| Go/database/sql | `?` oder `$1` | `db.Exec(string)` mit `+` |
| .NET/ADO.NET | `@param` in `SqlParameter` | `SqlCommand` mit String-Konkatenation |

---

## Datenbankspezifischer Schweregrad {#database-specific-severity}

| DB | Eskalation über den Datenzugriff hinaus |
|----|-----------------------------------------|
| MSSQL | `xp_cmdshell` → Ausführung von OS-Befehlen (bei sysadmin-Rechten) |
| PostgreSQL | `COPY TO PROGRAM` → Ausführung von OS-Befehlen (bei Superuser-Rechten) |
| MySQL | `INTO OUTFILE` → Schreiben von Dateien ins Webroot; Laden von UDFs |
| SQLite | Dateilesezugriff über `ATTACH DATABASE`; begrenzte Eskalation |
| Oracle | `DBMS_SCHEDULER` → OS-Befehle (bei DBA-Rechten) |

---

## Behebungsmuster {#fixing-patterns}

| Muster | Hinweise |
|--------|----------|
| Parametrisierte Abfragen | Primäre Verteidigung. Funktioniert für alle Wertetypen. |
| Stored Procedures | Wirksam, sofern die Prozedur selbst intern parametrisiert arbeitet |
| Allowlisting von Eingaben für Bezeichner | Zwingend für Tabellen-, Spaltennamen und ORDER BY; Parametrisierung reicht hier nicht aus |
| ORMs mit sicherer Abfrage-API | Standardmäßig sicher; alle Entsprechungen von `raw()` prüfen |
| WAF (Web Application Firewall) | Nur Defense-in-Depth; umgehbar, keine primäre Kontrolle |
| Datenbankkonto mit minimalen Rechten | Begrenzt den Schaden; verhindert Injection nicht |
| Unterdrückung von Fehlermeldungen | Erschwert Blind-Injection-Enumeration; keine Behebung |

---

## Fallstricke: Indikatoren für Fehlalarme {#gotchas-false-positive-indicators}

- **Konstante Abfragestrings ohne Interpolation:** `db.execute("SELECT 1")`. Es sind keine Benutzerdaten beteiligt.
- **Nur ganzzahlige Parameter, vor der Abfrage umgewandelt:** `id = int(request.GET['id'])` und anschließend `f"WHERE id = {id}"`. Die Umwandlung in Ganzzahlen verhindert String-Injection. Dennoch ist dies ein Code-Smell; Parametrisierung ist vorzuziehen.
- **Escaping-Funktionen, korrekt verwendet:** `pg_escape_string()`, `mysql_real_escape_string()` in eng begrenzten Kontexten. Für Stringwerte technisch sicher, schützt aber keine Bezeichner und ist bei veränderlichem Zeichensatz fragil. Nicht empfohlen, aber kein automatischer Befund.
- **Methoden des ORM-Query-Builders (nicht roh):** `User.objects.filter(name=value)` wird vom ORM parametrisiert und ist kein Befund. Nur `.raw()` und `.extra()` sind Escape Hatches.
- **Test- und Fixture-Code:** Fest codierte Abfragen in Testdateien mit Literalen wie `'test_user'` sind kein Befund.

---

## Siehe auch {#see-also}

- CWE-564: Hibernate Injection - SQL-Injection-Variante speziell für ORM
- CWE-943: Improper Neutralization - übergeordnet zu NoSQL-Injection (MongoDB `$where` usw.)
- CWE-116: Encoding/Escaping - Verteidigungsmechanismus; escape-basierte Schadensbegrenzung
- [[sql-injection-deep-dive]] - bestehender Wissensdatenbank-Eintrag mit vertieften Exploitation-Mustern
