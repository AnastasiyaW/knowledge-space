---
description: "CWE-400 : un attaquant déclenche une consommation non contrôlée de CPU, de mémoire, de disque ou de descripteurs de fichiers via un DoS par expression régulière, une collision de hachage, des bombes zip, une expansion d'entités XML ou des collections non bornées."
date: 2026-04-16
tags: [security, cwe, dos, redos, regex, zip-bomb, xml-bomb, algorithmic-complexity, resource-exhaustion]
level: Advanced
source_sha256: 553600169d8216a7cde67194472423c9f1c725266584d2ceecb349e48a2b86ab
translation: machine
translated_at: '2026-10-24'
---
# CWE-400 : Consommation de ressources non contrôlée {#cwe-400-uncontrolled-resource-consumption}

**CWE-400** | Pilier CWE : Resource Management | Plage de score de base CVSS : 5.3-7.5 (DoS) | Rang 24 du Top 25 CWE

## Sémantique fonctionnelle {#functional-semantics}

La classe de vulnérabilités couvre les entrées qui provoquent une consommation de ressources asymétrique : l'attaquant envoie O(n) octets, tandis que le serveur consomme O(n²) ou O(2^n) de CPU ou de mémoire. L'application ne fixe aucune borne supérieure au travail effectué pour une requête donnée. L'exploitation ne nécessite ni authentification ni injection de code ; une seule requête soigneusement construite peut épuiser toutes les ressources disponibles d'un type donné, dégradant ou interrompant le service pour l'ensemble des utilisateurs.

Types de ressources visés : temps CPU, mémoire tas, frames de pile (récursion), E/S disque, descripteurs de fichiers, slots du pool de threads, pool de connexions à la base de données, bande passante réseau sortante.

## Taxonomie de la surface d'attaque {#attack-surface-taxonomy}

| Classe d'attaque | Ressource | Complexité | Exemples |
|---|---|---|---|
| ReDoS — backtracking catastrophique | CPU | O(2^n) au pire | Expression régulière malveillante appliquée à une chaîne fournie par l'utilisateur |
| Collision de hachage (HashDoS) | CPU | O(n²) par bucket | Paramètres POST HTTP forgés remplissant un seul bucket de hachage |
| Décompression bomb | Mémoire + disque | O(taux_de_compression) | 42.zip (4,5 Po à partir de 42 Ko), gzip bomb |
| Expansion d'entités XML (Billion Laughs) | Mémoire | O(10^9) | Références d'entités XML imbriquées |
| Algorithme quadratique | CPU | O(n²) | Expression régulière avec un moteur peu performant, concaténation naïve de chaînes dans une boucle |
| Croissance de collection non bornée | Mémoire | O(n) non borné | Ajout à une liste sans plafond de taille |
| Épuisement du pool de connexions | Descripteurs de fichiers | O(connexions_ouvertes) | Attaque HTTP slow-read / Slowloris |
| Inondation de journaux | E/S disque | O(entrées_de_journal) | Requête qui déclenche une sortie de journal non bornée |
| Profondeur de requête GraphQL | CPU + BD | O(profondeur^branchement) | `{ user { friends { friends { friends ... } } } }` |
| Inondation de flux gRPC | Mémoire + CPU | O(messages) | RPC en streaming non borné, sans backpressure |

## ReDoS — backtracking catastrophique {#redos-catastrophic-backtracking}

Un moteur d'expressions régulières utilisant le backtracking peut présenter une complexité temporelle exponentielle lorsqu'un motif contient des quantificateurs imbriqués ou une alternative sur des ensembles de caractères qui se chevauchent.

**Anatomie d'une expression régulière catastrophique :**
- `(a+)+` — quantificateurs imbriqués : les mêmes caractères `a` peuvent être appariés de façon exponentielle
- `(a|a)+` — alternative avec des branches identiques
- `([a-zA-Z]+)*` — groupe non borné avec un quantificateur appliqué au groupe
- `(.*a){n}` — correspondance répétée jusqu'à un caractère rare avec un `.*` glouton

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

**Motifs catastrophiques à signaler lors de la revue de code :**

| Motif | Pourquoi c'est catastrophique |
|---|---|
| `(a+)+` | Chaque `a` peut appartenir au groupe interne ou externe |
| `(\w+\s?)+` | Le même caractère correspond ambigûment aux deux groupes |
| `(.*,)*` | `.` correspond à `,`, créant une ambiguïté exponentielle |
| `([a-z]+)*` | Répétition imbriquée non bornée |
| `^(([a-z])+.)+[A-Z]([a-z])+$` | Plusieurs groupes qui se chevauchent |

## Décompression bombs {#decompression-bombs}

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

## Expansion d'entités XML (Billion Laughs) {#xml-entity-expansion-billion-laughs}

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

## Collision de hachage / HashDoS {#hash-collision-hashdos}

L'attaquant forge des paramètres POST dont les clés produisent toutes le même hachage et tombent dans le même bucket, transformant des recherches en O(1) en parcours de chaîne en O(n). Pour n=100 000 paramètres : O(n²) = 10^10 opérations.

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

Python 3.2+ utilise par défaut la randomisation des hachages (`PYTHONHASHSEED`), ce qui atténue le HashDoS pour les dictionnaires Python. Le `HashMap` de Java utilise une structure en arbre pour les buckets volumineux (Java 8+). PHP a historiquement été la plateforme la plus touchée.

## Croissance de collection non bornée {#unbounded-collection-growth}

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

## Profondeur et complexité des requêtes GraphQL {#graphql-query-depth-complexity}

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

## Heuristiques de détection {#detection-heuristics}

**Déclencheurs d'analyse statique :**
- Expression régulière avec quantificateurs imbriqués appliquée à une chaîne contrôlée par l'utilisateur : `re.match(pattern, user_input)` où le motif contient `(X+)+`, `(X*Y*)+`, `(\w+\s?)+`
- `zipfile.ZipFile.read()`, `tarfile.extractall()`, `gzip.decompress()` sans vérification de taille
- Analyse XML : `lxml.etree.fromstring()` sans `XMLParser(resolve_entities=False)`, `DocumentBuilderFactory.newDocumentBuilder()` sans options de fonctionnalités
- `list.append(item)` dans un gestionnaire de requêtes sans plafond de taille sur la liste
- `dict` ou `map` construit à partir de clés fournies par l'utilisateur, sans limite de nombre
- Fonction récursive dont la profondeur de récursion est contrôlée par l'utilisateur (la profondeur de parcours d'arbre correspond au niveau d'imbrication du JSON utilisateur)
- `json.loads(user_data)` en Python : sans risque d'injection, mais le module json de Python a une profondeur de récursion maximale pour les structures imbriquées ; un JSON profondément imbriqué provoque une `RecursionError`

**Déclencheurs de configuration :**
- `MAX_CONTENT_LENGTH` non défini dans Flask (corps de requête illimité)
- Absence de `client_max_body_size` dans la configuration Nginx
- Serveur GraphQL sans limite de profondeur ni de complexité
- Elasticsearch sans `index.mapping.total_fields.limit`
- Redis sans politique `maxmemory`

**Indicateurs de faux positifs :**
- Expression régulière avec quantificateurs imbriqués dont la chaîne d'entrée est bornée par une vérification préalable (`if len(s) > 100: reject`) : la borne élimine le backtracking catastrophique si elle est suffisamment serrée. À signaler pour revue, en mentionnant l'atténuation.
- Décompression de fichiers issus des ressources statiques de l'application (non fournis par l'utilisateur) : aucun contrôle par l'attaquant.
- Analyse XML de réponses provenant d'API internes de confiance (et non de XML fourni par l'utilisateur) : risque plus faible, mais la compromission d'une API externe pourrait introduire du XML malveillant.
- `list.append()` dans un gestionnaire de requêtes où la liste est éphémère (variable locale, pas d'état partagé) et où la taille du corps de requête est limitée en amont (`client_max_body_size` de Nginx).

## Pièges à éviter {#gotchas}

- **re2 n'est pas un remplacement direct de `re` en Python.** `re2` ne prend pas en charge les références arrière (`\1`), les assertions d'anticipation et de rétrospection (lookahead/lookbehind), ni certaines fonctionnalités Unicode. Évaluez les fonctionnalités d'expressions régulières nécessaires avant de changer de moteur.
- **La compilation d'une expression régulière peut aussi constituer un vecteur de DoS.** Certains moteurs présentent une complexité polynomiale lors de la *compilation* de motifs pathologiques, et pas seulement lors de la recherche. Si l'utilisateur fournit le motif (cas rare, mais présent dans les fonctions de filtrage et de recherche), le choix du moteur est déterminant.
- **Le path traversal dans les archives ZIP et la ZIP bomb sont deux problèmes distincts.** Vérifier la taille décompressée n'empêche pas un path traversal tel que `../../../etc/cron.d/evil`. Les deux vérifications sont nécessaires pour le traitement des archives ZIP.
- **Les limites de profondeur JSON dépendent de la bibliothèque.** En Python, `json.loads` lève `RecursionError` vers 1000 niveaux d'imbrication (limite de récursion par défaut de CPython). `JSON.parse` de Node.js est itératif et n'est pas vulnérable à une bombe de récursion, mais une structure profondément imbriquée consomme tout de même une mémoire en O(n). Utilisez `sys.setrecursionlimit` ou une vérification préalable de profondeur avant `json.loads` pour les JSON profondément imbriqués et non fiables.
- **Le multiplexage de flux HTTP/2 permet un DoS au niveau de la connexion.** Une seule connexion TCP transporte plusieurs flux ; un client ouvrant le nombre maximal de flux simultanés puis envoyant RST_STREAM force le serveur à allouer puis libérer immédiatement l'état de chaque flux. Limitez `http2_max_concurrent_streams` dans la configuration du serveur.
- **Le rate limiting n'empêche pas le DoS par requête unique.** Une bombe 42.zip, un XML Billion Laughs ou une expression régulière catastrophique peuvent épuiser les ressources en une seule requête, avant que le rate limiting ne se déclenche. Des défenses basées sur le contenu (vérifications de taille, limites d'entités, RE2) sont nécessaires en complément du rate limiting.

## Voir aussi {#see-also}

- CWE-190 : Integer Overflow — un dépassement de capacité dans les calculs de taille peut conduire à une allocation sous-dimensionnée, avec un DoS lié lorsque la taille correcte est ensuite requise
- CWE-611 : XML External Entities — XXE partage avec billion laughs les mêmes correctifs de configuration du parseur XML
- CWE-020 : Input Validation — validation en amont : limiter la taille, la profondeur et le nombre avant tout traitement
- CWE-770 : Allocation Without Limits — lié : allocation sans vérification des ressources disponibles
