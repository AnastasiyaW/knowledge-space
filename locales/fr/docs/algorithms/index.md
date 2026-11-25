---
title: "Algorithmes et structures de données"
type: MOC
level: 2
source_sha256: d316ab52fa72b977d5430928a540c1ab8e20644086a95c740d9d8bb85821c69b
translation: machine
translated_at: '2026-10-24'
---
# Algorithmes et structures de données {#algorithms-data-structures}

## Complexité et théorie {#complexity-theory}
- [[complexity-analysis]] - Notation Big-O, complexité en temps et en espace, méthodes d'analyse des boucles et de la récursion
- [[amortized-analysis]] - Coût moyen par opération sur des séquences, exemple du tableau dynamique
- [[complexity-classes]] - P, NP, NP-complet, NP-difficile, réductions entre problèmes

## Tri et recherche {#sorting-searching}
- [[sorting-algorithms]] - Tableau comparatif de tous les tris, tri par insertion, fusion, rapide et par base, avec code
- [[searching-algorithms]] - Recherche linéaire, recherche dichotomique, recherche de motifs KMP
- [[two-pointer-technique]] - Two-sum, vérification de sous-séquence, motifs à pointeurs convergents et parallèles

## Programmation dynamique {#dynamic-programming}
- [[dynamic-programming-fundamentals]] - Concepts de la PD, mémoïsation et tabulation, identification des récurrences
- [[dp-sequence-problems]] - LCS, distance d'édition, LIS, word break, entrelacement de chaînes
- [[dp-optimization-problems]] - Sac à dos, rendu de monnaie, house robber, découpe de tige, produit matriciel en chaîne
- [[dp-grid-problems]] - Problème de partition, carré maximal, comptage de chemins, PD combinatoire

## Fondements des graphes {#graph-fundamentals}
- [[graph-representation]] - Liste d'adjacence ou matrice, terminologie, compromis de complexité des opérations
- [[graph-traversal-bfs-dfs]] - DFS et BFS avec code, graphes implicites, BFS multi-sources, problèmes sur grille
- [[trees-and-binary-trees]] - Définitions des arbres, parcours d'arbres binaires, arbres couvrants

## Algorithmes sur les graphes {#graph-algorithms}
- [[shortest-path-algorithms]] - Dijkstra, Bellman-Ford, Floyd-Warshall, plus court chemin dans un DAG, Johnson
- [[minimum-spanning-trees]] - Algorithmes de Prim et de Kruskal, propriété de coupe
- [[topological-sort]] - Tri topologique par DFS et algorithme de Kahn, chemin critique, applications aux DAG
- [[network-flow]] - Flot maximal et coupe minimale, Ford-Fulkerson, Edmonds-Karp, Dinic, couplage biparti
- [[union-find]] - Union-find (ensembles disjoints) avec compression de chemin et union par rang

## Problèmes avancés sur les graphes {#advanced-graph-problems}
- [[graph-coloring]] - Nombre chromatique, test de bipartition, coloration gloutonne, NP-complétude
- [[eulerian-hamiltonian-paths]] - Chemins et circuits eulériens, chemins hamiltoniens, algorithme de Hierholzer
- [[traveling-salesman-problem]] - TSP exact (Held-Karp) et approximations (plus proche voisin, Christofides)

## Références complémentaires {#additional-references}

- [[backtracking]] - Exploration systématique de l'espace des solutions par construction incrémentale de candidats et abandon
- [[bit-manipulation]] - Opérations sur les bits individuels des entiers
- [[data-structures-fundamentals]] - Opérations de base des structures de données et analyse de complexité - tableaux, tableaux triés avec recherche dichotomique
- [[dynamic-programming]] - Fondements de la récursion, mémoïsation (descendante), tabulation ascendante et reconnaissance de la PD
- [[greedy-algorithms]] - Construction de solutions pas à pas en effectuant le choix localement optimal à chaque étape
- [[hash-tables]] - Structure de données associant des clés à des valeurs via une fonction de hachage
- [[heap-priority-queue]] - Tas binaire : arbre binaire complet satisfaisant la propriété de tas
- [[problem-patterns]] - Approche systématique des problèmes algorithmiques - processus d'entretien en 7 étapes, motifs courants
- [[recursion-fundamentals]] - Fonction qui s'appelle elle-même pour résoudre des instances plus petites du même problème
- [[sliding-window]] - Maintenir une fenêtre (sous-tableau ou sous-chaîne contigu) qui glisse sur l'entrée, en s'étendant et se contractant
- [[string-algorithms]] - Algorithmes de recherche, de correspondance et de manipulation de chaînes de caractères
- [[trees-and-graphs]] - Arbres binaires de recherche, tas et files de priorité, tries (arbres de préfixes), représentation des graphes, et
