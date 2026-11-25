---
title: "Tests de services SOAP avec Python"
category: tools
tags: [soap, xml, wsdl, requests, zeep, api-testing, web-services]
level: 3
source_sha256: c9f0908d7d92a83eb3dbcbb2b56a1f1404e3907f845598c7ca074548f546d6b4
translation: machine
translated_at: '2026-10-24'
---
# Tests de services SOAP avec Python {#soap-service-testing-with-python}

Tests de services web SOAP/XML avec `requests` (XML brut) et `zeep` (client compatible WSDL). SOAP reste courant dans les intégrations d'entreprise, bancaires et gouvernementales.

## Bases de SOAP pour les testeurs {#soap-basics-for-testers}

SOAP = enveloppe XML avec Header + Body. WSDL = contrat de service décrivant les endpoints, les opérations et les types de messages.

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

## Tests avec requests (XML brut) {#testing-with-requests-raw-xml}

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

## Tests avec zeep (client WSDL) {#testing-with-zeep-wsdl-client}

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

Zeep génère automatiquement des objets Python à partir du WSDL, sans construction manuelle du XML.

## Analyse des réponses XML {#parsing-xml-responses}

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

## Gestion des SOAP Fault {#soap-fault-handling}

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

## SOAP avec authentification {#soap-with-authentication}

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

Pour WS-Security (WSSE) :

```python
from zeep.wsse.username import UsernameToken

wsse = UsernameToken("user", "pass")
client = Client(wsdl_url, wsse=wsse)
```

## Pièges courants {#gotchas}

- **Problème :** un en-tête `SOAPAction` absent ou de valeur incorrecte provoque des erreurs 500 aux messages peu explicites. **Correction :** vérifiez dans le WSDL la valeur exacte de `<soap:operation soapAction="...">`. Certains services exigent un `SOAPAction: ""` vide.

- **Problème :** incohérence de namespace. Le XPath renvoie None alors que l'élément existe dans la réponse. **Correction :** inspectez toujours d'abord le XML brut de la réponse (`print(response.text)`), puis déclarez les bons préfixes de namespace dans vos requêtes XPath.

- **Problème :** Zeep met en cache le WSDL au moment de l'import. Si le service évolue, les tests utilisent un contrat obsolète. **Correction :** désactivez le cache en CI : `Client(url, transport=Transport(cache=None))`.

## Voir aussi {#see-also}

- [[api-testing-requests]]
- [[grpc-testing]]
- [[oauth-testing]]
