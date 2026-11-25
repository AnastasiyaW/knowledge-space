---
title: "Liste de contrôle de révision pour la qualité du texte"
description: "Préserver les faits et le sens technique tout en améliorant la clarté, la structure et la mise en état de publication."
category: tools
tags: [writing, editing, checklist, verification, quality]
level: 4
source_sha256: c0adc70de1dd5788d0756d6f288e1f49fb404e4313b68a502c45affb9eb20a45
translation: machine
translated_at: '2026-10-24'
---
# Liste de contrôle de révision pour la qualité du texte {#editing-checklist-for-text-quality}

Utilisez cette liste de contrôle pour améliorer un document sans modifier ce que
ses preuves permettent d'affirmer. Périmètre vérifié le 2026-09-06 : références
techniques, tutoriels, analyses et comptes rendus d'incidents, y compris les
brouillons assistés par IA.

Un mot peu familier ou un rythme de phrase trop régulier n'est pas un défaut
factuel. Privilégiez l'exactitude et la tâche du lecteur plutôt que les scores
des détecteurs ou des quotas stylistiques.

## Préserver l'affirmation avant de modifier sa formulation {#preserve-the-claim-before-editing-its-wording}

Conservez la source originale et le brouillon accessibles pendant la révision.
Pour les affirmations importantes, identifiez les preuves et la portée exacte
de l'énoncé.

| Élément protégé | Modification risquée | Vérification requise |
|---|---|---|
| Comptage et dénominateur | Transformer 12 enregistrements vérifiés sur 40 en 12 enregistrements réussis | Préserver ce qui a été compté et ce qui reste non vérifié |
| Date historique | Remplacer une observation datée par « actuellement » | Conserver la date, sauf si de nouvelles preuves justifient une mise à jour |
| Modalité | Transformer « peut se rétablir » en « se rétablira » | Préserver l'incertitude et les conditions |
| Négation | Supprimer « ne pas » en raccourcissant une phrase | Comparer la proposition, et non seulement les mots-clés correspondants |
| Unités et versions | Supprimer une unité ou une version jugée encombrante | Conserver les conditions nécessaires à l'interprétation du résultat |
| Citation ou expérience personnelle | Inventer « nous avons testé » pour rendre la prose plus authentique | N'utiliser que des témoignages fournis, clairement attribués |
| Identifiant technique | Renommer une API ou un indicateur pour une prose plus fluide | Vérifier l'orthographe exacte dans la source concernée |

Les quantités inconnues restent inconnues. Un exemple hypothétique clairement
signalé est acceptable lorsqu'il sert le lecteur, mais il ne doit pas se faire
passer pour un résultat observé.

## Choisir la structure en fonction de la tâche du lecteur {#choose-the-structure-for-the-readers-task}

| Document | Ce qui doit être facile à trouver | Ce qui n'est pas obligatoire |
|---|---|---|
| Référence | Contrat, paramètres, contraintes, version, modes de défaillance | Anecdote, ouverture dramatique, opinion personnelle |
| Tutoriel | Prérequis, séquence exécutable, résultat attendu, reprise | Un benchmark ou un historique de projet inventé |
| Analyse | Question, preuves, critères de comparaison, limites | Sections de taille égale ou verdict prédéterminé |
| Compte rendu d'incident | Défaillance observée, cause, intervention, vérification | Un récit de succès bien ordonné lorsque la reprise est incomplète |

Supprimez les répétitions lorsqu'elles masquent ces éléments. Ne rallongez pas
un paragraphe et n'ajoutez pas de question rhétorique seulement pour que le
document paraisse moins régulier. Le [guide de ton de la documentation pour
développeurs de Google](https://developers.google.com/style/tone) encourage une
prose claire et directe, adaptée au lecteur ; il ne prescrit pas de tels quotas.

## Réviser par ordre de conséquence {#review-in-order-of-consequence}

1. Vérifier les affirmations non étayées ou contradictoires, ainsi que les omissions importantes.
2. Vérifier si le lecteur peut accomplir la tâche visée.
3. Vérifier les exemples, les identifiants, les liens et les conditions de version pertinentes.
4. Améliorer les formulations ambiguës et les répétitions inutiles.
5. Appliquer la charte éditoriale demandée sans altérer les quatre premiers résultats.

Une constatation éditoriale utile identifie le passage, explique sa conséquence
et propose une correction cohérente avec les preuves disponibles. « Ça sonne
comme une IA » ne désigne pas un défaut technique exploitable.

## Vérifier les exemples et les affirmations d'achèvement {#verify-examples-and-completion-claims}

Si un document contient du code, testez la portée exécutable annoncée avec
l'environnement d'exécution et les dépendances nommés. Signalez un fragment
illustratif comme tel ; n'impliquez pas qu'un service, une fixture, un
identifiant ou un modèle omis ait été exercé.

Gardez ces affirmations distinctes :

- Inspection de la source : une recommandation ou un chemin de code a été examiné.
- Vérification de la fixture : l'exemple fourni a réussi un test borné.
- Vérification de l'installation : les fichiers ou la configuration prévus ont atteint la cible.
- Vérification côté consommateur : l'outil ou le lecteur visé a chargé le résultat livré.
- Résultat en production : le flux de travail réel demandé s'est achevé dans ses conditions réelles.

Une fixture au vert ne valide pas le dernier élément. De même, une source d'article
valide ou un `git push` réussi ne prouve pas que les lecteurs peuvent voir la
nouvelle page.

## Utiliser l'automatisation pour des assertions précises {#use-automation-for-narrow-assertions}

Les contrôles automatisés peuvent détecter des liens cassés, un balisage
malformé, des nombres modifiés ou des identifiants protégés manquants. Leur
résultat se limite à ces assertions.

Une comparaison de nombres ne peut pas détecter tous les changements de sens :
« 12 échecs » et « 12 réussites » partagent le même nombre. Conservez une
relecture sémantique de l'affirmation et de sa source. Un signalement d'un
linter de prose doit inciter à l'inspection, et non au remplacement automatique
de mots.

N'utilisez pas le score d'un détecteur comme condition d'acceptation éditoriale.
L'étude de référence sur le [biais des détecteurs envers l'anglais non natif](https://arxiv.org/abs/2304.02819)
documente les limites des détecteurs et des échantillons évalués ; elle
n'établit pas de test universel de l'auteur actuel.

## S'arrêter lorsque le document demandé est prêt {#stop-when-the-requested-document-is-ready}

Une fois les défauts importants résolus et les vérifications demandées réussies,
arrêtez la révision cosmétique. Consignez une relecture sans modification lorsque
c'est approprié. Poursuivez toute étape de publication ou de livraison demandée
qui reste à accomplir : relire le texte ne suffit pas à achever une demande de
publication.

## Pièges à éviter {#gotchas}

- **Précision inventée :** un quota de chiffres ou d'anecdotes pousse à fournir des faits non étayés. Supprimez le quota, pas l'incertitude.
- **Affirmations historiques devenues actuelles :** remplacer une date par « maintenant » modifie silencieusement ses conditions de vérité. Conservez la date de la source ou obtenez de nouvelles preuves.
- **Passes éditoriales sans fin :** chaque passe trouve une nouvelle préférence personnelle. Rouvrez uniquement un défaut important ou une condition d'acceptation modifiée.
- **Réécrire de mémoire :** les conditions de la source disparaissent lors d'une réécriture fluide. Comparez l'affirmation révisée à la source réelle, non au souvenir qu'on en a.

## Voir aussi {#see-also}

- [[ai-text-detection]]
- [[technical-article-structure]]
- [[agent-evaluation]]
