---
title: "Méthodes bayésiennes en ML"
category: concepts
tags: [data-science, bayesian, naive-bayes, inference, prior]
level: 2
source_sha256: aad80d100fe194f4e5c2fe4aa8804d39301b5f14d6a04628d50e940313479779
translation: machine
translated_at: '2026-10-24'
---
# Méthodes bayésiennes en ML {#bayesian-methods-in-ml}

La pensée bayésienne met à jour les croyances à partir de nouvelles preuves. Du simple classifieur Naive Bayes à l'inférence bayésienne, ces méthodes offrent une quantification de l'incertitude fondée sur des principes solides.

## Application du théorème de Bayes {#bayes-theorem-applied}

P(hypothèse | données) = P(données | hypothèse) * P(hypothèse) / P(données)

- **A priori** P(hypothèse) : ce que nous croyons avant d'observer les données
- **Vraisemblance** P(données | hypothèse) : probabilité des données sachant l'hypothèse
- **A posteriori** P(hypothèse | données) : croyance mise à jour après observation des données
- **Évidence** P(données) : constante de normalisation

## Classifieur Naive Bayes {#naive-bayes-classifier}

P(classe | caractéristiques) proportionnel à P(classe) * produit(P(caractéristique_i | classe))

Hypothèse « naïve » : les caractéristiques sont conditionnellement indépendantes sachant la classe. Cette hypothèse est souvent violée, mais le modèle fonctionne étonnamment bien.

```python
from sklearn.naive_bayes import GaussianNB, MultinomialNB

# Gaussian: continuous features (assumes normal distribution)
gnb = GaussianNB()
gnb.fit(X_train, y_train)

# Multinomial: count features (great for text/TF-IDF)
mnb = MultinomialNB()
mnb.fit(X_train_tfidf, y_train)
```

**Idéal pour** : la classification de textes (filtrage de spam, analyse de sentiments), lorsque les données d'entraînement sont peu nombreuses, lorsqu'un entraînement rapide est nécessaire.

### Pourquoi cela fonctionne malgré une hypothèse erronée {#why-it-works-despite-wrong-assumption}
- La classification nécessite seulement de classer correctement les probabilités, et non de les estimer avec précision
- Les dépendances entre caractéristiques se compensent souvent d'une classe à l'autre
- Avec des données limitées, les modèles plus simples généralisent mieux

## Bayésien vs fréquentiste {#bayesian-vs-frequentist}

| Aspect | Fréquentiste | Bayésien |
|--------|-------------|----------|
| Paramètres | Fixes, inconnus | Variables aléatoires avec distributions |
| Données | Aléatoires (échantillonnage répété) | Fixes (observées) |
| Inférence | Estimation ponctuelle + IC | Distribution a posteriori complète |
| Connaissances a priori | Non intégrées | Intégrées explicitement |
| Incertitude | Intervalles de confiance | Intervalles de crédibilité |

## Inférence bayésienne {#bayesian-inference}

Plutôt que des estimations ponctuelles, on calcule la distribution a posteriori complète des paramètres.

**Lois a priori conjuguées** : la loi a priori et la loi a posteriori appartiennent à la même famille.
- Vraisemblance normale + loi a priori normale -> loi a posteriori normale
- Vraisemblance binomiale + loi a priori Bêta -> loi a posteriori Bêta

**MCMC (Markov Chain Monte Carlo)** : échantillonner la loi a posteriori lorsque la solution analytique est inaccessible.

## Applications en data science {#applications-in-data-science}

- **Tests A/B** : les tests A/B bayésiens donnent la probabilité que B soit meilleur que A (plus intuitif que les p-valeurs)
- **Réglage des hyperparamètres** : optimisation bayésienne (Optuna, Hyperopt)
- **Filtrage de spam** : Naive Bayes avec fréquences des mots
- **Diagnostic médical** : prévalence a priori de la maladie + sensibilité du test
- **Systèmes de recommandation** : personnalisation bayésienne

## Pièges courants {#gotchas}
- Naive Bayes suppose l'indépendance des caractéristiques : la corrélation entre elles dégrade les performances
- Le choix de la loi a priori compte, surtout avec peu de données
- MCMC peut converger lentement pour les modèles complexes
- Le calcul dans l'espace logarithmique est indispensable pour éviter le sous-dépassement numérique (produit de nombreuses petites probabilités)
- Multinomial NB exige des caractéristiques non négatives (comptages, TF-IDF)

## Voir aussi {#see-also}
- [[probability-distributions]] - théorie des distributions sous-jacente à Bayes
- [[nlp-text-processing]] - Naive Bayes pour la classification de textes
- [[hypothesis-testing]] - alternative bayésienne aux tests fréquentistes
- [[math-probability-statistics]] - fondements formels des probabilités
