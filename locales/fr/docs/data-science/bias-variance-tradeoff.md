---
title: "Compromis biais-variance"
category: concepts
tags: [data-science, ml, overfitting, underfitting, regularization]
level: 2
source_sha256: ddbccf5644bf36c42536dd73071a9f6ea9a2a84be21744ec265ef67d8a40fa39
translation: machine
translated_at: '2026-10-24'
---
# Bias-Variance Tradeoff {#bias-variance-tradeoff}

La tension fondamentale en apprentissage automatique : les modèles trop simples manquent des motifs (biais), les modèles trop complexes mémorisent le bruit (variance). Chaque décision de modélisation est un point sur ce spectre.

## Définitions {#definitions}

**Biais** = erreur systématique. Écart moyen entre les prédictions et les valeurs réelles.
- Biais élevé = sous-apprentissage (modèle trop simple, manque les motifs)
- Exemple : ajuster une régression linéaire à des données quadratiques

**Variance** = ampleur des fluctuations des prédictions d'un jeu d'entraînement à l'autre.
- Variance élevée = surapprentissage (le modèle capture le bruit, pas le signal)
- Exemple : polynôme de degré 10 sur 20 points de données

**Erreur totale = Biais^2 + Variance + Bruit irréductible**

## Diagnostic {#diagnosis}

| Symptôme | Diagnostic | Solution |
|---------|-----------|----------|
| Erreur d'entraînement élevée, erreur de validation élevée | Sous-apprentissage (biais élevé) | Modèle plus complexe, plus de features |
| Erreur d'entraînement faible, erreur de validation élevée | Surapprentissage (variance élevée) | Régularisation, plus de données, modèle plus simple |
| Erreur d'entraînement faible, erreur de validation faible | Bon ajustement | Mettre en production |
| Erreur d'entraînement élevée, erreur de validation faible | Impossible (fuite de données ?) | Vérifier les bugs |

**Courbes d'apprentissage** : tracer l'erreur d'entraînement et de validation en fonction de la taille du jeu d'entraînement.
- Convergence à une erreur élevée -> problème de biais (plus de données n'aideront pas, il faut un meilleur modèle)
- Écart important -> problème de variance (plus de données aideront)

## Spectre de complexité des modèles {#model-complexity-spectrum}

Faible complexité <---------> Forte complexité
Régression linéaire --- Polynomiale --- Arbre de décision --- Forêt profonde --- Réseau de neurones

Faible biais, forte variance <--> Fort biais, faible variance

## Gérer le compromis {#managing-the-tradeoff}

### Réduire la variance (combattre le surapprentissage) {#reduce-variance-fight-overfitting}
- **Régularisation** : pénalités L1/L2 sur les poids du modèle
- **Dropout** : désactivation aléatoire de neurones pendant l'entraînement
- **Arrêt anticipé** : arrêter l'entraînement lorsque la perte de validation augmente
- **Validation croisée** : estimation robuste des performances
- **Plus de données d'entraînement** : meilleur remède contre le surapprentissage
- **Méthodes d'ensemble** : la moyenne réduit la variance (Random Forest, Bagging)
- **Sélection de features** : supprimer les features bruitées ou non pertinentes
- **Modèle plus simple** : moins de paramètres, arbres moins profonds

### Réduire le biais (combattre le sous-apprentissage) {#reduce-bias-fight-underfitting}
- **Modèle plus complexe** : arbres plus profonds, plus de couches
- **Features plus nombreuses ou de meilleure qualité** : ingénierie de features
- **Moins de régularisation** : réduire la pénalité
- **Méthodes d'ensemble** : le boosting réduit le biais (Gradient Boosting, AdaBoost)
- **Entraîner plus longtemps** : plus d'époques/itérations

## Méthodes d'ensemble et compromis {#ensemble-methods-and-the-tradeoff}

- **Bagging** (Random Forest) : entraîne plusieurs modèles indépendamment et en fait la moyenne. Réduit la VARIANCE
- **Boosting** (Gradient Boosting) : entraîne les modèles séquentiellement, chacun corrigeant les erreurs précédentes. Réduit le BIAIS

C'est pourquoi le gradient boosting (réduit le biais) combiné à la régularisation (contrôle la variance) est si puissant.

## Pièges à éviter {#gotchas}
- « Plus de données » aide la variance mais PAS le biais : si le modèle est trop simple, plus de données ne le corrigeront pas
- La régularisation n'est PAS gratuite : une régularisation excessive augmente le biais
- Le surapprentissage sur le jeu de validation est réel : un réglage intensif des hyperparamètres sur le même jeu de validation
- Les réseaux de neurones remettent en cause le compromis classique : les très grands modèles peuvent bien généraliser (phénomène de double descente)
- La validation croisée donne une meilleure estimation qu'une séparation unique, mais elle est plus lente

## Voir aussi {#see-also}
- [[model-evaluation]] - détecter le surapprentissage
- [[feature-engineering]] - techniques de régularisation
- [[gradient-boosting]] - gestion pratique du compromis biais-variance
- [[neural-networks]] - régularisation en apprentissage profond
