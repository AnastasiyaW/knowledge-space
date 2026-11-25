---
title: "Sicherheit und Sandboxing"
category: operations
tags: [nodejs, security, crypto, vm, sandbox, password-hashing, macaroons, jwt]
level: 3
source_sha256: edee00148cdae44588709b1b658daf3987da2c9af0e44ea88390712558b329df
translation: machine
translated_at: '2026-10-24'
---
# Sicherheit und Sandboxing {#security-and-sandboxing}

Die Sicherheit in Node.js umfasst Passwort-Hashing mit Salt, tokenbasierte Authentifizierung, sandboxed Codeausführung über das `vm`-Modul und Kontextisolation für Multi-Tenant-Anwendungen. Das Verständnis sowohl kryptografischer Primitive als auch der Laufzeitisolation ist für die serverseitige Sicherheit unerlässlich.

## Wichtige Fakten {#key-facts}

- UUID v4: 128 Bit insgesamt, 122 zufällige Bit, ~10 Milliarden Jahre bis zu einer Kollision
- Verwende UUID für: Session-Tokens, Request-Kontext-IDs, Datei-Identifikatoren, Datenbankschlüssel
- **Macaroons** (Googles Token-Format) sind besser als JWT: ein ehrlicheres Sicherheitsmodell, unterstützen Attenuation (das Hinzufügen von Einschränkungen zu bestehenden Tokens)
- Macaroons haben eine schwache Unterstützung in JavaScript-Bibliotheken – die Verbreitung ist gering, weil JWT überbewertet ist
- TypeScript 5 führte Standard-Decorators (als Ersatz für die experimentellen) ein, mit `reflect-metadata` für Reflection zur Laufzeit

## Muster {#patterns}

### Passwort-Hashing mit Salt {#password-hashing-with-salt}

```js
const crypto = require('node:crypto');

const hashPassword = (password) => {
  const salt = crypto.randomBytes(16).toString('hex');
  const hash = crypto.scryptSync(password, salt, 64).toString('hex');
  return `${salt}:${hash}`;
};

const verifyPassword = (password, stored) => {
  const [salt, hash] = stored.split(':');
  const derived = crypto.scryptSync(password, salt, 64).toString('hex');
  return hash === derived;
};
```

**Warum Salt:** Ohne Salt erzeugen identische Passwörter identische Hashes. Rainbow-Tables können gängige Passwörter zurückrechnen. Ein Salt macht jeden Hash eindeutig.

### Sandboxed Codeausführung {#sandboxed-code-execution}

```js
const vm = require('vm');

class AppError extends Error {
  constructor(message, code) {
    super(message);
    this.code = code;
  }
}

const context = vm.createContext({
  AppError,
  // Only expose safe APIs to untrusted code
});

const result = vm.runInContext(userCode, context, { timeout: 5000 });
// instanceof AppError distinguishes app errors from system errors
// Never expose system error details to untrusted code
```

### Vergleich der Sicherheit über mehrere Frameworks {#multi-framework-security-comparison}

Dieselbe Sicherheitsschicht in Pure Node.js, Fastify, NestJS, Metarhia:
- Benutzerregistrierung und Authentifizierung
- Session-Verwaltung mit TTL
- Kontextisolation pro Verbindung
- Unterschiedliche DB-Berechtigungen pro Benutzersitzung

## NPM-Sicherheit {#npm-security}

- `npm test` – führt Tests aus den Skripten in package.json aus
- `npm audit` – prüft auf bekannte Schwachstellen
- Lies immer die npm-Dokumentation für verfügbare Flags – 3–5 Minuten Lesen ersparen Stunden des Ratens
- Prüfe Abhängigkeiten, bevor du sie hinzufügst – die Qualität von npm-Paketen wirkt sich direkt auf die Sicherheit aus

## Stolperfallen {#gotchas}

- Das `vm`-Modul ist KEINE Sicherheits-Sandbox – ein entschlossener Angreifer kann es verlassen. Für echte Isolation isolierte Prozesse oder Container verwenden
- Timing-Angriffe auf Stringvergleiche: `crypto.timingSafeEqual()` für die Passwortprüfung verwenden
- Macaroons bieten ein überlegenes Sicherheitsmodell, aber die Ökosystem-Unterstützung in JS ist begrenzt

## Siehe auch {#see-also}

- [[application-architecture]] – Kontextisolationsstufen (call, connection, session, application)
- [Fehlerbehandlung](error-handling.md) – AppError vs. Systemfehler, sichere Fehlerweitergabe
- [[modules-and-packages]] – npm-Sicherheit und Abhängigkeitsverwaltung
