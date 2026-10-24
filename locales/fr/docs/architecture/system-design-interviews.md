---
title: "Entretiens de conception système et pratique"
category: reference
tags: [system-design, interview, estimation, architecture, practice]
level: 3
source_sha256: b3d3998010e117811c907decc11f9a9c60e4ac08d9300c417835e3af506c49d5
translation: machine
translated_at: '2026-10-24'
---
# Entretiens de conception système et pratique {#system-design-interviews-and-practice}

Approche structurée pour les problèmes de conception système, qu'il s'agisse d'entretiens ou de travail d'architecture réel. La même méthodologie s'applique aux deux.

## Processus en 7 étapes {#7-step-process}

1. **Clarifier les exigences** - poser des questions, ne pas faire d'hypothèses
2. **Définir le périmètre et les limites** - ce qui est inclus, ce qui est exclu
3. **Identifier les entités clés et leurs relations** - modèle de données
4. **Concevoir l'architecture de haut niveau** - composants et interactions
5. **Approfondir les composants critiques** - les parties les plus difficiles
6. **Traiter les préoccupations transversales** - sécurité, supervision, tolérance aux pannes
7. **Discuter des compromis et des alternatives** - toujours expliquer POURQUOI

## Erreurs courantes {#common-mistakes}

- Passer directement à la solution sans avoir compris les exigences
- Ignorer les exigences non fonctionnelles
- Ne pas considérer les scénarios de défaillance
- Sur-concevoir pour une échelle peu probable
- Ne présenter qu'une seule option, sans alternatives
- Omettre les calculs d'exigences non fonctionnelles (aucun chiffre pour la charge, le stockage, la latence)
- Ne pas expliquer POURQUOI une technologie a été choisie

## Tableaux d'estimation des exigences non fonctionnelles {#nfr-estimation-tables}

Pour chaque système, établir des projections sur les années 1 à 5 :
- DAU, pic d'utilisateurs simultanés
- Requêtes par seconde (RPS)
- Volume de données et taux de croissance
- Besoins en stockage
- Code couleur : vert (gérable), jaune (vigilance), rouge (défi)

## Ordres de grandeur de performance {#performance-reference-numbers}

| Opération | Latence |
|-----------|---------|
| Accès à la mémoire | ~100 ns |
| Lecture SSD | ~100 us |
| Aller-retour réseau (même DC) | ~500 us |
| Cache distribué (Redis) | ~1 ms |
| Requête simple en base de données | ~1-10 ms |
| Réseau inter-régions | ~50-150 ms |

## Règle des trois options {#three-option-rule}

Pour chaque décision, présenter au minimum 3 approches :
- Même si deux sont manifestement mauvaises, expliquer POURQUOI elles le sont
- S'entraîner à communiquer auprès de parties prenantes non techniques
- Favorise une prise de décision éclairée

## Pratique : raccourcisseur d'URL {#practice-url-shortener}

**Exigences :** raccourcir des URL, rediriger, suivre les statistiques. Latence <100ms, disponibilité de 99,9 %, 10K+ RPS.

**Architecture :**
- Redis pour les correspondances d'URL les plus sollicitées, PostgreSQL pour les métadonnées
- ClickHouse pour l'analyse et les agrégations
- Mise à l'échelle horizontale du service de redirection sans état
- Encodage Base62 pour les identifiants courts

## Pratique : service de notification {#practice-notification-service}

**Exigences :** multicanal (SMS, e-mail, push, messageries), intégration des fournisseurs, historique, analyse, modèles, tests A/B.

**Architecture :**
- Kafka pour la fiabilité et la mise en tampon
- Couche d'abstraction des canaux pour l'indépendance vis-à-vis des fournisseurs
- Système de priorité pour les différents types de notifications
- Moteur de modèles avec substitution de variables

## Documenter pour les parties prenantes non techniques {#documenting-for-non-technical-stakeholders}

1. **Expliquer l'évident** - ce que les ingénieurs savent n'est pas évident pour les managers
2. **Montrer la chaîne de raisonnement** - comment vous êtes arrivé à la conclusion
3. **Identifier les points de bifurcation** - où le raisonnement pourrait diverger
4. **Quantifier les compromis** - coût, délai, risque pour chaque option
5. **Utiliser des tableaux comparatifs** - côte à côte, avec des critères

## Motif de stockage chaud/froid {#hotcold-storage-pattern}

- **Chaud :** données récentes (3-6 mois) sur un stockage rapide (SSD, en mémoire)
- **Froid :** données anciennes sur un stockage bon marché (S3, HDD)
- 999 requêtes sur 1000 touchent les données chaudes ; l'accès au froid est lent mais rare

### Dictionnaire et normalisation pour l'analyse {#dictionarynormalization-for-analytics}
Remplacer les chaînes répétées par des identifiants entiers :
- Chaîne de version du navigateur (50-100 octets) -> entier de 2 octets
- Réduction du stockage de 25 à 50 fois
- Appliquer le dictionnaire aux frontières des requêtes (décoder en entrée, encoder en sortie)

## Pièges à éviter {#gotchas}

- **La collecte des exigences est la plus sous-estimée** - c'est là que la plupart des candidats et des projets échouent
- **« La solution la plus simple qui répond aux exigences l'emporte »** - ne pas sur-concevoir
- **Toujours quantifier** - « forte charge » ne veut rien dire. « 10K RPS avec un P99 <100ms » veut tout dire
- **Les clients décrivent l'existant MÊLÉ à la cible** - séparer l'état actuel de l'état souhaité
- **Conserver les anciennes versions d'API plus longtemps que prévu** - certains clients n'appellent les API qu'une fois par an

## Voir aussi {#see-also}

- [[solution-architecture-process]] - Chaîne complète des exigences
- [[architecture-documentation]] - C4, ADR, vues 4+1
- [[database-selection]] - Choix des bases de données
- [[quality-attributes-reliability]] - SLA, calculs de disponibilité
