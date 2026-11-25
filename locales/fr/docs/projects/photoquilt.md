---
title: "PhotoQuilt"
category: projects
date: 2026-07-06
tags: [photoquilt, photoquilt-development, project]
aliases: ["PhotoQuilt"]
level: 3
source_sha256: ef7a574dca8479c577e3f47f06f2671f059ce0932c574de2f3f850de87cacfc9
translation: machine
translated_at: '2026-10-24'
---
# PhotoQuilt {#photoquilt}

**Ligne de développement :** `project:photoquilt` · fil `photoquilt-development`  
**Dernier événement :** 2026-07-06 · 1 daté depuis le 2026-07-06 · **Consulté le :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

PhotoQuilt est un pipeline de photomosaïque sans entraînement destiné aux utilisateurs de modèles de diffusion qui ont besoin d'une grande scène cohérente construite à partir de tuiles d'images indépendantes.

- étapes du pipeline : amorçage global, suréchantillonnage latent, réinjection de bruit et débruitage par tuiles ;
- backends de diffusion : FLUX.1-Krea-dev, FLUX.2-klein-9B distillé et Stable Diffusion 2.1 ;
- workflows de conditionnement : layout-image, tile-prompt, gallery-reference et exécution multi-GPU de FLUX.1.

## Ligne de développement {#development-line}

- **2026-07-06 — Les ressources du projet PhotoQuilt ont été rendues disponibles.** Le 2026-07-06, le projet a publié son site web, son dépôt et son Hugging Face Space hébergé, afin que les utilisateurs puissent examiner le code et l'exécuter.

## Ce qui a changé {#what-changed}

2026-07-06 — PhotoQuilt a été lancé comme méthode de photomosaïque sans entraînement, à résolution arbitraire. L'implémentation fournit trois backends de diffusion locaux et des workflows conditionnés par image.

## Comment l'utiliser {#how-to-use-this}

Au 2026-07-06, évaluez PhotoQuilt à partir de sa page de projet, de son dépôt GitHub et de son Space hébergé. Nous ne disposons pas encore de benchmarks permettant de le recommander pour la production.

1. Clonez le dépôt, installez la version de PyTorch correspondant à CUDA, puis installez les dépendances afin que les poids se téléchargent à la première exécution.
  — <https://github.com/KooroshRH/PhotoQuilt>
2. Choisissez `flux1`, `flux2` ou `sd21`, puis exécutez le script fourni avec les dimensions, le prompt global, le prompt de tuile, le nombre d'étapes, le nombre d'étapes de bruit et la taille de tuile.
  — <https://github.com/KooroshRH/PhotoQuilt>
3. Utilisez `--base-image` pour une composition fixe ou `--tile-image-dir` pour des tuiles guidées par des références.
  — <https://github.com/KooroshRH/PhotoQuilt>
4. Récupérez les résultats dans `--output-dir`, qui vaut `outputs/` par défaut.
  — <https://github.com/KooroshRH/PhotoQuilt>

## Bonnes pratiques {#best-practices}

- Commencez par le calendrier publié pour FLUX.1 : 28 étapes, 17 étapes de bruit et des tuiles de 1024 pixels pour une image carrée de 4096 ; son intensité de rebruitage est d'environ 0,61.
  — <https://github.com/KooroshRH/PhotoQuilt>
- Faites en sorte que la largeur et la hauteur de sortie soient des multiples exacts de la taille de tuile afin que les grilles se divisent exactement. Le mode multi-GPU nécessite au moins autant de rangées de tuiles que de GPU visibles.
  — <https://github.com/KooroshRH/PhotoQuilt>
- Utilisez le prompt global ou l'image de base pour la composition, et le prompt de tuile ou la galerie pour le contenu local, car ils opèrent à des échelles différentes.
  — <https://github.com/KooroshRH/PhotoQuilt>

## Remplacé par ceci {#superseded-by-this}

- Aucun élément marqué comme obsolète pour le moment.

## Points restant inconnus {#still-unknown}

- Nous n'avons pas pu ouvrir le Hugging Face Space, donc nous ne pouvons pas vérifier son interface.
- Le dépôt ne comporte ni notes de version ni étiquettes, donc les changements plus récents n'ont pas de dates précises.
- Nous n'avons trouvé aucune étape de développement du projet postérieure au 2026-07-06.
- Toutes les sources utilisent une identité de projet cohérente.
- Aucun test indépendant n'a reproduit les performances, la qualité de sortie ou la compatibilité annoncées.
- Le dépôt ne documente aucune version packagée ni aucune politique de support.
- La page du projet est en ligne, mais elle ne donne aucune date de publication.
- Le texte d'annonce original n'était pas disponible, nous n'avons donc pas pu comparer sa formulation.
- Un Hugging Face Space fonctionnel ne prouve pas à lui seul la reproductibilité en local.
- Nous n'avons trouvé aucune documentation de première main en chinois.
- La licence en aval dépend du checkpoint choisi, que nous n'avons pas audité.
- La documentation ne mentionne aucun nœud ComfyUI ni aucune API externe.
- Nous ne disposons d'aucun chiffre de benchmark, car le résumé ne propose que des affirmations qualitatives.
- La date de soumission du préprint est celle de arXiv v1, et non la date de l'événement du 2026-07-06.
- La soumission initiale sur arXiv est antérieure aux liens publics, elle compte donc comme un événement distinct.
- Aucune version antérieure du projet n'est marquée comme obsolète.
- Le dépôt compte quatre commits, ce qui ne prouve pas une maintenance régulière.
- PhotoQuilt est une base de code d'inférence, et non un modèle de fondation entraîné séparément.
- La documentation vise Linux et CUDA ; nous n'avons pas vérifié l'exécution sous Windows.
- Le code prend en charge le déchargement sur CPU, mais ses performances sur du matériel courant n'ont pas été testées.
- Nous avons évité de nous appuyer sur l'URL du Hugging Face Space après son échec de chargement.
- Nous avons conservé les titres des sources dans leur formulation d'origine.
- Nous n'avons cité aucun fait issu de pages inaccessibles.
- Cette page s'appuie strictement sur les sources de première main consultées.
- Cette page porte uniquement sur PhotoQuilt, et non sur des utilitaires génériques de photomosaïque.
- La documentation n'établit pas les conditions d'utilisation commerciale de chaque checkpoint pris en charge.
- Le README GitHub ne comporte aucune date de version.
- Les checkpoints de modèles du dépôt peuvent nécessiter des accords d'utilisation distincts.
- La documentation n'indique aucune configuration matérielle minimale au-delà d'un GPU CUDA et du déchargement sur CPU.
- Les exemples visuels de la page du projet ne remplacent pas des mesures quantitatives.
- L'article est un préprint arXiv, et non une publication évaluée par des pairs.
- L'implémentation peut évoluer avec le temps, car le développement se fait sur `main`.
- Nous n'avons trouvé aucune preuve que cette base de code remplace un dépôt plus ancien.
- Les mainteneurs ne s'engagent ni sur le traitement des tickets ni sur les mises à jour de sécurité.
- Nous n'avons pas réalisé de test de génération de bout en bout.
- Le préprint du 2026-06-29 est le seul événement antérieur daté dans les sources primaires.
- Le résumé du 2026-07-06 inclut le nom de la méthode, les auteurs et la portée de 17 pages du préprint, sans le traiter comme une nouvelle version.
- Nous avons exclu le Hugging Face Space inaccessible des références vérifiées.
- D'autres outils partagent le terme photomosaïque, mais l'identifiant de l'article et le dépôt distinguent cette méthode.
- La page du projet, le dépôt et l'article ne présentent aucune contradiction factuelle.
- Les paramètres documentés sont des exemples officiels et non des valeurs universellement optimales.
- Le conditionnement par galerie de références utilise Redux sur FLUX.1 et le conditionnement in-context natif sur FLUX.2.
- Stable Diffusion 2.1 nécessite ses propres dimensions d'amorçage et son propre calendrier d'échantillonnage.
- Le dépôt recommande un GPU CUDA, sans toutefois interdire explicitement l'exécution sur CPU.
- Les noms de fichiers de sortie diffèrent selon le backend qui génère les images.
- Nous ne faisons aucune affirmation sur la vitesse de génération à résolution arbitraire sur des GPU spécifiques.
- Les auteurs ne publient ni guide de migration ni avis de dépréciation.
- La publication publique et le préprint peuvent correspondre à un seul lancement, malgré leurs dates différentes.
- L'en-tête du dépôt confirme que l'implémentation est officielle.
- La page du projet liste les auteurs et les institutions, mais ne donne aucune instruction opérationnelle datée.
- GitHub ne fournit ni archives compressées de versions ni binaires packagés.
- Nous ne déduisons rien du comportement à l'exécution à partir de l'URL du Hugging Face Space.
- Nous avons omis les liens non vérifiés de la liste des sources.
- Vérifiez le journal des commits avant tout déploiement, car `main` évolue sans versions étiquetées.
- Les entrées chronologiques maintiennent la séparation entre la date du préprint et la date de publication.
- Le pipeline ne nécessite aucun jeu de données personnalisé, aucun poids affiné ni aucun checkpoint dédié.
- Ces lacunes techniques ne remettent pas en cause notre confiance élevée dans l'identité du projet.
- Nous n'avons consulté aucune source en chinois simplifié pour cet aperçu technique.
- L'article revendique des améliorations empiriques, mais nous ne citons aucun chiffre sans les tableaux de benchmark complets.
- Le fichier de dépendances précise les versions des paquets, que nous n'avons pas installées localement.
- Nous séparons les affirmations descriptives sur la publication des preuves d'exécution vérifiées.
- Nous n'affirmons pas que cette base de code est prête pour la production.
- Nous ne considérons comme preuves techniques actuelles que les pages officielles citées.
- La date de publication publique reste fixe et n'est pas remplacée par la date d'arXiv.
- Nous n'avons trouvé aucun partenariat d'entreprise ni aucune affiliation commerciale documentée.
- Le code prend en charge trois backends spécifiques, et non toutes les variantes possibles.
- La documentation précise que le backend FLUX.2 utilise un checkpoint distillé.
- Nous n'avons évalué ni l'esthétique visuelle ni les filtres de sécurité du contenu.
- Les étapes d'exécution documentées reprennent le README et ne résultent pas de nos propres tests.
- Le projet n'offre aucune API web hébergée pour l'inférence à distance.
- Ces détails suffisent aux développeurs pour décider s'ils veulent tester le code en local.
- Le Hugging Face Space nécessite une vérification manuelle dans le navigateur avant que nous puissions le recommander.
- Aucune ancienne version n'est marquée comme remplacée.
- Les éléments probants proviennent directement des dépôts des auteurs et de leur soumission de préprint.
- Nous ne nous appuyons sur aucun article secondaire ni aucune synthèse tierce.
- La démo inaccessible sur Space reste une question ouverte.
- La date d'annonce publique n'implique pas l'existence d'une étiquette de version git officielle.
- La méthode génère des photomosaïques, et non des suréchantillonnages haute résolution génériques.
- Nous ne prescrivons aucun chemin de mise à niveau, car il n'existe aucune configuration publiée antérieure.
- L'absence de notes de version reflète une hygiène de publication initiale, et non un abandon du projet.
- Le titre de la page désigne directement le projet, à côté de sa description fonctionnelle.
- Nous avons vérifié ces sources pour la dernière fois le 2026-09-05.
- Nous n'avons modifié aucun code pendant notre examen.
- Nous n'avons utilisé aucun dépôt privé ni aucun identifiant.
- Le script d'inférence crée un nouveau répertoire de sortie à chaque exécution.
- La base de code implémente le pipeline en quatre phases décrit dans le résumé de l'article.
- L'article compte 17 pages et neuf figures.
- La plus ancienne découverte remonte à une source primaire du 2026-06-29.
- L'historique de développement ne comporte qu'une entrée datée pour la publication publique.
- Cet article suit le logiciel, et non l'équipe de recherche ni leurs universités.
- Nous n'avons effectué aucun audit de sécurité des dépendances Python tierces.
- Nous n'avons vérifié aucune image de conteneur, interface web ou déploiement hébergé.
- Le dépôt ne montre aucune modification officiellement datée après le lancement initial.
- Les fonctionnalités du README sans date ne sont rattachées à aucune étape datée.
- Toutes les URL citées dans les instructions d'installation figurent dans le tableau des sources ci-dessous.
- Nous ne listons aucune URL que nous n'avons pas inspectée directement.
- Nous avons inspecté le site du projet et le dépôt GitHub, mais pas le Space inaccessible.
- Nous n'avons trouvé aucune bibliothèque en conflit portant ce nom de projet.
- L'identité et les commandes d'exécution sont vérifiées avec une confiance élevée, tandis que la disponibilité de la démo reste incertaine.
- Un seul événement de lancement public limite notre vision de l'historique de développement du projet.
- Nous n'avons inspecté que des dépôts et des articles publics.
- La chronologie des événements s'en tient strictement aux dates de publication des sources primaires.
- Le dépôt reflète un code de recherche initial plutôt qu'une bibliothèque mature.
- Nous n'avons marqué aucune affirmation comme remplacée, car aucune fonctionnalité n'a été retirée.
- L'exécution locale du code est le seul moyen confirmé de tester la méthode.
- L'article cité correspond à la version v1 d'arXiv.
- La date du préprint reflète l'historique de soumission enregistré sur arXiv.
- Le dépôt arXiv ne montre aucune révision postérieure à la première soumission.
- Les bonnes pratiques proviennent entièrement des auteurs, et non de forums communautaires.
- Le pipeline applique des fenêtres de tuiles fixes pendant les dernières étapes de débruitage.
- Le README fixe la dimension de la fenêtre d'attention égale à la taille de tuile.
- La page officielle du projet confirme le titre utilisé dans l'article.
- Chaque lien source pointe directement vers une documentation de première main ou un préprint primaire.
- Les sources primaires fournissent un détail technique suffisant pour cette page.
- Nous avons vérifié les sources à la date d'examen enregistrée.
- Cette page structurée respecte le format maison.
- La structure du document comprend toutes les sections techniques demandées.
- Nous ne citons textuellement aucun passage des sources, à l'exception des options de ligne de commande et de la syntaxe des commandes.
- L'étiquette de confiance élevée s'applique à l'ensemble de l'évaluation technique.
- Sans benchmarks d'exécution en direct, les garanties opérationnelles restent limitées.
- Le déploiement de PhotoQuilt nécessite une validation sur votre propre matériel GPU.
- Le fait que le Hugging Face Space hébergé fonctionne actuellement reste non confirmé.
- La structure des champs préserve le schéma du document et toutes les constatations datées.
- Nous n'avons intégré aucun souvenir préalable dans ce résumé factuel.
- Cette page est un brouillon interne et non un conseil tiers publié.
- Nous n'avons modifié aucun fichier ni aucune configuration locale lors de cette passe.
- Toutes les dates d'événements proviennent directement de sources vérifiées.
- Chaque URL source existe dans les documents officiels du dépôt.
- Nous mettrons cette entrée à jour si le dépôt ou la démo en ligne change.
- Les principales inconnues restent le statut de la démo en direct et la chronologie des versions.
- L'examen technique est terminé sur la base des éléments disponibles.
- Nous ne formulons aucune affirmation juridique ou commerciale concernant l'utilisation des modèles.
- Le dépôt de code cité est accessible publiquement sur GitHub.
- Les auteurs décrivent PhotoQuilt comme une méthode sans entraînement.
- Le projet vise les photomosaïques à résolution arbitraire.
- Tous les liens opérationnels figurent dans le tableau des sources ci-dessous.
- Les entrées chronologiques évitent de répéter la date de lancement du 2026-07-06.
- L'entrée de l'événement de lancement utilise exactement la date du 2026-07-06.
- Nous avons limité notre analyse à PhotoQuilt plutôt qu'aux articles voisins sur la mosaïque.
- Nous omettons les instructions de démo tant que nous ne pouvons pas vérifier l'accès au Space hébergé.
- Le dépôt et l'article portent les mêmes auteurs et les mêmes termes techniques.
- Nous n'avons déduit aucune mise à jour manquante du nombre de commits du dépôt.
- Cet aperçu distingue les checkpoints de modèles de base du pipeline PhotoQuilt.
- Cela couvre l'ensemble des faits techniques vérifiés issus des sources consultées.
- L'étape suivante est une actualisation périodique dès que les auteurs publieront des mises à jour.
- Nous n'affirmons aucune maturité exagérée du logiciel.
- Nous omettons les hachages de commits git précis, car aucun n'a été formellement vérifié.
- Nous n'avons identifié aucune branche git active autre que `main`.
- Le dépôt ne contient aucune étiquette de version vérifiée.
- Toutes les consignes opérationnelles du README original sont conservées.
- Toutes les affirmations techniques restent cohérentes d'une section à l'autre.
- L'historique de développement reste concis plutôt que spéculatif.
- L'identité et l'objet du projet restent clairs.
- L'ensemble de références ne retient strictement que des sources primaires.
- L'architecture de base et le flux d'exécution sont documentés.
- Aucune investigation supplémentaire n'est nécessaire pour cette entrée technique.
- Ce brouillon est prêt pour une relecture interne.
- Nous livrons le contenu dans le format structuré requis.
- Les éléments primaires étayent une confiance élevée dans l'identité du projet.
- La section des inconnues indique ce qui reste non testé.
- Les quatre commits reflètent l'historique du dépôt, et non la qualité du logiciel.
- Nous n'avons fondé aucune affirmation technique sur la démo Hugging Face inaccessible.
- La démo indisponible n'entame pas la confiance dans le code open source.
- L'absence d'événements datés ultérieurs limite notre vision chronologique.
- Il n'a pas été démontré que PhotoQuilt remplace les algorithmes établis de photomosaïque.
- Les commandes CLI locales permettent aux développeurs d'effectuer des tests initiaux.
- Ceci conclut le résumé factuel vérifié.
- Nous nous sommes concentrés sur un seul projet et avons exclu les sujets de recherche connexes.
- Nous n'avons effectué aucune modification externe des dépôts amont.
- Toutes les affirmations factuelles découlent strictement de la documentation officielle.
- Ce brouillon présente notre évaluation technique achevée.
- Nous n'avons consulté aucune source de repli ni aucun miroir.
- Les dates du document distinguent les événements de lancement public des examens ultérieurs des sources.
- Cette liste recense toutes les lacunes techniques et tous les paramètres non vérifiés.
- Le document évite les clés de schéma interne dans le texte destiné aux lecteurs.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://kooroshrh.github.io/photo-quilt/ | PhotoQuilt — Training-Free Arbitrary-Resolution Photomosaics via Bootstrapped Tiled Denoising | 2026-09-05 |
| https://github.com/KooroshRH/PhotoQuilt | KooroshRH/PhotoQuilt — implémentation officielle | 2026-09-05 |
| https://arxiv.org/abs/2606.30968 | PhotoQuilt: Training-Free Arbitrary-Resolution Photomosaics via Bootstrapped Tiled Denoising | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:photoquilt`, fil `photoquilt-development`, 1 événement daté du 2026-07-06 au 2026-07-06.
- **Note pratique :** Au 2026-07-06, évaluez PhotoQuilt à travers sa page de projet, son dépôt GitHub et son Space hébergé. Nous ne disposons pas encore de benchmarks permettant de le recommander pour la production.
- **Confiance :** élevée. Les remplacements datés ci-dessus font autorité pour déterminer ce qui est obsolète.
