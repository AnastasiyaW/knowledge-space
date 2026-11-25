---
title: "Cadre des métriques produit"
category: concepts
tags: [bi-analytics, product-analytics, metrics, dau, mau, retention, stickiness]
level: 3
source_sha256: f657cf95c21da26aef4e751de3d3915555a2f0e257c941cf5adb2fed04ee78c9
translation: machine
translated_at: '2026-10-24'
---
# Cadre des métriques produit {#product-metrics-framework}

Métriques produit essentielles pour mesurer l'engagement des utilisateurs, la rétention et la santé du produit. Ces métriques constituent la base de l'analyse produit pour les applications mobiles, les produits web et les plateformes SaaS.

## Points clés {#key-facts}

- **DAU** (Daily Active Users) - utilisateurs uniques actifs dans une journée
- **WAU** (Weekly Active Users) - utilisateurs uniques actifs sur 7 jours
- **MAU** (Monthly Active Users) - utilisateurs uniques actifs sur 30 jours
- **Stickiness** = DAU/MAU - mesure le caractère incitatif du produit à être utilisé régulièrement
- **Taux de rétention** - % d'utilisateurs qui reviennent après la première utilisation au jour N
- **Taux de churn** = 1 - Rétention - % d'utilisateurs qui cessent d'utiliser le produit
- « Actif » doit être défini explicitement pour chaque produit (une connexion ? une transaction ? l'utilisation d'une fonctionnalité ?)

## Schémas types {#patterns}

### Benchmarks de stickiness (DAU/MAU) {#stickiness-benchmarks-daumau}

```toml
Stickiness = DAU / MAU
```

| Plage | Interprétation | Exemples |
|-------|---------------|----------|
| 50 % et plus | Usage quotidien ancré | Réseaux sociaux, messagerie électronique |
| 25-50 % | Plusieurs fois par semaine | Applications de productivité |
| 10-25 % | Usage hebdomadaire | Applications de fitness, de finance |
| <10 % | Usage occasionnel | Réservation de voyages, immobilier |

La stickiness dépend du contexte : ne comparez pas la stickiness d'une application de messagerie à celle d'une application de réservation d'hôtel.

### Types de rétention {#retention-types}

**Rétention à N jours** : % des utilisateurs d'une cohorte d'installation qui reviennent exactement le jour N.

**Rétention par tranche** : % des utilisateurs qui reviennent dans une plage de jours (par exemple, du jour 7 au jour 14).

**Rétention de présence** : % des utilisateurs ayant utilisé l'application au moins une fois depuis l'installation et toujours actifs au jour N.

Comment lire les courbes de rétention :
- Une courbe qui s'aplatit = le produit a une valeur centrale (les utilisateurs qui restent, restent sur le long terme)
- Une courbe qui tombe à 0 = pas d'adéquation produit-marché, tous les utilisateurs partent
- Un D1 supérieur au D7 ou au D30 = l'engagement précoce est déterminant

### Étapes du cycle de vie utilisateur {#user-lifecycle-stages}

1. **Impression** - l'utilisateur voit la publicité
2. **Clic** - l'utilisateur clique sur la publicité
3. **Installation** - application téléchargée et installée
4. **Première ouverture** (inscription/onboarding)
5. **Événement clé** - action cible (premier achat, activation)
6. **Rétention** - utilisation récurrente
7. **Monétisation** - achat/abonnement
8. **Churn** - arrêt de l'utilisation de l'application

### Schéma SQL de stickiness DAU/MAU {#daumau-stickiness-sql-pattern}

```sql
SELECT
    event_date,
    COUNT(DISTINCT user_id) as dau,
    COUNT(DISTINCT user_id) OVER (
        ORDER BY event_date
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as mau_rolling,
    ROUND(100.0 * COUNT(DISTINCT user_id) /
        COUNT(DISTINCT user_id) OVER (
            ORDER BY event_date
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ), 1) as stickiness
FROM events
GROUP BY event_date;
```

### Stratégie d'alerte {#alert-strategy}

Configurez des alertes automatiques pour :
- Chutes brutales du DAU (>15 % par rapport à la moyenne glissante)
- Taux de conversion du tunnel inférieur au seuil
- Revenu par utilisateur inférieur à l'objectif

## Pièges à éviter {#gotchas}

- Le ratio DAU/MAU peut être trompeur si « actif » est défini trop largement (par exemple, en comptant les pages vues passives)
- Les benchmarks de rétention varient fortement selon la catégorie de produit : comparez toujours au sein de votre secteur
- La stickiness peut être artificiellement gonflée par les notifications push qui génèrent des ouvertures sans engagement réel
- Le churn = 1 - Rétention n'est valide que si les deux métriques utilisent la même fenêtre temporelle et la même définition de « actif »

## Voir aussi {#see-also}

- [[product-analytics-fundamentals]] - rôle de l'analyste et pyramide des métriques
- [[cohort-retention-analysis]] - analyse de rétention par cohortes
- [[unit-economics]] - LTV et rentabilité client
- [[mobile-analytics-platforms]] - outils de mesure de ces métriques
