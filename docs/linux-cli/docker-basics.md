---
title: Docker Basics
category: reference
tags: [linux-cli, docker, containers, images, volumes, devops]
---

# Docker Basics

Docker packages applications into containers - isolated, portable runtime environments built from images. This entry covers images, containers, volumes, Dockerfiles, and common operational patterns.

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Image** | Immutable template for containers. Stored in registries. |
| **Container** | Running instance of an image. Can be started/stopped/deleted. |
| **Volume** | Persistent storage outside container filesystem. Survives `docker rm`. |
| **Registry** | Image repository (Docker Hub, GHCR, private). |

Image naming: `[registry/][namespace/]name[:tag]` (e.g., `nginx:latest`, `ghcr.io/org/repo:v1.2`)

## Images

```bash
docker pull ubuntu:20.04              # pull specific version
docker images                         # list local images
docker rmi ubuntu:20.04               # remove image
docker image prune                    # remove dangling images
docker image prune -a                 # remove ALL unused images
```

## Containers

### Run

```bash
docker run ubuntu echo "hello"        # run command and exit
docker run -it ubuntu /bin/bash       # interactive terminal
docker run -d -p 8080:80 --name web nginx  # detached, port mapping
docker run --rm -it ubuntu bash       # auto-remove on exit
docker run -e KEY=VALUE myapp         # with env variable
docker run -v /host:/container image  # bind mount
docker run -v myvolume:/data image    # named volume
```

Key flags: `-i` (interactive), `-t` (TTY), `-d` (detach), `--rm` (auto-remove), `--name` (name), `-p` (port), `-v` (volume), `-e` (env var)

### Lifecycle

```bash
docker ps                             # running containers
docker ps -a                          # all containers
docker stop container                 # graceful stop
docker kill container                 # force stop
docker start container                # start stopped
docker restart container
docker rm container                   # remove stopped
docker rm -f container                # force remove
docker container prune                # remove all stopped
```

### Interact

```bash
docker exec -it container bash        # shell in running container
docker exec container ls /app         # run command
docker logs container                 # view stdout/stderr
docker logs -f container              # follow logs
docker logs --tail 100 container      # last 100 lines
docker inspect container              # detailed JSON info
docker stats container                # live resource usage
docker top container                  # processes inside
docker cp file.txt container:/path/   # copy to container
docker cp container:/path/file.txt ./ # copy from container
```

## Volumes

### Named Volumes

```bash
docker volume create myvol
docker volume ls
docker volume inspect myvol
docker volume rm myvol
docker volume prune                   # remove unused
```

### Bind Mounts

```bash
docker run -v /host/path:/container/path image
docker run -v $(pwd):/app image           # mount current dir
docker run -v $(pwd):/app:ro image        # read-only
```

## Dockerfile

```dockerfile
FROM ubuntu:20.04
WORKDIR /app
COPY . .
COPY requirements.txt /app/
RUN apt-get update && apt-get install -y python3 pip
RUN pip install -r requirements.txt
ENV PORT=8080
EXPOSE 8080
CMD ["python3", "app.py"]

# ENTRYPOINT + CMD pattern
ENTRYPOINT ["python3"]
CMD ["app.py"]     # default arg, overridable
```

### Build

```bash
docker build -t myapp:latest .
docker build -t myapp:1.0 -f Dockerfile.prod .
docker tag myapp:latest registry/myapp:1.0
docker push registry/myapp:1.0
```

## Cleanup

```bash
docker container prune                # stopped containers
docker image prune -a                 # unused images
docker volume prune                   # unused volumes
docker network prune                  # unused networks
docker system prune -a --volumes      # EVERYTHING unused
docker system df                      # disk usage
```

## Patterns

```bash
# Stop all running containers
docker stop $(docker ps -q)

# Remove all containers
docker rm $(docker ps -aq)

# Remove all images
docker rmi $(docker images -q)

# Enter running container by name filter
docker exec -it $(docker ps -q -f name=myapp) bash
```

### Deletion Order

When removing an image with containers:
1. `docker stop container` - stop
2. `docker rm container` - remove container
3. `docker rmi image` - remove image

## Gotchas

- Container filesystem is ephemeral - data lost on `docker rm` unless volumes are used
- `EXPOSE` in Dockerfile is documentation only - does NOT publish the port; use `-p` at run time
- `CMD` is overridden by `docker run` arguments; `ENTRYPOINT` is not (use `--entrypoint` to override)
- Anonymous volumes get random names and are hard to manage - prefer named volumes
- `docker system prune` does NOT remove named volumes - add `--volumes` flag
- Build context (`.`) includes all files in current dir - use `.dockerignore` to exclude large files

## See Also

- [[disks-and-filesystems]] - Mount commands, device files
- [[process-management]] - Processes inside containers
- [[linux-security]] - Namespaces, isolation
