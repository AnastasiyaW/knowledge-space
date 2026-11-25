---
title: "Logique mathématique"
category: foundations
tags: [data-science, math, logic, propositional, sets, proofs]
level: 3
source_sha256: 7281068e6a65810dfbe1eba8b18d5ef141cbd48c23e8ddab617f580b629549a3
translation: machine
translated_at: '2026-10-24'
---
# Logique mathématique {#mathematical-logic}

Systèmes de raisonnement formels sur lesquels reposent l'informatique et les démonstrations mathématiques. Logique propositionnelle, logique du premier ordre, techniques de démonstration et théorie des algorithmes.

## Logique propositionnelle {#propositional-logic}

### Connecteurs {#connectives}

| Connecteur | Symbole | Vrai quand |
|-----------|--------|-----------|
| Négation | ~P | P est faux |
| Conjonction | P & Q | Les deux sont vrais |
| Disjonction | P v Q | Au moins un est vrai |
| OU exclusif | P XOR Q | Exactement un est vrai |
| Implication | P -> Q | P est faux, ou les deux sont vrais |
| Équivalence | P <-> Q | Même valeur de vérité |

### Propriétés clés {#key-properties}
- **Tautologie** : toujours vraie, quelles que soient les valeurs des variables. Exemple : P v ~P
- **Contradiction** : toujours fausse. Exemple : P & ~P
- **Équivalence logique** : même table de vérité
- **Lois de De Morgan** : ~(P & Q) = ~P v ~Q, ~(P v Q) = ~P & ~Q
- **Contraposée** : P -> Q équivaut à ~Q -> ~P
- Pour n variables : 2^n lignes dans la table de vérité

### Piège de l'implication {#implication-gotcha}
P -> Q est vraie lorsque P est faux (vérité vide). « Si les cochons volent, alors je suis le roi » est logiquement vrai.

## Logique du premier ordre {#first-order-logic}

Étend la logique propositionnelle avec :
- **Variables** parcourant un domaine
- **Quantificateurs** : « pour tout » (universel) et « il existe » (existentiel)
- **Prédicats** : P(x), R(x, y)
- **Fonctions** : f(x)

**Négation des quantificateurs :**
- ~(forall x, P(x)) = exists x, ~P(x)
- ~(exists x, P(x)) = forall x, ~P(x)

## Techniques de démonstration {#proof-techniques}

| Méthode | Approche |
|--------|----------|
| Directe | Supposer les prémisses, en déduire la conclusion |
| Par contradiction | Supposer la négation de la conclusion, en déduire une contradiction |
| Par contraposée | Prouver ~Q -> ~P au lieu de P -> Q |
| Par récurrence | Cas de base + étape d'hérédité (P(n) -> P(n+1)) |
| Par contre-exemple | Réfuter un énoncé universel par un seul exemple |

### Récurrence mathématique {#mathematical-induction}
1. **Cas de base** : prouver P(1) (ou P(0))
2. **Étape d'hérédité** : supposer P(k) vraie, prouver P(k+1)
3. **Conclusion** : P(n) vraie pour tout n >= base

## Théorie des algorithmes {#algorithm-theory}

### Calculabilité {#computability}
- **Machine de Turing** : modèle abstrait de calcul
- **Thèse de Church-Turing** : tout ce qui est calculable peut l'être par une machine de Turing
- **Problème de l'arrêt** : aucun algorithme ne peut déterminer si un programme quelconque s'arrête (indécidable)
- **Décidable** : il existe un algorithme qui s'arrête toujours en donnant la bonne réponse

### Complexité {#complexity}
- **P** : résoluble en temps polynomial
- **NP** : vérifiable en temps polynomial
- **NP-complet** : les problèmes les plus difficiles de NP (si l'un d'eux est dans P, alors tout NP est dans P)
- **P vs NP** : problème ouvert du millénaire

## Systèmes axiomatiques {#axiomatic-systems}

- **Axiomes** : énoncés admis sans démonstration
- **Théorèmes** : énoncés démontrés à partir des axiomes
- **Cohérence** : aucune contradiction n'est déductible
- **Complétude** : tout énoncé vrai est démontrable (Gödel : impossible pour des systèmes suffisamment puissants)

## Pertinence pour la data science {#relevance-to-ds}
- La logique booléenne sous-tend le filtrage pandas : `df[(cond1) & (cond2)]`
- Les clauses SQL WHERE sont de la logique propositionnelle
- Les arbres de décision sont des conjonctions de prédicats
- La complexité algorithmique détermine la capacité de passage à l'échelle des algorithmes

## Voir aussi {#see-also}
- [[math-precalculus]] - ensembles et combinatoire
- [[python-for-ds]] - opérations booléennes en Python
- [[sql-for-data-science]] - WHERE en SQL comme logique
