---
title: "Mathématiques pour le Machine Learning"
category: foundations
tags: [data-science, math, calculus, optimization, gradient]
level: 3
source_sha256: 425e14aec93d37680ce5610a8704e348d5b167df4ea4a1b74fec5ce3bb3278d1
translation: machine
translated_at: '2026-10-24'
---
# Mathématiques pour le Machine Learning {#mathematics-for-machine-learning}

Les mathématiques essentielles qui sous-tendent les algorithmes de ML. L'accent est mis sur ce qu'il faut comprendre pour saisir POURQUOI les algorithmes fonctionnent, et pas seulement sur la manière de les appeler.

## Calcul différentiel pour le ML {#calculus-for-ml}

### Dérivées {#derivatives}

f'(x) = lim(h->0) [f(x+h) - f(x)] / h. Taux de variation. Pente de la tangente.

**Règles clés :**
- Puissance : (x^n)' = n*x^(n-1)
- Règle de la chaîne : (f(g(x)))' = f'(g(x)) * g'(x)
- Produit : (fg)' = f'g + fg'
- e^x : (e^x)' = e^x
- ln(x) : (ln(x))' = 1/x

### Dérivées partielles et gradient {#partial-derivatives-and-gradient}

Pour f(x1, ..., xn) : gradient = vecteur des dérivées partielles.

nabla f = [df/dx1, df/dx2, ..., df/dxn]

**Le gradient pointe dans la direction de la plus forte montée.** La descente de gradient se déplace dans le sens opposé : w -= lr * nabla_f.

### Points critiques et optimisation {#critical-points-and-optimization}

- Point critique : gradient = 0
- Test de la dérivée seconde : f''(x) > 0 -> minimum, f''(x) < 0 -> maximum
- **Matrice hessienne** : dérivées partielles secondes. Les valeurs propres déterminent la nature du point critique
- **Fonctions convexes** : tout minimum local est un minimum global. L'erreur quadratique moyenne (MSE) est convexe pour la régression linéaire

### Rétropropagation {#backpropagation}

Règle de la chaîne appliquée à travers le graphe de calcul. Pour une sortie de couche = sigma(Wx + b) :
```text
d(Loss)/dW = d(Loss)/d(output) * d(output)/d(Wx+b) * d(Wx+b)/dW
```

Le graphe de calcul et la différentiation automatique rendent cela faisable pour les réseaux profonds.

### Série de Taylor {#taylor-series}

f(x) = f(a) + f'(a)(x-a) + f''(a)(x-a)^2/2! + ...

Développements clés : e^x = 1 + x + x^2/2! + ..., ln(1+x) = x - x^2/2 + ...

Dans le ML : comprendre le comportement de la perte au voisinage des optima, méthode de Newton (approximation du second ordre).

## Optimisation {#optimization}

### Descente de gradient {#gradient-descent}

w_(t+1) = w_t - alpha * nabla f(w_t)

- **Taux d'apprentissage** alpha : trop grand -> divergence, trop petit -> convergence lente
- **GD stochastique** : gradient calculé sur un seul échantillon (bruité mais rapide)
- **GD par mini-batch** : petit lot (compromis)
- **Momentum** : v_t = beta*v_(t-1) + nabla f. Accélère à travers les vallées étroites
- **Convergence** : O(1/t) pour les fonctions convexes à gradient lipschitzien

### Méthode de Newton {#newtons-method}

w_new = w_old - H^(-1) * gradient. Utilise les dérivées secondes (hessienne). Converge plus vite, mais H^(-1) est coûteux à calculer.

**Quasi-Newton** (L-BFGS) : approximation peu coûteuse de l'inverse de la hessienne.

### Multiplicateurs de Lagrange {#lagrange-multipliers}

Optimiser f(x) sous la contrainte g(x) = 0 : nabla f = lambda * nabla g.

Dans le ML : optimisation des SVM (maximiser la marge sous contraintes).

## Astuce log-sum-exp {#log-sum-exp-trick}

Éviter le dépassement numérique (overflow) dans softmax et la log-vraisemblance :
```sql
log(sum(exp(x_i))) = c + log(sum(exp(x_i - c)))  where c = max(x_i)
```

## Intégration dans le ML {#integration-in-ml}

- Calcul des espérances et des probabilités (aire sous la PDF)
- Constantes de normalisation des distributions
- Divergence KL entre distributions
- Intégrale de Lebesgue : fondement de la théorie moderne des probabilités

## Pièges courants {#gotchas}

- La descente de gradient sur des fonctions non convexes (réseaux de neurones) converge vers des minima locaux, pas globaux, mais c'est généralement acceptable
- La stabilité numérique compte : utiliser l'espace logarithmique pour les produits de probabilités
- Le calcul de la hessienne est en O(n^2) par rapport aux paramètres, ce qui le rend impraticable pour les grands modèles
- Les erreurs de règle de la chaîne se propagent : toujours vérifier les gradients numériquement

## Voir aussi {#see-also}

- [[math-linear-algebra]] - vecteurs, matrices, valeurs propres
- [[linear-models]] - application directe du calcul au ML
- [[neural-networks]] - la rétropropagation utilise la règle de la chaîne
- [[probability-distributions]] - intégration pour le calcul des espérances
