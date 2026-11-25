---
title: "Analyse de sécurité des conteneurs"
category: tools
tags: [security, containers, vulnerability, trivy, cosign, supply-chain]
level: 3
source_sha256: d87b6a3238bf897b0ecb1d4f54fbb29a8ae5bfd2758e87f94b97721bbc53cb6e
translation: machine
translated_at: '2026-10-24'
---
# Analyse de sécurité des conteneurs {#container-security-scanning}

Détection automatisée des vulnérabilités, des mauvaises configurations et des secrets dans les images de conteneurs, les fichiers IaC et les charges de travail en cours d'exécution. Indispensable pour la sécurité de la chaîne d'approvisionnement CI/CD.

## Faits clés {#key-facts}

- Analyser les images avant le push (CI), après le pull (contrôle d'admission) et à l'exécution
- Bases de données de vulnérabilités : NVD (NIST), GitHub Advisory, spécifiques aux OS (Alpine, Debian)
- Score CVSS : Critique (9.0-10.0), Élevé (7.0-8.9), Moyen (4.0-6.9), Faible (0.1-3.9)
- SBOM (Software Bill of Materials) : liste de tous les composants d'une image
- Signature d'images (Cosign/Notary) : attestation cryptographique de la provenance de l'image
- Shift left : analyser en CI avant que les images n'atteignent le registre
- Les images sans CVE sont une cible mouvante : de nouvelles CVE sont découvertes chaque jour

## Panorama des outils {#tool-landscape}

| Outil | Type | Périmètre | Licence |
|------|------|-------|---------|
| Trivy | Scanner | Images, IaC, SBOM, secrets | Open source |
| Grype | Scanner | Images, SBOM | Open source |
| Snyk Container | Scanner | Images, code | Commercial |
| Cosign | Signature | Signature et vérification d'images | Open source |
| Notary v2 | Signature | Signature d'artefacts OCI | Open source |
| Falco | Runtime | Détection d'anomalies à l'exécution | Open source |
| kube-bench | Audit | Benchmark CIS Kubernetes | Open source |
| Kubescape | Audit | Durcissement NSA/CISA | Open source |

## Utilisation de Trivy {#trivy-usage}

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

## Intégration CI/CD {#cicd-integration}

### GitHub Actions {#github-actions}

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

## Signature d'images avec Cosign {#image-signing-with-cosign}

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

## Contrôle d'admission (bloquer les images vulnérables) {#admission-control-block-vulnerable-images}

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

## Bonnes pratiques de sécurité pour Dockerfile {#dockerfile-security-best-practices}

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

## Protection à l'exécution (Falco) {#runtime-protection-falco}

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

## Pipeline d'analyse {#scanning-pipeline}

```php
Developer -> Dockerfile lint (hadolint)
    -> Build image
    -> Scan image (Trivy: vulns + secrets + config)
    -> Sign image (Cosign)
    -> Push to registry
    -> Admission controller verifies signature
    -> Runtime monitoring (Falco)
```

## Pièges courants {#gotchas}

- **Problème :** l'image de base contient des vulnérabilités sans correctif disponible -> **Correctif :** utiliser des images distroless ou scratch pour réduire la surface d'attaque. Accepter les CVE non corrigeables connues, avec une acceptation de risque documentée.
- **Problème :** une analyse uniquement au moment de la construction ne détecte pas les CVE découvertes ultérieurement -> **Correctif :** mettre en place une analyse continue des images en cours d'exécution. Des outils comme Trivy Operator analysent les charges de travail selon un planning, à l'intérieur du cluster.
- **Problème :** un tag `:latest` ou un tag mutable peut être remplacé après l'analyse -> **Correctif :** utiliser systématiquement des références par digest (`image@sha256:abc...`) en production. Signer les images et les vérifier à l'admission.

## Voir aussi {#see-also}

- [[docker-fundamentals]] - bases des conteneurs
- [[dockerfile-and-image-building]] - construction d'images sécurisées
- [[container-registries]] - sécurité des registres
- [[kubernetes-security]] - sécurité au niveau du cluster
- [[cicd-pipelines]] - intégration de l'analyse dans la CI
