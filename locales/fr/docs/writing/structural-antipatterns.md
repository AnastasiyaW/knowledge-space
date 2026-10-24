---
title: "Anti-patrons structurels dans le texte IA"
category: patterns
tags: [writing, ai-detection, structure, antipatterns]
level: 3
source_sha256: 32ce8141fd32077bfef91cdbe8a0489992ceaf352306a4e4c250b7a5cc1d4aa4
translation: machine
translated_at: '2026-10-24'
---
# Anti-patrons structurels dans le texte IA {#structural-anti-patterns-in-ai-text}

Le texte généré par une IA possède une « forme » reconnaissable, indépendante du vocabulaire. Même après avoir remplacé les mots-signaux, la structure trahit l'origine machine. Ces motifs sont plus difficiles à corriger que la substitution de mots, car ils imposent de repenser l'organisation du contenu.

## La « forme IA » {#the-ai-shape}

### Structure de paragraphe symétrique {#symmetrical-paragraph-structure}

Chaque paragraphe a à peu près la même longueur (4 à 6 phrases). Chaque section comporte 3 à 5 puces. Aucun paragraphe n'est constitué d'une seule phrase. Aucun ne dépasse 10 phrases.

**Texte IA (uniforme) :**
> Le machine learning a transformé de nombreux secteurs. Les entreprises adoptent les réseaux de neurones pour des tâches variées. Ces modèles demandent des ressources de calcul considérables. L'entraînement implique généralement de grands jeux de données et du matériel spécialisé. Les résultats peuvent être impressionnants lorsqu'ils sont correctement mis en œuvre.
>
> Le traitement automatique du langage naturel est un autre domaine clé. Les chercheurs ont développé des modèles sophistiqués pour l'analyse de texte. Ces systèmes peuvent comprendre le contexte et générer des réponses cohérentes. Les applications vont des chatbots aux services de traduction. Le domaine continue d'évoluer rapidement.

Chaque paragraphe : 5 phrases, environ 20 mots par phrase, même rythme.

**Texte humain (irrégulier) :**
> Nous avons essayé trois architectures différentes avant que quoi que ce soit fonctionne.
>
> Le premier essai utilisait un LSTM basique. L'entraînement a pris 14 heures sur un seul GPU, et le modèle ne parvenait pas à traiter des entrées de plus de 512 tokens, ce qui représentait 60 % de notre jeu de données. Nous y avons consacré une semaine avant d'admettre que c'était une impasse. L'approche à base d'attention qui l'a remplacé s'est entraînée en 3 heures et a géré des longueurs arbitraires, ce qui, honnêtement, semblait injuste au vu du temps passé sur le LSTM.
>
> Troisième tentative : BERT affiné. Ça a marché immédiatement.

Paragraphes : 1 phrase, 4 phrases, 1 phrase. Le rythme change. Les paragraphes courts servent à marquer l'effet.

### Transitions prévisibles {#predictable-transitions}

Chaque paragraphe s'ouvre sur un mot de transition. Le motif est visible sans même lire le contenu :

```text
Moreover, [paragraph]...
Furthermore, [paragraph]...
Additionally, [paragraph]...
In conclusion, [paragraph]...
```

Le texte humain n'a pas besoin de transitions mécaniques. Le contexte et l'enchaînement guident le lecteur. Lorsque des transitions apparaissent dans un texte humain, elles sont variées, informelles et peu fréquentes (« Mais voilà le truc », « Donc », « Il s'avère que », ou aucune transition du tout).

### Listification {#list-ification}

L'IA convertit tout en listes numérotées ou en puces :
- Chaque élément a à peu près la même longueur (10 à 15 mots)
- Des éléments qui pourraient être de la prose sont forcés dans un format de liste
- Des listes dont l'ordre n'a pas d'importance sont présentées en numérotation
- Des sous-listes qui n'apportent aucune valeur

**Quand les listes sont appropriées :** éléments réellement parallèles, étapes d'une séquence, options de configuration, tableaux comparatifs.

**Quand elles ne le sont pas :** argumentations qui s'appuient les unes sur les autres, récits, explications où le contexte s'accumule.

### Le motif sandwich {#the-sandwich-pattern}

Chaque paragraphe suit le schéma : **affirmation générale -> détail à l'appui -> reformulation de l'affirmation.**

> Le machine learning transforme le secteur de la santé. [affirmation]
> Des études récentes montrent que l'IA peut détecter le cancer sur des images médicales avec une précision de 95 %. [détail]
> Cela illustre l'impact considérable du machine learning sur le secteur de la santé. [reformulation]

Ce schéma se répète à l'identique dans tous les paragraphes. Les rédacteurs humains énoncent une idée, la développent, puis passent à la suite. Ils ne reviennent pas reformuler l'affirmation initiale dans chaque paragraphe.

### Motifs des intertitres {#header-patterns}

Les intertitres de l'IA suivent des modèles prévisibles :
- « Comprendre X »
- « Le rôle de Y »
- « Pourquoi Z compte »
- « Explorer la puissance de W »
- « Guide complet de V »

Les intertitres humains tendent à être précis et orientés vers l'action :
- « LSTM a échoué, BERT a fonctionné »
- « Le problème de la limite de 512 tokens »
- « Coûts d'entraînement : 47 $ contre 3 $ »

## Déficit de burstiness {#burstiness-deficit}

**Burstiness** = variation de la longueur et de la structure des phrases. C'est le signal structurel le plus fort pour la détection.

**Burstiness du texte humain :**
```yaml
Sentence lengths: 5, 23, 8, 41, 12, 3, 28, 15, 6, 35
SD: ~13 words
```

**Burstiness du texte IA :**
```yaml
Sentence lengths: 18, 22, 19, 21, 17, 20, 23, 18, 21, 19
SD: ~2 words
```

Le texte humain a du rythme. Les phrases courtes frappent. Les phrases longues développent des idées complexes, avec des subordonnées, des digressions et des nuances qui reflètent la pensée réelle. Le texte IA reste à un rythme constant de 18 à 22 mots par phrase.

## Déficit de perplexité {#perplexity-deficit}

**Perplexité** = caractère imprévisible des choix lexicaux. C'est le second indicateur clé, après la burstiness.

- **Texte humain** : verbes inattendus, métaphores surprenantes, associations de mots inhabituelles. Des pics de forte perplexité (choix créatifs) alternent avec une faible perplexité (formules courantes).
- **Texte IA** : perplexité constamment faible. Chaque mot est le « choix statistique le plus sûr ». Techniquement correct, mais prévisible. Aucune surprise.

La burstiness mesure la variation du rythme. La perplexité mesure l'imprévisibilité du vocabulaire. Les deux sont faibles dans le texte IA ; elles doivent être élevées pour une lecture naturelle.

## Marqueurs humains absents {#missing-human-markers}

Ce que le texte humain possède et que le texte IA n'a pas :

- **Digressions** qui ne servent pas parfaitement la thèse
- **Opinions tranchées** formulées sans nuance (« Cette approche est fausse »)
- **Autocorrection** (« En fait, ce n'est pas tout à fait exact... »)
- **Changements de registre** : du formel à l'informel, puis retour (« l'algorithme converge, du moins c'est ce qu'il a fait sur mon portable »)
- **Pensées inachevées** que le lecteur doit compléter lui-même
- **Incohérence émotionnelle** : enthousiasme suivi de frustration
- **Erreurs et corrections spécifiques** qui montrent le processus de réflexion
- **Raccourcis personnels** : supposer la connaissance du lecteur sans expliquer les bases

## Anti-patrons de ton {#tone-anti-patterns}

### Enthousiasme excessif {#excessive-enthusiasm}

Tout est « fascinant », « remarquable », « passionnant ». Superlatifs génériques appliqués à des sujets banals. Aucun humain n'est réellement enthousiaste de manière égale pour chaque aspect d'un sujet technique.

### Excès de précautions {#hedge-heavy-writing}

- « Il convient de noter que... »
- « Bien qu'il puisse sembler... »
- « On pourrait soutenir que... »
- Ne jamais prendre position de façon définitive. Les experts humains ont des opinions et les énoncent directement.

### Équilibre à outrance {#balanced-to-a-fault}

« D'un côté... de l'autre... » pour chaque sujet, même lorsqu'un côté est clairement plus solide. Conclusions évasives : « Cela dépend de vos besoins et exigences spécifiques. »

### Vernis de surface, rien en dessous {#surface-polish-nothing-underneath}

Selon les travaux de Northeastern/Khoury sur le « AI slop » (arxiv 2509.19163), trois propriétés le définissent :
1. **Compétence superficielle** : le texte se lit sans accroc mais ne dit rien de précis
2. **Effort asymétrique** : facile à produire, difficile à vérifier
3. **Production de masse** : le texte pourrait s'appliquer à n'importe quel sujet voisin moyennant des modifications minimes

## Pièges {#gotchas}

- **Problème :** corriger isolément certains défauts structurels (par exemple varier la longueur des paragraphes) tout en gardant les autres (motif sandwich, absence d'opinion) produit un texte qui se lit toujours comme de l'IA. **Solution :** la structure suit la pensée. Écrivez ce que vous pensez réellement, dans l'ordre où vous l'avez pensé, puis relisez pour la clarté. Ne plaquez pas une variation de type humain sur une structure IA.
- **Problème :** ajouter des puces pour fragmenter une prose IA empire les choses, car cela ajoute une listification aux problèmes structurels existants. **Solution :** si le contenu est une argumentation ou un récit, gardez-le en prose. Les listes ne servent que pour des éléments réellement parallèles.
- **Problème :** « Ajoutons un peu d'humour » produit des blagues forcées, qui sont un autre signe de l'IA. **Solution :** l'humour en rédaction technique naît d'observations honnêtes, pas de traits insérés. « La doc annonce 5 minutes. Il nous a fallu trois jours. » est plus drôle que n'importe quelle blague construite.

## Voir aussi {#see-also}

- [[ai-text-detection]]
- [[overused-words-phrases]]
- [[natural-writing-style]]
- [[editing-checklist]]
