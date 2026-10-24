---
title: "Refactorisation pilotée par les frontières"
description: "Choisir l'extraction, les interfaces et le travail de migration à partir des frontières de propriété et de consommation observées, puis vérifier que le comportement demandé fonctionne toujours."
tags: [architecture, refactoring, interfaces, domain-driven-design, testing]
level: 4
source_sha256: 6f245f4bad70012613caddb988c7a2b9d4c4d8470b77bcdabafad40ee7bf4c7e
translation: machine
translated_at: '2026-10-24'
---
# Refactorisation pilotée par les frontières {#boundary-driven-refactoring}

**Périmètre vérifié : 2026-09-06.** Les décisions de refactorisation doivent reposer sur une raison concrète : une responsabilité qui évolue indépendamment, une dépendance qui doit être contrôlée, une erreur de propriété ou un contrat de consommation que la structure actuelle rend illisible. La longueur d'un fichier et un score de propreté peuvent aider à localiser les zones à inspecter. Ni l'un ni l'autre ne démontrent qu'une couche supplémentaire est nécessaire.

Cette référence propose une politique de décision d'ingénierie. Elle ne prescrit ni limite universelle de taille de fichier, ni nombre de classes, ni hiérarchie d'héritage, ni nombre de relectures. L'objectif est une implémentation maintenable du comportement accepté, y compris le travail d'intégration nécessaire pour le rendre utilisable.

## Identifier la frontière avant de choisir l'abstraction {#identify-the-boundary-before-choosing-the-abstraction}

Commencez par l'opération modifiée. Identifiez ses entrées, son résultat, le propriétaire de son état, ses appelants, ses effets externes et son comportement en cas d'échec. Demandez-vous ensuite quelle responsabilité nécessite un contrat distinct.

| Signal observé | Modification candidate | Éléments qui la justifient |
|---|---|---|
| un calcul répété a une signification cohérente unique | extraire une fonction nommée | les appelants partagent la même sémantique et le même comportement en cas d'erreur |
| la politique métier évolue indépendamment de l'orchestration | séparer la politique du flux applicatif | une règle réelle ou un historique de modifications identifie le propriétaire de la politique |
| plusieurs implémentations prises en charge doivent satisfaire un même consommateur | définir une interface ou un port étroit | les implémentations réelles et les besoins des appelants s'accordent sur le contrat |
| une frontière de plugin ou de binaire exige une surface stable | isoler le contrat de compatibilité | les consommateurs pris en charge, la propriété, le versionnement et la sémantique d'échec sont connus |
| un effet externe empêche un test ciblé | exposer une couture étroite au niveau de cet effet | le test isole une dépendance réelle sans remplacer le comportement testé |
| un grand fichier contient des cycles de vie sans rapport | découper selon la responsabilité et la propriété | les exigences distinctes d'état, de libération des ressources ou de dépendances peuvent être nommées |
| le fichier est simplement long | examiner sa cohésion avant de restructurer | aucune extraction n'est justifiée tant qu'une frontière réelle ou un problème de maintenance n'a pas été identifié |

Plusieurs implémentations constituent une justification pour une interface, et non une condition préalable à toute interface. Une implémentation unique peut tout de même se trouver derrière un contrat de plugin obligatoire ou une frontière d'effet externe. Inversement, deux classes similaires ne partagent pas nécessairement une abstraction stable.

L'héritage n'est approprié que si l'objet dérivé peut satisfaire le contrat de la classe de base, y compris en matière de durée de vie et de comportement en cas d'échec. Partager quelques lignes d'implémentation ne suffit pas. Une fonction utilitaire ou un collaborateur composé peut exprimer cette réutilisation sans imposer d'obligations de substitution.

## Placer le comportement métier là où ses invariants peuvent être garantis {#put-domain-behavior-where-its-invariants-can-be-enforced}

Conservez le comportement local à l'état dont il protège les invariants, lorsque cela correspond à un modèle métier cohérent. Un service de domaine convient à une opération métier qui n'appartient pas naturellement à une entité ou à un objet valeur, y compris les règles impliquant plusieurs entités ou agrégats. Un service applicatif coordonne un cas d'usage, les transactions et les interactions externes. Ce sont des responsabilités différentes, et non une règle selon laquelle tout comportement doit se trouver dans des classes de service. [Conception pilotée par le domaine tactique](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/tactical-domain-driven-design)

Prenons par exemple une fonctionnalité d'export d'image. Il s'agit d'un exemple de conception hypothétique, et non d'une implémentation mesurée dans un produit :

- une spécification d'export valide ses propres contraintes de dimensions et de format ;
- un composant de politique colorimétrique décide de la politique de conversion prise en charge ;
- une opération applicative obtient l'image, applique la politique sélectionnée et écrit le résultat ;
- un adaptateur de sortie prend en charge les effets sur le système de fichiers ou le stockage distant.

Ne créez pas chaque composant simplement parce que la liste existe. Dans une implémentation de petite taille, une fonction et un adaptateur d'effet peuvent couvrir les frontières réelles. Découpez davantage lorsque des propriétaires, des politiques ou des consommateurs différents rendent le contrat utile. Conservez les comportements transversaux nécessaires dans les critères d'acceptation, plutôt que de déclarer un succès au seul motif que les classes compilent séparément.

## Faire correspondre les dépendances de build au contrat {#make-build-dependencies-match-the-contract}

Une séparation au niveau du code source reste incomplète si le build expose encore les dépendances d'implémentation à tous les consommateurs. Dans CMake, les exigences `PRIVATE` s'appliquent à la construction de la cible, les exigences `INTERFACE` aux consommateurs, et les exigences `PUBLIC` aux deux. Choisissez la portée en fonction de ce dont les consommateurs ont besoin, en particulier de ce qu'exigent les en-têtes publics. Les exigences d'utilisation doivent représenter des besoins réels, et non des préférences sans rapport. [Spécification de build et exigences d'utilisation de CMake](https://cmake.org/cmake/help/latest/manual/cmake-buildsystem.7.html)

Une dépendance utilisée uniquement par un fichier d'implémentation est un candidat à une liaison privée. Si l'API publique expose des types issus de cette dépendance ou si ses en-têtes la requièrent, masquer cette exigence peut casser les consommateurs. La preuve appropriée est une construction réelle d'un consommateur à partir de l'interface déclarée de la cible, et non un build réussi qui hérite accidentellement de chemins d'inclusion globaux.

Cette distinction n'impose pas une nouvelle cible CMake pour chaque classe. Ajoutez une cible lorsqu'elle constitue une frontière réelle de build, de distribution, de propriété ou de dépendances.

## Achever la migration des consommateurs {#finish-the-consumer-migration}

Une extraction n'est pas livrée tant que des appelants connus utilisent encore le chemin cassé ou que le remplacement est inaccessible. Recensez les consommateurs au niveau de la frontière modifiée et préservez les conditions de compatibilité dont ils dépendent.

| Frontière | Éléments de migration pertinents |
|---|---|
| fonction interne | les appelants connus compilent et les vérifications de comportement concernées réussissent |
| API de bibliothèque partagée | les consommateurs pris en charge se construisent et respectent le contrat convenu de propriété et d'erreur |
| schéma de fichier ou de message | le producteur et le consommateur s'accordent sur la version, l'interprétation et le comportement en cas d'échec |
| état persistant | des données existantes représentatives restent lisibles ou disposent d'un chemin de migration vérifié |
| point de terminaison déployé | une vérification d'intégration autorisée atteint la version cible et observe son résultat |

Un test canari en production est pertinent lorsque le changement accepté inclut une frontière de service déployé. Ce n'est pas un prérequis universel pour l'extraction d'une fonction locale. De même, un test unitaire est insuffisant lorsque le résultat demandé dépend d'un consommateur déployé indépendamment.

Conservez l'ancien chemin tant que les preuves de migration requises ne sont pas disponibles. Sa suppression constitue une modification distincte, avec ses propres conditions de compatibilité et d'autorisation. Ne changez pas silencieusement de fournisseur ou d'emplacement de données pour faire réussir une vérification.

## Sélectionner un ensemble de vérifications suffisant {#select-a-sufficient-verification-set}

Utilisez un exemple en échec lorsque la refactorisation corrige un défaut observé. Conservez des vérifications pour les contrats que la modification pourrait invalider : forme du résultat, propriété, sémantique des erreurs, transitions d'état et comportement réel des consommateurs. Un simple nettoyage du code source, sans changement de comportement, peut nécessiter une vérification différente d'une réparation de cycle de vie.

Consignez quelle preuve correspond à quelle révision et à quelle frontière. La compilation établit une propriété de build ; une fixture établit ses assertions ; un justificatif d'intégration établit l'interaction observée dans cet environnement. Aucun de ces éléments n'établit automatiquement le résultat complet du produit. Voir [[agent-evaluation]] et [[testing-and-quality]].

Une fois qu'une vérification réussit, ne la relancez que si une modification ultérieure ou une nouvelle observation rend son résultat antérieur insuffisant. Poursuivez les autres travaux acceptés restant à terminer, mais n'ajoutez pas de couches ni de cycles de relecture simplement parce que la branche courante est verte.

## Pièges courants {#gotchas}

- **Substitution par le nombre de lignes :** découper un fichier cohérent en de nombreux fichiers peut conserver le même couplage tout en rendant la navigation plus difficile. Examinez la responsabilité et la propriété avant de choisir le découpage.
- **Interface avant la sémantique :** une interface dont la propriété, l'annulation ou le comportement en cas d'erreur ne sont pas spécifiés déplace l'incertitude sans la résoudre.
- **Inflation des classes de service :** sortir toutes les méthodes d'une entité peut rendre plus difficile la garantie des invariants métier. Distinguez l'orchestration du comportement métier.
- **Intégration entièrement simulée :** des tests qui remplacent les deux côtés d'une frontière modifiée peuvent réussir alors que les consommateurs réels restent incompatibles.
- **Fuite de configuration globale du build :** les builds des consommateurs peuvent sembler sains parce que des chemins d'inclusion globaux masquent une interface de cible incomplète.
- **Retrait prématuré :** supprimer un ancien point d'entrée sans avoir vérifié ses appelants transforme un nettoyage structurel en échec de compatibilité.

## Limites {#limitations}

Cette politique ne remplace ni l'analyse métier, ni les engagements de compatibilité, ni un travail d'optimisation de performance mesuré. Certaines frontières établies sont justifiées par des contraintes de plateforme ou d'organisation qui ne sont pas visibles dans un seul fichier. Consignez ces contraintes avant de fusionner ou de remplacer ces frontières. Aucun seuil universel de taille ou de complexité ne permet d'établir qu'une architecture est correcte.

## Références associées {#related-references}

- [[architecture-documentation]] — consigner la frontière, la décision, les alternatives et le contrat de consommation.
- [[cmake-build-systems]] — cibles de build et propagation des dépendances.
- [[object-lifetime]] — exigences de durée de vie qu'une abstraction doit préserver.
- [[agent-evaluation]] — distinguer les preuves issues du code source, des fixtures, de l'installation et du flux de travail du consommateur.
