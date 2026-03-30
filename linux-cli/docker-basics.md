---
title: Docker Basics
category: patterns
tags: [docker, containers, images, volumes]
---
# Docker Basics

Core Docker concepts and commands for working with containers, images, and volumes.

## Key Facts

- **Image** - immutable template (blueprint); **Container** - running instance created from an image
- One image can create many containers; images are stored in registries (Docker Hub)
- `docker pull` downloads image; `docker run` creates AND starts a container from an image
- `docker run -it` = interactive + pseudo-TTY (for shell access)
- `--rm` flag auto-removes container after it stops (prevents accumulation of stopped containers)
- **Volumes** persist data outside container filesystem; survive container removal
- Named volumes can be reused across containers; anonymous volumes are deleted with container
- Image tags specify version: `ubuntu:20.04`, `nginx:latest`; omitting tag defaults to `latest`
- Must stop container before removing it; must remove container before removing its image
- Docker commands need [[users-and-groups]] root or docker group membership
- Docker modifies [[iptables-firewall]] rules for container networking

## Patterns

```bash
# Pull image from Docker Hub
docker pull busybox              # defaults to :latest tag
docker pull busybox:latest       # explicit latest tag
docker pull ubuntu:22.04         # specific version

# List local images
docker images

# Run container interactively
docker run -it ubuntu /bin/bash        # interactive shell
docker run -it python:3.11 python3     # Python REPL
docker run -it --rm busybox /bin/sh    # auto-remove on exit

# Run container in background (detached)
docker run -d --name myapp nginx

# List containers
docker ps                   # running containers only
docker ps -a                # all containers (including stopped)

# Stop and remove container
docker stop myapp
docker rm myapp

# Force remove running container
docker rm -f myapp

# Remove image (container must be stopped and removed first)
docker stop bboxcntr
docker rm bboxcntr
docker rmi busybox:1.36.1

# Correct order: stop container -> remove container -> remove image

# Volume management
docker volume create myvol           # Create named volume
docker volume ls                     # List volumes
docker volume rm myvol               # Remove volume

# Run with volume mount
docker run -v myvol:/data myimage    # Named volume
docker run -v /host/path:/container/path myimage  # Bind mount

# Execute command in running container
docker exec -it myapp /bin/bash

# View container logs
docker logs myapp
docker logs -f myapp                 # Follow (tail -f equivalent)
```

## Gotchas

- `docker pull busybox/latest` is WRONG - correct syntax is `busybox:latest` (colon, not slash)
- `--rm` removes the CONTAINER, not the image - the image stays
- Cannot remove an image while a container (even stopped) is using it - remove containers first
- `-it` = `-i` (interactive, keeps stdin open) + `-t` (pseudo-TTY for formatting) - both needed for shell
- `docker run` always creates a NEW container; use `docker start` to restart a stopped one
- Named volumes persist data; anonymous volumes are removed with `docker rm -v`
- Any program can run in `docker run -it` as long as it is installed in the image and in `$PATH`

## See Also

- [[process-management]] - containers are processes visible via `ps`
- [[filesystem-hierarchy]] - mount points for volumes
- [[iptables-firewall]] - Docker creates firewall rules for port mapping
- Docker documentation: https://docs.docker.com/reference/cli/docker/
