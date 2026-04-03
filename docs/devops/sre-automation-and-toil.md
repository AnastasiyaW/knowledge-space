---
title: SRE Automation and Toil Reduction
category: concepts
tags: [devops, sre, automation, toil, jenkins, ansible, n8n, workflow]
---

# SRE Automation and Toil Reduction

SRE teams become platform developers. Key principle: if an operator logs in via SSH, it is a bug in the platform. Automation reduces toil, ensures consistency, and enables less qualified colleagues to operate complex systems.

## Toil Characteristics

- Manual, repetitive, automatable
- Tactical (interrupt-driven)
- No enduring value
- Scales linearly with service growth

Target: keep toil below 50% of work time. `Toil / All tasks` = toil ratio.

## Automation Value

- **Consistency** - no human error variation
- **Speed** - faster than manual
- **Platform** - reusable foundation
- **Auditability** - who, when, what tracked
- **Documentation-as-code** - automation IS the documentation

## Automation Tools

### Jenkins

Automation server (NOT CI itself). Run via Docker:
```bash
docker run -p 8080:8080 --name=jenkins-master \
  --env JAVA_OPTS="-Xmx1024m" jenkins/jenkins
```

API-driven: list plugins, check jobs, create directories, trigger builds via curl.

### Ansible

Agentless configuration management. SSH-based, YAML playbooks, idempotent.

### n8n (Workflow Automation)

Open-source IFTTT alternative. JSON parsing, API handling (~90% of use). Connect disconnected systems (Jira + Jenkins + Slack) via webhooks.

### Serverless (Lambda/GCF/Azure Functions)

Event-driven automation without server management.

## IaC Principles

- **Quality gates**: vulnerability scanning, hardening, infrastructure testing
- **Pull requests + code review** for infrastructure changes
- **DRY principle** (Terraform verbose -> Terragrunt helps)
- **Declarative > Imperative**: describe desired state, tool figures out how

## Practical SRE Tools

```bash
# Quick network check
timeout 1 bash -c 'cat < /dev/null > /dev/tcp/8.8.8.8/443'; echo $?

# SSL cert check
docker run harisekhon/nagios-plugins check_ssl_cert.pl --host "google.com" -c 14 -w 30

# Colorized logs
grc -c grc.conf journalctl -f

# IP extraction
egrep '([0-9]{1,3}\.){3}[0-9]{1,3}' file
```

## Scheduled Tasks

- **cron** - standard scheduling
- **systemd timers** - modern Linux
- **`at` command** - one-time delayed execution (useful for automatic rollbacks)

## API Contracts

- Understand system interaction patterns
- Simulate interactions, compare test with real requests
- Structured data exchange validation

## Gotchas

- Automation that nobody understands is worse than manual processes
- Start with the highest-toil items - biggest ROI
- Document debug messages for colleagues in automation output
- `ansible-galaxy install -r requirements.yml` for vendoring roles
- Verbosity `-v` to `-vvvv` in Ansible for debugging

## See Also

- [[sre-principles]] - toil philosophy and error budgets
- [[terraform-iac]] - infrastructure as code
- [[ansible-configuration-management]] - configuration automation
- [[jenkins-automation]] - pipeline automation
- [[cicd-pipelines]] - automated delivery
