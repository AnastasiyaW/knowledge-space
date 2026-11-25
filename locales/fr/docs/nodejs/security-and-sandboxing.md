---
title: "Sécurité et sandboxing"
category: operations
tags: [nodejs, security, crypto, vm, sandbox, password-hashing, macaroons, jwt]
level: 3
source_sha256: edee00148cdae44588709b1b658daf3987da2c9af0e44ea88390712558b329df
translation: machine
translated_at: '2026-10-24'
---
# Sécurité et sandboxing {#security-and-sandboxing}

La sécurité de Node.js englobe le hachage de mots de passe avec sel, l'authentification par jetons, l'exécution de code en sandbox via le module `vm`, et l'isolation de contexte pour les applications multi-locataires. Comprendre à la fois les primitives cryptographiques et l'isolation à l'exécution est indispensable pour la sécurité côté serveur.

## Faits clés {#key-facts}

- UUID v4 : 128 bits au total, 122 bits aléatoires, ~10 milliards d'années pour trouver une collision
- Utiliser les UUID pour : les jetons de session, les identifiants de contexte de requête, les identifiants de fichiers, les clés de base de données
- **Macaroons** (le format de jeton de Google) sont préférables à JWT : un modèle de sécurité plus honnête, et ils supportent l'atténuation (ajout de restrictions à des jetons existants)
- Les Macaroons bénéficient d'un support médiocre dans les bibliothèques JavaScript : faible adoption, car JWT est surévalué
- TypeScript 5 a introduit les décorateurs standard (remplaçant les décorateurs expérimentaux) avec `reflect-metadata` pour la réflexion à l'exécution

## Patrons {#patterns}

### Hachage de mots de passe avec sel {#password-hashing-with-salt}

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

**Pourquoi un sel :** sans sel, des mots de passe identiques produisent des empreintes identiques. Les tables arc-en-ciel peuvent retrouver les mots de passe courants. Le sel rend chaque empreinte unique.

### Exécution de code en sandbox {#sandboxed-code-execution}

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

### Comparaison de la sécurité entre frameworks {#multi-framework-security-comparison}

La même couche de sécurité dans Pure Node.js, Fastify, NestJS, Metarhia :
- Inscription et authentification des utilisateurs
- Gestion des sessions avec TTL
- Isolation de contexte par connexion
- Permissions de base de données différentes selon la session utilisateur

## Sécurité NPM {#npm-security}

- `npm test` : exécuter les tests depuis les scripts de package.json
- `npm audit` : rechercher les vulnérabilités connues
- Toujours lire la documentation npm pour les options disponibles : 3 à 5 minutes de lecture évitent des heures de tâtonnement
- Examiner les dépendances avant de les ajouter : la qualité des paquets npm influe directement sur la sécurité

## Pièges à éviter {#gotchas}

- Le module `vm` N'EST PAS un sandbox de sécurité : un attaquant déterminé peut s'en échapper. Utiliser des processus isolés ou des conteneurs pour une isolation réelle
- Attaques par canal temporel sur la comparaison de chaînes : utiliser `crypto.timingSafeEqual()` pour la vérification des mots de passe
- Les Macaroons offrent un modèle de sécurité supérieur, mais le support dans l'écosystème JS est limité

## Voir aussi {#see-also}

- [[application-architecture]] - niveaux d'isolation de contexte (call, connection, session, application)
- [Gestion des erreurs](error-handling.md) - AppError contre erreurs système, propagation sûre des erreurs
- [[modules-and-packages]] - sécurité npm et gestion des dépendances
