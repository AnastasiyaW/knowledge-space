---
title: "Durée de vie des QObject Qt et propriétés de contexte QML"
description: "Règles de suppression liées à l'affinité de thread et politique de migration bornée pour les propriétés de contexte QML dans Qt 6."
tags: [cpp, qt, qml, qobject, lifetime]
level: 4
source_sha256: 91ed85c38fe743f8aa5b5543a899c1a4fc06190d8bf9432b561822236509ad4d
translation: machine
translated_at: '2026-10-24'
---
# Durée de vie des QObject Qt et propriétés de contexte QML {#qt-qobject-lifetime-and-qml-context-properties}

Dans Qt 6, la durée de vie d'un objet est régie par la propriété de l'objet (ownership), son affinité de thread et l'état de la boucle d'événements. L'exposition dans un contexte QML ajoute un contrat de durée de vie distinct : le contexte ne possède pas le QObject injecté.

## Examiner la durée de vie, pas seulement `deleteLater()` {#review-the-lifetime-not-just-deletelater}

Avant d'accepter un chemin de nettoyage, identifiez le propriétaire de l'objet, son affinité actuelle, si le thread propriétaire peut traiter les événements différés et ce qui met fin à ce thread.

| Situation | Conclusion de revue correcte |
| --- | --- |
| Le parent et l'enfant vivent dans un même thread | Le parent possède et supprime l'enfant. Le parent et l'enfant ne peuvent pas avoir des affinités de thread différentes. |
| L'objet reçoit du travail en file d'attente | Son gestionnaire d'événements s'exécute dans le thread de son affinité, pas nécessairement dans le thread appelant. |
| Un autre thread demande le nettoyage | La suppression directe est dangereuse, sauf si la durée de vie et le traitement des événements sont synchronisés. Privilégiez le chemin de démantèlement documenté, dans le thread d'affinité de l'objet. |
| `deleteLater()` appelé avant le démarrage d'une boucle d'événements | Qt supprime l'objet une fois cette boucle démarrée. |
| `deleteLater()` appelé après l'arrêt de la boucle d'événements principale | Qt ne supprime pas l'objet. L'arrêt nécessite une décision de nettoyage plus tôt. |
| Objet vivant dans un thread worker sans boucle en cours d'exécution | Un objet ayant reçu `deleteLater()` est détruit lorsque ce thread se termine. |

La règle générale « pas de boucle d'événements, donc pas de suppression » est fausse. Ce qui compte, c'est la phase du cycle de vie : Qt documente des résultats différents avant le démarrage, après l'arrêt de la boucle principale et à la fin d'un thread worker. [QObject](https://doc.qt.io/qt-6/qobject.html) et [Threads and QObjects](https://doc.qt.io/qt-6/threads-qobject.html) définissent ces cas.

### Démantèlement d'un objet worker {#worker-object-teardown}

Gardez séparés l'objet QThread et son worker. L'objet QThread a l'affinité du thread qui l'a créé ; il n'est pas le thread worker lui-même.

Le schéma de worker documenté connecte `QThread::finished()` à `QObject::deleteLater()` du worker. Ce schéma ne remplace ni l'annulation, ni un protocole de fin de traitement, ni un séquencement correct : demandez la fin du traitement par le chemin de livraison propre au worker, laissez le thread se terminer et attendez avant de détruire les objets qui possèdent ce thread ou en dépendent. Ne bloquez pas le thread créateur d'une manière qui empêche l'exécution de son chemin de fin en file d'attente.

## L'exposition dans un contexte QML comporte deux mutations distinctes {#qml-context-exposure-has-two-separate-mutations}

Les propriétés de `QQmlContext` sont des noms détenus par le contexte. Ce ne sont pas des propriétés de `QObject`. Ajouter ou remplacer un tel nom avec `setContextProperty()` modifie le contexte et peut forcer la réévaluation des liaisons de ce contexte après la création des objets.

Un QObject injecté dans le contexte est différent. Ses valeurs `Q_PROPERTY` peuvent changer via leurs signaux `NOTIFY`, sans ajouter ni remplacer une propriété de contexte. Traitez ces cas comme des questions de revue distinctes :

| Modification | Question de revue |
| --- | --- |
| Ajouter, remplacer ou modifier l'objet ou la propriété du contexte | Toute la configuration du contexte était-elle terminée avant la création des objets QML ? |
| Mettre à jour une propriété d'un QObject injecté existant | La `Q_PROPERTY` a-t-elle le bon signal `NOTIFY`, la bonne affinité de thread et la bonne durée de vie du propriétaire ? |

`QQmlContext` indique que les mises à jour des propriétés d'un objet de contexte sont observées via le signal de notification de la propriété, alors que définir l'objet de contexte ou ajouter des propriétés de contexte après la création force la réévaluation des liaisons. [QQmlContext](https://doc.qt.io/qt-6/qqmlcontext.html) documente ces deux comportements.

### Exposition de compatibilité bornée {#bounded-compatibility-exposure}

L'exposition de contexte existante, réalisée avant le chargement, peut constituer une frontière de compatibilité plutôt qu'un déclencheur de réécriture automatique. Gardez-la bornée : injectez avant `setSource()` ou la création du composant, documentez les noms attendus par la racine QML, faites en sorte que le propriétaire de l'objet injecté survive au moteur QML, et ne modifiez pas la structure du contexte après le démarrage.

`setContextProperty()` ne transfère pas la propriété du QObject injecté ; son propriétaire C++ doit survivre à l'utilisation QML. Pour les nouvelles API réutilisables, privilégiez les propriétés de l'objet racine, les types enregistrés ou les singletons. Les propriétés de contexte créent des dépendances non déclarées et sont invisibles pour les outils QML en compilation anticipée. Voir [Embedding C++ Objects into QML with Context Properties](https://doc.qt.io/qt-6/qtqml-cppintegration-contextproperties.html).

## Liste de contrôle de revue {#review-checklist}

- Consignez l'affinité et le propriétaire de chaque QObject de longue durée, y compris ses enfants.
- Pour chaque suppression différée, indiquez si la boucle concernée n'a pas encore démarré, est en cours d'exécution, s'est arrêtée, ou se termine avec un thread worker.
- Suivez la fin de traitement, l'annulation, la terminaison du thread et la destruction, dans cet ordre ; une seule ligne de connexion ne constitue pas un protocole d'arrêt.
- Traitez chaque nom de contexte QML comme une dépendance d'API implicite. Consignez son fournisseur, son propriétaire et le point, avant la création des objets QML, où il est injecté.
- Utilisez une propriété de QObject adossée à `NOTIFY` pour un état vivant stable ; ne remplacez pas un nom de contexte pour transmettre des changements d'état ordinaires.

## Pièges courants {#gotchas}

- **Appeler `deleteLater()` pendant l'arrêt :** La boucle d'événements principale peut déjà être arrêtée, la suppression différée n'aura alors jamais lieu. Décidez de la propriété et du démantèlement avant la sortie de la boucle.
- **Supprimer depuis le thread créateur un QObject déplacé :** L'affinité a suivi le QObject ; un `delete` direct inter-threads peut entrer en concurrence avec la livraison des événements. Utilisez le cycle de vie du worker et un chemin de suppression sûr depuis le thread propriétaire.
- **Remplacer une propriété de contexte pour les mises à jour d'état courantes :** Cela modifie le contexte et peut réévaluer toutes les liaisons. Exposez un QObject avec `Q_PROPERTY` et `NOTIFY` lorsque la structure est stable et que seules les valeurs changent.
- **Supposer que QML possède un pointeur injecté :** `QQmlContext` ne prend pas la propriété. Un objet sur la pile n'est valide que tant que sa portée C++ survit à la vue ou au moteur qui l'utilise.
- **Considérer l'injection de contexte comme une colle anodine et invisible :** Le fichier QML a une dépendance non déclarée que `qmllint`, le serveur de langage QML et le Quick Compiler ne peuvent pas résoudre à l'avance.

## Limites {#limitations}

Ce document est une référence de revue, non une preuve à l'exécution pour une application quelconque. Il ne choisit ni le protocole d'annulation, ni la frontière de module QML, ni l'ordre d'arrêt d'une application. Vérifiez le graphe réel des affinités, les connexions de signaux, la propriété de la boucle d'événements et le comportement au démarrage et à l'arrêt dans la build cible.

## Voir aussi {#see-also}

- [[object-lifetime]]
- [[scope-and-lifetime]]
- [[concurrency]]
- [[smart-pointers]]
