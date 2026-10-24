---
title: "Dockerfile und Image-Erstellung"
category: concepts
tags: [devops, docker, dockerfile, multi-stage, image-optimization]
level: 3
source_sha256: 7e91e9ab94b0be1b3e274d748c788cc870e32534edce4299e61f50b3f580ff48
translation: machine
translated_at: '2026-10-24'
---
# Dockerfile und Image-Erstellung {#dockerfile-and-image-building}

Ein Dockerfile ist eine Textdatei mit Anweisungen zum Erstellen von Docker-Images. Jede Anweisung erzeugt einen Layer, der für inkrementelle Neuerstellungen gecacht wird. Das Verständnis des Layer-Cachings ist der Schlüssel zu schnellen Builds.

## Dockerfile-Anweisungen {#dockerfile-instructions}

| Anweisung | Zweck |
|-----------|-------|
| `FROM` | Basis-Image (muss die erste Anweisung sein) |
| `RUN` | Befehl während des Builds ausführen (erzeugt einen Layer) |
| `COPY` | Dateien/Verzeichnisse aus dem Build-Kontext in das Image kopieren |
| `ADD` | Wie COPY, unterstützt aber URLs und entpackt Archive automatisch |
| `CMD` | Standardbefehl beim Start des Containers (überschreibbar) |
| `ENTRYPOINT` | Fester Befehl (CMD wird zu Argumenten) |
| `WORKDIR` | Arbeitsverzeichnis für nachfolgende Anweisungen setzen |
| `EXPOSE` | Dokumentiert, auf welchen Ports der Container lauscht |
| `ENV` | Umgebungsvariable setzen (zur Laufzeit verfügbar) |
| `ARG` | Variable zur Build-Zeit (zur Laufzeit nicht verfügbar) |
| `VOLUME` | Mount-Punkt für externen Speicher deklarieren |
| `USER` | Benutzer für nachfolgende Anweisungen und zur Laufzeit setzen |
| `LABEL` | Metadaten hinzufügen (Maintainer, Version) |
| `HEALTHCHECK` | Befehl zur Überprüfung des Container-Zustands definieren |

## Einfaches Dockerfile {#basic-dockerfile}

```dockerfile
FROM python:3.11-slim
LABEL maintainer="dev@company.com"
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
ENV APP_ENV=production
CMD ["python", "app.py"]
```

## CMD vs. ENTRYPOINT {#cmd-vs-entrypoint}

```dockerfile
# CMD: easily overridable
CMD ["python", "app.py"]
# docker run myapp               -> runs python app.py
# docker run myapp bash           -> runs bash (overrides CMD)

# ENTRYPOINT: fixed base command
ENTRYPOINT ["python"]
CMD ["app.py"]
# docker run myapp               -> runs python app.py
# docker run myapp test.py        -> runs python test.py (CMD overridden)
# docker run --entrypoint sh myapp -> overrides ENTRYPOINT
```

## Optimierung des Layer-Caching {#layer-caching-optimization}

Anweisungen von am seltensten zu am häufigsten geänderten ordnen:

```dockerfile
FROM node:20-alpine           # rarely changes
WORKDIR /app
COPY package*.json ./          # changes when deps change
RUN npm ci                     # cached if package.json unchanged
COPY . .                       # changes on every code change
CMD ["node", "server.js"]
```

## Multi-Stage-Builds {#multi-stage-builds}

Build- und Laufzeit-Stages trennen, um die finale Image-Größe drastisch zu reduzieren:

```dockerfile
# Stage 1: Build
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Runtime (much smaller)
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Benannte Stages mit `AS`. Zwischen Stages kopieren mit `--from=<stage>`. Es können mehrere Build-Stages vorhanden sein.

### Java-Multi-Stage-Beispiel {#java-multi-stage-example}

```dockerfile
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

## HEALTHCHECK {#healthcheck}

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/ || exit 1
```

Zustände: healthy, unhealthy, starting. `--start-period` ist die Schonfrist vor der ersten Prüfung. In Kombination mit `--restart=always` und einem Autoheal-Container lassen sich eingefrorene Container automatisch wiederherstellen.

## Build-Befehle {#build-commands}

```bash
docker build -t myapp:v1 .                          # build from current dir
docker build -t myapp:v1 -f custom.Dockerfile .      # custom Dockerfile
docker build --no-cache -t myapp:v1 .                # ignore cache
docker build --build-arg VERSION=3.11 -t myapp:v1 .  # build argument
```

## Veröffentlichen von Images {#publishing-images}

```bash
docker login
docker tag myapp:v1 username/myapp:v1
docker push username/myapp:v1
```

## Alternativen zur Erstellung von Java-Images {#java-image-generation-alternatives}

| Ansatz | Vorteile | Nachteile |
|--------|----------|-----------|
| Dockerfile | Volle Kontrolle | Muss geschrieben und gepflegt werden |
| Buildpacks (`mvn spring-boot:build-image`) | Keine Konfiguration, geschichtet | Langsamster Build |
| Google Jib (`mvn jib:build`) | Kein Docker-Daemon, schnelle inkrementelle Builds | Nur als Maven/Gradle-Plugin verfügbar |

## .dockerignore {#dockerignore}

Dateien aus dem Build-Kontext ausschließen (ähnlich wie .gitignore):

```text
node_modules/
.git/
*.log
.env
```

## Fallstricke {#gotchas}

- `--no-cache-dir` bei pip verhindert, dass Pakete im Image-Layer gecacht werden
- `COPY . .` invalidiert den Cache bei JEDER Dateiänderung – daher ans Ende stellen
- Alpine-Basisimages (~5 MB) können wegen musl libc Kompatibilitätsprobleme mit C-Erweiterungen haben
- Die Anweisung `VOLUME` erzeugt automatisch anonyme Volumes, die schwer nachzuverfolgen sind – explizite Mounts bevorzugen
- Zur Laufzeit gesetztes `-e` überschreibt das `ENV` aus dem Dockerfile
- Ein mit `docker commit` (imperativer Ansatz) erstelltes Image ist größer und weniger reproduzierbar als ein Build aus einem Dockerfile

## Siehe auch {#see-also}

- [[docker-fundamentals]] - Container-Grundlagen, Lebenszyklus, Netzwerk
- [[docker-compose]] - Orchestrierung mehrerer Container
- [[container-registries]] - ECR, ACR, Docker Hub, Nexus
- [[cicd-pipelines]] - automatisierte Image-Erstellung
