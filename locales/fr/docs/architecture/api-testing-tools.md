---
title: "Outils de test d'API"
category: tools
tags: [testing, curl, postman, devtools, api, debugging]
level: 3
source_sha256: 8c2459d222d3d5205a3543400d5985a0aacc162b3ec13fc5195a8fb29af536fb
translation: machine
translated_at: '2026-10-24'
---
# Outils de test d'API {#api-testing-tools}

Outils pratiques pour tester, déboguer et valider des API pendant le développement et les travaux d'intégration.

## cURL {#curl}

Client HTTP en ligne de commande. Multiplateforme, scriptable, prend en charge toutes les méthodes et tous les types d'authentification.

```bash
# GET request
curl -X GET https://api.example.com/users

# POST with JSON
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"name":"John"}' \
  https://api.example.com/users

# With auth header
curl -H "Authorization: Bearer TOKEN" https://api.example.com/data

# Upload file
curl -X POST -F "file=@photo.jpg" https://api.example.com/upload

# Verbose output (debug TLS, headers)
curl -v https://api.example.com/users
```

**Options principales :** `-X` (méthode), `-H` (en-têtes), `-d` (données/corps), `-u` (identifiants), `-k` (ignorer SSL), `-v` (mode verbeux), `-o` (sortie vers un fichier).

## Chrome DevTools (onglet Réseau) {#chrome-devtools-network-tab}

Ouvrir avec F12. Surveiller toutes les requêtes réseau en temps réel.

**Panneaux principaux :** Headers (requête/réponse, statut), Preview (mise en forme), Response (brut), Timing (DNS, TCP, TLS, TTFB, téléchargement), Cookies.

**Déroulement :** Ouvrir DevTools -> onglet Network -> effectuer l'action -> cliquer sur la requête -> inspecter. Utiliser **« Copy as cURL »** pour reproduire les requêtes dans le terminal.

**Cascade de timing :** résolution DNS -> connexion TCP -> négociation TLS -> Time to First Byte -> téléchargement du contenu.

**Filtres :** XHR, JS, CSS, Img, Media, Font, Doc, WS. Limiter la vitesse du réseau pour tester les connexions lentes.

## Postman {#postman}

Plateforme de test d'API avec interface graphique.

**Fonctionnalités principales :**
- Collections et dossiers pour organiser les requêtes
- Variables d'environnement (dev/staging/prod)
- Enchaînement de requêtes avec extraction de variables
- Scripts de pré-requête et de test (JavaScript)
- Serveurs mock pour le prototypage d'API
- Newman CLI pour l'intégration CI/CD
- Import/export de spécifications OpenAPI

**Flux de test :**
```javascript
pm.test("Status is 200", () => {
  pm.response.to.have.status(200);
});

pm.test("Response has user ID", () => {
  const json = pm.response.json();
  pm.expect(json.id).to.be.a("number");
});
```

## Swagger UI / Editor {#swagger-ui-editor}

Documentation interactive et test pour les spécifications OpenAPI. Écriture/édition en YAML/JSON avec aperçu en direct. Tester les endpoints directement depuis la documentation.

## Comparaison des outils {#tool-comparison}

| Fonctionnalité | cURL | DevTools | Postman |
|----------------|------|----------|---------|
| Environnement | CLI | Navigateur | GUI/CLI |
| Automatisation | Scripts shell | Limitée | Collections/Newman |
| Collaboration | Aucune | Aucune | Équipes/Workspaces |
| Idéal pour | Tests rapides, CI/CD | Débogage du trafic en direct | Tests d'API complexes |

## SoapUI (tests SOAP) {#soapui-soap-testing}

1. Créer un projet SOAP avec l'URL du WSDL
2. Créer une TestSuite et des TestCases
3. Ajouter des étapes SOAP Request avec des assertions
4. Exécuter - les assertions indiquent réussite/échec

## Pièges courants {#gotchas}

- **cURL -k en production** - ignorer la vérification SSL uniquement en développement, jamais en production
- **Fuite d'environnements Postman** - ne pas committer dans git des environnements Postman contenant des secrets
- **Cache de DevTools** - cocher la case de désactivation du cache pour tester sans cache du navigateur
- **Copy as cURL** depuis DevTools inclut les cookies - les nettoyer avant de partager

## Voir aussi {#see-also}

- [[http-rest-fundamentals]] - méthodes HTTP, codes de statut, en-têtes
- [[api-documentation-specs]] - spécifications OpenAPI, WSDL
- [[soap-api]] - tests SOAP avec SoapUI
