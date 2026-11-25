---
title: "Docker pour l'ingénierie des données"
category: tools
tags: [data-engineering, docker, containers, devops, deployment]
level: 3
source_sha256: 09bf5b78b5d3bca142a4e7b5130250094f7b27224727663eabe1a5e9befb62e6
translation: machine
translated_at: '2026-10-24'
---
# Docker pour l'ingénierie des données {#docker-for-data-engineering}

Docker fournit des environnements isolés et reproductibles pour les charges de travail d'ingénierie des données. Les conteneurs regroupent les applications avec leurs dépendances, garantissant des environnements de développement, de test et de production identiques.

## Conteneurs vs VM {#containers-vs-vms}

| Caractéristique | Conteneurs | VM |
|-----------------|-----------|-----|
| OS | Partagent le noyau de l'hôte | OS invité complet |
| Poids | Léger | Lourd |
| Démarrage | Secondes | Minutes |
| Outils IaC | Dockerfile, docker-compose | Vagrant |

## Concepts clés {#core-concepts}
- **Image** - modèle en lecture seule (plan)
- **Conteneur** - instance en cours d'exécution d'une image
- **Couche** - chaque instruction du Dockerfile crée une couche mise en cache
- **Volume** - stockage persistant indépendant du cycle de vie du conteneur
- **Registre** - stockage des images (Docker Hub, privé)

## Commandes essentielles {#essential-commands}

```bash
# Run container
docker run --rm --name pg \
  -e POSTGRES_PASSWORD=test \
  -p 5432:5432 \
  -v $(pwd)/data:/var/lib/postgresql/data \
  -d postgres:14

# Management
docker ps                         # list running
docker exec -it pg psql -U postgres  # shell into container
docker logs --tail=10 -f pg      # follow logs
docker stop pg && docker rm pg

# Docker Compose
docker compose up -d              # start in background
docker compose ps                 # list services
docker compose logs --tail=100 -f
docker compose down               # stop + remove
```

## Dockerfile {#dockerfile}

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "etl.py"]
```

## Docker Compose {#docker-compose}

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:14
    restart: always
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_PASSWORD=secret
    volumes:
      - pgdata:/var/lib/postgresql/data
volumes:
  pgdata:
```

## Bonnes pratiques {#best-practices}
- **1 application = 1 conteneur**
- Configurer via des **variables d'environnement** (pas de reconstruction pour les changements de configuration)
- **Données persistantes sur des volumes** (le redémarrage d'un conteneur ne perd pas les données)
- Ne jamais stocker de mots de passe dans le Dockerfile ou docker-compose.yml

## Pièges à éviter {#gotchas}
- Changements de variables d'environnement : `docker compose restart` ne suffit PAS, il faut stop/rm/up
- Contexte de build : ne garder que les fichiers nécessaires dans le répertoire du Dockerfile
- Windows/Mac : Docker s'exécute dans une VM Linux (WSL2 ou VirtualBox)
- Après des changements de variables d'environnement dans docker-compose.yml, une recréation complète est nécessaire

## Voir aussi {#see-also}
- [[kubernetes-for-de]] - orchestration de conteneurs à grande échelle
- [[cloud-data-platforms]] - déploiement cloud
- [[apache-airflow]] - Airflow dans Docker
