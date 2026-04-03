---
title: Docker for Machine Learning
category: patterns
tags: [devops, docker, machine-learning, mlflow, jupyter, mlops]
---

# Docker for Machine Learning

Docker standardizes ML workflows by eliminating "works on my machine" problems across data collection, experimentation, training, evaluation, deployment, and monitoring stages.

## Key Benefits for ML

- Reproducible experiments with pinned dependency versions
- Consistent environments across dev/staging/production
- Team onboarding - new engineers get identical setup instantly
- Model serving in production with isolated dependencies
- GPU access via NVIDIA Container Toolkit

## ML Development Environment

### JupyterLab with Persistent Notebooks

```bash
docker run -d -p 8888:8888 \
  -v $(pwd)/notebooks:/home/jovyan/work \
  jupyter/scipy-notebook
```

Volume mount ensures notebooks persist beyond container lifecycle.

### MLflow Experiment Tracking

```bash
docker run -d -p 5555:5000 \
  ghcr.io/mlflow/mlflow:latest mlflow server --host 0.0.0.0
```

### Connecting JupyterLab to MLflow

Both run as separate containers. Connect via host networking or Docker network. JupyterLab notebooks train models and log metrics/parameters/artifacts to MLflow.

## Containerizing ML Applications

### Dockerfile for ML App

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 7860
CMD ["python", "app.py"]
```

### ML Stack with Docker Compose

```yaml
services:
  mlflow:
    image: ghcr.io/mlflow/mlflow:latest
    ports: ["5555:5000"]
    command: mlflow server --host 0.0.0.0

  api:
    build: ./src/api
    ports: ["8000:8000"]
    depends_on: [mlflow]

  streamlit:
    build: ./src/streamlit
    ports: ["8501:8501"]
    environment:
      - API_URL=http://api:8000
    depends_on: [api]
```

### ML Pipeline Workflow

1. Raw data -> preprocessing -> clean data
2. Feature engineering -> selected features
3. Model training -> model.pkl + encoders
4. Package model in FastAPI wrapper -> Docker image
5. Package Streamlit frontend -> Docker image
6. Compose all services together

## Docker Model Runner (Local LLM)

Apple Silicon only (M1-M4), Docker Desktop 4.40+.

```bash
docker model list           # list downloaded models
docker model pull <model>   # download from Docker Hub AI models
docker model run <model>    # run inference
```

Integration endpoints:
- From containers: `http://modelrunner.docker.internal/v1`
- From host: `http://localhost:<port>/v1`
- **OpenAI-compatible API** - same connection string works for both

## Docker MCP Toolkit (AI Agents)

MCP (Model Context Protocol) connects LLMs to external tools (filesystem, GitHub, databases) through standardized interfaces.

```json
{
  "mcpServers": {
    "github": {
      "image": "docker.io/mcp/github",
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "<token>" }
    }
  }
}
```

## Deployment Targets

- **Docker Hub** - public registry, free for public images
- **Hugging Face Spaces** - push Dockerfile + code, auto-builds and deploys
- **AWS App Runner** - ECR image -> managed deployment with auto-scaling

## Gotchas

- Alpine base images are smaller but may lack compilation tools needed for ML libraries (numpy, scipy, torch)
- Volume mounts are critical - without them, trained models and notebooks are lost on container removal
- GPU access requires NVIDIA Container Toolkit and `--gpus` flag
- ML images are often large (2-10GB) - multi-stage builds and `.dockerignore` help reduce size
- `--no-cache-dir` flag on pip prevents caching packages inside image layers

## See Also

- [[docker-compose]] - multi-container orchestration for ML stacks
- [[dockerfile-and-image-building]] - image optimization techniques
- [[container-registries]] - ECR, ACR, Docker Hub for ML images
- [[monitoring-and-observability]] - monitoring ML services in production
