---
title: Docker Images & Containers
category: containers
tags: [docker, images, containers, dockerfile, multi-stage, registry]
---
# Docker Images & Containers

Docker image lifecycle: building, layering, multi-stage builds, registries, and container runtime.

## Key Facts

- **Image** = immutable filesystem snapshot built from a Dockerfile; **Container** = running process from an image
- Each Dockerfile instruction creates a **layer**; layers are cached and shared between images
- `FROM` sets the base image; every Dockerfile must start with `FROM`
- `COPY` adds files from build context; `ADD` supports URLs and tar extraction (prefer `COPY`)
- `RUN` executes commands during build (creates new layer); `CMD` / `ENTRYPOINT` define runtime command
- `ENTRYPOINT` = fixed command; `CMD` = default args (overridable); combine for flexible entry
- **Multi-stage builds** use multiple `FROM` statements - copy artifacts from builder stage to slim final image
- Image tags follow `registry/repo:tag` format; `latest` is default tag but NOT auto-updated
- [[docker-networking]] port mapping with `-p host:container` exposes container ports
- [[kubernetes-pods]] run containers using the same OCI image format
- Docker uses **copy-on-write** filesystem; container writes happen in a thin writable layer on top of image layers
- Distroless / Alpine base images reduce attack surface and image size

## Patterns

```dockerfile
# Multi-stage build - Go application
FROM golang:1.21 AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /server .

FROM gcr.io/distroless/static:nonroot
COPY --from=builder /server /server
ENTRYPOINT ["/server"]

# Python ML application
FROM python:3.11-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

```bash
# Build image with tag
docker build -t myapp:1.0 .
docker build -t myapp:1.0 -f Dockerfile.prod .

# Run container
docker run -d --name web -p 8080:80 myapp:1.0
docker run -it --rm myapp:1.0 /bin/sh       # interactive, auto-remove
docker run -d --restart=unless-stopped myapp  # auto-restart policy

# Image management
docker images                          # list local images
docker image prune                     # remove dangling images
docker image prune -a                  # remove all unused images
docker system df                       # show disk usage
docker history myapp:1.0               # show layer history

# Push to registry
docker tag myapp:1.0 registry.example.com/myapp:1.0
docker push registry.example.com/myapp:1.0

# Inspect running container
docker exec -it web /bin/sh
docker logs -f web --tail 100
docker stats web                       # live resource usage
docker inspect web                     # full JSON metadata
```

## Gotchas

- Each `RUN` creates a layer; chaining with `&&` reduces layers: `RUN apt-get update && apt-get install -y pkg && rm -rf /var/lib/apt/lists/*`
- `.dockerignore` is critical - without it, `COPY . .` sends entire context including `.git`, `node_modules`, etc.
- `latest` tag is just a convention, not a pointer to newest build; always pin versions in production
- `CMD` in exec form `["python","app.py"]` preferred over shell form `python app.py` - shell form wraps in `/bin/sh -c` which breaks signal handling
- Build cache invalidation cascades - if layer N changes, all subsequent layers rebuild; put frequently-changing instructions last
- `COPY --chown=user:group` avoids extra `RUN chown` layer
- Running as root in containers is a security risk; use `USER nonroot` or distroless images

## See Also

- [[docker-compose]] - multi-container applications
- [[docker-networking]] - bridge, host, overlay networks
- [[kubernetes-pods]] - K8s uses same OCI image specification
- [[ci-cd-pipelines]] - automated image building
- Docker reference: https://docs.docker.com/reference/dockerfile/
- Multi-stage builds: https://docs.docker.com/build/building/multi-stage/
