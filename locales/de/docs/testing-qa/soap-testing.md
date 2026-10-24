---
title: "SOAP-Service-Tests mit Python"
category: tools
tags: [soap, xml, wsdl, requests, zeep, api-testing, web-services]
level: 3
source_sha256: c9f0908d7d92a83eb3dbcbb2b56a1f1404e3907f845598c7ca074548f546d6b4
translation: machine
translated_at: '2026-10-24'
---
# SOAP-Service-Tests mit Python {#soap-service-testing-with-python}

Tests für SOAP/XML-Webservices mit `requests` (rohes XML) und `zeep` (WSDL-bewusster Client). SOAP ist in Unternehmens-, Banken- und Behördenintegrationen nach wie vor verbreitet.

## SOAP-Grundlagen für Tester {#soap-basics-for-testers}

SOAP = XML-Envelope mit Header und Body. WSDL = Dienstbeschreibung, die Endpunkte, Operationen und Nachrichtentypen festlegt.

```xml
<!-- SOAP Request -->
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:usr="http://example.com/users">
  <soapenv:Header/>
  <soapenv:Body>
    <usr:GetUser>
      <usr:userId>123</usr:userId>
    </usr:GetUser>
  </soapenv:Body>
</soapenv:Envelope>
```

## Tests mit requests (rohes XML) {#testing-with-requests-raw-xml}

```python
import requests
from lxml import etree

def test_get_user_soap():
    url = "http://example.com/soap/UserService"
    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": "GetUser",
    }
    body = """<?xml version="1.0" encoding="utf-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:usr="http://example.com/users">
      <soapenv:Body>
        <usr:GetUser>
          <usr:userId>123</usr:userId>
        </usr:GetUser>
      </soapenv:Body>
    </soapenv:Envelope>"""

    response = requests.post(url, data=body, headers=headers)
    assert response.status_code == 200

    root = etree.fromstring(response.content)
    ns = {"usr": "http://example.com/users"}
    name = root.find(".//usr:name", ns)
    assert name is not None
    assert name.text == "John Doe"
```

## Tests mit zeep (WSDL-Client) {#testing-with-zeep-wsdl-client}

```python
from zeep import Client

@pytest.fixture(scope="session")
def soap_client():
    return Client("http://example.com/soap/UserService?wsdl")

def test_get_user_zeep(soap_client):
    result = soap_client.service.GetUser(userId="123")
    assert result.name == "John Doe"
    assert result.email is not None
```

Zeep erzeugt aus dem WSDL automatisch Python-Objekte – ohne manuelle XML-Konstruktion.

## XML-Antworten parsen {#parsing-xml-responses}

```python
from lxml import etree

def parse_soap_response(response_bytes, namespace_map):
    root = etree.fromstring(response_bytes)
    body = root.find(".//{http://schemas.xmlsoap.org/soap/envelope/}Body")
    return body

def extract_values(body, xpath, namespaces):
    elements = body.findall(xpath, namespaces)
    return [el.text for el in elements]
```

## Behandlung von SOAP-Faults {#soap-fault-handling}

```python
def test_invalid_user_returns_fault():
    response = send_soap_request(user_id="nonexistent")
    root = etree.fromstring(response.content)

    fault = root.find(".//{http://schemas.xmlsoap.org/soap/envelope/}Fault")
    assert fault is not None

    faultcode = fault.find("faultcode").text
    faultstring = fault.find("faultstring").text
    assert "Client" in faultcode
    assert "not found" in faultstring.lower()
```

## SOAP mit Authentifizierung {#soap-with-authentication}

```python
from requests import Session
from zeep.transports import Transport

session = Session()
session.auth = ("username", "password")  # Basic auth
# or
session.headers.update({"Authorization": "Bearer token123"})

transport = Transport(session=session)
client = Client("http://example.com/service?wsdl", transport=transport)
```

Für WS-Security (WSSE):

```python
from zeep.wsse.username import UsernameToken

wsse = UsernameToken("user", "pass")
client = Client(wsdl_url, wsse=wsse)
```

## Fallstricke {#gotchas}

- **Problem:** Der `SOAPAction`-Header fehlt oder hat einen falschen Wert, was zu 500-Fehlern mit wenig aussagekräftigen Meldungen führt. **Lösung:** Den exakten Action-String im WSDL unter `<soap:operation soapAction="...">` prüfen. Manche Dienste erwarten einen leeren `SOAPAction: ""`-Header.

- **Problem:** Namensraum-Konflikt – XPath liefert None, obwohl das Element in der Antwort vorhanden ist. **Lösung:** Zuerst immer die rohe Antwort-XML prüfen (`print(response.text)`). Die korrekten Namespace-Präfixe in den XPath-Abfragen registrieren.

- **Problem:** Zeep cacht das WSDL zum Zeitpunkt des Imports – ändert sich der Dienst, testen die Tests gegen einen veralteten Vertrag. **Lösung:** Cache für CI deaktivieren: `Client(url, transport=Transport(cache=None))`.

## Siehe auch {#see-also}

- [[api-testing-requests]]
- [[grpc-testing]]
- [[oauth-testing]]
