---
title: "SIEM et réponse aux incidents"
category: techniques
tags: [security, siem, incident-response, soc, soar, monitoring, forensics]
level: 3
source_sha256: 0c37f2c652301a0b202dbac2075e70524d4ecd26a1bd6432cbfa29c233c996ed
translation: machine
translated_at: '2026-10-24'
---
# SIEM et réponse aux incidents {#siem-and-incident-response}

Security Information and Event Management : collecte de journaux, règles de corrélation, réglage des alertes. Cycle de vie de la réponse aux incidents : classification, tri, investigation, confinement, éradication, reprise et revue post-incident. Opérations SOC et automatisation SOAR.

## Points clés {#key-facts}
- Un SIEM combine agrégation de journaux, normalisation, corrélation, alerte et rétention
- Les règles de corrélation relient des événements entre sources et dans le temps pour détecter des schémas d'attaque
- Phases de la réponse aux incidents : Classifier -> Trier -> Investiguer -> Confiner -> Éradiquer -> Reprendre -> Revoir
- Le MTTD (Mean Time to Detect) et le MTTR (Mean Time to Respond) sont des indicateurs clés du SOC
- SOAR automatise les actions de réponse répétitives (bloquer une IP, isoler un hôte, désactiver un compte)
- Priorité d'intégration des sources de journaux : systèmes d'authentification -> pare-feux -> serveurs critiques -> postes de travail -> cloud

## Architecture SIEM {#siem-architecture}
- **Collecte de journaux** - agents, récepteurs syslog, intégrations API
- **Normalisation** - conversion de formats hétérogènes vers un schéma commun
- **Indexation** - recherche rapide parmi des milliards d'événements
- **Corrélation** - liaison d'événements connexes entre sources
- **Alerte** - des règles déclenchent des notifications
- **Tableaux de bord** - visibilité en temps réel
- **Rétention** - stockage à long terme pour l'investigation et la conformité

### Méthodes de collecte de journaux {#log-collection-methods}
- **Basée sur agent** - logiciel installé sur les postes qui transmet les journaux
- **Sans agent** - syslog, WMI, API, interrogation de partages de fichiers
- **Capture réseau** - capture directe du trafic
- **API cloud** - intégrations natives des services (CloudTrail, Azure Activity Log)

### Règles de corrélation {#correlation-rules}
```bash
# Brute force detection
IF count(failed_login) > 5 from same source_ip within 5 minutes
THEN alert "Potential brute force"

# Lateral movement
IF successful_login from IP_A to Host_B
AND Host_B not previously accessed from IP_A
AND Host_B has privileged services
THEN alert "Potential lateral movement"

# Data exfiltration
IF outbound_data_volume > threshold from single host
AND destination not in whitelist
AND time outside business hours
THEN alert "Potential data exfiltration"
```

### Réglage des alertes {#alert-tuning}
- Commencer par les indicateurs de compromission connus (IoC)
- Ajouter des règles comportementales (échecs de connexion, élévation de privilèges)
- Régler pour réduire les faux positifs sans manquer les vrais positifs
- Suppression pour éviter les tempêtes d'alertes dues à des déclenchements répétés
- Enrichissement : ajout d'informations sur les actifs, de renseignements sur la menace, de géolocalisation

## Réponse aux incidents {#incident-response}

### Classification {#classification}
- **Catégorie** : logiciel malveillant, accès non autorisé, DDoS, fuite de données, menace interne, hameçonnage
- **Gravité** : Critique (P1), Élevée (P2), Moyenne (P3), Faible (P4)
- **Périmètre** : hôte unique, segment réseau, environnement complet, orienté client

### Questions de tri {#triage-questions}
1. Vrai positif ou faux positif ?
2. Qu'est-ce qui est affecté ?
3. La menace est-elle active ou historique ?
4. Quel est l'impact métier ?
5. Une escalade est-elle nécessaire ?

### Déroulement de l'investigation {#investigation-workflow}
1. **Délimitation** - déterminer l'étendue de la compromission
2. **Collecte des preuves** - préserver les journaux, les images mémoire et les images disque (maintenir la chaîne de possession)
3. **Construction de la chronologie** - reconstituer les actions de l'attaquant
4. **Analyse des causes profondes** - vecteur d'accès initial
5. **Évaluation de l'impact** - quelles données et quels systèmes ont été affectés

### Confinement {#containment}
- **Court terme** : isoler les systèmes, désactiver les comptes, bloquer les IP et domaines
- **Long terme** : corriger les vulnérabilités, reconstruire si nécessaire
- Équilibre : contenir la menace sans détruire les preuves

### Éradication {#eradication}
- Supprimer les logiciels malveillants, les portes dérobées et les mécanismes de persistance
- Réinitialiser toutes les identifiants potentiellement compromis
- Corriger les vulnérabilités exploitées
- Relancer un scan pour vérifier la suppression

### Reprise {#recovery}
- Restaurer à partir de sauvegardes saines
- Reconstruire les systèmes compromis
- Reconnexion progressive avec une surveillance renforcée
- Vérifier l'intégrité avant le retour en production

### Post-incident {#post-incident}
- Réunion de retour d'expérience
- Documentation complète (chronologie, actions, résultats)
- Améliorations des contrôles pour les lacunes identifiées
- Mise à jour des règles de détection en fonction des constats

## Opérations SOC {#soc-operations}

### Modèle à niveaux {#tier-model}
| Niveau | Rôle | Responsabilités |
|------|------|-----------------|
| L1 | Tri des alertes | Investigation initiale, identification des faux positifs, escalade |
| L2 | Traitement des incidents | Investigation approfondie, analyse forensique, chasse aux menaces |
| L3 | Analyse avancée | Rétro-ingénierie de logiciels malveillants, développement d'outils, amélioration des processus |

### Indicateurs SOC {#soc-metrics}
- **MTTD** - délai entre l'attaque et la détection
- **MTTR** - délai entre la détection et le confinement
- **Dwell time** - durée de présence de l'attaquant
- **Taux de faux positifs** - bruit par rapport aux alertes réelles
- **Couverture** - pourcentage d'actifs surveillés

## SOAR (Security Orchestration, Automation and Response) {#soar-security-orchestration-automation-and-response}

### Automatisations de playbooks {#playbook-automations}
- **Hameçonnage** : extraire les IoC -> vérifier les renseignements sur la menace -> bloquer l'expéditeur -> mettre en quarantaine les courriels similaires
- **Logiciel malveillant** : isoler l'hôte -> collecter les preuves -> rechercher des mouvements latéraux
- **Compromission de compte** : forcer la réinitialisation du mot de passe -> désactiver le compte -> vérifier les accès aux données
- **Alerte de vulnérabilité** : vérifier les actifs touchés -> déterminer l'exposition -> créer un ticket

Avantages : réponse cohérente, plus rapide (minutes au lieu d'heures), extensible, piste d'audit complète.

## Sources de journaux critiques {#critical-log-sources}
- **Authentification** : AD, VPN, SSO
- **Réseau** : pare-feux, IDS/IPS, proxy
- **DNS** : révèle les communications C2, l'exfiltration de données
- **Postes de travail** : journal d'événements Windows, syslog, télémétrie EDR
- **Courriel** : distribution, quarantaine, détections d'hameçonnage
- **Cloud** : CloudTrail, Azure Activity Log, GCP Audit Log
- **Base de données** : journaux d'audit (requêtes, modifications de schéma)

## Pièges à éviter {#gotchas}
- Un SIEM ne vaut que par ses sources de journaux - les angles morts non couverts sont les endroits où les attaquants se cachent
- Les règles de corrélation exigent un réglage continu - les évolutions de l'environnement rendent les anciennes règles bruyantes ou aveugles
- La préservation des preuves doit intervenir avant le confinement - isoler un système peut détruire des données volatiles
- La documentation de l'incident doit être rédigée en temps réel, et non après coup (la mémoire se dégrade sous pression)
- Les playbooks SOAR doivent être testés régulièrement - une réponse automatisée non testée peut causer plus de dégâts que l'incident

## Voir aussi {#see-also}
- [[security-solutions-architecture]] - mise en œuvre IDS/IPS, EDR, DLP
- [[windows-security-and-powershell]] - identifiants d'événements Windows pour les règles SIEM
- [[linux-system-hardening]] - auditd, configuration syslog
- [[compliance-and-regulations]] - exigences de surveillance liées à la conformité
