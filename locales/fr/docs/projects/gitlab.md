---
title: "Gitlab : gitlab-critical-vulnerability-patch-19-5-1 — Gitlab Critical Vulnerability Patch 19 5 1"
category: "projects"
date: 2026-10-22
tags: ["gitlab", "gitlab-critical-vulnerability-patch-19-5-1", "project"]
aliases: ["Gitlab: gitlab-critical-vulnerability-patch-19-5-1"]
level: 2
source_sha256: 8adfa4680d5bd54ed043af0cd330c8563fd90e5d706bcac91ee4e134c533841e
translation: machine
translated_at: '2026-10-24'
---
# Gitlab: gitlab-critical-vulnerability-patch-19-5-1 — Gitlab Critical Vulnerability Patch 19 5 1 {#gitlab-gitlab-critical-vulnerability-patch-19-5-1-gitlab-critical-vulnerability-patch-19-5-1}

**Ligne de développement :** project:gitlab · thread gitlab-critical-vulnerability-patch-19-5-1  
**Dernier événement :** 2026-10-22 · 2 datés depuis le 2026-10-22 · **Recherche :** 2026-10-23 · confiance : élevée

## Ce que c'est {#what-it-is}

GitLab 19.5.1 est une version de sécurité d'urgence pour GitLab auto-hébergé, la plateforme de collaboration sur le code et de DevOps. Elle corrige une faille d'exécution de code à distance non authentifiée dans le compilateur d'expressions régulières et rétablit la sécurité de la mémoire sur les déploiements auto-hébergés. Les correctifs sont rétroportés vers les anciennes branches de version, et les workflows Git principaux ne changent pas.

Il n'existe aucune solution de contournement par la configuration ; la seule correction consiste donc à mettre à jour le binaire ou le paquet immédiatement. Une fois la mise à jour effectuée, le risque de prise de contrôle du serveur disparaît, et les dépôts existants ainsi que les pipelines CI restent inchangés.

## Ligne de développement {#development-line}

- **2026-10-22 — GitLab corrige une faille d'exécution de code à distance de gravité maximale.** La vulnérabilité a obtenu un score de 10/10 et permettait à n'importe qui d'exécuter du code arbitraire sur le serveur sans se connecter. Elle touche les versions à partir de la 7.0. GitLab.com était déjà corrigé, et les utilisateurs auto-hébergés ont été invités à mettre à jour immédiatement avec la version de correctif GitLab 19.5.1.
- **2026-10-22 — GitLab corrige une faille critique d'exécution de code non authentifiée.** Classée 10/10 en gravité, elle permettait d'exécuter du code arbitraire sur le serveur sans connexion, dans les versions à partir de la 7.0. L'instance GitLab.com hébergée dans le cloud était déjà corrigée. Les utilisateurs auto-hébergés ont été invités à mettre à jour immédiatement avec la version de correctif 19.5.1.
- **2026-10-22 — autres détails de la même date.**
  - La faille est CVE-2026-110264, CVSS 10.0. Elle provient d'un dépassement d'entier (integer overflow) dans le compilateur d'expressions régulières (Onigmo) et a été signalée par le chercheur joaxcar via HackerOne. Les versions rétroportées sont 19.4.3, 19.3.6, 19.2.9, 19.1.9, 19.0.10 et 18.11.13, couvrant les branches plus anciennes jusqu'à la version 7.0. (2026-10-22) — <https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/>
  - Le code s'exécute sous l'utilisateur git et ne nécessite aucun privilège. Le déclencheur est une expression forgée dans un chemin de rendu de documents, comme Org-mode. Il n'existe aucune solution de contournement par la configuration ; seule une mise à jour permet de se protéger. (2026-10-22) — <https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/>

## Ce qui a changé {#what-changed}

GitLab a publié des correctifs d'urgence sur les branches de version actives et anciennes pour corriger un dépassement d'entier dans le compilateur d'expressions régulières. Le flux de développement principal a reçu la mise à jour de sécurité, et les rétroportages atteignent les arborescences de maintenance héritées jusqu'à la première version affectée. Des règles de tests automatisés et des signatures de détection d'erreurs ont également été publiées, afin que les administrateurs puissent surveiller les processus workers pour détecter les tentatives d'exploitation.

## Comment l'utiliser {#how-to-use-this}

1. Repérez la version de votre instance GitLab auto-hébergée dans le tableau de bord d'administration, ou exécutez gitlab-rake gitlab:env:info sur l'hôte.
  — <https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/>
2. Choisissez le correctif correspondant à votre ligne de version : 19.5.x vers 19.5.1, 19.4.x vers 19.4.3, 19.3.x vers 19.3.6, 19.2.x vers 19.2.9, 19.1.x vers 19.1.9, 19.0.x vers 19.0.10, et les versions anciennes de 7.0 à 18.11.x vers 18.11.13.
  — <https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/>
3. Lancez la mise à jour du gestionnaire de paquets ou récupérez l'image de conteneur, puis redémarrez les services GitLab pour que les nouveaux binaires prennent effet.
  — <https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/>
4. Vérifiez les journaux des workers Puma et les journaux d'erreurs applicatives pour détecter les erreurs du compilateur d'expressions régulières ou les arrêts anormaux de workers. Ceux-ci indiquent d'éventuelles tentatives d'exploitation passées.
  — <https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/>

## Bonnes pratiques {#best-practices}

- Appliquez les correctifs sans délai sur les instances auto-hébergées exposées à Internet, car l'attaque ne nécessite ni identifiants ni interaction de l'utilisateur.
  — <https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/>
- Passez directement à la version de correctif au sein de votre branche mineure actuelle, afin d'éviter les migrations de base de données inutiles et de limiter la durée d'indisponibilité.
  — <https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/>
- Ne vous fiez pas uniquement aux règles de pare-feu périmétriques ni aux solutions de contournement par la configuration, car des expressions régulières malveillantes peuvent arriver par de nombreux chemins de rendu de documents.
  — <https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/>

## Remplacé par ceci {#superseded-by-this}

- Les instances GitLab auto-hébergées non corrigées, en versions 7.0 à 19.5.0, sont protégées contre l'exécution de code à distance non authentifiée.
  — <https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/>

## Toujours inconnu {#still-unknown}

- La couverture médiatique secondaire et les discussions communautaires ne sont pas citées. Leurs liens de recherche ont redirigé vers des cibles peu claires, et des URL directes stables n'ont pas pu être confirmées.

## Sources {#sources}

| source | title | read |
|---|---|---|
| https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/ | GitLab Critical Security Release: Patch Release 19.5.1 | 2026-10-23 |

## Brief agent {#agent-brief}

- **Sujet :** project:gitlab, thread gitlab-critical-vulnerability-patch-19-5-1, 2 événements datés du 2026-10-22 au 2026-10-22.
- **Note pratique :** Voir les sections d'usage et de pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** élevée. Les remplacements datés ci-dessus font autorité pour ce qui est obsolète.
