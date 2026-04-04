---
title: SOAP Service Testing with Python
category: tools
tags: [soap, xml, wsdl, requests, zeep, api-testing, web-services]
---

# SOAP Service Testing with Python

Testing SOAP/XML web services using `requests` (raw XML) and `zeep` (WSDL-aware client). SOAP is still common in enterprise, banking, and government integrations.

## SOAP Basics for Testers

SOAP = XML envelope with Header + Body. WSDL = service contract describing endpoints, operations, and message types.

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

## Testing with requests (Raw XML)

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

## Testing with zeep (WSDL Client)

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

Zeep auto-generates Python objects from WSDL - no manual XML construction.

## Parsing XML Responses

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

## SOAP Fault Handling

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

## SOAP with Authentication

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

For WS-Security (WSSE):

```python
from zeep.wsse.username import UsernameToken

wsse = UsernameToken("user", "pass")
client = Client(wsdl_url, wsse=wsse)
```

## Gotchas

- **Issue:** `SOAPAction` header missing or wrong value causes 500 errors with unhelpful messages. **Fix:** Check WSDL `<soap:operation soapAction="...">` for exact action string. Some services require empty `SOAPAction: ""`.

- **Issue:** Namespace mismatch - XPath returns None even though element exists in response. **Fix:** Always inspect raw response XML first (`print(response.text)`). Register correct namespace prefixes in your XPath queries.

- **Issue:** Zeep caches WSDL at import time - if service changes, tests use stale contract. **Fix:** Disable cache for CI: `Client(url, transport=Transport(cache=None))`.

## See Also

- [[api-testing-requests]]
- [[grpc-testing]]
- [[oauth-testing]]
