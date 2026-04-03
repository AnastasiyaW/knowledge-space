---
title: API Testing Tools
category: tools
tags: [testing, curl, postman, devtools, api, debugging]
---

# API Testing Tools

Practical tools for testing, debugging, and validating APIs during development and integration work.

## cURL

Command-line HTTP client. Cross-platform, scriptable, supports all methods and auth types.

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

**Key flags:** `-X` (method), `-H` (headers), `-d` (data/body), `-u` (credentials), `-k` (skip SSL), `-v` (verbose), `-o` (output to file).

## Chrome DevTools (Network Tab)

Open with F12. Monitor all network requests in real-time.

**Key panels:** Headers (request/response, status), Preview (formatted), Response (raw), Timing (DNS, TCP, TLS, TTFB, Download), Cookies.

**Workflow:** Open DevTools -> Network tab -> perform action -> click request -> inspect. Use **"Copy as cURL"** to reproduce requests in terminal.

**Timing waterfall:** DNS lookup -> TCP connect -> TLS handshake -> Time to First Byte -> Content Download.

**Filters:** XHR, JS, CSS, Img, Media, Font, Doc, WS. Throttle network speed for slow connection testing.

## Postman

GUI-based API testing platform.

**Key features:**
- Collections and folders for request organization
- Environment variables (dev/staging/prod)
- Request chaining with variable extraction
- Pre-request and test scripts (JavaScript)
- Mock servers for API prototyping
- Newman CLI for CI/CD integration
- Import/export OpenAPI specs

**Testing workflow:**
```javascript
pm.test("Status is 200", () => {
  pm.response.to.have.status(200);
});

pm.test("Response has user ID", () => {
  const json = pm.response.json();
  pm.expect(json.id).to.be.a("number");
});
```

## Swagger UI / Editor

Interactive documentation and testing for OpenAPI specs. Write/edit YAML/JSON with live preview. Test endpoints directly from docs.

## Tool Comparison

| Feature | cURL | DevTools | Postman |
|---------|------|----------|---------|
| Environment | CLI | Browser | GUI/CLI |
| Automation | Shell scripts | Limited | Collections/Newman |
| Collaboration | None | None | Teams/Workspaces |
| Best for | Quick tests, CI/CD | Live traffic debugging | Complex API testing |

## SoapUI (SOAP Testing)

1. Create SOAP project with WSDL URL
2. Create TestSuite and TestCases
3. Add SOAP Request steps with assertions
4. Run - assertions show pass/fail

## Gotchas

- **cURL -k in production** - skip SSL verification only in dev, never in prod
- **Postman environment leaks** - don't commit Postman environments with secrets to git
- **DevTools caching** - disable cache checkbox to test without browser cache
- **Copy as cURL** from DevTools includes cookies - sanitize before sharing

## See Also

- [[http-rest-fundamentals]] - HTTP methods, status codes, headers
- [[api-documentation-specs]] - OpenAPI, WSDL specifications
- [[soap-api]] - SOAP testing with SoapUI
