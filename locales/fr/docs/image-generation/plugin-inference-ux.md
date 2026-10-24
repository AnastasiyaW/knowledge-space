---
title: "Expérience d'inférence des plugins ML : contrat d'état de l'hôte"
description: "L'expérience d'inférence des plugins ML est un contrat explicite sur l'état de l'hôte et du job : figer l'API de l'hôte, documenter les versions du snapshot et des modèles, le comportement d'annulation et de progression, les clés de cache et d'invalidation, la provenance des aperçus, le commit non destructif et la latence mesurée, plutôt que promettre une réactivité universelle."
category: techniques
tags: [plugin, inference, ux, caching, progress, cancellation, non-destructive, evidence]
aliases: ["ML Plugin Inference UX Patterns", "Inference UX"]
level: 3
source_sha256: e25834384a052289dec26ba5e95a898ceaf29446e54616c1076d05fbf71f8900
translation: machine
translated_at: '2026-10-24'
---
# Expérience d'inférence des plugins ML : contrat d'état de l'hôte {#ml-plugin-inference-ux-host-state-contract}

Une opération ML dans un hôte de création est un job qui dépend de l'état du
document, du modèle et de l'hôte. Un indicateur de chargement, un résultat en
cache ou un aperçu n'est fiable que si l'utilisateur peut savoir quel snapshot
de source il représente, s'il peut être annulé, et ce qui changera au moment du
commit. Ne promettez pas de seuil de latence universel : mesurez plutôt le
modèle exact, le périphérique, la classe de document, l'état à froid ou à
chaud, et la version de l'hôte.

## Définir des états de job observables {#define-observable-job-states}

Utilisez un modèle d'états dont les transitions sont visibles et auditables :

`Draft → queued → snapshot verified → preprocessing → inference → preview ready
→ user accepts → atomic non-destructive commit`

Les alternatives terminales incluent `cancelled`, `invalidated`, `failed` et
`review required`. Une modification du document, un changement de paramètres,
de modèle, de permissions ou une incohérence de source doit invalider les
aperçus dépendants plutôt que de les appliquer silencieusement plus tard.

Pour chaque job, enregistrez la politique de digest/composite de la source, la
version du document et des calques, l'état couleur/orientation/sélection, la
version du modèle/checkpoint/runtime, les paramètres, la frontière
matériel/fournisseur, les horodatages, le digest du résultat et l'état terminal.

## Respecter la frontière de l'hôte {#respect-the-host-boundary}

Les API de l'hôte déterminent le fonctionnement de la mutation du document, de
l'historique, de l'annulation et de la progression. Dans Photoshop UXP, les
commandes qui modifient le document nécessitent
[`executeAsModal`](https://developer.adobe.com/photoshop/uxp/ps_reference), et
l'[API d'exécution modale](https://developer.adobe.com/photoshop/uxp/2022/ps-reference/media/executeasmodal)
expose l'annulation et le rapport de progression. Ces éléments ne autorisent
pas pour autant un plugin à maintenir une portée modale pendant une inférence
distante, ni à appliquer un résultat une fois la source modifiée.

Effectuez la préparation sans risque avant d'obtenir un accès exclusif à la
mutation, lorsque l'hôte le permet. N'obtenez la transaction de l'hôte la plus
étroite et documentée que pour le commit explicite, relu au préalable. Préservez
la sémantique d'annulation/rétablissement et l'historique, et laissez les
données d'origine intactes.

## Ne mettre en cache que des intermédiaires attribuables {#cache-only-attributable-intermediates}

Une clé de cache doit inclure toutes les entrées susceptibles de modifier le
résultat : pixels source ou digest de composite immuable,
dimensions/recadrage/orientation, domaine colorimétrique, région ou masque
sélectionné, version du prétraitement, modèle/checkpoint/runtime, paramètres et
politique du fournisseur. Stockez la provenance de la sortie avec l'entrée de
cache. Un nom de fichier, un identifiant du document actif ou un échantillon
partiel de pixels ne suffit pas.

Déclarez la propriété, le chiffrement et la rétention, le budget de taille,
l'éviction et l'invalidation. Ne réutilisez jamais un intermédiaire entre
documents ou utilisateurs au seul motif qu'il semble similaire. Le préchargement
est un travail optionnel : attribuez-lui un budget, un chemin d'annulation et une
politique locale/distante explicite ; il ne doit ni envoyer le contenu source, ni
consommer un quota distant sans autorisation.

## Rendre les aperçus honnêtes {#make-previews-honest}

Indiquez qu'un aperçu est un brouillon, par tuiles, sous-échantillonné, mélangé,
obsolète ou approximatif, en précisant la propriété qui lui manque. Un curseur
qui mélange source et sortie est une approximation d'affichage, sauf si le modèle
a réellement été évalué à ce réglage. Affichez l'association entre source et
résultat, et proposez un rafraîchissement explicite lorsque les paramètres ou
l'état de la source diffèrent.

Avant le commit, comparez la sortie acceptée avec le snapshot enregistré, et
vérifiez les dimensions de la sortie, la politique alpha/masque, la conversion
colorimétrique, les zones protégées et la provenance du modèle. Si une
condition n'est pas remplie, conservez l'aperçu comme non committé et signalez
la raison.

## Mesurer l'expérience annoncée {#measure-the-claimed-experience}

Pour la version effectivement livrée, rapportez les distributions de latence à
froid et à chaud, le délai de file d'attente, le temps de réponse à l'annulation,
l'écart entre aperçu et résultat final, le taux de succès/échec du cache, la
pression mémoire, le taux d'erreur et le comportement de récupération de l'hôte.
Testez les grands documents, les changements rapides de paramètres,
l'annulation/rétablissement, les modifications de la source pendant la mise en
file d'attente, la réorganisation de la file, les défaillances hors ligne ou
fournisseur, et les actions concurrentes de l'hôte.

Ne remplacez jamais un échec par un autre modèle, une autre entrée de cache, un
autre service cloud ou un résultat obsolète. Le repli doit être explicitement
nommé, équivalent pour l'opération demandée, et visible par l'utilisateur.

## Pages connexes {#related-pages}

- [[tiled-inference]]
- [[low-vram-inference-strategies]]
- [[frequency-decomposition-editing]]
- [[diffusion-lora-training]]
