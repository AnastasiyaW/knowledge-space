---
title: "Fondamentaux de Docker"
category: concepts
tags: [devops, docker, containers, images, networking, volumes]
level: 2
source_sha256: 24a5692db2be29635796afa81a2bc64a9e2aaa884a2fb8ab199b1509894672b2
translation: machine
translated_at: '2026-10-24'
---
# Fondamentaux de Docker {#docker-fundamentals}

Docker est une plateforme permettant de construire, empaqueter et exécuter des applications dans des conteneurs isolés qui partagent le noyau du système hôte. Les conteneurs sont plus légers que les machines virtuelles (quelques Mo contre plusieurs Go, démarrage en quelques secondes contre quelques minutes) et assurent une isolation au niveau des processus grâce aux namespaces et aux cgroups de Linux.

## Architecture {#architecture}

- **Docker Daemon** (`dockerd`) - service en arrière-plan qui gère les conteneurs, les images et les réseaux
- **Docker CLI** (`docker`) - client en ligne de commande qui communique avec le daemon via une API REST
- **containerd** - runtime de conteneurs qui gère le cycle de vie des conteneurs sous dockerd
- **runc** - runtime bas niveau conforme à l'OCI qui crée effectivement les conteneurs
- **Docker Hub** - registre public par défaut pour les images de conteneurs

Les images sont stockées dans `/var/lib/docker/`. Le daemon écoute sur la socket Unix `/var/run/docker.sock`.

## Conteneurs et machines virtuelles {#containers-vs-vms}

| Caractéristique | Conteneur | Machine virtuelle |
|-----------------|-----------|-------------------|
| Isolation | Au niveau des processus (noyau partagé) | OS complet (hyperviseur) |
| Démarrage | Secondes | Minutes |
| Taille | Mo | Go |
| Surcharge | Minimale | Significative (OS invité) |
| Densité | Centaines par hôte | Dizaines par hôte |

## Exécution de conteneurs {#running-containers}

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

### Mappage de ports {#port-mapping}

Plusieurs conteneurs peuvent exposer le même port de conteneur, mais doivent utiliser des ports hôtes différents :
```bash
docker run -d -p 3000:80 --name app1 nginx
docker run -d -p 3001:80 --name app2 nginx
```

### Politiques de redémarrage {#restart-policies}

- `no` (par défaut) - ne jamais redémarrer
- `always` - redémarrer à la sortie, y compris après un redémarrage de la machine
- `unless-stopped` - comme `always`, mais pas après un arrêt manuel
- `on-failure[:N]` - redémarrer uniquement en cas de code de sortie non nul, avec un nombre maximal de tentatives optionnel

## Cycle de vie des conteneurs {#container-lifecycle}

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

### Inspection des conteneurs {#inspecting-containers}

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

## Images Docker {#docker-images}

Les images sont des modèles en couches et en lecture seule. Chaque instruction du Dockerfile crée une couche. Les couches sont mises en cache : seules les couches modifiées sont reconstruites.

```bash
docker images                   # list local images
docker pull nginx:1.25          # download
docker image inspect nginx      # metadata
docker image history nginx      # layer history
docker tag myapp:latest myapp:v1.0   # create tag
docker rmi nginx:1.25           # remove image
docker image prune -a           # remove ALL unused images
```

Utilisez toujours des tags précis en production. `latest` n'est qu'une convention, et ne désigne pas nécessairement la version la plus récente.

## Volumes et persistance des données {#volumes-and-data-persistence}

Les conteneurs sont éphémères : les données sont perdues à leur suppression. Les volumes permettent de persister les données.

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

**Couche inscriptible** : chaque conteneur possède sa propre couche inscriptible (copy-on-write). Les modifications sont perdues à la suppression du conteneur. Les volumes contournent ce mécanisme.

**Mise à niveau d'une base de données** : un volume nommé contenant les données de la base survit au remplacement du conteneur. Il suffit de lancer une version plus récente de l'image avec le même volume.

## Réseaux Docker {#docker-networking}

```bash
docker network ls
docker network create mynet
docker run -d --network mynet --name app1 nginx
docker run -d --network mynet --name app2 nginx
# app1 and app2 communicate by name (DNS resolution)
```

| Type | Description |
|------|-------------|
| bridge | Par défaut. Communication conteneur à conteneur sur le même hôte. Les bridges personnalisés permettent la résolution DNS par nom |
| host | Partage le réseau de l'hôte. Aucun mappage de port nécessaire |
| none | Aucun réseau. Isolation totale |
| overlay | Multi-hôtes (Docker Swarm) |

**Bridge par défaut** : les conteneurs ne communiquent que par adresse IP, et non par nom. **Bridge personnalisé** : résolution DNS par nom de conteneur. C'est la solution recommandée pour les applications composées de plusieurs conteneurs.

## Nettoyage {#cleanup}

```bash
docker system prune              # stopped containers + unused networks + dangling images
docker system prune -a           # also unused images
docker system prune --volumes    # also unused volumes
docker system df                 # disk usage
```

## Pièges courants {#gotchas}

- `EXPOSE` dans un Dockerfile n'est que de la documentation : il ne publie pas le port. Utilisez `-p` à l'exécution
- `localhost` à l'intérieur d'un conteneur désigne CE conteneur, et non l'hôte. Utilisez les noms de conteneurs sur les réseaux personnalisés
- Le réseau bridge par défaut ne fournit pas de résolution DNS par nom : créez toujours des réseaux personnalisés
- `docker cp` effectue une copie ponctuelle, et non une synchronisation. Utilisez des bind mounts pour une synchronisation continue pendant le développement
- Les images Alpine utilisent musl libc : des problèmes de compatibilité peuvent survenir avec les extensions C (modules natifs Python, Node)

## Voir aussi {#see-also}

- [[dockerfile-and-image-building]] - syntaxe du Dockerfile, builds multi-étapes, optimisation
- [[docker-compose]] - orchestration multi-conteneurs
- [[docker-for-ml]] - patterns Docker spécifiques au machine learning
- [[kubernetes-architecture]] - orchestration de conteneurs à grande échelle
