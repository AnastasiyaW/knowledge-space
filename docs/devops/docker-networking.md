---
title: Docker Networking
category: containers
tags: [docker, networking, bridge, overlay, port-mapping, dns]
---
# Docker Networking

Docker network drivers, port mapping, service discovery, and inter-container communication.

## Key Facts

- Docker provides 4 network drivers: **bridge** (default), **host**, **overlay** (Swarm), **none**
- **Bridge** network: containers get private IPs; communicate via container name (user-defined bridges) or IP (default bridge)
- **Host** network: container shares host network stack; no port mapping needed; `--network host`
- **Overlay** network: spans multiple Docker hosts (Swarm/K8s); encrypted inter-node communication
- Default bridge (`docker0`) does NOT support DNS resolution by container name - must use `--link` (deprecated) or user-defined bridge
- User-defined bridge networks provide automatic DNS resolution between containers by name
- Port mapping `-p hostPort:containerPort` creates iptables NAT rules
- `-p 127.0.0.1:8080:80` binds only to localhost (not externally accessible)
- [[docker-compose]] creates a user-defined bridge per project automatically
- [[kubernetes-services]] provides more advanced service discovery than Docker networking
- Containers on different networks cannot communicate unless connected to a shared network
- `docker network connect/disconnect` dynamically attaches containers to networks

## Patterns

```bash
# Create user-defined bridge network
docker network create mynet
docker network create --subnet=172.20.0.0/16 mynet

# Run containers on same network (can resolve by name)
docker run -d --name api --network mynet myapi:1.0
docker run -d --name db --network mynet postgres:16
# api can reach db at hostname "db"

# Port mapping variations
docker run -p 8080:80 nginx           # map host 8080 -> container 80
docker run -p 80:80 -p 443:443 nginx  # multiple port mappings
docker run -p 127.0.0.1:3000:3000 app # localhost only
docker run -P nginx                    # publish all EXPOSE'd ports to random host ports

# Inspect network
docker network ls
docker network inspect mynet
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mycontainer

# Connect running container to additional network
docker network connect mynet existing_container

# Host networking (container uses host's network directly)
docker run --network host nginx        # nginx listens on host port 80 directly
```

## Gotchas

- Default `docker0` bridge does NOT support container name DNS - only user-defined bridges do
- Docker modifies iptables rules; running `iptables -F` can break Docker networking
- `-p 0.0.0.0:8080:80` (default) binds to ALL interfaces including public; use `127.0.0.1:` prefix for local-only
- Overlay networks require Swarm mode or external key-value store
- Container restart changes IP address; always use DNS names (container names), not IPs
- Docker Desktop on macOS/Windows runs in a VM - `host` networking behaves differently than on Linux
- IPv6 must be explicitly enabled in Docker daemon config

## See Also

- [[docker-compose]] - automatic network creation per project
- [[docker-images-containers]] - EXPOSE instruction documents ports
- [[kubernetes-services]] - advanced service discovery and load balancing
- [[microservices-architecture]] - inter-service communication patterns
- Docker networking: https://docs.docker.com/network/
