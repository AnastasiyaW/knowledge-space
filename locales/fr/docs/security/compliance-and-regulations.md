---
title: "Conformité et réglementations"
category: concepts
tags: [security, compliance, gdpr, pci-dss, iso-27001, nist, audit]
level: 2
source_sha256: f14b8af06066ad54b15ae611151bce7f6683ffdfaa7834f5a7792c9b08cd130b
translation: machine
translated_at: '2026-10-24'
---
# Conformité et réglementations {#compliance-and-regulations}

Cadres réglementaires et exigences de conformité : ISO 27001, NIST Cybersecurity Framework, PCI DSS, RGPD, hiérarchie des politiques, évaluation des risques pour la conformité, collecte des preuves et préparation d'audit.

## Faits clés {#key-facts}
- Conformité != sécurité : réussir un audit ne signifie pas que vous êtes sécurisé
- Amendes RGPD : jusqu'à 4 % du chiffre d'affaires annuel mondial ou 20 M EUR (le montant le plus élevé étant retenu)
- Le RGPD impose une notification de violation de données à l'autorité de contrôle dans un délai de 72 heures
- PCI DSS impose des analyses de vulnérabilités trimestrielles et des tests d'intrusion annuels
- ISO 27001 repose sur le cycle Plan-Do-Check-Act et comprend 114 mesures réparties en 14 domaines
- NIST CSF : cinq fonctions : Identify, Protect, Detect, Respond, Recover

## Normes internationales {#international-standards}

### ISO 27001 (SMSI) {#iso-27001-isms}
Système de management de la sécurité de l'information :
- Cycle d'amélioration continue Plan-Do-Check-Act
- Annexe A : 114 mesures réparties en 14 domaines
- Approche fondée sur les risques : les mesures sont sélectionnées à partir de l'évaluation
- La certification exige un audit externe
- Reconnue mondialement

### NIST Cybersecurity Framework {#nist-cybersecurity-framework}
Cinq fonctions : **Identify** -> **Protect** -> **Detect** -> **Respond** -> **Recover**
- Niveaux : Partiel (1), Informé des risques (2), Reproductible (3), Adaptatif (4)
- Profils de mise en œuvre : état actuel par rapport à l'état cible
- Volontaire, mais largement adopté

### NIST 800-53 {#nist-800-53}
Catalogue complet de mesures de sécurité :
- 20 familles de mesures (AC, AU, CM, IA, IR, SC, SI, etc.)
- Mesures associées à des niveaux d'impact (faible, modéré, élevé)
- Socle de FedRAMP et de la conformité FISMA

### PCI DSS {#pci-dss}
Norme de sécurité des données de l'industrie des cartes de paiement :
- 12 exigences pour le traitement des données de titulaires de cartes
- Segmentation réseau, chiffrement, contrôle d'accès, supervision
- Analyses de vulnérabilités trimestrielles (ASV)
- Tests d'intrusion annuels
- Niveaux de conformité déterminés par le volume de transactions
- SAQ pour les petits commerçants, ROC pour les grands

### RGPD {#gdpr}
Protection des données de l'UE, à portée extraterritoriale :
- **Base légale** : consentement, contrat, obligation légale, intérêt vital, intérêt public, intérêt légitime
- **Droits des personnes concernées** : accès, rectification, effacement (droit à l'oubli), portabilité, opposition
- **DPO** requis pour les traitements à grande échelle
- **Notification de violation sous 72 heures**
- **Privacy by Design** : la sécurité intégrée dès la conception
- **Minimisation des données** : ne collecter que le nécessaire

## Hiérarchie des politiques {#policy-hierarchy}
1. **Politique de sécurité** : objectifs de haut niveau et engagement de la direction
2. **Standards** : exigences obligatoires (standards de chiffrement, standards de mots de passe)
3. **Procédures** : instructions de mise en œuvre pas à pas
4. **Lignes directrices** : recommandations et bonnes pratiques (facultatives)

## Évaluation des risques pour la conformité {#risk-assessment-for-compliance}
1. Inventaire des actifs : ce qui doit être protégé
2. Identification des menaces
3. Identification des vulnérabilités
4. Évaluation de l'impact
5. Évaluation de la probabilité
6. Mise en correspondance du traitement des risques avec les exigences de conformité :
   - La réglementation exige le chiffrement -> mettre en œuvre AES-256 au repos
   - La réglementation exige la journalisation -> déployer un système de piste d'audit
   - La réglementation exige la détection des violations -> mettre en place un SIEM avec alertes

## Collecte des preuves {#evidence-collection}
| Type de preuve | Exemples |
|----------------|----------|
| Configuration | Captures d'écran et exports des paramètres système |
| Rapports d'analyse | Analyses de vulnérabilités, résultats de tests d'intrusion |
| Échantillons de journaux | Démonstration de la capacité de supervision |
| Documents de politique | Versions approuvées et à jour |
| Registres de formation | Suivi de la sensibilisation des collaborateurs |
| Rapports d'incident | Démonstration de la capacité de réponse |
| Gestion des changements | Enregistrements des modifications contrôlées |

## Préparation d'audit {#audit-preparation}

### Audit interne {#internal-audit}
- Auto-évaluation régulière par rapport aux référentiels
- Analyse des écarts : état actuel par rapport à l'état requis
- Planification des actions correctives avec responsables et échéances
- Tenue continue du référentiel de preuves

### Audit externe {#external-audit}
- Évaluation de l'état de préparation avant audit
- Organisation des documents et des preuves
- Préparation des personnes clés pour les entretiens
- Compréhension de la méthodologie d'échantillonnage
- Planification des actions correctives pour les constats

### Gravité des constats {#finding-severity}
| Niveau | Signification |
|--------|---------------|
| Non-conformité majeure | Défaillance significative d'une mesure, bloque la certification |
| Non-conformité mineure | La mesure existe mais présente des lacunes |
| Observation | Point d'amélioration, pas une défaillance |
| Opportunité d'amélioration | Suggestion, pas un constat |

## Pièges à éviter {#gotchas}
- Les référentiels de conformité se recoupent largement : cartographier les mesures une seule fois, puis les appliquer à plusieurs normes
- La « conformité case à cocher » crée un faux sentiment de sécurité : la conformité est un minimum, pas un plafond
- Le « droit à l'oubli » du RGPD entre en conflit avec la conservation des sauvegardes : disposer d'une procédure documentée
- La réduction du périmètre PCI DSS par la segmentation réseau permet d'économiser un effort de conformité considérable
- Les preuves d'audit doivent être contemporaines (de la période auditée), et non préparées après coup
- La conformité des tiers et prestataires (rapports SOC 2) ne signifie pas que votre utilisation de leur service est conforme

## Voir aussi {#see-also}
- [[information-security-fundamentals]] - notions de gestion des risques
- [[siem-and-incident-response]] - supervision dictée par la conformité
- [[security-solutions-architecture]] - mise en œuvre des mesures
- [Sécurité des bases de données](database-security.md) - exigences de protection des données
