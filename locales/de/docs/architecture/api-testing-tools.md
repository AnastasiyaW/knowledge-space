---
title: "API-Testwerkzeuge"
category: tools
tags: [testing, curl, postman, devtools, api, debugging]
level: 3
source_sha256: 8c2459d222d3d5205a3543400d5985a0aacc162b3ec13fc5195a8fb29af536fb
translation: machine
translated_at: '2026-10-24'
---
# API-Testwerkzeuge {#api-testing-tools}

Praktische Werkzeuge zum Testen, Debuggen und Validieren von APIs während der Entwicklung und bei Integrationsarbeiten.

## cURL {#curl}

Kommandozeilen-HTTP-Client. Plattformübergreifend, skriptfähig, unterstützt alle Methoden und Authentifizierungsarten.

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

**Wichtige Flags:** `-X` (Methode), `-H` (Header), `-d` (Daten/Body), `-u` (Zugangsdaten), `-k` (SSL überspringen), `-v` (ausführlich), `-o` (Ausgabe in Datei).

## Chrome DevTools (Network-Tab) {#chrome-devtools-network-tab}

Öffnen mit F12. Alle Netzwerkanfragen in Echtzeit überwachen.

**Wichtige Bereiche:** Headers (Request/Response, Status), Preview (formatiert), Response (roh), Timing (DNS, TCP, TLS, TTFB, Download), Cookies.

**Workflow:** DevTools öffnen -> Network-Tab -> Aktion ausführen -> Anfrage anklicken -> untersuchen. Mit **„Copy as cURL"** lassen sich Anfragen im Terminal reproduzieren.

**Timing-Wasserfall:** DNS-Lookup -> TCP-Verbindungsaufbau -> TLS-Handshake -> Time to First Byte -> Content-Download.

**Filter:** XHR, JS, CSS, Img, Media, Font, Doc, WS. Netzwerkgeschwindigkeit drosseln, um langsame Verbindungen zu testen.

## Postman {#postman}

GUI-basierte Plattform für API-Tests.

**Wichtige Funktionen:**
- Collections und Ordner zur Organisation von Anfragen
- Umgebungsvariablen (dev/staging/prod)
- Request-Verkettung mit Extraktion von Variablen
- Pre-Request- und Test-Skripte (JavaScript)
- Mock-Server für API-Prototyping
- Newman-CLI für CI/CD-Integration
- Import/Export von OpenAPI-Spezifikationen

**Testablauf:**
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

Interaktive Dokumentation und Tests für OpenAPI-Spezifikationen. YAML/JSON bearbeiten mit Live-Vorschau. Endpunkte direkt aus der Dokumentation testen.

## Werkzeugvergleich {#tool-comparison}

| Feature | cURL | DevTools | Postman |
|---------|------|----------|---------|
| Umgebung | CLI | Browser | GUI/CLI |
| Automatisierung | Shell-Skripte | Eingeschränkt | Collections/Newman |
| Zusammenarbeit | Keine | Keine | Teams/Workspaces |
| Geeignet für | Schnelle Tests, CI/CD | Debugging von Live-Traffic | Komplexe API-Tests |

## SoapUI (SOAP-Tests) {#soapui-soap-testing}

1. SOAP-Projekt mit WSDL-URL anlegen
2. TestSuite und TestCases erstellen
3. SOAP-Request-Schritte mit Assertions hinzufügen
4. Ausführen - Assertions zeigen Pass/Fail

## Fallstricke {#gotchas}

- **cURL -k in Produktion** - SSL-Prüfung nur in Entwicklung überspringen, niemals in Produktion
- **Postman-Umgebungen mit Geheimnissen** - Postman-Umgebungen mit Secrets nicht in Git committen
- **DevTools-Caching** - Checkbox „Disable cache" aktivieren, um ohne Browser-Cache zu testen
- **Copy as cURL** aus DevTools enthält Cookies - vor dem Teilen bereinigen

## Siehe auch {#see-also}

- [[http-rest-fundamentals]] - HTTP-Methoden, Statuscodes, Header
- [[api-documentation-specs]] - OpenAPI-, WSDL-Spezifikationen
- [[soap-api]] - SOAP-Tests mit SoapUI
