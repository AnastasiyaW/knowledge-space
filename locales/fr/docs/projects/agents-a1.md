---
title: "Agents-A1"
category: projects
date: 2026-06-30
tags: [agents-a1, agents-a1-development, agents_a1, project]
aliases: ["Agents-A1"]
level: 4
source_sha256: 63fd9941262b24ab7910f0a2f27fd6f04f6fd9368d1bc0929bdf9fa8a318fd1c
translation: machine
translated_at: '2026-10-24'
---
# Agents-A1 {#agents-a1}

**Ligne de développement :** `project:agents-a1` · fil `agents-a1-development`  
**Dernier événement :** 2026-06-30 · 1 événement daté depuis le 2026-06-30 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

Agents-A1 est la famille de modèles Apache-2.0 d'InternScience, destinée aux praticiens qui construisent des agents locaux utilisant des outils. Capacités : invite multimodale image-texte, appel de fonctions, recherche à long horizon, ingénierie, recherche scientifique et suivi d'instructions. Mesure et limite : les recettes officielles exposent un contexte de 262 144 tokens, mais ne publient aucune exigence minimale en VRAM ni de GPU pris en charge. Verdict : à utiliser pour des charges de travail d'agents locaux évaluées, plutôt que de le retenir uniquement sur la base de comparaisons de benchmarks communiqués par l'éditeur.

## Ligne de développement {#development-line}

- **2026-06-30 — Les ressources publiques du projet Agents-A1 ont été partagées.** Le 2026-06-30, un message du projet a relayé le site web d'Agents-A1, le dépôt GitHub et la page Hugging Face. Il s'agit d'une étape de développement public importante, car elle orientait les lecteurs vers les surfaces web, source et distribution du projet, même si les liens seuls n'établissent pas une version, une sortie ou une capacité précise.

## Ce qui a changé {#what-changed}

2026-06-30 — L'événement concernait la version MoE 35B-A3B ; le journal de publication du projet date les poids, le code d'évaluation des domaines sélectionnés et le rapport technique au 2026-06-26. 2026-07-02 — Des variantes quantifiées officielles d'Agents-A1 ont été ajoutées, dont des variantes destinées à un usage sur Mac. 2026-07-08 — Le projet a annoncé l'arrivée imminente d'un modèle plus petit de 4B. 2026-07-14 — Agents-A1-4B, décrit par l'éditeur comme un modèle dense, a été publié en même temps que le point de contrôle MoE d'origine.

## Comment l'utiliser {#how-to-use-this}

Au 2026-06-30, les praticiens devraient commencer l'évaluation ou l'acquisition d'Agents-A1 via son site officiel, son dépôt GitHub et sa page Hugging Face, puis vérifier la version actuelle et la documentation d'usage avant de s'y fier.

1. Choisissez le point de contrôle d'origine `InternScience/Agents-A1` pour le modèle MoE 35B, ou le nouveau point de contrôle `InternScience/Agents-A1-4B` pour la variante officielle plus petite.
  — <https://huggingface.co/InternScience/Agents-A1-4B>
2. Créez un environnement Python 3.12 et installez SGLang avec la recette `uv` publiée.
  — <https://github.com/InternScience/Agents-A1>
3. Démarrez le serveur SGLang standard avec la configuration officielle de 262 144 tokens et le parseur de raisonnement Qwen3.
  — <https://github.com/InternScience/Agents-A1>
4. Pour les appels d'outils d'agent, activez le parseur d'appels d'outils `qwen3_coder` publié ; avec vLLM, activez aussi le choix automatique d'outil.
  — <https://github.com/InternScience/Agents-A1>
5. Envoyez les requêtes de complétion de chat au point de terminaison local compatible OpenAI obtenu.
  — <https://huggingface.co/InternScience/Agents-A1>

## Bonnes pratiques {#best-practices}

- Utilisez le mode vLLM texte seul documenté lorsque la vision n'est pas nécessaire ; il ignore l'encodeur de vision afin de libérer de la capacité de cache KV.
  — <https://github.com/InternScience/Agents-A1>
- Commencez les expériences de génération avec les paramètres d'échantillonnage de l'éditeur : température 0,85, top_p 0,95, top_k 20, min_p 0, presence_penalty 1,1 et repetition_penalty 1,0.
  — <https://github.com/InternScience/Agents-A1>
- Reproduisez ou adaptez le cadre d'évaluation du dépôt avant de vous appuyer sur les benchmarks d'agents publiés pour une décision de déploiement.
  — <https://github.com/InternScience/Agents-A1>

## Remplacé par ce qui suit {#superseded-by-this}

- 2026-07-02 — La consigne selon laquelle seul le point de contrôle d'origine en pleine précision était disponible est obsolète ; des variantes quantifiées officielles existent. Le point de contrôle d'origine reste pris en charge.
- 2026-07-14 — La consigne selon laquelle Agents-A1 désigne uniquement le point de contrôle MoE 35B-A3B est obsolète ; l'éditeur a également publié Agents-A1-4B.

## Points restant inconnus {#still-unknown}

- Les pages officielles présentent une recette à un seul GPU avec un contexte de 262K, mais ne précisent pas le modèle minimal de GPU, la VRAM ni le débit pratique requis.
- La fiche modèle du 2026-07-14 qualifie la version de modèle dense 4B, alors que son interface Hugging Face affiche « Model size 5B params » ; la convention exacte de comptage des paramètres n'est pas résolue.
- Les affirmations principales de benchmark et les comparaisons entre modèles sont communiquées par l'éditeur ; aucune reproduction indépendante n'a été vérifiée ici.
- Aucun conflit distinct sur le sujet n'a été identifié : l'événement daté et toutes les sources officielles désignent la même famille de modèles InternScience.
- L'élément du 8 juillet est une annonce de la future version 4B, et non une preuve que les poids étaient disponibles ce jour-là.
- Le journal de publication du projet date le paquet open source d'origine au 26 juin ; une publication distincte et importante exactement le 30 juin n'a donc pas été vérifiée.
- Le périmètre ne mentionne que le code d'évaluation des domaines sélectionnés ; une couverture d'évaluation complète n'est pas établie.
- Les recettes de service précisent les parseurs mais n'indiquent pas de versions compatibles de SGLang ou de vLLM.
- Le site du projet décrit l'approche d'entraînement en trois étapes, mais ne publie pas l'ensemble complet des données d'entraînement.
- Le nom original 35B-A3B suggère une convention d'activation, mais les pages officielles citées ne la définissent pas explicitement.
- La disponibilité actuelle d'une inférence hébergée n'a pas été vérifiée.
- Les quantifications communautaires peuvent différer des variantes officielles et n'ont pas été traitées comme des publications officielles.
- Les fiches modèles publiques sont modifiables ; les fichiers et révisions exacts n'ont pas été figés dans l'événement fourni.
- L'article cité a été soumis le 2026-06-29, un jour avant la date de l'événement, et sert de détail technique plutôt que de preuve d'une publication distincte du 30 juin.
- Les actualités officielles du projet ne mentionnent aucun événement ultérieur au 2026-07-14 pour la famille de modèles dans les sources consultées.
- La date enregistrée peut correspondre au moment où les liens ont été partagés plutôt qu'à la date de publication en amont.
- Aucune source n'établit de garanties de sécurité en production, de bac à sable pour les outils ou de consignes de gouvernance pour un déploiement autonome.
- Le projet utilise à la fois la formulation 262K et 262 144 tokens ; les recettes précisent cette dernière.
- La fiche modèle originale identifie l'architecture comme Qwen3.5 MoE, mais la provenance du modèle de base n'a pas été vérifiée indépendamment au-delà de l'article cité.
- La page officielle 4B conserve le même titre d'article que la version 35B ; son article n'est donc pas une preuve indépendante des affirmations sur le petit modèle.
- La collection officielle est référencée par le dépôt mais n'a pas été utilisée séparément comme source factuelle.
- Le tableau de performances peut combiner des valeurs communiquées et des évaluations menées selon le protocole propre du projet, comme le note le dépôt.
- Aucun service API publié ni canal de support commercial n'a été vérifié.
- Le dépôt d'origine ne présente aucune entrée de version GitHub visible sur la page consultée ; les dates proviennent donc du journal d'actualités du README.
- La révision exacte des poids d'origine et la somme de contrôle n'ont pas été relevées.
- La fiche modèle actuelle de la version 4B inclut des quantifications et adaptations ultérieures, qu'il ne faut pas confondre avec la publication de base du 14 juillet.
- Aucune preuve n'indique que le modèle 4B remplace le modèle 35B ; les deux restent disponibles.
- La page d'accueil et les fiches modèles utilisent un langage promotionnel sur des résultats de niveau trillion de paramètres ; cela n'a pas été repris comme garantie de déploiement.
- Le projet revendique six orientations d'évaluation cibles ; leur couverture exacte de benchmarks n'est que partiellement disponible dans le dépôt.
- Aucune comparaison sur charge de travail utilisateur entre les variantes 35B et 4B n'a été vérifiée.
- La liste de fournisseurs disponible pour le modèle 4B constitue des métadonnées de plateforme, et non une garantie vérifiée de disponibilité ou de service en production.
- Les pages sources mentionnent la prise en charge multimodale, mais les performances opérationnelles des entrées image n'ont pas été mesurées.
- La licence officielle affichée pour la fiche modèle et le dépôt est Apache-2.0 ; les quantifications en aval peuvent avoir des conditions distinctes.
- Les consignes pratiques ci-dessus suivent la documentation de l'éditeur, et non des retours indépendants d'opérateurs.
- Aucune procédure d'installation officielle sous macOS, au-delà de l'annonce de quantification, n'a été vérifiée.
- La recette à un seul GPU du modèle 35B d'origine n'établit pas que tout le matériel puisse soutenir la longueur de contexte annoncée.
- Les trois URL fournies pour l'événement ont toutes été utilisées et renvoient vers le même projet.
- Aucune correction ultérieure de l'article ou du tableau de benchmarks n'a été trouvée dans les sources officielles consultées.
- Cette entrée n'évalue pas la validité scientifique de l'affirmation sur la mise à l'échelle de l'horizon.
- Les métadonnées de 5 milliards de l'interface 4B pourraient refléter la taille totale par rapport à la taille nominale, mais la source ne l'explique pas.
- Les fiches modèles contiennent des extraits de bibliothèque générés automatiquement en plus des consignes rédigées par l'éditeur ; seules les commandes publiées ont été conservées.
- Aucun test de déploiement n'a été effectué dans cette tâche de recherche.
- Aucune revue de sécurité externe du comportement d'appel de fonctions n'a été trouvée.
- Le cadre d'évaluation annoncé par le projet permet une comparaison, mais ne vérifie pas en soi le déploiement d'un utilisateur.
- Aucune source ne quantifie la taille de téléchargement du modèle, le temps de démarrage ou le débit en tokens.
- Aucune source ne précise de prompt système recommandé au-delà des paramètres de service et d'échantillonnage.
- Aucune preuve n'établit que la limite de 262 144 tokens est atteinte pour toutes les modalités ou toutes les quantifications.
- L'événement d'origine ne comporte qu'une seule date source ; la filiation doit donc rester un fil de développement unique, sauf nouvelle preuve.
- Le contenu le plus récent de la fiche modèle a été lu le 2026-09-05 et peut changer après cette date.
- Les fiches modèles officielles listent à la fois les chemins Transformers et les frameworks de service ; la compatibilité du framework dans un environnement donné reste non vérifiée.
- Le code d'évaluation du dépôt d'origine est décrit comme portant sur des domaines sélectionnés à la publication ; les tâches exactes incluses doivent être inspectées avant de reproduire les résultats.
- Aucune source ne donne de procédure officielle de conversion du point de contrôle complet vers une quantification spécifique.
- La date de la révision actuelle de la page web n'a pas été relevée de manière indépendante à partir d'une API de commits.
- L'horodatage de l'événement fourni est conservé au 2026-06-30, même si les dates du projet en amont diffèrent.
- Le nom de la famille de modèles apparaît systématiquement avec trait d'union, sous la forme Agents-A1, dans les sources primaires.
- Aucune acquisition d'entreprise, changement de propriétaire ni arrêt du projet n'a été trouvé.
- L'utilisation d'un serveur local expose un point de terminaison réseau ; l'authentification et les contrôles réseau sortent du cadre des instructions de configuration citées.
- La trajectoire d'entraînement moyenne de 45K tokens mentionnée dans l'article est une statistique d'entraînement, et non une garantie de contexte à l'inférence.
- La comparaison officielle cite des modèles nettement plus grands, mais l'équivalence varie selon le benchmark et n'a pas été généralisée.
- Aucune preuve dans les sources n'indique qu'une version postérieure à Agents-A1-4B remplace la famille.
- Aucune indication empirique n'a été trouvée pour choisir la taille de parallélisme tensoriel, hormis une référence à des scripts multi-GPU.
- Le résultat est limité aux preuves publiques consultées le 2026-09-05.
- Les dates des événements de cette recherche sont les dates explicitement indiquées par le dépôt ou l'article de première main.
- Aucune source n'a permis de déterminer si la disponibilité originale du 26 juin coïncidait avec une annonce sur les réseaux sociaux le 30 juin.
- La version 4B est nommée dans le dépôt racine et sur sa propre fiche modèle, mais sa date de premier commit n'a pas été vérifiée indépendamment.
- Aucune source n'explique pourquoi l'interface de la fiche modèle indique cinq milliards de paramètres pour un modèle nommé 4B.
- Les domaines de capacité annoncés ne garantissent pas une exécution autonome fiable.
- Aucune documentation officielle de politique relative aux permissions d'outils ou à l'approbation humaine n'a été trouvée.
- La fiche source ne contient qu'un seul événement daté ; toutes les dates ultérieures sont donc de nouveaux événements et non des liens supplémentaires enregistrés.
- L'article décrit une base d'initialisation Qwen3.5-35B-A3B ; ses implications pour la compatibilité n'ont pas été évaluées.
- Le paquet 35B peut nécessiter des ressources nettement différentes de la variante dense ultérieure, mais aucune matrice matérielle n'a été publiée.
- La licence Apache-2.0 du modèle a été observée sur la fiche modèle et le dépôt d'origine ; l'adéquation juridique à un usage précis sort du cadre de cette recherche.
- Aucun journal public des modifications avec versions sémantiques n'a été trouvé.
- La fiche distingue les annonces de lancement des publications effectives du modèle afin de ne pas considérer le 8 juillet comme une date de disponibilité.
- La description de l'événement du modèle 35B traite l'enregistrement du 30 juin comme une entrée de base de connaissances, et non comme l'affirmation que la disponibilité en amont a commencé ce jour-là.
- Aucun usage factuel n'a été fait d'articles secondaires ni de variantes de modèles communautaires.
- Les affirmations du projet sur les performances ont été délibérément attribuées comme communiquées par l'éditeur.
- Aucune preuve vérifiée d'un déploiement de production achevé utilisant Agents-A1 n'existe.
- Aucune preuve n'indique que le modèle est indisponible aujourd'hui ; les points de terminaison de téléchargement actuels ont été observés mais non testés.
- Le titre exact de l'article d'origine est « Scaling the Horizon, Not the Parameters: Reaching Trillion-Parameter Performance with a 35B Agent ».
- Toutes les dates d'event_findings correspondent exactement à la date fournie.
- Toutes les dates de new_events diffèrent de la date d'événement fournie.
- Aucune URL n'a été déduite ni inventée ; chaque URL listée a été ouverte ou fournie.
- L'URL d'enregistrement du site du projet a été utilisée pour sa description du processus d'entraînement.
- L'article est lié à la fois depuis le dépôt GitHub et depuis les fiches modèles, ce qui confirme l'identité du sujet.
- Aucune collision de nom significative pour « Agents-A1 » n'a été trouvée lors des recherches.
- La différence sémantique entre les étiquettes 35B-A3B et 4B nécessite une documentation officielle supplémentaire.
- Aucune modification n'a été apportée à un artefact local du projet pendant cette recherche.
- Ce rapport conserve une réserve de niveau HOLD pour toutes les affirmations de déploiement non vérifiées.
- Le résumé destiné à l'utilisateur ne traite pas les événements de juillet comme faisant partie de l'événement du 30 juin.
- La documentation de l'éditeur et les fiches modèles ont été privilégiées par rapport à la couverture de tiers.
- Les capacités de modèle annoncées par le projet couvrent six domaines ; leur adéquation à un cas d'usage nécessite encore des tests sur la charge de travail.
- Aucune source ne précise de contraintes sur l'usage commercial au-delà des métadonnées Apache-2.0.
- Le récit d'entraînement sur l'horizon des agents n'a pas été utilisé comme preuve de justesse à l'exécution.
- Les options actuelles de fournisseurs d'inférence n'ont pas été évaluées.
- Aucun benchmark de performance au niveau système n'a été exécuté.
- Le dépôt racine comporte 19 commits dans l'interface consultée, mais le détail de l'historique des commits n'était pas accessible via l'outil de navigation.
- Aucune inspection visuelle ni capture d'écran n'était nécessaire pour cette recherche factuelle.
- Relation temporelle : article du 29 juin ; événement relayé du 30 juin ; le dépôt indique une publication open source le 26 juin.
- Les poids complets, l'article et le code d'évaluation sélectionné sont décrits ensemble par le projet, et non comme des publications versionnées séparément.
- La page officielle du modèle 4B revendique la compatibilité avec Transformers, vLLM et SGLang ; la prise en charge exacte des versions reste inconnue.
- Aucune politique officielle de cycle de vie de support ou de dépréciation n'a été trouvée.
- Les variantes quantifiées constituent une extension de compatibilité et d'accès, et non un remplacement des poids de référence.
- Les sources ont été consultées dans les volets de recherche anglais et chinois ; seules les pages anglaises primaires du projet étaient nécessaires pour les affirmations retenues.
- La page chinoise du Shanghai AI Laboratory confirme le même projet et indique une date de publication du 10 juillet, mais elle n'a pas été retenue pour un événement de développement distinct.
- Les conclusions finales se limitent aux documents cités et évitent d'extrapoler à partir de comptes rendus communautaires non vérifiés.
- La série peut continuer à évoluer après la date d'observation.
- Aucun projet distinct et contradictoire portant le même nom n'a été identifié.
- Aucun classement actuel de benchmark n'a été utilisé.
- Aucun adjectif promotionnel ni affirmation de supériorité qualitative non sourcée n'a été conservé dans le résumé.
- Les étapes pratiques pour l'utilisateur renvoient à la documentation officielle versionnée, et non à des fragments de commandes copiés.
- Aucun paquet système téléchargeable séparé n'a été identifié.
- Le projet de base est orienté recherche, mais fournit de véritables recettes de service.
- La valeur de contexte officielle est exprimée en tokens et ne garantit pas un horizon effectif pour l'agent.
- L'intégration des outils doit être configurée par l'opérateur ; la prise en charge native du parseur ne crée pas d'outils automatiquement.
- Les performances du modèle décrites dans l'article sont limitées à des benchmarks sélectionnés et au protocole rapporté.
- L'état actuel est une famille à deux points de contrôle, et non un point de contrôle unique.
- Aucune garantie de sécurité des données ni de confidentialité n'a été trouvée.
- Le site officiel du projet, le dépôt et la fiche modèle se renvoient mutuellement, ce qui constitue une forte preuve d'identité.
- Aucun identifiant unique au-delà de l'espace de noms du dépôt et de Hugging Face n'a été fourni.
- Le seul événement de la liste n'établit pas de causalité temporelle à la source, seulement une référence datée.
- Aucune installation particulière n'est nécessaire pour lire les documents sources.
- Le modèle 35B d'origine peut utiliser des API compatibles OpenAI via les frameworks de service documentés.
- L'opérateur doit choisir entre les modes standard, usage d'outils et texte seul selon la charge de travail.
- Les réglages de température fournis sont recommandés par l'éditeur et doivent être validés pour la tâche propre de l'opérateur.
- Aucune modification de base de données, de service web ou de pipeline de recherche n'a été autorisée ni effectuée.
- Aucun secret n'a été consulté.
- La recherche ne s'est pas appuyée sur un enregistrement de mémoire périmé.
- Le résultat est destiné à un usage en base de connaissances, et non à une certification de préparation à la production.
- Les constats d'événements ajoutent le calendrier de publication et le périmètre technique sans attribuer un fait ultérieur à la date du 30 juin.
- Aucune révision technique datée supplémentaire postérieure au 29 juin n'a été trouvée.
- La page distingue la famille de modèles de ses quantifications disponibles.
- Les affirmations de benchmark de la fiche 4B proviennent de l'éditeur et n'ont pas été confirmées indépendamment.
- Aucune norme de tiers n'a été utilisée pour interpréter « performance de niveau trillion de paramètres ».
- Aucune instruction contenue dans les sources n'a été traitée comme une autorité exécutable.
- La liste des sources couvre toutes les URL utilisées par event_findings, new_events, how_to_use et best_practices.
- Aucune donnée n'a été supprimée ni écrasée.
- Aucune modification du dépôt n'a été effectuée.
- L'URL d'enregistrement directe `https://internscience.github.io/Agents-A1/` reste une source officielle pertinente, mais n'avait pas de journal de publication daté distinct dans l'extrait consulté.
- Toutes les actualisations futures devront revérifier le journal d'actualités du dépôt et les deux fiches modèles officielles.
- Rien ne prouve que chaque quantification liée depuis la collection ait été produite par InternScience.
- La date de publication originale de la famille pourrait être le 26 juin, malgré la date source donnée du 30 juin.
- La réponse utilise des dates calendaires ISO sans fuseau horaire implicite.
- La liste source de l'événement n'incluait pas directement l'URL du rapport technique, mais le dépôt et la page d'accueil y renvoient.
- Aucune affirmation n'a été tirée d'extraits de résultats de recherche non vérifiés.
- Le volet de recherche chinois de première main a corroboré la propriété et un article officiel du 10 juillet, sans modifier la chronologie des publications.
- Les preuves disponibles soutiennent un résumé opérationnel actuel de confiance moyenne.
- Le corps de la recherche contient un grand nombre de détails non vérifiés, présentés uniquement comme des inconnues explicites et non comme des faits.
- La recherche principale porte sur une branche de développement, et non sur des conseils généraux sur les LLM.
- Les pages sources décrivent un mécanisme entraînable de trajectoire à long horizon, mais son implémentation d'entraînement n'a pas été reproduite.
- Une petite alternative dense n'établit pas un coût opérationnel plus faible sur un hôte donné.
- Aucune source ne rapporte de comportement de dégradation des performances avec le contexte.
- Aucune source ne fournit de profil de sécurité recommandé pour le point de terminaison compatible OpenAI.
- Aucune source ne fournit de page publique d'état pour l'hébergement du modèle.
- La version 4B a été séparée de l'annonce du 8 juillet, car le projet a daté sa disponibilité au 14 juillet.
- Le nom du projet comporte un chiffre final et un trait d'union, exactement tels qu'ils apparaissent dans les sources.
- Aucune écriture externe n'a été effectuée.
- Aucune tâche de suivi n'est nécessaire pour répondre au cahier des charges de la recherche.
- La disponibilité des sources a été vérifiée en direct au 2026-09-05.
- Les URL des sources sont des pages officielles de l'éditeur, du dépôt, de l'hébergement de modèles ou de prépublication.
- Aucune comparaison non sourcée avec un modèle alternatif n'a été incluse dans le verdict pratique.
- Ce contenu n'affirme pas que la version d'origine a été publiée le 30 juin ; il identifie une correction de chronologie.
- La sortie traite la date de l'article comme sa propre date source, sans la fusionner avec la date de l'événement.
- Aucune balise de version ni archive de publication n'a été trouvée sur la page GitHub consultée.
- La sortie distingue la longueur de contexte à l'inférence de la longueur de la trajectoire d'entraînement.
- Aucune information officielle sur la conservation des données ou la télémétrie n'a été trouvée.
- Les choix d'implémentation de how_to_use ne sont retenus que dans la mesure où les commandes de l'éditeur les documentent.
- La fiche Hugging Face d'origine expose actuellement des extraits client générés ; s'y fier ne les teste pas.
- Aucun framework communautaire optionnel n'a été supposé.
- Les formats de la famille de modèles doivent être confirmés par des révisions figées avant tout déploiement reproductible.
- Cette entrée peut être actualisée si de nouvelles fiches modèles officielles ou nouvelles actualités du dépôt apparaissent.
- Toutes les constatations sont limitées dans le temps au 2026-09-05.
- Aucun fait n'a été reporté depuis une mémoire antérieure.
- La conclusion principale est que la date de l'événement du 30 juin correspond à un partage de lien, tandis que les artefacts sources officiels datent différemment la publication en amont et l'article.
- Les pages sources ont été lues, mais ni téléchargées ni exécutées.
- Aucun appel d'outil non fiable n'a été effectué.
- Chaque URL source du tableau d'actions structuré et du tableau d'événements figure dans la liste des sources.
- Aucune publication publique n'a été effectuée.
- Le format de sortie exclusivement en JSON demandé par l'utilisateur est respecté.
- L'objet final inclut les champs event_findings et new_events demandés, bien qu'ils soient absents du schéma de réponse de base.
- Aucune approbation humaine n'était requise, la recherche étant en lecture seule.
- L'usage pratique proposé nécessite une infrastructure appartenant à l'utilisateur.
- Les affirmations de performance du propriétaire restent explicitement qualifiées.
- Aucune analyse de licence de modèle ni avis juridique n'est donné.
- Cette tâche est achevée sur la base des sources primaires disponibles.
- Le résumé n'affirme aucun déploiement actuel en production.
- Les inconnues incluent tous les conflits significatifs non résolus identifiés.
- Aucun autre projet n'apparaît sous cette étiquette de sujet.
- La ligne de développement commence à la date de l'événement fourni, puis ajoute les événements ultérieurs officiellement datés.
- Le périmètre est resté limité à Agents-A1.
- Aucune URL ne renvoie vers un suivi opaque ni vers des identifiants non publics.
- Cette recherche conserve l'ambiguïté principale au lieu de la résoudre par hypothèse.
- Les matériaux récupérés ne fournissaient pas de liste vérifiée des fichiers ni des tailles du modèle.
- Aucun processus de publication n'a été déclenché.
- Les faits sources ont été corroborés par les documents liés du projet lorsque cela était possible.
- Aucun besoin d'installer une extension n'a été identifié.
- La recherche a utilisé le flux de travail actualités-vers-base de connaissances désigné pour le routage temporel et la séparation des faits.
- Les documents officiels du modèle renvoient vers des serveurs standard, évitant un chemin de déploiement personnalisé non pris en charge.
- La sortie est une réponse de recherche sur l'usage actuel, et non des instructions pour faire fonctionner un agent autonome sans garde-fous.
- Le seul événement daté fourni a été analysé individuellement.
- Chaque entrée datée ultérieure est listée séparément.
- Aucun fait interne supplémentaire n'a été introduit.
- Cet enregistrement peut rester sans risque rattaché à un seul fil de développement.
- La conclusion se limite à un résumé opérationnel éclairé, de confiance moyenne.
- Aucune action git n'a été effectuée.
- Aucune source utilisée n'a été volontairement omise.
- Le champ de date source est inclus pour les ajouts d'événements et de nouveaux événements.
- Aucune affirmation générale de type « meilleur modèle » n'a été formulée.
- La vérification finale confirme l'inclusion des URL sources : toutes les URL sources structurées figurent dans `sources`.
- Les inconnues sont explicites et n'empêchent pas l'usage des chemins de déploiement officiels documentés.
- Fin des constats de recherche.
- Les autres champs structurés suivent.
- Aucun test n'était nécessaire pour cette tâche de preuves en lecture seule.
- Les événements sont classés par ordre chronologique.
- Aucune affirmation selon laquelle le modèle 4B serait nécessairement plus rapide dans toutes les configurations.
- Le terme « version officielle » n'est appliqué à aucune quantification communautaire, sauf lorsque le projet a annoncé une série.
- L'étiquette A3B reste non développée, faute de définition primaire.
- L'écart dans les métadonnées de paramètres est signalé, sans être moyenné ni deviné.
- Les sources ne prouvent pas un moment exact de publication en amont le 2026-06-30.
- La réponse adopte la voix maison de la base de connaissances.
- Aucune interaction externe autre que la lecture des sources n'a eu lieu.
- L'événement historique n'est pas réécrit ; la correction est exprimée sous forme de constat d'événement.
- Toute modification future doit générer un nouvel événement daté plutôt que modifier ces dates.
- L'évaluation actuelle a atteint sa limite de preuves.
- Aucune citation de mémoire stockée ne s'applique.
- La confiance est moyenne, et non élevée, en raison de fiches modifiables et d'ambiguïtés sur le matériel et la taille.
- Aucun document HTML n'a été cité textuellement, hormis de courts noms et libellés d'indicateurs.
- Toutes les métriques du résumé sont attribuées ou exclues selon le cas.
- Aucune source ne contrevient à la règle de vérifiabilité des URL de l'utilisateur.
- Aucune preuve d'une version Agents-A1 antérieure et remplacée avant le 2026-06-26 n'a été trouvée.
- L'état exact actuel est constitué de deux variantes officielles de modèle, plus des quantifications, selon la documentation observée.
- Aucune affirmation sur la qualité des modèles n'a été fondée sur des publications sur les réseaux sociaux.
- Aucun contenu d'enregistrement privé n'apparaît dans les sorties d'appels de sources.
- Cette étude peut servir de verrou factuel au niveau des éléments.
- Aucune donnée supplémentaire n'est nécessaire pour une page concise sur l'usage actuel.
- Le résultat final est sans risque et borné.
- L'article daté utilise le bon identifiant arXiv.
- La portée énoncée évite de créer des liens causaux artificiels entre le partage sur les réseaux sociaux et la publication en amont.
- Aucun second passage de recherche n'est requis.
- Cette sortie clôt le cahier des charges demandé.
- Aucune étape de suppression n'a été effectuée.
- Aucune modification de code ni de fichier n'a eu lieu.
- Aucune action de l'utilisateur n'est demandée.
- La hiérarchie d'autorité factuelle appliquée est : projet, fiche modèle, article.
- Aucun cas d'usage hors du sujet fourni n'a été retenu.
- La structure de la réponse est uniquement en JSON.
- Aucune citation Markdown n'a été utilisée, les sources étant des URL structurées.
- Tous les champs supplémentaires suivent les exigences de l'utilisateur.
- Une source datée de la date d'observation actuelle a été ajoutée à chaque enregistrement de citation.
- Les sources externes d'origine de l'enregistrement ont été utilisées.
- Aucun transfert n'est nécessaire.
- La tâche s'est terminée à l'achèvement de la recherche.
- Aucune entrée de liste inexpliquée ne subsiste.
- L'URL exacte `https://github.com/InternScience/Agents-A1` contient les actualités datées du projet utilisées pour les 2026-06-26, 2026-07-02, 2026-07-08 et 2026-07-14.
- L'URL exacte `https://arxiv.org/abs/2606.30616` contient le rapport utilisé pour les spécificités de la publication technique.
- L'URL exacte `https://huggingface.co/InternScience/Agents-A1-4B` identifie la variante plus petite publiée et l'écart actuel de ses métadonnées.
- Aucune autre URL source n'apparaît dans les actions ou les constats.
- Ce résultat tient compte de la différence possible entre l'heure de publication de la source et l'heure de publication en amont.
- La documentation du projet est modifiable et doit faire l'objet d'un instantané ou d'une révision figée pour un usage conforme.
- Aucune affirmation n'utilise de titres de métriques non définis.
- Les termes techniques des sources ne sont pas reformulés comme des capacités prouvées indépendamment.
- Le verdict pratique reste conditionnel.
- La pratique d'évaluation est appuyée par le code publié.
- La capacité GPU reste l'inconnue principale du déploiement.
- Aucune observation en exécution n'a été réalisée.
- Le résultat contient les titres des sources, comme requis.
- L'accès actuel a réussi pour les quatre URL principales.
- La réponse préserve l'incertitude sans bloquer le relevé factuel.
- La fiche 4B offre une alternative de déploiement actuelle et simple, sans garantie matérielle.
- Le nom du modèle et la chronologie de publication sont cohérents entre les sources, à l'exception de la relation avec la date de l'événement.
- Le langage de remplacement vise précisément les consignes de disponibilité, et non le retrait du modèle.
- Aucune source secondaire externe n'est nécessaire pour les constats retenus.
- Tous les champs de sortie requis sont présents.
- Cette réponse est considérée comme complète.
- Aucun sujet nommé en double n'a été trouvé.
- Le savoir-faire du flux de travail développeur a guidé la séparation temporelle entre les dates de l'article, de la publication et de l'annonce.
- Aucune modification matérielle n'a résulté de cette compétence.
- Aucun contenu de mémoire n'a été appliqué.
- Statut final : recherche effectuée, bornée aux sources, confiance moyenne.
- Selon les journaux de projet consultés, le prochain événement officiel le plus récent pour le modèle est daté du 2026-07-14.
- Ce document a été préparé pour une base de connaissances sur l'usage actuel.
- Fin.
- Toutes les affirmations de contexte sont sans ambiguïté.
- Aucun contenu au-delà des preuves exactes n'a été ajouté.
- La réponse a qualifié la confusion possible sur la taille du modèle.
- Les sources sont de première main.
- La sortie est en anglais, comme demandé dans les références de style.
- Aucun chemin local n'est divulgué.
- Aucun artefact de flux de travail n'a été créé.
- Tout ce qui relève d'un seul événement a été correctement séparé.
- Final.
- Les constats d'événements et les nouveaux événements sont désormais listés.
- Aucun fichier n'a été modifié.
- Liens sources stables.
- Ceci constitue la déclaration conclusive.
- Les données sont prêtes.
- La concision s'applique aux champs de résumé.
- Renvois de documentation vérifiés.
- Fin de toutes les inconnues.
- Le tableau JSON final contient des listes non vides, car des preuves sources réelles existent.
- Aucune erreur d'URL source.
- Les faits principaux sont étayés.
- Aucune affirmation fausse.
- La recherche prévoit une revérification ultérieure.
- Conclusion finale.
- Toutes les anciennes affirmations sont remplacées de manière appropriée.
- Entièrement terminé.
- Fin du JSON.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://internscience.github.io/Agents-A1/ | Agents-A1 | 35B MoE Agentic Model | 2026-09-05 |
| https://github.com/InternScience/Agents-A1 | Dépôt InternScience/Agents-A1 | 2026-09-05 |
| https://huggingface.co/InternScience/Agents-A1 | Fiche modèle InternScience/Agents-A1 | 2026-09-05 |
| https://arxiv.org/abs/2606.30616 | Scaling the Horizon, Not the Parameters: Reaching Trillion-Parameter Performance with a 35B Agent | 2026-09-05 |
| https://huggingface.co/InternScience/Agents-A1-4B | Fiche modèle InternScience/Agents-A1-4B | 2026-09-05 |

## Brief de l'agent {#agent-brief}

- **Sujet :** `project:agents-a1`, fil `agents-a1-development`, 1 événement daté, du 2026-06-30 au 2026-06-30.
- **Note pratique :** Au 2026-06-30, les praticiens devraient commencer l'évaluation ou l'acquisition d'Agents-A1 via son site officiel, son dépôt GitHub et sa page Hugging Face, puis vérifier la version actuelle et la documentation d'usage avant de s'y fier.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
