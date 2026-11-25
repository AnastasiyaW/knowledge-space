---
title: "Algorithmen & Datenstrukturen"
type: MOC
level: 2
source_sha256: d316ab52fa72b977d5430928a540c1ab8e20644086a95c740d9d8bb85821c69b
translation: machine
translated_at: '2026-10-24'
---
# Algorithmen & Datenstrukturen {#algorithms-data-structures}

## Komplexität & Theorie {#complexity-theory}
- [[complexity-analysis]] - Big-O-Notation, Zeit- und Speicherkomplexität, Analysemuster für Schleifen und Rekursion
- [[amortized-analysis]] - Durchschnittliche Kosten pro Operation über Folgen von Operationen, Beispiel mit dynamischem Array
- [[complexity-classes]] - P, NP, NP-vollständig, NP-schwer, Reduktionen zwischen Problemen

## Sortieren & Suchen {#sorting-searching}
- [[sorting-algorithms]] - Vergleichstabelle aller Sortierverfahren, Insertion-, Merge-, Quick- und Radix-Sort mit Code
- [[searching-algorithms]] - Lineare Suche, binäre Suche, KMP-Mustersuche
- [[two-pointer-technique]] - Two-Sum, Prüfung auf Teilfolge, konvergierende und parallele Zeigermuster

## Dynamische Programmierung {#dynamic-programming}
- [[dynamic-programming-fundamentals]] - DP-Konzepte, Memoization vs. Tabulation, Erkennen von Rekurrenzen
- [[dp-sequence-problems]] - LCS, Editierdistanz, LIS, Word Break, verschachtelte Strings
- [[dp-optimization-problems]] - Rucksackproblem, Münzwechsel, House Robber, Stangenschneiden, Matrixkettenmultiplikation
- [[dp-grid-problems]] - Partitionsproblem, maximales Quadrat, Zählen von Pfaden, Kombinatorik mit DP

## Graphen-Grundlagen {#graph-fundamentals}
- [[graph-representation]] - Adjazenzliste vs. Adjazenzmatrix, Terminologie, Kompromisse bei der Komplexität der Operationen
- [[graph-traversal-bfs-dfs]] - DFS und BFS mit Code, implizite Graphen, Multi-Source-BFS, Gitterprobleme
- [[trees-and-binary-trees]] - Baumdefinitionen, Traversierungen binärer Bäume, aufspannende Bäume

## Graphalgorithmen {#graph-algorithms}
- [[shortest-path-algorithms]] - Dijkstra, Bellman-Ford, Floyd-Warshall, kürzeste Pfade in DAGs, Johnson
- [[minimum-spanning-trees]] - Algorithmen von Prim und Kruskal, Schnitteigenschaft
- [[topological-sort]] - DFS-basiert und Kahns Algorithmus, kritischer Pfad, DAG-Anwendungen
- [[network-flow]] - Max-Flow-Min-Cut, Ford-Fulkerson, Edmonds-Karp, Dinic, bipartites Matching
- [[union-find]] - Disjunkte Mengen (Union-Find) mit Pfadkompression und Union by Rank

## Fortgeschrittene Graphprobleme {#advanced-graph-problems}
- [[graph-coloring]] - Chromatische Zahl, Test auf Bipartitheit, gieriges Färben, NP-Vollständigkeit
- [[eulerian-hamiltonian-paths]] - Eulersche Wege und Kreise, Hamiltonsche Pfade, Hierholzers Algorithmus
- [[traveling-salesman-problem]] - TSP exakt (Held-Karp) und Approximation (Nearest Neighbor, Christofides)

## Weiterführende Referenzen {#additional-references}

- [[backtracking]] - Systematische Durchsuchung des Lösungsraums durch schrittweisen Aufbau von Kandidaten und Verwerfen
- [[bit-manipulation]] - Operationen auf einzelnen Bits von Ganzzahlen
- [[data-structures-fundamentals]] - Grundlegende Operationen von Datenstrukturen und Komplexitätsanalyse - Arrays, sortierte Arrays mit binärer Suche
- [[dynamic-programming]] - Grundlagen der Rekursion, Memoization (Top-down), Bottom-up-Tabulation und Erkennen von DP
- [[greedy-algorithms]] - Lösungen schrittweise aufbauen, indem in jedem Schritt die lokal optimale Wahl getroffen wird
- [[hash-tables]] - Datenstruktur, die Schlüssel über eine Hashfunktion auf Werte abbildet
- [[heap-priority-queue]] - Binärer Heap: vollständiger Binärbaum, der die Heap-Eigenschaft erfüllt
- [[problem-patterns]] - Systematischer Ansatz für Algorithmusprobleme - der 7-Schritte-Interviewprozess, gängige Muster
- [[recursion-fundamentals]] - Funktion, die sich selbst aufruft, um kleinere Instanzen desselben Problems zu lösen
- [[sliding-window]] - Ein Fenster (zusammenhängendes Teilarray/Teilstring) verwalten, das über die Eingabe gleitet und sich dabei vergrößert und verkleinert
- [[string-algorithms]] - Algorithmen für Stringsuche, Mustervergleich und Stringmanipulation
- [[trees-and-graphs]] - Binäre Suchbäume, Heaps/Prioritätswarteschlangen, Tries (Präfixbäume), Graphdarstellung und
