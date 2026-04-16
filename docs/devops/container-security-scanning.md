---
title: Container Security Scanning
category: tools
tags: [security, containers, vulnerability, trivy, cosign, supply-chain]
---

# Container Security Scanning

Automated detection of vulnerabilities, misconfigurations, and secrets in container images, IaC files, and running workloads. Essential for CI/CD supply chain security.

## Key Facts

- Scan images before push (CI), after pull (admission control), and at runtime
- Vulnerability databases: NVD (NIST), GitHub Advisory, OS-specific (Alpine, Debian)
- CVSS scoring: Critical (9.0-10.0), High (7.0-8.9), Medium (4.0-6.9), Low (0.1-3.9)
- SBOM (Software Bill of Materials): lists all components in an image
- Image signing (Cosign/Notary): cryptographic attestation of image provenance
- Shift left: scan in CI before images reach registry
- Zero-CVE images are a moving target - new CVEs discovered daily

## Tool Landscape

| Tool | Type | Scope | License |
|------|------|-------|---------|
| Trivy | Scanner | Images, IaC, SBOM, secrets | Open source |
| Grype | Scanner | Images, SBOM | Open source |
| Snyk Container | Scanner | Images, code | Commercial |
| Cosign | Signing | Image signing/verification | Open source |
| Notary v2 | Signing | OCI artifact signing | Open source |
| Falco | Runtime | Runtime anomaly detection | Open source |
| kube-bench | Audit | CIS Kubernetes benchmark | Open source |
| Kubescape | Audit | NSA/CISA hardening | Open source |

## Trivy Usage

```bash
# Scan image for vulnerabilities
trivy image nginx:latest

# Scan with severity filter
trivy image --severity HIGH,CRITICAL myapp:v1.0

# Scan Dockerfile / IaC
trivy config .

# Generate SBOM
trivy image --format spdx-json -o sbom.json myapp:v1.0

# Scan filesystem (local project)
trivy fs --security-checks vuln,secret,config .

# Scan Kubernetes cluster
trivy k8s --report summary cluster

# Exit code on findings (for CI gates)
trivy image --exit-code 1 --severity CRITICAL myapp:v1.0
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Security Scan
on: [push, pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Trivy scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          format: sarif
          output: trivy-results.sarif
          severity: CRITICAL,HIGH
          exit-code: 1

      - name: Upload results
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: trivy-results.sarif
```

## Image Signing with Cosign

```bash
# Generate key pair
cosign generate-key-pair

# Sign image
cosign sign --key cosign.key myregistry/myapp:v1.0

# Verify signature
cosign verify --key cosign.pub myregistry/myapp:v1.0

# Keyless signing (using OIDC identity)
cosign sign myregistry/myapp:v1.0
# Opens browser for OIDC authentication

# Verify keyless signature
cosign verify \
  --certificate-identity=user@example.com \
  --certificate-oidc-issuer=https://accounts.google.com \
  myregistry/myapp:v1.0
```

## Admission Control (Block Vulnerable Images)

```yaml
# OPA/Gatekeeper policy to require image scanning
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredImageScanning
metadata:
  name: require-trivy-scan
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
    namespaces: ["production"]
  parameters:
    maxSeverity: "HIGH"
```

## Dockerfile Security Best Practices

```dockerfile
# Use specific version, not :latest
FROM python:3.11-slim-bookworm

# Run as non-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy only needed files
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser . /app
WORKDIR /app

USER appuser

# Read-only filesystem friendly
EXPOSE 8080
CMD ["python", "app.py"]
```

## Runtime Protection (Falco)

```yaml
# Falco custom rule: detect shell in container
- rule: Terminal shell in container
  desc: Detect shell opened in a container
  condition: >
    spawned_process and container and
    proc.name in (bash, sh, zsh)
  output: >
    Shell opened in container
    (user=%user.name container=%container.name
     image=%container.image.repository)
  priority: WARNING
  tags: [container, shell]
```

## Scanning Pipeline

```php
Developer -> Dockerfile lint (hadolint)
    -> Build image
    -> Scan image (Trivy: vulns + secrets + config)
    -> Sign image (Cosign)
    -> Push to registry
    -> Admission controller verifies signature
    -> Runtime monitoring (Falco)
```

## Gotchas

- **Issue:** Base image has vulnerabilities but no fix available -> **Fix:** Use distroless or scratch images to minimize attack surface. Accept known unfixable CVEs with documented risk acceptance.
- **Issue:** Scanning only at build time misses newly discovered CVEs -> **Fix:** Implement continuous scanning of running images. Tools like Trivy Operator scan workloads on a schedule inside the cluster.
- **Issue:** Image tag `:latest` or mutable tags can be replaced after scanning -> **Fix:** Always use digest-based references (`image@sha256:abc...`) in production. Sign images and verify at admission.

## See Also

- [[docker-fundamentals]] - container basics
- [[dockerfile-and-image-building]] - building secure images
- [[container-registries]] - registry security
- [[kubernetes-security]] - cluster-level security
- [[cicd-pipelines]] - integrating scanning in CI
