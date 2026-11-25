---
title: "C++"
type: MOC
level: 3
source_sha256: 5392d0919d186ad7e39dc2c68fc389082e7769916b5cbb4ca58faf5060dafdaf
translation: machine
translated_at: '2026-10-24'
---
# C++ {#c}

## Langage de base {#core-language}
- [[scope-and-lifetime]] - Portée et durée de vie des variables
- [[object-lifetime]] - Durée de vie et construction des objets
- [[const-and-type-safety]] - Correction de const et sûreté des types
- [Error Handling - Exceptions and Alternatives](error-handling.md) - Gestion des erreurs avec les exceptions et alternatives

## Gestion de la mémoire {#memory-management}
- [[manual-memory-management]] - Gestion manuelle de la mémoire en C++
- [Smart Pointers and Memory Management](smart-pointers.md) - Pointeurs intelligents et gestion de la mémoire
- [[raii-resource-management]] - RAII et gestion des ressources
- [[move-semantics]] - Sémantique de déplacement et transmission parfaite

## Qt et QML {#qt-and-qml}
- [[qt-qobject-lifetime-and-qml-context-properties]] - Affinité des QObject, suppression différée et exposition bornée des propriétés de contexte QML

## C++ moderne (17/20/23) {#modern-c-172023}
- [[modern-cpp-features]] - Vue d'ensemble des fonctionnalités modernes de C++
- [[lambda-expressions]] - Expressions lambda
- [[concepts-and-constraints]] - Concepts et contraintes en C++20
- [[coroutines]] - Coroutines en C++20
- [[ranges-and-views]] - Ranges et vues en C++20

## Templates et généricité {#templates-generics}
- [[templates-and-concepts]] - Templates et concepts
- [[operator-overloading]] - Surcharge d'opérateurs

## POO et conception {#oop-design}
- [[inheritance-and-polymorphism]] - Héritage et polymorphisme
- [[design-patterns-cpp]] - Patrons de conception en C++ moderne
- [[function-pointers-and-callbacks]] - Pointeurs de fonction et callbacks

## STL et performance {#stl-performance}
- [[stl-containers]] - Conteneurs STL
- [[stl-algorithms]] - Algorithmes STL et ranges
- [[string-handling]] - Manipulation de chaînes de caractères
- [[file-io-streams]] - Entrées/sorties de fichiers et flux
- [Concurrency - Threads, Async, Atomics](concurrency.md) - Concurrence avec threads, async, atomics
- [Performance Optimization](performance-optimization.md) - Optimisation des performances

## Systèmes de build {#build-systems}
- [[cmake-build-systems]] - CMake et systèmes de build

## Références complémentaires {#additional-references}

- [[cross-platform-cpp-desktop-app]] - Référence sur les différences de plateforme lors de la création d'applications de bureau C++ (avec inférence ML) ciblant
- [[cross-platform-ml-inference]] - Référence pour la création d'applications de bureau C++ avec inférence ML ciblant à la fois Windows et macOS
- [[external-heartbeat-monitoring-for-native-process-crashes]] - Les gestionnaires d'exceptions standard en processus échouent souvent à capturer les plantages « silencieux » causés par des erreurs de bas niveau
- [[winhttp-async-client]] - Notifications de fin versus de progression, attentes bornées et sémantique d'annulation pour WinHTTP dans
