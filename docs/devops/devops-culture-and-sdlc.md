---
title: DevOps Culture and SDLC
category: concepts
tags: [devops, culture, sdlc, agile, automation, collaboration]
---

# DevOps Culture and SDLC

DevOps is a set of practices, tools, and cultural philosophies automating and integrating processes between software development and IT operations. It emphasizes collaboration, shared responsibility, and continuous improvement.

## The Traditional Problem

- Dev teams: focus on features, speed, "throw code over the wall"
- Ops teams: focus on stability, resist changes, manual deployments
- Result: friction, delays, finger-pointing, slower time to market

## DevOps Principles

1. **Collaboration** - shared goals between dev and ops
2. **Automation** - CI/CD pipelines, IaC, automated testing
3. **Continuous improvement** - feedback loops, iterative refinement
4. **Customer focus** - fast delivery of value, rapid response

## SDLC (Software Development Life Cycle)

```
Plan -> Code -> Build -> Test -> Release -> Deploy -> Operate -> Monitor -> (back to Plan)
```

DevOps automates Build through Deploy, monitors Operate, feeds back into planning.

## Tools Landscape

| Category | Tools |
|----------|-------|
| Source Control | Git, GitHub, GitLab, Bitbucket |
| CI/CD | Jenkins, GitLab CI, GitHub Actions, Azure DevOps |
| Containerization | Docker, containerd |
| Orchestration | Kubernetes, Docker Swarm |
| IaC | Terraform, Ansible, CloudFormation, Pulumi |
| Monitoring | Prometheus, Grafana, ELK, Datadog |
| Cloud | AWS, Azure, GCP |
| Artifact Repo | Nexus, JFrog Artifactory, Docker Hub |

## Agile and Scrum

- **Sprints** - 2-week iterations
- **Roles** - Product Owner, Scrum Master, Dev Team
- **Ceremonies** - Sprint Planning, Daily Standup, Review, Retrospective
- **Board** - To Do -> In Progress -> In Review -> Done

## Deployment Stages

| Stage | Purpose | Access |
|-------|---------|--------|
| Development | Local coding, testing | Developers |
| Testing/QA | Integration testing | QA team |
| Staging | Pre-production validation | Internal |
| Production | Live user traffic | Public |

## Semantic Versioning

Format: `MAJOR.MINOR.PATCH` (e.g., 2.1.3)
- MAJOR: breaking changes
- MINOR: new features, backward compatible
- PATCH: bug fixes

## Security Fundamentals

- SSH keys over passwords
- Firewall rules (least privilege)
- Secrets in env vars, not code
- HTTPS/TLS for external communication
- Keep software updated

## See Also

- [[sre-principles]] - reliability engineering extending DevOps
- [[cicd-pipelines]] - automating the pipeline
- [[git-version-control]] - source control foundation
- [[monitoring-and-observability]] - feedback loop
