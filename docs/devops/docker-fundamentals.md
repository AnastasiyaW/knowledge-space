---
title: Docker Fundamentals
category: concepts
tags: [devops, docker, containers, images, networking, volumes]
---

# Docker Fundamentals

Docker is a platform for building, packaging, and running applications in isolated containers that share the host OS kernel. Containers are lighter than VMs (MBs vs GBs, seconds vs minutes startup) and provide process-level isolation via Linux namespaces and cgroups.

## Architecture

- **Docker Daemon** (`dockerd`) - background service managing containers, images, networks
- **Docker CLI** (`docker`) - command-line client communicating with daemon via REST API
- **containerd** - container runtime managing container lifecycle under dockerd
- **runc** - OCI-compliant low-level runtime that actually creates containers
- **Docker Hub** - default public registry for container images

Images stored in `/var/lib/docker/`. Daemon listens on Unix socket `/var/run/docker.sock`.

## Containers vs VMs

| Feature | Container | VM |
|---------|-----------|-----|
| Isolation | Process-level (shared kernel) | Full OS (hypervisor) |
| Startup | Seconds | Minutes |
| Size | MBs | GBs |
| Overhead | Minimal | Significant (guest OS) |
| Density | Hundreds per host | Tens per host |

## Running Containers

```bash
docker run nginx                              # foreground (attached)
docker run -d nginx                           # background (detached)
docker run -d --name web nginx                # custom name
docker run -d -p 8080:80 nginx               # port mapping host:container
docker run -it ubuntu /bin/bash               # interactive + TTY
docker run --rm nginx echo "hello"            # auto-remove after exit
docker run -d -e MYSQL_ROOT_PASSWORD=secret mysql:8  # env var
docker run -d -v /host/path:/container/path nginx    # volume mount
docker run -d --restart=always nginx          # restart policy
```

### Port Mapping

Multiple containers can expose the same container port but must use different host ports:
```bash
docker run -d -p 3000:80 --name app1 nginx
docker run -d -p 3001:80 --name app2 nginx
```

### Restart Policies

- `no` (default) - never restart
- `always` - restart on any exit, including reboot
- `unless-stopped` - like always but not after manual stop
- `on-failure[:N]` - restart only on non-zero exit code, optional max retries

## Container Lifecycle

```bash
docker ps                    # list running
docker ps -a                 # list all (including stopped)
docker stop <name|id>        # graceful (SIGTERM, then SIGKILL after 10s)
docker start <name|id>       # start stopped container
docker restart <name|id>     # stop + start
docker kill <name|id>        # force stop (SIGKILL immediately)
docker rm <name|id>          # remove stopped container
docker rm -f <name|id>       # force remove running
docker rm $(docker ps -aq)   # remove all stopped
```

### Inspecting Containers

```bash
docker exec -it <name> /bin/bash   # shell into container
docker exec <name> ls /app         # single command
docker logs <name>                 # stdout/stderr
docker logs -f <name>              # follow logs (live)
docker logs --tail 100 <name>      # last 100 lines
docker inspect <name>              # full metadata (JSON)
docker stats                       # live resource usage
docker top <name>                  # processes in container
```

## Docker Images

Images are read-only layered templates. Each Dockerfile instruction creates a layer. Layers are cached - only changed layers rebuilt.

```bash
docker images                   # list local images
docker pull nginx:1.25          # download
docker image inspect nginx      # metadata
docker image history nginx      # layer history
docker tag myapp:latest myapp:v1.0   # create tag
docker rmi nginx:1.25           # remove image
docker image prune -a           # remove ALL unused images
```

Always use specific tags in production. `latest` is just a convention - not necessarily the newest version.

## Volumes and Data Persistence

Containers are ephemeral - data lost when removed. Volumes persist data.

```bash
# Named volume (Docker-managed)
docker volume create mydata
docker run -d -v mydata:/var/lib/mysql mysql

# Bind mount (host directory)
docker run -d -v $(pwd)/html:/usr/share/nginx/html nginx

# Volume management
docker volume ls
docker volume inspect mydata
docker volume rm mydata
docker volume prune            # remove unused
```

**Writable layer**: each container has own writable layer (copy-on-write). Changes lost on removal. Volumes bypass this.

**Database upgrade pattern**: named volume with DB data survives container replacement - run newer image version with same volume.

## Docker Networking

```bash
docker network ls
docker network create mynet
docker run -d --network mynet --name app1 nginx
docker run -d --network mynet --name app2 nginx
# app1 and app2 communicate by name (DNS resolution)
```

| Type | Description |
|------|-------------|
| bridge | Default. Container-to-container on same host. Custom bridges enable DNS by name |
| host | Shares host network. No port mapping needed |
| none | No networking. Fully isolated |
| overlay | Multi-host (Docker Swarm) |

**Default bridge**: containers communicate by IP only, not name. **Custom bridge**: DNS resolution by container name - recommended for multi-container apps.

## Cleanup

```bash
docker system prune              # stopped containers + unused networks + dangling images
docker system prune -a           # also unused images
docker system prune --volumes    # also unused volumes
docker system df                 # disk usage
```

## Gotchas

- `EXPOSE` in Dockerfile is documentation only - does not publish the port. Use `-p` at runtime
- `localhost` inside a container refers to THAT container, not the host. Use container names on custom networks
- Default bridge network does not provide DNS resolution by name - always create custom networks
- `docker cp` is one-time copy, not sync. Use bind mounts for continuous sync during development
- Alpine images use musl libc - potential compatibility issues with C extensions (Python, Node native modules)

## See Also

- [[dockerfile-and-image-building]] - Dockerfile syntax, multi-stage builds, optimization
- [[docker-compose]] - multi-container orchestration
- [[docker-for-ml]] - ML-specific Docker patterns
- [[kubernetes-architecture]] - container orchestration at scale
