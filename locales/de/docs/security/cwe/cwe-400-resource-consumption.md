---
description: "CWE-400: Angreifer löst unkontrollierten CPU-, Speicher-, Festplatten- oder fd-Verbrauch aus, etwa über Regex-DoS, Hash-Kollisionen, Zip-Bomben, XML-Entity-Expansion oder unbegrenzte Collections."
date: 2026-04-16
tags: [security, cwe, dos, redos, regex, zip-bomb, xml-bomb, algorithmic-complexity, resource-exhaustion]
level: Advanced
source_sha256: 553600169d8216a7cde67194472423c9f1c725266584d2ceecb349e48a2b86ab
translation: machine
translated_at: '2026-10-24'
---
# CWE-400: Unkontrollierter Ressourcenverbrauch {#cwe-400-uncontrolled-resource-consumption}

**CWE-400** | CWE-Pillar: Resource Management | CVSS-Basiswert-Bereich: 5.3-7.5 (DoS) | Rang 24 in den CWE Top 25

## Funktionale Semantik {#functional-semantics}

Diese Schwachstellenklasse umfasst Eingaben, die einen asymmetrischen Ressourcenverbrauch verursachen: Der Angreifer sendet O(n) Bytes, der Server benötigt O(n²) oder O(2^n) CPU-Zeit bzw. Speicher. Der Anwendung fehlt eine Obergrenze für den Arbeitsaufwand einer einzelnen Anfrage. Für die Ausnutzung ist keine Authentifizierung und keine Code-Injection nötig; eine einzelne, gezielt konstruierte Anfrage kann alle verfügbaren Ressourcen eines Typs aufbrauchen und so den Dienst für alle Benutzer beeinträchtigen oder verweigern.

Angegriffene Ressourcentypen: CPU-Zeit, Heap-Speicher, Stack-Frames (Rekursion), Festplatten-I/O, File Descriptors, Thread-Pool-Slots, Datenbank-Connection-Pool, ausgehende Netzwerkbandbreite.

## Taxonomie der Angriffsfläche {#attack-surface-taxonomy}

| Angriffsklasse | Ressource | Komplexität | Beispiele |
|---|---|---|---|
| ReDoS — katastrophales Backtracking | CPU | O(2^n) im Worst Case | Böser Regex auf benutzergelieferter Zeichenkette |
| Hash-Kollision (HashDoS) | CPU | O(n²) pro Bucket | Gezielt konstruierte HTTP-POST-Parameter füllen einen Hash-Bucket |
| Dekompressionsbombe | Speicher + Festplatte | O(Kompressionsverhältnis) | 42.zip (4,5 PB aus 42 KB), gzip-Bombe |
| XML-Entity-Expansion (Billion Laughs) | Speicher | O(10^9) | Verschachtelte XML-Entity-Referenzen |
| Quadratischer Algorithmus | CPU | O(n²) | Regex mit schlechter Engine, naive String-Konkatenation in Schleife |
| Unbegrenztes Wachstum von Collections | Speicher | O(n) unbegrenzt | Anhängen an eine Liste ohne Größenlimit |
| Erschöpfung des Connection-Pools | File Descriptors | O(offene_Verbindungen) | Slow-Read- / Slowloris-HTTP-Angriff |
| Log-Flooding | Festplatten-I/O | O(Log-Einträge) | Anfrage, die unbegrenzte Logausgabe erzeugt |
| GraphQL-Abfragetiefe | CPU + DB | O(Tiefe^Verzweigung) | `{ user { friends { friends { friends ... } } } }` |
| gRPC-Stream-Flood | Speicher + CPU | O(Nachrichten) | Unbegrenzter Streaming-RPC ohne Backpressure |

## ReDoS — katastrophales Backtracking {#redos-catastrophic-backtracking}

Eine Regex-Engine mit Backtracking kann exponentielle Laufzeit zeigen, wenn ein Muster verschachtelte Quantoren oder Alternativen mit überlappenden Zeichenmengen enthält.

**Musteranatomie katastrophaler Regexe:**
- `(a+)+` — verschachtelte Quantoren; dieselben `a`-Zeichen können auf exponentiell viele Arten zugeordnet werden
- `(a|a)+` — Alternative mit identischen Zweigen
- `([a-zA-Z]+)*` — unbegrenzte Gruppe, auf die ein Quantor angewendet wird
- `(.*a){n}` — wiederholte Übereinstimmung mit einem seltenen Zeichen über gieriges `.*`

```python
# VULNERABLE: user-supplied string tested against catastrophic regex
import re
from flask import request

@app.route("/validate-email")
def validate_email():
    email = request.args.get("email", "")
    # Catastrophic: (a+)+ pattern equivalent — overlapping quantifiers
    # Input "aaaaaaaaaaaaaaaaaaa@" causes exponential backtracking
    pattern = r"^([a-zA-Z0-9_\-\.]+)+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,}$"
    if re.match(pattern, email):  # hangs on crafted input
        return "valid"
    return "invalid"
```

```python
# FIXED: use re with timeout wrapper, or switch to possessive quantifiers / atomic groups
import re
import signal

def regex_with_timeout(pattern, string, timeout_sec=0.1):
    def handler(signum, frame):
        raise TimeoutError("Regex timeout")
    signal.signal(signal.SIGALRM, handler)
    signal.setitimer(signal.ITIMER_REAL, timeout_sec)
    try:
        result = re.match(pattern, string)
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
    return result

# Better: use a non-backtracking regex engine
# pip install google-re2
import re2  # Google RE2 — linear time guarantee, no catastrophic backtracking
pattern = re2.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")
if pattern.match(email):
    return "valid"
```

**Katastrophale Muster, die im Code-Review markiert werden sollten:**

| Muster | Warum katastrophal |
|---|---|
| `(a+)+` | Jedes `a` kann zur inneren oder äußeren Gruppe gehören |
| `(\w+\s?)+` | Dasselbe Zeichen passt mehrdeutig auf beide Gruppen |
| `(.*,)*` | `.` passt auf `,`, dadurch entsteht exponentielle Mehrdeutigkeit |
| `([a-z]+)*` | Verschachtelte unbegrenzte Wiederholung |
| `^(([a-z])+.)+[A-Z]([a-z])+$` | Mehrere überlappende Gruppen |

## Dekompressionsbomben {#decompression-bombs}

```python
# VULNERABLE: no size limit on decompression
import zipfile, io
from flask import request

@app.route("/upload-zip")
def upload_zip():
    data = request.data  # attacker sends 42.zip (42KB → 4.5PB decompressed)
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        for name in zf.namelist():
            content = zf.read(name)  # reads entire decompressed content into memory
            process(content)
```

```python
# FIXED: enforce decompressed size limit
import zipfile, io

MAX_COMPRESSED_SIZE = 10 * 1024 * 1024    # 10 MB input
MAX_DECOMPRESSED_SIZE = 100 * 1024 * 1024  # 100 MB output
MAX_FILES = 100
MAX_COMPRESSION_RATIO = 10

@app.route("/upload-zip")
def upload_zip():
    if len(request.data) > MAX_COMPRESSED_SIZE:
        return "File too large", 413

    total_decompressed = 0
    with zipfile.ZipFile(io.BytesIO(request.data)) as zf:
        if len(zf.namelist()) > MAX_FILES:
            return "Too many files", 400
        for name in zf.namelist():
            info = zf.getinfo(name)
            total_decompressed += info.file_size
            if total_decompressed > MAX_DECOMPRESSED_SIZE:
                return "Decompressed size limit exceeded", 400
            # Check per-file compression ratio
            if info.compress_size > 0 and info.file_size / info.compress_size > MAX_COMPRESSION_RATIO:
                return "Suspicious compression ratio", 400
            content = zf.read(name, pwd=None)
            process(content)
```

## XML-Entity-Expansion (Billion Laughs) {#xml-entity-expansion-billion-laughs}

```xml
<!-- Billion Laughs attack: 9 entity levels, each expanding 10x → 10^9 entities -->
<?xml version="1.0"?>
<!DOCTYPE lolz [
  <!ENTITY lol "lol">
  <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
  <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
  <!ENTITY lol4 "&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;">
  ...
  <!ENTITY lol9 "&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;">
]>
<root>&lol9;</root>
```

```python
# VULNERABLE: default lxml/ElementTree settings allow entity expansion
from lxml import etree

def parse_xml(xml_bytes):
    return etree.fromstring(xml_bytes)  # processes entity expansion

# FIXED: disable entity expansion and DTD processing
from lxml import etree

def parse_xml_safe(xml_bytes):
    parser = etree.XMLParser(
        resolve_entities=False,  # do not expand &entities;
        no_network=True,         # no external entity fetches (also prevents XXE/SSRF)
        dtd_validation=False,
        load_dtd=False
    )
    return etree.fromstring(xml_bytes, parser=parser)
```

```java
// FIXED: Java SAX/DOM with entity expansion disabled
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
dbf.setExpandEntityReferences(false);
DocumentBuilder db = dbf.newDocumentBuilder();
Document doc = db.parse(inputStream);
```

## Hash-Kollision / HashDoS {#hash-collision-hashdos}

Der Angreifer konstruiert POST-Parameter mit Schlüsseln, die alle auf denselben Bucket hashen. Dadurch werden O(1)-Lookups zu einer O(n)-Kettentraversierung. Bei n = 100.000 Parametern ergibt sich O(n²) = 10^10 Operationen.

```python
# VULNERABLE: default dict/form parsing with no key count limit
from flask import request

@app.route("/process", methods=["POST"])
def process():
    # Flask/Werkzeug by default limits form keys but older versions did not
    data = request.form  # attacker posts 100,000 keys with hash collisions
    for key, value in data.items():  # O(n²) in a poor hash implementation
        store(key, value)
```

```python
# FIXED: limit form field count
from werkzeug.formparser import MultiPartParser

app.config['MAX_FORM_PARTS'] = 1000     # Werkzeug 2.3+
app.config['MAX_FORM_MEMORY_SIZE'] = 500_000  # 500KB

# Or explicit check:
@app.route("/process", methods=["POST"])
def process():
    if len(request.form) > 100:
        return "Too many form fields", 400
    data = request.form
```

Python 3.2+ verwendet standardmäßig Hash-Randomisierung (`PYTHONHASHSEED`), was HashDoS bei Python-Dictionaries abschwächt. Java-`HashMap` nutzt ab Java 8 für große Buckets eine Baumstruktur. PHP war historisch die am stärksten betroffene Plattform.

## Unbegrenztes Wachstum von Collections {#unbounded-collection-growth}

```javascript
// VULNERABLE: SSE/WebSocket with no client limit
const activeConnections = new Map(); // grows without bound

io.on("connection", (socket) => {
    activeConnections.set(socket.id, socket); // never cleaned up on error
    socket.on("subscribe", (topic) => {
        if (!subscriptions[topic]) subscriptions[topic] = [];
        subscriptions[topic].push(socket.id); // attacker subscribes 10M times
    });
});

// FIXED: per-client limits and cleanup
const MAX_CONNECTIONS = 10_000;
const MAX_SUBSCRIPTIONS_PER_CLIENT = 100;

io.on("connection", (socket) => {
    if (activeConnections.size >= MAX_CONNECTIONS) {
        socket.disconnect(true);
        return;
    }
    activeConnections.set(socket.id, socket);
    let clientSubCount = 0;

    socket.on("subscribe", (topic) => {
        if (++clientSubCount > MAX_SUBSCRIPTIONS_PER_CLIENT) {
            socket.disconnect(true);
            return;
        }
        subscriptions[topic] = subscriptions[topic] || [];
        subscriptions[topic].push(socket.id);
    });

    socket.on("disconnect", () => {
        activeConnections.delete(socket.id);
        // cleanup subscriptions...
    });
});
```

## GraphQL-Abfragetiefe / -Komplexität {#graphql-query-depth-complexity}

```graphql
# ATTACK: exponential DB queries through unbounded nesting
query {
    user(id: 1) {
        friends {           # N users
            friends {       # N² users
                friends {   # N³ users
                    name
                }
            }
        }
    }
}
```

```javascript
// FIXED: depth limiting with graphql-depth-limit
const depthLimit = require("graphql-depth-limit");
const { createComplexityLimitRule } = require("graphql-validation-complexity");

const schema = makeExecutableSchema({ typeDefs, resolvers });
const server = new ApolloServer({
    schema,
    validationRules: [
        depthLimit(5),                    // max nesting depth
        createComplexityLimitRule(1000),  // total complexity score
    ]
});
```

## Erkennungsheuristiken {#detection-heuristics}

**Auslöser für statische Analyse:**
- Regex mit verschachtelten Quantoren, angewendet auf benutzergesteuerte Zeichenketten: `re.match(pattern, user_input)`, wobei das Muster `(X+)+`, `(X*Y*)+` oder `(\w+\s?)+` enthält
- `zipfile.ZipFile.read()`, `tarfile.extractall()`, `gzip.decompress()` ohne Größenprüfung
- XML-Parsing: `lxml.etree.fromstring()` ohne `XMLParser(resolve_entities=False)`, `DocumentBuilderFactory.newDocumentBuilder()` ohne Feature-Flags
- `list.append(item)` innerhalb eines Request-Handlers ohne Größenlimit für die Liste
- `dict` oder `map`, die aus benutzergelieferten Schlüsseln aufgebaut werden, ohne Anzahlbegrenzung
- Rekursive Funktion, deren Rekursionstiefe vom Benutzer bestimmt wird (Tiefe der Baumtraversierung = Verschachtelungstiefe des JSON-Eingabe-Benutzers)
- `json.loads(user_data)` in Python — gegen Injection sicher, aber das `json`-Modul von Python hat eine maximale Rekursionstiefe für verschachtelte Strukturen; tief verschachteltes JSON führt zu `RecursionError`

**Auslöser in der Konfiguration:**
- `MAX_CONTENT_LENGTH` in Flask nicht gesetzt (unbegrenzter Request-Body)
- Kein `client_max_body_size` in der Nginx-Konfiguration
- GraphQL-Server ohne Tiefen- bzw. Komplexitätslimits
- Elasticsearch ohne `index.mapping.total_fields.limit`
- Redis ohne `maxmemory`-Richtlinie

**Indikatoren für Fehlalarme:**
- Regex mit verschachtelten Quantoren, bei dem die Eingabezeichenkette durch eine vorgelagerte Prüfung begrenzt ist (`if len(s) > 100: reject`) — die Begrenzung beseitigt katastrophales Backtracking, wenn sie eng genug ist. Zur Prüfung markieren, die Maßnahme aber vermerken.
- Dekompression von Dateien aus den eigenen statischen Assets der Anwendung (nicht benutzergeliefert) — keine Kontrolle durch den Angreifer.
- XML-Parsing von Antworten vertrauenswürdiger interner APIs (nicht benutzergeliefertes XML) — geringeres Risiko, allerdings könnte eine Kompromittierung der externen API schädliches XML einschleusen.
- `list.append()` innerhalb eines Request-Handlers, wenn die Liste flüchtig ist (lokale Variable, kein geteilter Zustand) und die Request-Body-Größe vorgelagert begrenzt ist (Nginx `client_max_body_size`).

## Stolperfallen {#gotchas}

- **re2 ist kein Drop-in-Ersatz für Python-`re`.** `re2` unterstützt keine Rückreferenzen (`\1`), keine Lookahead-/Lookbehind-Assertions und einige Unicode-Features nicht. Vor einem Engine-Wechsel prüfen, welche Regex-Features benötigt werden.
- **Die Kompilierung von Regexen ist ebenfalls ein DoS-Vektor.** Manche Regex-Engines zeigen bei pathologischen Mustern polynomielle Laufzeit während der *Kompilierung*, nicht nur beim Matching. Wenn der Benutzer das Muster liefert (selten, kommt aber in Filter- und Suchfunktionen vor), ist die Wahl der Engine relevant.
- **ZIP-Path-Traversal und ZIP-Bombe sind getrennte Probleme.** Die Prüfung der dekomprimierten Größe verhindert kein Path-Traversal wie `../../../etc/cron.d/evil`. Für die Verarbeitung von ZIP-Dateien sind beide Prüfungen nötig.
- **Die Tiefenlimits für JSON unterscheiden sich je nach Bibliothek.** Python-`json.loads` wirft bei etwa 1000 Verschachtelungsebenen einen `RecursionError` (Standard-Rekursionslimit von CPython). Node.js `JSON.parse` arbeitet iterativ und ist nicht rekursionsanfällig, eine tief verschachtelte Struktur verbraucht aber dennoch O(n) Speicher. Für tief verschachteltes, nicht vertrauenswürdiges JSON `sys.setrecursionlimit` setzen oder `json.loads` mit einer vorgelagerten Tiefenprüfung verwenden.
- **HTTP/2-Stream-Multiplexing ermöglicht DoS auf Verbindungsebene.** Eine einzelne TCP-Verbindung trägt mehrere Streams. Öffnet ein Client die maximal zulässige Anzahl gleichzeitiger Streams und sendet danach RST_STREAM, muss der Server Stream-Zustände anlegen und sofort wieder abbauen. `http2_max_concurrent_streams` in der Serverkonfiguration begrenzen.
- **Rate Limiting verhindert keinen DoS durch eine einzelne Anfrage.** Eine 42.zip-Bombe, ein Billion-Laughs-XML oder ein katastrophaler Regex können die Ressourcen bereits mit einer einzigen Anfrage erschöpfen, bevor das Rate Limiting greift. Inhaltsbasierte Schutzmaßnahmen (Größenprüfungen, Entity-Limits, RE2) sind zusätzlich zum Rate Limiting erforderlich.

## Siehe auch {#see-also}

- CWE-190: Integer Overflow — Überläufe bei Größenberechnungen können zu einer Allokation führen, die zu klein ausfällt; daraus ergibt sich ein verwandtes DoS, wenn später die korrekte Größe benötigt wird
- CWE-611: XML External Entities — XXE nutzt dieselben XML-Parser-Konfigurationen wie die Behebung von Billion Laughs
- CWE-020: Input Validation — vorgelagerte Validierung: Größe, Tiefe und Anzahl vor der Verarbeitung begrenzen
- CWE-770: Allocation Without Limits — verwandt: Allokation ohne Prüfung der verfügbaren Ressourcen
