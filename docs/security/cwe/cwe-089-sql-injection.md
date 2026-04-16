---
description: "CWE-89: SQL Injection - untrusted data alters query structure. Non-obvious vectors: ORM raw queries, dynamic identifiers, LIKE/JSON paths, GraphQL resolvers."
date: 2026-04-16
tags: [security, cwe, sql-injection, web, owasp, database]
level: Advanced
---

# CWE-89: SQL Injection

**CWE Top 25 Rank:** 3 (2024). OWASP A03:2021.
**Impact range:** authentication bypass, full DB dump, RCE via `xp_cmdshell`/`COPY TO PROGRAM`/UDF.

---

## Functional Semantics

SQL is a data-as-code language: the parser cannot distinguish intended query structure from injected structure. The vulnerability exists at the boundary where a string containing SQL is constructed by concatenating or interpolating untrusted data. The database parser evaluates the combined string as a single query; injected tokens alter the parse tree, not just the data values.

**Canonical parse tree manipulation:**

```sql
-- Intended: SELECT * FROM users WHERE name = '<input>'
-- Input: ' OR '1'='1
-- Result:  SELECT * FROM users WHERE name = '' OR '1'='1'
--                                               ^^^^^^^^^^ injected predicate, always true
```

The critical distinction: parameterized queries pass the value *after* parsing, so the parse tree is fixed and injected SQL tokens are treated as literal string data.

---

## Non-Obvious Injection Vectors

### 1. ORM "escape hatch" raw queries

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

**ORM raw query functions that bypass parameterization (all require manual scrutiny):**
- Django: `Model.objects.raw()`, `connection.cursor().execute()` with interpolation, `extra(where=)`, `RawSQL()`
- SQLAlchemy: `text()` with `.format()` or f-strings, `engine.execute(string % values)`
- ActiveRecord: `where("name = '#{params[:name]}'")`
- Hibernate: `session.createNativeQuery(hql_string)` with string concat
- GORM: `db.Raw("... " + userInput)`

### 2. Dynamic table and column names

Parameterization only applies to *values*, not identifiers (table names, column names, ORDER BY fields). Identifiers cannot be parameterized in standard SQL.

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

**Note:** backtick/double-quote quoting of identifiers does NOT prevent injection - an attacker can close the quote. Allowlist is the only safe approach for identifiers.

### 3. LIKE pattern injection

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

Even with parameterization, LIKE metacharacters (`%`, `_`) in the *value* cause DoS (full table scan) or unexpected results. Two separate concerns:

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

### 4. PostgreSQL JSON/JSONB path injection

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

### 5. GraphQL resolvers building raw queries

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

### 6. Second-order injection

Data stored safely (correctly parameterized) but later retrieved and embedded unescaped into a new query.

```sql
-- Registration: username 'admin'--  stored safely in DB
INSERT INTO users (username) VALUES ($1)  -- parameterized, safe

-- Password change: username retrieved from session, embedded into new query
SELECT * FROM users WHERE username = 'admin'--' AND password = 'x'
-- The -- comments out the password check
```

**Detection:** trace all paths where DB-resident data is read and then used in query construction. The parameterization at write time does not protect the read-then-use path.

---

## Trigger Conditions

| Vector | Trigger |
|--------|---------|
| HTTP query param/body | Direct user input into query |
| HTTP header (User-Agent, Referer) | Logged to DB via raw INSERT |
| Cookie/session value | Retrieved and used in query |
| JSON body field | Extracted field used in dynamic SQL |
| File upload (filename) | Filename stored/queried without parameterization |
| External API response | Stored then used in second-order injection |
| GraphQL `variables` | Any field passed to dynamic SQL |

---

## Detection Heuristics

**Trace: HTTP input → query construction**

1. Identify all HTTP input sources: `request.GET`, `request.POST`, `request.headers`, cookies, URL path segments, JSON body fields.
2. Follow each value through the call stack.
3. Flag any point where the value (or a derivative) is concatenated/interpolated into a string that is passed to a DB execution function.
4. Specifically check: `cursor.execute(string)`, `raw()`, `text()`, f-strings/`.format()` calls within DB layer, `+` operator applied to strings in functions named `query`, `search`, `filter`, `find`, `fetch`.

**High-signal code patterns:**

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

**ORM-specific escape hatches to search:**

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

## Affected Ecosystems

| Ecosystem | Parameterization API | Common escape hatch |
|-----------|---------------------|---------------------|
| Python/Django | `%s` placeholders in `execute()` | `raw()`, `extra()`, `RawSQL()` |
| Python/SQLAlchemy | `bindparam()`, `:name` in `text()` | `text()` with `.format()` |
| Node.js/pg | `$1`/`$2` placeholders | Template literals |
| Node.js/mysql2 | `?` placeholders | Template literals |
| Java/JDBC | `PreparedStatement` `?` | `Statement.execute(string)` |
| PHP/PDO | `?` or `:name` | `query()` with concatenation |
| Ruby/ActiveRecord | `?` or hash conditions | String interpolation in `where()` |
| Go/database/sql | `?` or `$1` | `db.Exec(string)` with `+` |
| .NET/ADO.NET | `@param` in `SqlParameter` | `SqlCommand` with string concat |

---

## Database-Specific Severity

| DB | Escalation beyond data access |
|----|-------------------------------|
| MSSQL | `xp_cmdshell` → OS command execution (if sysadmin) |
| PostgreSQL | `COPY TO PROGRAM` → OS command execution (if superuser) |
| MySQL | `INTO OUTFILE` → write files to web root; UDF loading |
| SQLite | File read via `ATTACH DATABASE`; limited escalation |
| Oracle | `DBMS_SCHEDULER` → OS commands (if DBA) |

---

## Fixing Patterns

| Pattern | Notes |
|---------|-------|
| Parameterized queries | Primary defense. Works for all value types. |
| Stored procedures | Effective if SP itself uses parameterization internally |
| Input allowlisting for identifiers | Mandatory for table/column/ORDER BY; parameterization is insufficient |
| ORMs with safe query API | Safe by default; audit all `raw()` equivalents |
| WAF (Web Application Firewall) | Defense-in-depth only; bypassable, not a primary control |
| Least privilege DB account | Limits blast radius; does not prevent injection |
| Error message suppression | Prevents blind-injection enumeration; not a fix |

---

## Gotchas - False Positive Indicators

- **Constant query strings with no interpolation:** `db.execute("SELECT 1")` - no user data involved.
- **Integer-only params cast before query:** `id = int(request.GET['id'])` then `f"WHERE id = {id}"` - integer casting prevents string injection. Still a code smell; prefer parameterization.
- **Escaping functions used correctly:** `pg_escape_string()`, `mysql_real_escape_string()` in narrow contexts - technically safe for string values but does not protect identifiers; fragile if charset is mutable. Not recommended but not automatically a finding.
- **ORM query builder methods (not raw):** `User.objects.filter(name=value)` - this is parameterized by the ORM; not a finding. Only `.raw()` and `.extra()` are escape hatches.
- **Test/fixture code:** hardcoded queries in test files with `'test_user'` literals - not a finding.

---

## See Also

- CWE-564: Hibernate Injection - ORM-specific SQL injection variant
- CWE-943: Improper Neutralization - parent for NoSQL injection (MongoDB `$where`, etc.)
- CWE-116: Encoding/Escaping - defense mechanism; escape-based mitigation
- [[sql-injection-deep-dive]] - existing knowledge base entry with deeper exploitation patterns
