---
title: "SOAP-API-Design"
category: reference
tags: [soap, xml, wsdl, web-services, enterprise]
level: 3
source_sha256: d6eb4e05dc9e4a543c27c0088fcbf582945c93b9c80ee4860fae646159c12569
translation: machine
translated_at: '2026-10-24'
---
# SOAP-API-Design {#soap-api-design}

SOAP (Simple Object Access Protocol) ist ein XML-basiertes Nachrichtenprotokoll für den Datenaustausch. Leistungsstark, aber schwergewichtig – wird vor allem in Unternehmens- und Finanzsystemen eingesetzt, in denen strikte Verträge und Sicherheit wichtig sind.

## Nachrichtenstruktur {#message-structure}

Alle Anfragen gehen an einen einzigen Endpunkt. Nachrichten sind XML-Envelopes.

```xml
<Envelope>
  <Header>
    <SecurityToken>user_token_here</SecurityToken>
  </Header>
  <Body>
    <getBalanceRequest>
      <number>12345</number>
    </getBalanceRequest>
  </Body>
</Envelope>
```

### Elemente {#elements}

| Element | Erforderlich | Zweck |
|---------|--------------|-------|
| **Envelope** | Ja | Wurzelelement, definiert das XML als SOAP-Nachricht |
| **Body** | Ja | Eigentliche Nachricht mit Funktionsaufrufen und Parametern |
| **Header** | Nein | Anwendungsspezifische Informationen (Sicherheitstoken, Authentifizierung) |
| **Fault** | Nein | Fehlerinformationen (Kindelement von Body, maximal einmal pro Nachricht) |

### Fault-Struktur {#fault-structure}
- `faultcode` – Fehlertyp (`soap:Sender` = Clientfehler)
- `reason` – für Menschen lesbare Erklärung
- `detail` – zusätzliche Informationen zur Fehlersuche

### HTTP-Transport {#http-transport}

```http
POST /soap HTTP/1.1
Host: api.example.com
Content-Type: text/xml; charset=utf-8
SOAPAction: "doBalanceTransfer"
```

**Wichtig:** HTTP 200 wird sowohl bei Erfolg als auch bei fachlichen Fehlern zurückgegeben. Nur technische/protokollbezogene Fehler verwenden 4xx mit einem SOAP Fault.

## WSDL (Dokumentation) {#wsdl-documentation}

WSDL (Web Services Description Language) beschreibt die API in XML. Sie enthält:

1. **Types** – Datentypen (XSD-Schema)
2. **Interface** – verfügbare Methoden/Operationen und Eingaben
3. **Binding** – HTTP-Methode und Protokoll
4. **Service** – Endpunkt-URL

Da SOAP vollständig durch WSDL + XSD beschrieben wird, ist keine zusätzliche Dokumentation nötig. Entwickler erhalten die WSDL-Datei und verstehen die API.

## Vorteile {#advantages}

- **Strikte Datenformate** – XML + XSD-Schemas verringern das Risiko unsicherer Daten
- **Sprachunabhängigkeit** – Services aus WSDL erstellen, keine bestimmte Sprache erforderlich
- **Protokollunabhängigkeit** – funktioniert über HTTP, SMTP, FTP
- **WS-Security** – Sicherheit auf Nachrichtenebene über HTTPS hinaus
- **Zuverlässigkeit** – robuste Nachrichtenübermittlung mit Fehlererkennung und -wiederherstellung

## Nachteile {#disadvantages}

- **Komplexe Implementierung** – erfordert fundierte Kenntnisse in XML, WSDL und XSD
- **Performance** – langsamer als REST/gRPC aufgrund des Overheads durch XML-Verarbeitung
- **Ressourcenintensiv** – hoher Overhead bei der XML-Verarbeitung, Bandbreite und Serverlast
- **Nicht mobilfreundlich** – schwierig für ressourcenbeschränkte Geräte

## Einsatzgebiete {#when-to-use}

- **Finanzoperationen** – wo jede Einheit zählt und Fehlerkosten hoch sind
- **Unternehmensumgebungen** – API-Verträge sind an rechtliche Verträge gebunden
- **Legacy-Systeme** – bestehende SOAP-Infrastruktur
- **Große Mengen strukturierter Daten** – starres Format erforderlich (Behörden, Steuersysteme)

## Testen mit SoapUI {#testing-with-soapui}

1. SOAP-Projekt mit WSDL-URL erstellen
2. TestSuite und TestCases anlegen
3. SOAP-Request-Schritte hinzufügen
4. Assertions konfigurieren (Antwortvalidierung, Schemavalidierung)
5. Tests ausführen – grün (bestanden) oder rot (fehlgeschlagen)

## Fallstricke {#gotchas}

- **HTTP 200 bei fachlichen Fehlern** – SOAP gibt auch dann 200 OK zurück, wenn die fachliche Operation fehlschlägt. Nur Protokoll-/technische Fehler verwenden 4xx-Codes
- **WSDL-Komplexität** – WSDL-Dateien können extrem groß und schwer lesbar werden. Werkzeuge verwenden, niemals manuell bearbeiten
- **XML-Ausführlichkeit** – SOAP-Nachrichten sind deutlich größer als gleichwertiges JSON, was Bandbreite und Parsing-Zeit beeinflusst
- **Namespace-Chaos** – fehlerhafte Namespace-Deklarationen sind die häufigste Ursache für „message rejected"-Fehler

## Siehe auch {#see-also}

- [[http-rest-fundamentals]] – Vergleich REST vs. SOAP
- [[data-serialization-formats]] – Details zu XML, JSON, XSD
- [[enterprise-integration]] – ESB, Integrationsmuster
