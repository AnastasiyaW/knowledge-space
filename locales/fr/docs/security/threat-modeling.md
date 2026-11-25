---
title: "Modélisation des menaces"
category: concepts
tags: [security, threat-modeling, risk-assessment, information-security, compliance]
level: 3
source_sha256: 9758fbc8a05793b7a6fe6f4ef43ad2f0a3cc80aabce3364df2e5c6ef867bcb69
translation: machine
translated_at: '2026-10-24'
---
# Modélisation des menaces {#threat-modeling}

Processus systématique d'identification, d'évaluation et de documentation des menaces potentielles pesant sur les actifs informationnels d'une organisation. Il produit des documents formels de modélisation des menaces qui orientent les contrôles de sécurité, les décisions d'architecture et la conformité.

## Points clés {#key-facts}
- Le modèle de menaces général couvre l'ensemble de l'infrastructure de l'organisation ; les modèles privés couvrent des systèmes spécifiques
- Commencer par le modèle général, puis dériver des modèles privés pour les ressources informationnelles individuelles
- Les bases de données de menaces (registres nationaux de vulnérabilités) fournissent des catalogues de menaces standardisés
- Un modèle de menaces est un document vivant : il doit être mis à jour lorsque l'infrastructure, les actifs ou le paysage des menaces évoluent
- La plupart des référentiels de sécurité et de conformité exigent des modèles de menaces (ISO 27001, NIST, réglementations locales)

## Modèles de menaces généraux et privés {#general-vs-private-threat-models}

### Modèle de menaces général {#general-threat-model}

Couvre l'ensemble de l'infrastructure informationnelle de l'organisation : tous les systèmes, réseaux et actifs de données pris collectivement.

**Objectif** : établir une base de référence des menaces applicables à l'ensemble de l'organisation. Les modèles privés en sont ensuite dérivés.

**Processus de développement** :

1. **Inventorier les actifs informationnels** : identifier toutes les ressources informationnelles (systèmes RH, contrôle de production, bases de données clients, réseaux internes)
2. **Consulter les bases de données de menaces** : utiliser les bases nationales et internationales de vulnérabilités pour disposer de catalogues de menaces standardisés
3. **Si un registre de menaces existant est disponible** : l'utiliser comme fondation, car il filtre déjà les menaces pertinentes pour l'organisation
4. **Associer les menaces aux actifs** : déterminer quelles menaces s'appliquent à quelles catégories de systèmes
5. **Évaluer la probabilité et l'impact** : classer les menaces selon leur probabilité et leurs dommages potentiels
6. **Documenter les contre-mesures** : contrôles de sécurité existants et planifiés pour chaque menace

### Modèle de menaces privé {#private-threat-model}

Couvre une ressource informationnelle spécifique ou un groupe de ressources identiques.

**Exemples** :
- Système de traitement des données personnelles des employés
- Système de traitement des données personnelles des clients
- Système de contrôle industriel (SCADA/ICS) pour une ligne de production
- Groupe de systèmes identiques répartis sur plusieurs sites (même fournisseur, mêmes composants)

**Dérivation à partir du modèle général** :

1. Partir du modèle de menaces général
2. Filtrer les menaces pour ne retenir que celles pertinentes pour le système spécifique
3. Ajouter les menaces propres au système qui ne sont pas couvertes par le modèle général
4. Détailler les vecteurs d'attaque spécifiques à l'architecture du système
5. Associer les contrôles de sécurité propres au système
6. Documenter les risques résiduels une fois les contrôles appliqués

## Structure du modèle de menaces {#threat-model-structure}

### Sections minimales du document {#minimal-document-sections}

```bash
1. Scope and boundaries
   - What is covered (systems, networks, data flows)
   - What is explicitly excluded

2. Asset inventory
   - Information assets and their classification
   - Processing systems and their locations
   - Data flows between systems

3. Threat catalog
   - Threat ID, description, source
   - Applicable assets
   - Likelihood rating (1-5)
   - Impact rating (1-5)

4. Vulnerability assessment
   - Known vulnerabilities per asset
   - Exploitation difficulty

5. Existing countermeasures
   - Controls already in place
   - Effectiveness assessment

6. Residual risk
   - Threats not fully mitigated
   - Accepted risk vs planned remediation

7. Recommendations
   - Prioritized list of additional controls
```

## Référentiels courants {#common-frameworks}

| Référentiel | Axe | Usage privilégié |
|-------------|-----|------------------|
| **STRIDE** | Spoofing (usurpation), Tampering (altération), Repudiation (répudiation), Info Disclosure (divulgation d'informations), DoS (déni de service), Elevation (élévation de privilèges) | Modélisation des menaces logicielles et applicatives |
| **PASTA** | Process for Attack Simulation and Threat Analysis | Approche centrée sur le risque, alignée sur le métier |
| **OCTAVE** | Operationally Critical Threat, Asset, and Vulnerability Evaluation | Évaluation des risques à l'échelle de l'organisation |
| **DREAD** | Damage, Reproducibility, Exploitability, Affected users, Discoverability | Notation et priorisation des menaces |

### STRIDE par élément {#stride-per-element}

Appliquer les catégories STRIDE à chaque composant d'un diagramme de flux de données :

| Composant | Menaces STRIDE pertinentes |
|-----------|----------------------------|
| Entité externe | Spoofing (usurpation) |
| Processus | Les six catégories |
| Magasin de données | Tampering (altération), Information Disclosure (divulgation d'informations), Denial of Service (déni de service) |
| Flux de données | Tampering (altération), Information Disclosure (divulgation d'informations), Denial of Service (déni de service) |
| Frontière de confiance | Toutes les menaces au franchissement de la frontière |

## Démarche pratique {#practical-workflow}

```php
1. Define scope -> 2. Build DFD -> 3. Identify threats (STRIDE/catalog)
    -> 4. Rate risk (likelihood x impact) -> 5. Plan mitigations
    -> 6. Document -> 7. Review periodically
```

### Diagramme de flux de données (DFD) {#data-flow-diagram-dfd}

Fondement de la modélisation des menaces, il montre comment les données circulent dans le système :

```php
[User] --HTTPS--> [Web Server] --SQL--> [Database]
                       |
                  [Auth Service] --LDAP--> [Active Directory]
```

Marquer les frontières de confiance (lignes en pointillés) à chaque changement de niveau de privilège. Les menaces se concentrent aux franchissements de frontières de confiance.

## Pièges à éviter {#gotchas}
- **Modèle général en premier** : passer directement aux modèles privés sans modèle général crée des angles morts, car les menaces transverses à l'organisation passent inaperçues lorsque chaque équipe ne considère que son propre système
- **Modèle de menaces != analyse de vulnérabilités** : la modélisation des menaces est stratégique (ce qui POURRAIT se produire), l'analyse de vulnérabilités est tactique (ce qui EST exploitable maintenant). Les deux sont nécessaires, aucune ne remplace l'autre
- **Les modèles de menaces obsolètes sont dangereux** : un modèle vieux de deux ans peut ignorer une migration vers le cloud, de nouveaux modes de travail à distance ou des techniques d'attaque émergentes. Le revoir au minimum annuellement et après toute modification majeure de l'infrastructure
- **Systèmes identiques sur plusieurs sites** : lorsque plusieurs sites exploitent le même système (même fournisseur, même configuration), un seul modèle de menaces privé peut couvrir toutes les instances, sans duplication inutile

## Voir aussi {#see-also}
- [[information-security-fundamentals]] - concepts fondamentaux de sécurité
- [[compliance-and-regulations]] - cadres réglementaires exigeant des modèles de menaces
- [[vulnerability-scanning-and-management]] - complément tactique de la modélisation stratégique des menaces
- [[security-solutions-architecture]] - mise en œuvre des contrôles identifiés par les modèles de menaces
