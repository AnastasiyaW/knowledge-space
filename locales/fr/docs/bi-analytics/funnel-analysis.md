---
title: "Analyse d'entonnoir"
category: concepts
tags: [bi-analytics, product-analytics, funnel, conversion, optimization]
level: 2
source_sha256: 94af672a6b8552d16a083c5ba7782651afa1c8227cd96848a4fa52fcb38e8c87
translation: machine
translated_at: '2026-10-24'
---
# Analyse d'entonnoir {#funnel-analysis}

L'analyse d'entonnoir visualise et mesure la progression des utilisateurs à travers un parcours en plusieurs étapes vers un objectif de conversion. Chaque étape représente une action de l'utilisateur, et l'analyse se concentre sur les taux d'abandon entre les étapes afin d'identifier les opportunités d'optimisation.

## Points clés {#key-facts}

- Entonnoir = séquence d'étapes utilisateur vers un objectif de conversion
- Métriques clés : conversion par étape (N vers N+1), conversion globale, points d'abandon, temps entre les étapes
- Entonnoir e-commerce type : Visiteur -> Page produit -> Ajout au panier -> Début du paiement -> Paiement -> Commande terminée
- Entonnoir type d'application mobile : app_open -> registration_start -> registration_complete -> onboarding_complete -> first_purchase
- L'optimisation de l'entonnoir cible en priorité l'étape à plus fort taux d'abandon
- La fenêtre temporelle compte : ne comptabiliser la finalisation de l'entonnoir que si elle est réalisée dans un délai de N jours/heures

## Patterns {#patterns}

### Processus d'optimisation de l'entonnoir {#funnel-optimization-process}

1. Identifier l'étape à plus fort taux d'abandon
2. Formuler une hypothèse sur la cause (UX confuse, trop d'étapes, valeur peu claire)
3. Tester une amélioration (A/B ou séquentiel)
4. Mesurer l'évolution de la conversion

### Parcours utilisateur critique (carte d'événements) {#critical-user-path-event-map}

La séquence minimale d'événements qui définit le parcours utilisateur central :
1. `app_open` - application lancée
2. `registration_start` - parcours d'inscription ouvert
3. `registration_complete` - compte créé
4. `onboarding_complete` - tutoriel terminé
5. `first_purchase` - premier paiement

### Priorisation des événements {#event-prioritization}

1. Événements KPI métier (achat, abonnement, activation)
2. Événements d'étapes d'entonnoir (écrans clés, actions clés)
3. Événements d'erreur/plantage (identifier les problèmes)
4. Événements d'engagement (profondeur d'utilisation des fonctionnalités)

### Analyse d'entonnoir dans Amplitude {#funnel-analysis-in-amplitude}

- Définir la séquence d'événements : `sign_up` -> `onboarding_complete` -> `first_purchase`
- Affiche l'abandon à chaque étape
- Segmenter par propriété : comparer la conversion iOS et Android
- Fenêtre temporelle : ne comptabiliser l'entonnoir que s'il est terminé dans un délai de N jours/heures

### Modèle d'entonnoir en SQL {#sql-funnel-pattern}

```sql
SELECT
    COUNT(CASE WHEN event = 'page_view' THEN user_id END) as step1_views,
    COUNT(CASE WHEN event = 'add_to_cart' THEN user_id END) as step2_cart,
    COUNT(CASE WHEN event = 'checkout_start' THEN user_id END) as step3_checkout,
    COUNT(CASE WHEN event = 'purchase' THEN user_id END) as step4_purchase
FROM events
WHERE event_date = CURRENT_DATE;
```

### Taux de conversion d'installation (magasins d'applications) {#install-conversion-rate-app-stores}

**Taux de conversion** = installations / vues de la page produit. Référence : 25 à 35 % pour les applications bien optimisées.

Éléments influant sur la conversion :
- **Icône** - première impression visuelle, reconnaissable en petit format
- **Captures d'écran** - les 2 ou 3 premières visibles sans défilement (les plus importantes)
- **Vidéo de présentation** - lecture automatique sur iOS, présenter la valeur principale dans les 3 premières secondes
- **Nom de l'application + sous-titre** - transmettent immédiatement la proposition de valeur
- **Notes** - les applications dont la note est inférieure à 4,0 ont un taux de conversion nettement plus faible
- **Avis** - les avis positifs récents comptent davantage que les anciens

## Pièges à éviter {#gotchas}

- L'analyse d'entonnoir sans fenêtre temporelle peut être trompeuse : un utilisateur qui commence aujourd'hui et achète 90 jours plus tard n'est pas comparable à celui qui termine en 10 minutes
- Compter les événements ou compter les utilisateurs uniques donne des formes d'entonnoir très différentes
- Les entonnoirs non linéaires (utilisateurs qui sautent des étapes ou reviennent en arrière) nécessitent une analyse par session, et non un simple comptage par étape
- Segmenter les entonnoirs par source d'acquisition révèle souvent que les chiffres agrégés masquent des schémas de comportement très différents

## Voir aussi {#see-also}

- [[product-analytics-fundamentals]] - pyramide des métriques et rôle de l'analyste
- [[cohort-retention-analysis]] - suivi de la rétention après l'entonnoir
- [[web-marketing-analytics]] - mise en place d'un entonnoir web avec GA/GTM
- [[mobile-analytics-platforms]] - outils d'entonnoir dans Firebase, Amplitude
- [[app-store-optimization]] - entonnoirs de conversion des magasins d'applications
