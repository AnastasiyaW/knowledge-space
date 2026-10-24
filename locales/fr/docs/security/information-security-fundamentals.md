---
title: "Principes fondamentaux de la sécurité de l'information"
category: concepts
tags: [security, cia-triad, risk, threat-modeling, defense-in-depth]
level: 2
source_sha256: 04613f51d205263c6e9580cab9c69454d5ec7cd906b8bfafa8bdc4f37a926f6a
translation: machine
translated_at: '2026-10-24'
---
# Principes fondamentaux de la sécurité de l'information {#information-security-fundamentals}

Concepts fondamentaux de la sécurité de l'information : la triade CIA, la modélisation des menaces, la gestion des risques et les modèles d'architecture de sécurité. Cette entrée fournit le socle conceptuel sur lequel reposent tous les autres sujets de sécurité.

## Points clés {#key-facts}
- **Triade CIA** - Confidentialité (données accessibles aux seules personnes autorisées), Intégrité (données exactes et non altérées), Disponibilité (systèmes accessibles lorsque nécessaire)
- La priorisation dépend du contexte : banque = intégrité d'abord, militaire = confidentialité d'abord, e-commerce = disponibilité d'abord, santé = les trois à égalité
- Risque = Menace x Vulnérabilité x Impact : une vulnérabilité sans menace n'est pas un risque
- Défense en profondeur : aucune couche unique n'est suffisante ; chaque couche doit être indépendante
- Zero Trust : « ne jamais faire confiance, toujours vérifier » - y compris pour le trafic interne

## La triade CIA {#the-cia-triad}

### Confidentialité {#confidentiality}
Menaces : fuites de données, écoute clandestine, ingénierie sociale.
Contrôles : chiffrement, contrôles d'accès, classification des données.

### Intégrité {#integrity}
Menaces : modification non autorisée, attaque de type man-in-the-middle, corruption de données.
Contrôles : hachage, signatures numériques, gestion de versions, sommes de contrôle.

### Disponibilité {#availability}
Menaces : DDoS, défaillance matérielle, rançongiciels.
Contrôles : redondance, sauvegardes, répartition de charge, reprise après sinistre.

## Modèles {#patterns}

### Défense en profondeur {#defense-in-depth}
Plusieurs couches indépendantes de contrôles de sécurité :
1. Sécurité physique (serrures, caméras)
2. Sécurité réseau (pare-feu, IDS/IPS)
3. Sécurité des hôtes (antivirus, EDR, durcissement)
4. Sécurité applicative (WAF, validation des entrées)
5. Sécurité des données (chiffrement, DLP, contrôles d'accès)
6. Contrôles administratifs (politiques, formation)

### Architecture Zero Trust {#zero-trust-architecture}
- Micro-segmentation du réseau
- Accès selon le principe du moindre privilège pour chaque identité
- Vérification continue de chaque requête
- Considérer une compromission comme acquise en permanence
- Chiffrer toutes les communications, y compris internes

### Zones de sécurité (DMZ) {#security-zones-dmz}
- **Internet** - non fiable
- **DMZ** - semi-fiable, héberge les services exposés publiquement
- **Réseau interne** - fiable, systèmes métier
- **Réseau d'administration** - fortement restreint, gestion de l'infrastructure
- Pare-feu entre chaque zone, avec des jeux de règles stricts

## Actifs et menaces {#assets-and-threats}

### Catégories d'actifs {#asset-categories}
- **Information** - bases de données, propriété intellectuelle, données clients
- **Physique** - serveurs, équipements réseau, installations
- **Logiciel** - applications, systèmes d'exploitation, outils
- **Humain** - employés, prestataires, savoir-faire
- **Immatériel** - réputation, image de marque, confiance

### Acteurs de la menace {#threat-actors}
| Acteur | Motivation | Niveau de compétence |
|-------|-----------|-------------|
| Script kiddies | Curiosité, notoriété | Faible (utilisent des outils existants) |
| Hacktivistes | Idéologique (ex. Anonymous) | Faible à moyen |
| Cybercriminels | Financière (rançongiciels, carding) | Moyen à élevé |
| Initiés | Rancune, financière, contrainte | Variable (disposent d'un accès légitime) |
| États | Espionnage, sabotage (APT28, Lazarus) | Très élevé |
| Concurrents | Espionnage industriel | Moyen |

## Gestion des risques {#risk-management}

### Évaluation qualitative {#qualitative-assessment}
Utilise des échelles descriptives (élevé/moyen/faible). Matrice des risques 5x5 : probabilité (1-5) x impact (1-5). Scores 1-5 = faible (accepter), 6-12 = moyen (atténuer/transférer), 13-25 = critique (atténuer immédiatement).

### Évaluation quantitative {#quantitative-assessment}
- Valeur de l'actif (AV) - valeur monétaire
- Facteur d'exposition (EF) - pourcentage de perte (0-1)
- Perte unique attendue (SLE) = AV x EF
- Taux annuel d'occurrence (ARO) - incidents attendus par an
- Perte annuelle attendue (ALE) = SLE x ARO

### Options de traitement des risques {#risk-treatment-options}
1. **Accepter** - risque dans l'appétence au risque, coût du contrôle supérieur à la perte potentielle
2. **Atténuer** - mettre en œuvre des contrôles pour réduire la probabilité ou l'impact
3. **Transférer** - reporter sur un tiers (assurance, externalisation)
4. **Éviter** - supprimer l'activité à l'origine du risque

## Gestion des vulnérabilités {#vulnerability-management}

### CVE / CVSS / NVD {#cve-cvss-nvd}
- **CVE** - identifiant unique (CVE-ANNÉE-NUMÉRO)
- **CVSS** - score de gravité de 0 à 10 (de base + temporel + environnemental)
- **NVD** - base de données CVE maintenue par le NIST, avec scores CVSS

### Cycle de vie de la gestion des correctifs {#patch-management-lifecycle}
1. Découverte (analyse à la recherche de correctifs manquants)
2. Évaluation (étude de l'applicabilité et du risque)
3. Tests (environnement de préproduction)
4. Déploiement (mise en production progressive)
5. Vérification (confirmation de l'application des correctifs)
6. Documentation (piste d'audit)

## Pièges à éviter {#gotchas}
- Le score de base CVSS seul est trompeur : prenez toujours en compte le contexte environnemental de votre organisation
- Une acceptation de risque doit être documentée avec la validation du propriétaire métier, et non uniquement décidée par l'équipe sécurité
- « Conformité != sécurité » : réussir un audit ne signifie pas que vous êtes sécurisé
- Les couches de défense en profondeur doivent être réellement indépendantes : des identifiants partagés entre couches annulent l'intérêt de l'approche

## Voir aussi {#see-also}
- [[cryptography-and-pki]] - chiffrement, hachage, signatures numériques
- [[authentication-and-authorization]] - MFA, OAuth, Kerberos
- [[compliance-and-regulations]] - RGPD, PCI DSS, ISO 27001
- [[vulnerability-scanning-and-management]] - Nessus, OpenVAS, analyse de vulnérabilités
