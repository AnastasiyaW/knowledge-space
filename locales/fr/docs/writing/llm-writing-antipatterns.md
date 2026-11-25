---
title: "Antipatterns de rédaction LLM"
description: "Motifs de texte IA détectables - vocabulaire surutilisé, antipatterns structurels, métriques de burstiness/perplexité, marqueurs spécifiques au russe, et liste de contrôle d'humanisation."
level: 3
source_sha256: 8df2f456fc144c888015e06193c31cf6c5b7b1d0f26749e0b8f50c82fb605cc4
translation: machine
translated_at: '2026-10-24'
---
# Antipatterns de rédaction LLM {#llm-writing-anti-patterns}

Comment détecter et éviter les motifs de texte généré par IA. Couvre les marqueurs de vocabulaire anglais, les signatures structurelles, la métrique de burstiness, les motifs spécifiques au russe, et une liste de contrôle pratique pour l'édition.

## Vocabulaire anglais à fort signal {#high-signal-english-vocabulary}

D'après l'analyse de plus de 15 millions de résumés PubMed (Liang et al., arXiv 2406.07016) :

### Niveau 1 : signaux d'alerte immédiats {#tier-1-immediate-red-flags}

| Mot | Ratio d'excès | Remarque |
|------|-------------|------|
| delves | 25,2x | Marqueur IA canonique, abandonné après une large diffusion |
| showcasing | 9,2x | |
| underscores | 9,1x | |
| across, additionally, comprehensive | Élevé | Parmi les 10 marqueurs de détection les plus efficaces |
| crucial, enhancing, insights | Élevé | |
| notably, particularly, within | Élevé | |

**66 % du vocabulaire IA en excès sont des verbes et des adjectifs**, et non des noms de contenu. C'est pourquoi un texte IA est détectable en tant que *style* et non en tant que *contenu*.

### Niveau 2 : termes courants signalés {#tier-2-common-flagged-terms}

**Verbes :** delve, dive into, embark, navigate, uncover, unveil, unlock, unleash, leverage, harness, foster, bolster, spearhead, champion, resonate, captivate, illuminate, elevate, underscore, shed light on

**Adjectifs :** vibrant, meticulous, intricate, multifaceted, nuanced, holistic, comprehensive, compelling, profound, pivotal, paramount, cutting-edge, transformative, seamless, innovative

**Noms/métaphores :** tapestry, landscape, realm, labyrinth, beacon, crucible, interplay, synergy, zeitgeist, game changer, deep dive

**Transitions :** Moreover, Furthermore, Additionally, Notably, In conclusion, In summary, That being said, Subsequently

**Remplissage :** "A testament to...", "It's important to note...", "Let's dive in", "In the realm of..."

## Antipatterns structurels {#structural-anti-patterns}

### La « forme IA » {#the-ai-shape}

- Chaque paragraphe a à peu près la même longueur
- Chaque section comporte 3 à 5 puces
- Motif de titres prévisible : « Comprendre X », « Le rôle de Y », « Pourquoi Z compte »
- Chaque paragraphe commence par un mot de transition
- « En conclusion... » comme conclusion inévitable

### Burstiness (métrique la plus détectable) {#burstiness-most-detectable-metric}

Burstiness = variation de la longueur et de la structure des phrases.

**Écriture humaine :** mêle naturellement des phrases courtes et percutantes à des phrases longues et complexes. Un paragraphe peut contenir une phrase de 5 mots suivie d'une phrase de 40 mots.

**Écriture IA :** les phrases se regroupent autour d'une longueur moyenne (15 à 25 mots). Tempo monotone. Chaque phrase suit le même rythme.

La burstiness se calcule : mesurez l'écart type des longueurs de phrases. Le texte IA a un écart type faible, le texte humain un écart type élevé.

### Perplexité {#perplexity}

Faible perplexité = chaque mot est le « choix statistiquement le plus sûr ».

L'écriture humaine présente des pics de forte perplexité (choix créatifs, métaphores inattendues, associations de mots inhabituelles) mêlés à des passages de faible perplexité. Le texte IA est uniformément à faible perplexité : techniquement correct, ennuyeux.

### La signature centrale {#the-core-signature}

« Un beau vernis, rien en dessous » (recherche de Northeastern/Khoury) :
- Se lit sans accroc mais ne dit rien de précis
- Verbeux tout en étant pauvre en information
- Cadres génériques au lieu d'exemples concrets
- Pourrait s'appliquer à n'importe quel sujet voisin

## Antipatterns de ton {#tone-anti-patterns}

- **Enthousiasme excessif :** « Fascinant ! », « Remarquable ! » - chaque sujet traité comme également passionnant
- **Excès de précautions :** « Il convient de noter que... », « On pourrait soutenir que... » - ne prend jamais de position définitive
- **Équilibre excessif :** « D'un côté... de l'autre... » même lorsqu'un côté a clairement raison
- **Marqueurs absents :** aucune opinion personnelle, aucune incertitude exprimée naturellement, aucun humour, aucune autocorrection

## Marqueurs spécifiques au russe {#russian-specific-markers}

### Marqueurs lexicaux {#word-markers}

**Verbes copules surutilisés :**
- « является » (est) - les humains l'emploient rarement dans un écrit informel ou semi-formel
- « выступает » / « служит » (sert de)
- « играет важную роль » (joue un rôle important)

**Constructions favorites :**
- « не просто..., а... » (non pas seulement... mais...) - la formule russe signature de ChatGPT
- « мощный » (puissant) - adjectif surutilisé
- Noms déverbaux partout : привлечение, обеспечение, тестирование

**Calques de l'anglais :** ordre des mots peu naturel pour le russe, copié sur la syntaxe anglaise. Le russe autorise un ordre SVO beaucoup plus libre : un ordre des mots trop rigide est suspect.

### Signes structurels {#structural-signs}

- Chaque paragraphe commence par un nom déverbal suivi de deux-points
- Ordre sujet-prédicat partout (le russe a un ordre des mots plus libre)
- Les paragraphes peuvent être réordonnés sans dommage : aucune chaîne logique
- Ponctuation parfaite, zéro irrégularité grammaticale

### Formules révélatrices {#indicator-phrases}

- « Я надеюсь, это помогло Вам » (J'espère que cela vous a aidé)
- « Конечно » / « Безусловно » en position d'ouverture
- « Вы абсолютно правы » (Vous avez absolument raison)
- « По состоянию на [дата] » (En date du [date])

## À quoi ressemble réellement l'écriture humaine {#what-human-writing-actually-looks-like}

- **Longueurs de paragraphes inégales** (certains d'une seule phrase, d'autres de dix)
- **Opinions affirmées** sans précaution
- **Exemples précis** avec noms, dates, chiffres - et non « considérez un scénario où... »
- **Autocorrection** (« En fait, ce n'est pas tout à fait juste... »)
- **Changements de registre** (du soutenu au familier et retour)
- **Digressions** qui ne servent pas parfaitement la thèse
- **Erreurs et corrections** qui montrent le cheminement de la pensée

## Liste de contrôle d'édition {#editing-checklist}

Avant publication :
- [ ] Aucun mot de niveau 1 (delve, crucial, comprehensive, etc.)
- [ ] Les longueurs de phrases varient nettement (mesurer la plus courte et la plus longue)
- [ ] Au moins une opinion personnelle par tranche de 500 mots
- [ ] Aucune structure de paragraphes symétrique
- [ ] Exemples précis avec noms, chiffres et dates
- [ ] Au moins un aveu d'incertitude ou de limite
- [ ] Pas plus de 2 mots de transition par page (Moreover, Furthermore)
- [ ] Au moins un endroit où vous n'êtes pas d'accord ou prenez position
- [ ] Aucune conclusion générique (« En conclusion, X est important pour Y »)

**Pour les articles techniques en particulier :**
1. Commencez par le problème que vous avez réellement rencontré, pas par un aperçu du sujet
2. Incluez les impasses : « J'ai essayé X mais cela a échoué parce que... »
3. Montrez les messages d'erreur, traces de pile et numéros de version exacts
4. Utilisez vos propres chiffres : « a pris 47 minutes sur mon MacBook M1 »
5. Contredisez quelque chose : prenez position
6. Mentionnez le moment : « à 2 h du matin, j'ai compris... »

## Différence fondamentale {#fundamental-difference}

**Spécificité contre généralité.**

Le texte humain est spécifique : il renvoie à des éléments exacts, prend position, commet des erreurs, laisse transparaître une personnalité.  
Le texte IA est général : il couvre toutes les bases, nuance tout, emploie les formulations les plus courantes, et produit un texte qui pourrait s'appliquer à n'importe quel sujet voisin.

L'axe spécifique/général est la dimension unique la plus fiable pour la détection.

## Pièges à éviter {#gotchas}

- **Les motifs IA évoluent après exposition.** « Delve » a fortement reculé après avoir été largement dénoncé. LLM et humains coévoluent : la liste de mots précise va changer. Les motifs structurels et de burstiness sont plus stables.
- **Les articles de blog « 500 mots IA à éviter » reprennent souvent ces mêmes motifs.** La plupart de ces listes sont elles-mêmes du contenu généré par IA sur le contenu généré par IA. Les sources académiques (Liang et al., Northeastern) sont plus fiables.
- **La détection de l'IA en russe diffère de celle en anglais.** Le signal des verbes copules (« является ») est beaucoup plus fort en russe que « is » en anglais, car le russe a rarement besoin d'une copule. L'ordre des mots calqué de l'anglais est un signal IA propre au russe, sans équivalent direct en anglais.

## Voir aussi {#see-also}

- [[natural-writing-style]]
- [[overused-words-phrases]]
- [[ai-text-detection]]
- [[structural-antipatterns]]
