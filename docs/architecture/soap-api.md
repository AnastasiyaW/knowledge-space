---
title: SOAP API Design
category: reference
tags: [soap, xml, wsdl, web-services, enterprise]
---

# SOAP API Design

SOAP (Simple Object Access Protocol) is an XML-based messaging protocol for data exchange. Powerful but heavyweight - used primarily in enterprise and financial systems where strict contracts and security matter.

## Message Structure

All requests go to a single endpoint. Messages are XML envelopes.

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

### Elements

| Element | Required | Purpose |
|---------|----------|---------|
| **Envelope** | Yes | Root element, defines XML as SOAP message |
| **Body** | Yes | Actual message with function calls and parameters |
| **Header** | No | Application-specific info (security tokens, auth) |
| **Fault** | No | Error info (child of Body, max once per message) |

### Fault Structure
- `faultcode` - error type (`soap:Sender` = client error)
- `reason` - human-readable explanation
- `detail` - additional debugging info

### HTTP Transport

```http
POST /soap HTTP/1.1
Host: api.example.com
Content-Type: text/xml; charset=utf-8
SOAPAction: "doBalanceTransfer"
```

**Important:** HTTP 200 returned for both success AND business-level errors. Only technical/protocol errors use 4xx with SOAP Fault.

## WSDL (Documentation)

WSDL (Web Services Description Language) describes the API in XML. Contains:

1. **Types** - data types (XSD schema)
2. **Interface** - available methods/operations and inputs
3. **Binding** - HTTP method and protocol
4. **Service** - endpoint URL

Since SOAP is fully described by WSDL + XSD, no additional documentation needed. Give developers the WSDL file and they understand the API.

## Advantages

- **Strict data format** - XML + XSD schemas reduce risk of unsafe data
- **Language independence** - create services from WSDL, no specific language needed
- **Protocol independence** - works over HTTP, SMTP, FTP
- **WS-Security** - message-level security beyond HTTPS
- **Reliability** - robust messaging with error detection and recovery

## Disadvantages

- **Complex implementation** - requires deep XML, WSDL, XSD knowledge
- **Performance** - slower than REST/gRPC due to XML processing overhead
- **Resource intensive** - high XML processing overhead, bandwidth, server load
- **Not mobile-friendly** - challenging for resource-limited devices

## When to Use

- **Financial operations** - where every unit matters and error cost is high
- **Corporate environments** - API contracts tied to legal contracts
- **Legacy systems** - existing SOAP infrastructure
- **High-volume structured data** - rigid format needed (government, tax systems)

## Testing with SoapUI

1. Create SOAP project with WSDL URL
2. Create TestSuite and TestCases
3. Add SOAP Request steps
4. Configure assertions (response validation, schema validation)
5. Run tests - green (pass) or red (fail)

## Gotchas

- **HTTP 200 for business errors** - SOAP returns 200 OK even when the business operation fails. Only protocol/technical errors use 4xx codes
- **WSDL complexity** - WSDL files can become extremely large and hard to read. Use tools, never edit manually
- **XML verbosity** - SOAP messages are significantly larger than equivalent JSON, impacting bandwidth and parsing time
- **Namespace hell** - incorrect namespace declarations are the most common cause of "message rejected" errors

## See Also

- [[http-rest-fundamentals]] - REST vs SOAP comparison
- [[data-serialization-formats]] - XML, JSON, XSD details
- [[enterprise-integration]] - ESB, integration patterns
