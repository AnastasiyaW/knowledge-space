---
title: "Théorie des files d'attente pour les ingénieurs"
category: concepts
tags: [queueing-theory, performance, capacity-planning, latency, utilization]
level: 3
source_sha256: 455dbd3f94d5e00fe39256aa340b36a9aa5b5958daf557dc49ed54c69fe6ed0f
translation: machine
translated_at: '2026-10-24'
---
# Théorie des files d'attente pour les ingénieurs {#queueing-theory-for-engineers}

La théorie des files d'attente étudie le comportement des files d'attente. Les résultats sont fortement influencés par l'attente, et l'attente est du gaspillage. Réduire ce gaspillage est l'un des leviers de performance les plus importants pour les systèmes comme pour les équipes.

## La vérité contre-intuitive {#core-counterintuitive-truth}

**Une file d'attente se forme même lorsque la capacité est largement suffisante.** Une caissière traite des clients en 45 s en moyenne, avec un arrivant par minute (utilisation de 75 %) : l'intuition dit qu'il n'y a pas d'attente. La réalité : des files importantes se forment.

**Trois causes de formation de files d'attente :**
1. **Arrivées irrégulières** : les clients se chevauchent
2. **Tailles de tâches irrégulières** : certaines tâches bloquent la file
3. **Gaspillage** : le temps d'inactivité ne peut jamais être récupéré

**Empire avec :** une utilisation élevée, une forte variabilité, un petit nombre de serveurs.

## La courbe en crosse de hockey {#the-hockey-stick-curve}

La visualisation la plus importante : le temps de réponse en fonction de l'utilisation. Une augmentation progressive à faible utilisation, qui tend vers l'infini à l'approche de 100 %.

```text
Response |                          /
Time     |                        /
         |                      /
         |                   /
         |               ../
         |          ...
         |     ....
         |....
         +-------------------------
         0%    50%    80%  95% 100%
                Utilization
```

**L'intuition humaine est linéaire ; les systèmes de files d'attente sont non linéaires.** Les transitions peuvent être brutales et surprenantes.

## Formules clés {#key-formulas}

### Notation de Kendall : A/S/c {#kendall-notation-asc}
- **A** = distribution des arrivées (M = aléatoire, D = déterministe, G = générale)
- **S** = distribution des temps de service
- **c** = nombre de serveurs

Modèles courants : M/M/1, M/M/c, M/D/1, M/G/1

### M/M/1 (le plus simple, le plus courant) {#mm1-simplest-most-common}

```yaml
Utilization:    rho = arrival_rate / service_rate     (must be < 1)
Residence time: R = S / (1 - rho)                    (S = avg service time)
Queue length:   N = rho / (1 - rho)
```

| Utilisation | Multiplicateur d'attente | Longueur de la file |
|-------------|--------------------------|---------------------|
| 50 % | 2x le temps de service | 1 élément |
| 75 % | 4x le temps de service | 3 éléments |
| 90 % | 10x le temps de service | 9 éléments |
| 99 % | 100x le temps de service | 99 éléments |

### Multi-serveurs (M/M/c) {#multi-server-mmc}
Ajouter des serveurs réduit fortement les temps d'attente, même avec la même utilisation totale. La formule d'Erlang C donne la probabilité d'attendre.

## Une file unique > plusieurs files {#single-queue-multiple-queues}

**Une file unique alimentant plusieurs serveurs est TOUJOURS préférable à des files séparées par serveur.**

Quatre files distinctes devant quatre caisses contre une file unique alimentant ces quatre caisses : la file unique offre des attentes nettement plus courtes et plus prévisibles.

**Pourquoi :** elle supprime le problème du « bloqué derrière un client lent ». Avec une file unique, le prochain serveur disponible prend immédiatement le client suivant.

**Applications :** cordons de banque, contrôles de sécurité d'aéroport, routage des centres d'appels, pools de connexions, équilibrage de charge.

## Applications pratiques {#practical-applications}

| Scénario | Enseignement de la théorie des files |
|----------|--------------------------------------|
| **Planification de capacité** | Une hausse de 30 % du trafic entraîne une dégradation bien plus forte qu'une hausse de 30 % du temps de réponse (non linéaire) |
| **Mise à l'échelle** | Plusieurs disques plus lents valent mieux qu'un disque rapide (ajoute des serveurs à la file) |
| **Organisation d'équipe** | La spécialisation crée des transferts, donc de nouvelles files. Les profils polyvalents réduisent les files |
| **Pools de connexions** | La taille du pool = nombre de serveurs dans le modèle de files |
| **Équilibrage de charge** | Une file unique avec plusieurs backends > des files par backend |
| **Kanban / limites de WIP** | Limiter le WIP réduit la longueur des files |

## Points clés à retenir {#key-takeaways}

1. **Une utilisation au-delà de 70-80 %** provoque des hausses disproportionnées du temps de réponse
2. **Réduire la variabilité** des arrivées et des tailles de tâches lorsque c'est possible
3. **Regrouper les files** chaque fois que possible (une seule file, plusieurs serveurs)
4. **Ajouter de la capacité** a des rendements décroissants à faible utilisation, mais des gains massifs à forte utilisation
5. **Surveiller conjointement l'utilisation ET le temps de réponse** : l'utilisation seule est trompeuse
6. **Les files d'attente apparaissent partout** : CPU, disques, réseaux, équipes, processus

## Pièges à éviter {#gotchas}

- **L'utilisation moyenne est trompeuse** : une moyenne de 70 % peut cacher des pics à plus de 95 % qui provoquent une dégradation sévère
- **Loi de Little** (L = λ × W) : le nombre moyen d'éléments dans le système = taux d'arrivée × temps moyen passé dans le système. Un bon contrôle de cohérence
- **Retard de l'auto-scaling** : au moment où la mise à l'échelle automatique se déclenche, l'effet « crosse de hockey » peut déjà être en place
- **Pools de connexions à base de données** : trop petits = files d'attente au niveau du pool ; trop grands = files d'attente au niveau de la base de données

## Voir aussi {#see-also}

- [[distributed-systems-fundamentals]] - Ordres de grandeur de latence, performance des systèmes
- [[caching-and-performance]] - Réduire la charge pour éviter les files d'attente
- [[quality-attributes-reliability]] - SLA, calculs de disponibilité
