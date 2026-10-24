---
title: "Bases de Docker"
category: reference
tags: [linux-cli, docker, containers, images, volumes, devops]
level: 3
source_sha256: 204a8f29a0f9b080b9d93ca71d20a66325f0ca90203212ab5414dfe8f072d6a1
translation: machine
translated_at: '2026-10-24'
---
# Bases de Docker {#docker-basics}

Docker empaquette les applications dans des conteneurs, c'est-à-dire des environnements d'exécution isolés et portables construits à partir d'images. Cette entrée couvre les images, les conteneurs, les volumes, les Dockerfiles et les schémas opérationnels courants.

## Concepts fondamentaux {#core-concepts}

| Concept | Description |
|---------|-------------|
| **Image** | Modèle immuable pour les conteneurs. Stocké dans des registres. |
| **Conteneur** | Instance en cours d'exécution d'une image. Peut être démarré, arrêté ou supprimé. |
| **Volume** | Stockage persistant en dehors du système de fichiers du conteneur. Survit à `docker rm`. |
| **Registre** | Dépôt d'images (Docker Hub, GHCR, privé). |

Nommage des images : `[registre/][espace-de-noms/]nom[:tag]` (ex. : `nginx:latest`, `ghcr.io/org/repo:v1.2`)

## Images {#images}

```bash
docker pull ubuntu:20.04              # pull specific version
docker images                         # list local images
docker rmi ubuntu:20.04               # remove image
docker image prune                    # remove dangling images
docker image prune -a                 # remove ALL unused images
```

## Conteneurs {#containers}

### Exécution {#run}

```bash
docker run ubuntu echo "hello"        # run command and exit
docker run -it ubuntu /bin/bash       # interactive terminal
docker run -d -p 8080:80 --name web nginx  # detached, port mapping
docker run --rm -it ubuntu bash       # auto-remove on exit
docker run -e KEY=VALUE myapp         # with env variable
docker run -v /host:/container image  # bind mount
docker run -v myvolume:/data image    # named volume
```

Options principales : `-i` (interactif), `-t` (TTY), `-d` (détaché), `--rm` (suppression automatique), `--name` (nom), `-p` (port), `-v` (volume), `-e` (variable d'environnement)

### Cycle de vie {#lifecycle}

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

### Interaction {#interact}

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

## Volumes {#volumes}

### Volumes nommés {#named-volumes}

```bash
docker volume create myvol
docker volume ls
docker volume inspect myvol
docker volume rm myvol
docker volume prune                   # remove unused
```

### Montages de liaison (bind mounts) {#bind-mounts}

```bash
docker run -v /host/path:/container/path image
docker run -v $(pwd):/app image           # mount current dir
docker run -v $(pwd):/app:ro image        # read-only
```

## Dockerfile {#dockerfile}

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

### Construction {#build}

```bash
docker build -t myapp:latest .
docker build -t myapp:1.0 -f Dockerfile.prod .
docker tag myapp:latest registry/myapp:1.0
docker push registry/myapp:1.0
```

## Nettoyage {#cleanup}

```bash
docker container prune                # stopped containers
docker image prune -a                 # unused images
docker volume prune                   # unused volumes
docker network prune                  # unused networks
docker system prune -a --volumes      # EVERYTHING unused
docker system df                      # disk usage
```

## Schémas d'utilisation {#patterns}

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

### Ordre de suppression {#deletion-order}

Lors de la suppression d'une image utilisée par des conteneurs :
1. `docker stop conteneur` - arrêter
2. `docker rm conteneur` - supprimer le conteneur
3. `docker rmi image` - supprimer l'image

## Pièges courants {#gotchas}

- Le système de fichiers du conteneur est éphémère : les données sont perdues lors d'un `docker rm`, sauf si des volumes sont utilisés
- `EXPOSE` dans un Dockerfile n'est que de la documentation : il ne publie PAS le port ; utiliser `-p` à l'exécution
- `CMD` est remplacé par les arguments de `docker run`, contrairement à `ENTRYPOINT` (utiliser `--entrypoint` pour le remplacer)
- Les volumes anonymes reçoivent des noms aléatoires et sont difficiles à gérer : privilégier les volumes nommés
- `docker system prune` ne supprime PAS les volumes nommés : ajouter l'option `--volumes`
- Le contexte de construction (`.`) inclut tous les fichiers du répertoire courant : utiliser `.dockerignore` pour exclure les gros fichiers

## Voir aussi {#see-also}

- [[disks-and-filesystems]] - Commandes de montage, fichiers de périphériques
- [[process-management]] - Processus à l'intérieur des conteneurs
- [[linux-security]] - Espaces de noms, isolation
