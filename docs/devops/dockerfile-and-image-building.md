---
title: Dockerfile and Image Building
category: concepts
tags: [devops, docker, dockerfile, multi-stage, image-optimization]
---

# Dockerfile and Image Building

A Dockerfile is a text file with instructions for building Docker images. Each instruction creates a layer, cached for incremental rebuilds. Understanding layer caching is key to fast builds.

## Dockerfile Instructions

| Instruction | Purpose |
|-------------|---------|
| `FROM` | Base image (required first instruction) |
| `RUN` | Execute command during build (creates layer) |
| `COPY` | Copy files/dirs from build context to image |
| `ADD` | Like COPY but supports URLs and auto-extracts archives |
| `CMD` | Default command when container starts (overridable) |
| `ENTRYPOINT` | Fixed command (CMD becomes arguments) |
| `WORKDIR` | Set working directory for subsequent instructions |
| `EXPOSE` | Document which ports the container listens on |
| `ENV` | Set environment variable (available at runtime) |
| `ARG` | Build-time variable (not available at runtime) |
| `VOLUME` | Declare mount point for external storage |
| `USER` | Set user for subsequent instructions and runtime |
| `LABEL` | Add metadata (maintainer, version) |
| `HEALTHCHECK` | Define container health verification command |

## Basic Dockerfile

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

## CMD vs ENTRYPOINT

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

## Layer Caching Optimization

Order instructions from least-changing to most-changing:

```dockerfile
FROM node:20-alpine           # rarely changes
WORKDIR /app
COPY package*.json ./          # changes when deps change
RUN npm ci                     # cached if package.json unchanged
COPY . .                       # changes on every code change
CMD ["node", "server.js"]
```

## Multi-Stage Builds

Separate build and runtime stages to dramatically reduce final image size:

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

Named stages with `AS`. Copy between stages with `--from=<stage>`. Can have multiple build stages.

### Java Multi-Stage Example

```dockerfile
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

## HEALTHCHECK

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/ || exit 1
```

States: healthy, unhealthy, starting. `--start-period` is grace period before first check. Combine with `--restart=always` and autoheal container for auto-recovery of frozen containers.

## Build Commands

```bash
docker build -t myapp:v1 .                          # build from current dir
docker build -t myapp:v1 -f custom.Dockerfile .      # custom Dockerfile
docker build --no-cache -t myapp:v1 .                # ignore cache
docker build --build-arg VERSION=3.11 -t myapp:v1 .  # build argument
```

## Publishing Images

```bash
docker login
docker tag myapp:v1 username/myapp:v1
docker push username/myapp:v1
```

## Java Image Generation Alternatives

| Approach | Pros | Cons |
|----------|------|------|
| Dockerfile | Full control | Must write/maintain |
| Buildpacks (`mvn spring-boot:build-image`) | Zero config, layered | Slowest build |
| Google Jib (`mvn jib:build`) | No Docker daemon, fast incremental | Maven/Gradle plugin only |

## .dockerignore

Exclude files from build context (like .gitignore):
```text
node_modules/
.git/
*.log
.env
```

## Gotchas

- `--no-cache-dir` with pip prevents caching packages in the image layer
- `COPY . .` invalidates cache on ANY file change - put it last
- Alpine base images (~5MB) may have compatibility issues with C extensions due to musl libc
- `VOLUME` directive auto-creates anonymous volumes that are hard to track - prefer explicit mounts
- Runtime `-e` overrides Dockerfile `ENV`
- Image built by `docker commit` (imperative approach) is larger and less reproducible than Dockerfile builds

## See Also

- [[docker-fundamentals]] - container basics, lifecycle, networking
- [[docker-compose]] - multi-container orchestration
- [[container-registries]] - ECR, ACR, Docker Hub, Nexus
- [[cicd-pipelines]] - automated image building
