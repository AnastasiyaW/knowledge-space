---
title: "Gestion des processus"
category: reference
tags: [linux-cli, processes, signals, kill, ps, top, htop]
level: 3
source_sha256: 33c9daab4d53e4ae6d892e4f0fef4e8eae39b20a192c1f081ee381deb97e89e1
translation: machine
translated_at: '2026-10-24'
---
# Gestion des processus {#process-management}

Un processus est un programme en cours d'exécution, doté d'un PID, d'un état, d'une priorité et d'une allocation de ressources. Cette entrée couvre l'affichage, le filtrage et le contrôle des processus, indispensables pour l'administration système et le débogage.

## Points clés {#key-facts}

- Chaque processus possède un PID (Process ID) et un PPID (Parent Process ID)
- Le PID 1 correspond au processus init/systemd, parent de tous les autres
- **Daemon** = processus en arrière-plan (service système)
- **Thread** = unité d'exécution au sein d'un processus, partageant son espace mémoire

## États des processus {#process-states}

| État | Symbole | Description |
|------|---------|-------------|
| Running | R | En cours d'exécution ou prêt à s'exécuter |
| Sleeping (interruptible) | S | En attente d'un événement, peut être interrompu |
| Sleeping (uninterruptible) | D | En attente d'E/S, ne peut pas être interrompu |
| Stopped | T | En pause (Ctrl+Z ou signal) |
| Zombie | Z | Terminé, mais le parent n'a pas encore récupéré son code de sortie |

## ps - Instantané des processus {#ps-process-snapshot}

```bash
ps                          # processes in current terminal
ps aux                      # all processes, full info (BSD syntax)
ps -ef                      # all processes (UNIX syntax)
ps afx                      # process tree
ps -u username              # processes for specific user
ps -T -p PID                # show threads of a process
ps 1                        # info for PID 1
```

### Colonnes de ps aux {#ps-aux-columns}

```text
USER  PID  %CPU  %MEM  VSZ  RSS  TTY  STAT  START  TIME  COMMAND
```

- **VSZ** : taille de la mémoire virtuelle
- **RSS** : resident set size (RAM effectivement utilisée)
- **STAT** : état du processus

## top - Moniteur interactif {#top-interactive-monitor}

```bash
top                     # default (sort by CPU%)
top -o PID              # sort by PID
top -u username         # filter by user
top -p PID1,PID2        # monitor specific PIDs
```

### Dans top {#inside-top}

| Touche | Action |
|--------|--------|
| q | Quitter |
| k | Tuer un processus |
| r | Renice (modifier la priorité) |
| M | Trier par mémoire |
| P | Trier par CPU |
| 1 | Basculer l'affichage des statistiques par CPU |
| u | Filtrer par utilisateur |

### Charge moyenne (load average) {#load-average}

Affichée dans l'en-tête de top : `load average: 0.15, 0.20, 0.18` (sur 1, 5 et 15 minutes)

- Valeur < nombre de cœurs CPU = pas de surcharge
- Valeur = nombre de cœurs = capacité maximale atteinte
- Valeur > nombre de cœurs = surcharge

## htop - Moniteur amélioré {#htop-enhanced-monitor}

```bash
sudo apt install htop
htop                    # visual CPU/memory bars, mouse support
htop -u username        # filter by user
```

## Rechercher des processus {#finding-processes}

```bash
pidof firefox           # PID by exact name
pgrep pattern           # PIDs matching pattern
pgrep -la nginx         # PIDs + full command lines
```

## Signaux {#signals}

```bash
kill PID                # SIGTERM (graceful, default)
kill -9 PID             # SIGKILL (force, immediate)
kill -15 PID            # SIGTERM explicitly
kill -1 PID             # SIGHUP (reload config)
killall processname     # kill all by name
pkill pattern           # kill by pattern
kill -l                 # list all signals
```

| Signal | Numéro | Description |
|--------|--------|-------------|
| SIGHUP | 1 | Déconnexion / rechargement de la configuration |
| SIGINT | 2 | Interruption (Ctrl+C) |
| SIGQUIT | 3 | Arrêt avec génération d'un core dump |
| SIGKILL | 9 | Arrêt forcé (ne peut pas être intercepté) |
| SIGTERM | 15 | Arrêt propre |
| SIGSTOP | 19 | Mise en pause (ne peut pas être intercepté) |
| SIGCONT | 18 | Reprise d'un processus suspendu |

## Priorité des processus (nice) {#process-priority-nice}

Plage : -20 (priorité la plus élevée) à +19 (priorité la plus basse).

```bash
nice -n 10 command      # start with lower priority
renice -n 5 -p PID      # change running process priority
```

## Création d'un processus {#process-creation}

1. Attribution d'un nom au processus
2. Ajout à la liste des processus
3. Détermination de la priorité
4. Constitution du bloc de contrôle du processus (PCB)
5. Allocation des ressources

### Attributs d'un processus {#process-attributes}

| Attribut | Description |
|----------|-------------|
| `pid` | Identifiant du processus |
| `ppid` | Identifiant du processus parent |
| `fd` | Descripteurs de fichiers ouverts |
| `cwd` | Répertoire de travail courant |
| `environ` | Variables d'environnement |
| `nice` | Valeur de priorité |

## Pièges courants {#gotchas}

- `kill -9` doit rester un dernier recours : le processus ne peut pas nettoyer après lui (fichiers temporaires, verrous, sockets)
- Les processus zombies ne peuvent pas être tués, car ils sont déjà morts ; il faut plutôt agir sur leur parent
- La charge moyenne affichée par `top` inclut les processus en état D (en attente d'E/S)
- Sur Solaris, `killall` tue TOUS les processus ; sous Linux, il tue les processus par nom (prudence dans les environnements mixtes)
- Les processus lancés en arrière-plan avec `&` meurent tout de même à la fermeture du terminal : utilisez `nohup` ou `disown`

## Voir aussi {#see-also}

- [[systemd-and-services]] - Gestion des services avec systemctl
- [[monitoring-and-performance]] - Surveillance des ressources système
- [[linux-kernel-and-boot]] - Noyau, init, cycle de vie des processus
