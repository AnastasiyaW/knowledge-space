---
title: "Automatisation SRE et réduction du travail répétitif"
category: concepts
tags: [devops, sre, automation, toil, jenkins, ansible, n8n, workflow]
level: 3
source_sha256: edf835d54efb6a62fc2f66ab5560d43356bdcdb76a83a3dd8b2b15b57c1ae16a
translation: machine
translated_at: '2026-10-24'
---
# Automatisation SRE et réduction du travail répétitif {#sre-automation-and-toil-reduction}

Les équipes SRE deviennent des développeurs de plateforme. Principe clé : si un opérateur se connecte en SSH, c'est un bug de la plateforme. L'automatisation réduit le travail répétitif (toil), garantit la cohérence et permet à des collègues moins qualifiés d'opérer des systèmes complexes.

## Caractéristiques du travail répétitif (toil) {#toil-characteristics}

- Manuel, répétitif, automatisable
- Tactique (interrompu par les événements)
- Sans valeur durable
- Croît linéairement avec la croissance du service

Objectif : maintenir le toil en dessous de 50 % du temps de travail. `Toil / Toutes les tâches` = ratio de toil.

## Valeur de l'automatisation {#automation-value}

- **Cohérence** - aucune variation liée à l'erreur humaine
- **Rapidité** - plus rapide que le manuel
- **Plateforme** - fondation réutilisable
- **Auditabilité** - qui, quand, quoi est tracé
- **Documentation-as-code** - l'automatisation EST la documentation

## Outils d'automatisation {#automation-tools}

### Jenkins {#jenkins}

Serveur d'automatisation (PAS la CI elle-même). Exécution via Docker :
```bash
docker run -p 8080:8080 --name=jenkins-master \
  --env JAVA_OPTS="-Xmx1024m" jenkins/jenkins
```

Piloté par API : lister les plugins, vérifier les jobs, créer des répertoires, déclencher des builds via curl.

### Ansible {#ansible}

Gestion de configuration sans agent. Basé sur SSH, playbooks YAML, idempotent.

### n8n (automatisation de workflows) {#n8n-workflow-automation}

Alternative open-source à IFTTT. Analyse JSON, gestion d'API (environ 90 % des usages). Connecte des systèmes déconnectés (Jira + Jenkins + Slack) via des webhooks.

### Serverless (Lambda/GCF/Azure Functions) {#serverless-lambdagcfazure-functions}

Automatisation événementielle sans gestion de serveurs.

## Principes IaC {#iac-principles}

- **Portes de qualité** : analyse de vulnérabilités, durcissement, tests d'infrastructure
- **Pull requests + revue de code** pour les changements d'infrastructure
- **Principe DRY** (Terraform verbeux -> Terragrunt aide)
- **Déclaratif > impératif** : décrire l'état souhaité, l'outil détermine comment y parvenir

## Outils SRE pratiques {#practical-sre-tools}

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

## Tâches planifiées {#scheduled-tasks}

- **cron** - planification standard
- **timers systemd** - Linux moderne
- **Commande `at`** - exécution différée ponctuelle (utile pour les rollbacks automatiques)

## Contrats d'API {#api-contracts}

- Comprendre les schémas d'interaction entre systèmes
- Simuler les interactions, comparer les tests avec les requêtes réelles
- Validation des échanges de données structurées

## Pièges courants {#gotchas}

- Une automatisation que personne ne comprend est pire que les processus manuels
- Commencer par les éléments les plus répétitifs - meilleur retour sur investissement
- Documenter les messages de débogage pour les collègues dans la sortie des automatisations
- `ansible-galaxy install -r requirements.yml` pour vendoriser des rôles
- Verbosité `-v` à `-vvvv` dans Ansible pour le débogage

## Voir aussi {#see-also}

- [[sre-principles]] - philosophie du toil et budgets d'erreur
- [[terraform-iac]] - infrastructure as code
- [[ansible-configuration-management]] - automatisation de la configuration
- [[jenkins-automation]] - automatisation des pipelines
- [[cicd-pipelines]] - livraison automatisée
