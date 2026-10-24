---
title: "Dockerfile et construction d'images"
category: concepts
tags: [devops, docker, dockerfile, multi-stage, image-optimization]
level: 3
source_sha256: 7e91e9ab94b0be1b3e274d748c788cc870e32534edce4299e61f50b3f580ff48
translation: machine
translated_at: '2026-10-24'
---
# Dockerfile et construction d'images {#dockerfile-and-image-building}

Un Dockerfile est un fichier texte contenant des instructions pour construire des images Docker. Chaque instruction crée une couche, mise en cache pour les reconstructions incrémentales. Comprendre le cache des couches est essentiel pour des builds rapides.

## Instructions du Dockerfile {#dockerfile-instructions}

| Instruction | Rôle |
|-------------|------|
| `FROM` | Image de base (première instruction obligatoire) |
| `RUN` | Exécute une commande pendant le build (crée une couche) |
| `COPY` | Copie des fichiers/répertoires du contexte de build vers l'image |
| `ADD` | Similaire à COPY mais prend en charge les URL et extrait automatiquement les archives |
| `CMD` | Commande par défaut au démarrage du conteneur (surchargeable) |
| `ENTRYPOINT` | Commande fixe (CMD devient alors ses arguments) |
| `WORKDIR` | Définit le répertoire de travail pour les instructions suivantes |
| `EXPOSE` | Documente les ports sur lesquels le conteneur écoute |
| `ENV` | Définit une variable d'environnement (disponible à l'exécution) |
| `ARG` | Variable de build (non disponible à l'exécution) |
| `VOLUME` | Déclare un point de montage pour un stockage externe |
| `USER` | Définit l'utilisateur pour les instructions suivantes et à l'exécution |
| `LABEL` | Ajoute des métadonnées (mainteneur, version) |
| `HEALTHCHECK` | Définit la commande de vérification de l'état de santé du conteneur |

## Dockerfile de base {#basic-dockerfile}

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

## CMD ou ENTRYPOINT {#cmd-vs-entrypoint}

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

## Optimisation du cache des couches {#layer-caching-optimization}

Ordonnez les instructions du moins susceptible de changer au plus susceptible de changer :

```dockerfile
FROM node:20-alpine           # rarely changes
WORKDIR /app
COPY package*.json ./          # changes when deps change
RUN npm ci                     # cached if package.json unchanged
COPY . .                       # changes on every code change
CMD ["node", "server.js"]
```

## Builds multi-étapes {#multi-stage-builds}

Séparez les étapes de build et d'exécution pour réduire considérablement la taille de l'image finale :

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

Nommez les étapes avec `AS`. Copiez entre étapes avec `--from=<étape>`. Il est possible d'avoir plusieurs étapes de build.

### Exemple multi-étapes pour Java {#java-multi-stage-example}

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

États possibles : healthy, unhealthy, starting. `--start-period` correspond au délai de grâce avant la première vérification. Combinez avec `--restart=always` et un conteneur autoheal pour la récupération automatique des conteneurs figés.

## Commandes de build {#build-commands}

```bash
docker build -t myapp:v1 .                          # build from current dir
docker build -t myapp:v1 -f custom.Dockerfile .      # custom Dockerfile
docker build --no-cache -t myapp:v1 .                # ignore cache
docker build --build-arg VERSION=3.11 -t myapp:v1 .  # build argument
```

## Publication des images {#publishing-images}

```bash
docker login
docker tag myapp:v1 username/myapp:v1
docker push username/myapp:v1
```

## Alternatives de génération d'images Java {#java-image-generation-alternatives}

| Approche | Avantages | Inconvénients |
|----------|-----------|---------------|
| Dockerfile | Contrôle total | Doit être écrit et maintenu |
| Buildpacks (`mvn spring-boot:build-image`) | Aucune configuration, en couches | Build le plus lent |
| Google Jib (`mvn jib:build`) | Pas de daemon Docker, incréments rapides | Plugin Maven/Gradle uniquement |

## .dockerignore {#dockerignore}

Exclut des fichiers du contexte de build (à l'instar de .gitignore) :
```text
node_modules/
.git/
*.log
.env
```

## Pièges à éviter {#gotchas}

- `--no-cache-dir` avec pip empêche la mise en cache des paquets dans la couche de l'image
- `COPY . .` invalide le cache à CHAQUE modification de fichier : placez-le en dernier
- Les images de base Alpine (~5 Mo) peuvent poser des problèmes de compatibilité avec les extensions C à cause de musl libc
- La directive `VOLUME` crée automatiquement des volumes anonymes difficiles à suivre : privilégiez des montages explicites
- L'option `-e` à l'exécution surcharge le `ENV` du Dockerfile
- Une image construite avec `docker commit` (approche impérative) est plus volumineuse et moins reproductible qu'un build par Dockerfile

## Voir aussi {#see-also}

- [[docker-fundamentals]] - bases des conteneurs, cycle de vie, réseau
- [[docker-compose]] - orchestration multi-conteneurs
- [[container-registries]] - ECR, ACR, Docker Hub, Nexus
- [[cicd-pipelines]] - construction automatisée des images
