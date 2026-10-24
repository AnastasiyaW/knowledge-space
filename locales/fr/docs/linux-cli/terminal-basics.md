---
title: "Notions de base du terminal"
category: concepts
tags: [linux-cli, terminal, shell, keyboard-shortcuts]
level: 2
source_sha256: 226bc3671504aef21c85fa492a266bbc9b01ec5c68d78f43fae2757cbe7b4d52
translation: machine
translated_at: '2026-10-24'
---
# Notions de base du terminal {#terminal-basics}

Le terminal (émulateur de terminal) fournit une fenêtre pour interagir avec le shell, c'est-à-dire l'interpréteur de ligne de commande qui transmet les saisies de l'utilisateur au noyau du système d'exploitation. Cette entrée présente les types de shells, les commandes essentielles et les raccourcis clavier pour une utilisation efficace du terminal.

## Faits clés {#key-facts}

- Le **shell** interprète les commandes ; le **terminal** est la fenêtre graphique qui héberge le shell
- Shell par défaut sur la plupart des distributions Linux : **bash** (Bourne Again Shell)
- Shells disponibles : sh, bash, dash, zsh, fish
- Le système de fichiers Linux est **sensible à la casse** : `File.txt` et `file.txt` sont deux fichiers différents
- Port SSH par défaut : **22**

## Types de shells {#shell-types}

| Shell | Remarques |
|-------|-----------|
| **sh** (Bourne) | Standard POSIX, basique |
| **bash** | Le plus populaire, par défaut sur la plupart des distributions, étend sh |
| **dash** | Shell POSIX léger, `/bin/sh` par défaut sur Ubuntu, démarrage rapide |
| **zsh** | Historique partagé, tableaux améliorés, correction orthographique, plugins (Oh My Zsh) |
| **fish** | Coloration syntaxique, recherche rapide dans l'historique, configurateur web |

```bash
echo $SHELL         # current shell path
echo $0             # current shell name
cat /etc/shells     # all available shells
chsh -s /bin/zsh    # change default login shell
```

Fichiers de configuration du shell :
- bash : `~/.bashrc` (interactif), `~/.bash_profile` (connexion), `~/.bash_logout`
- zsh : `~/.zshrc`
- Global : `/etc/profile`, `/etc/bash.bashrc`

## Premières commandes essentielles {#essential-first-commands}

```bash
pwd             # print working directory
whoami          # print current username
clear           # clear screen (also Ctrl+L)
reset           # reset terminal to default state
history         # show command history
history -c      # clear history

# Getting help
man command     # full manual page
command --help  # brief usage info
whatis command  # one-line description
apropos keyword # search help by keyword
info command    # info page (alternative to man)
```

## Navigation {#navigation}

```bash
cd /path/to/dir   # absolute path
cd ~              # home directory (also just cd)
cd ..             # one level up
cd -              # previous directory
ls                # list contents
ls -l             # long format (permissions, size, date)
ls -a             # show hidden files (starting with .)
ls -la            # long + hidden
tree              # display directory tree
```

## Raccourcis clavier - Navigation {#keyboard-shortcuts-navigation}

| Raccourci | Action |
|-----------|--------|
| Ctrl+A | Aller au début de la ligne |
| Ctrl+E | Aller à la fin de la ligne |
| Alt+F | Avancer d'un mot |
| Alt+B | Reculer d'un mot |
| Ctrl+XX | Basculer entre le début de la ligne et la position courante |

## Raccourcis clavier - Édition {#keyboard-shortcuts-editing}

| Raccourci | Action |
|-----------|--------|
| Ctrl+U | Supprimer du curseur jusqu'au début de la ligne |
| Ctrl+K | Supprimer du curseur jusqu'à la fin de la ligne |
| Ctrl+W | Supprimer le mot situé avant le curseur |
| Alt+D | Supprimer du curseur jusqu'à la fin du mot |
| Ctrl+D | Supprimer le caractère sous le curseur |
| Alt+. | Insérer le dernier argument de la commande précédente |

## Raccourcis clavier - Contrôle des processus {#keyboard-shortcuts-process-control}

| Raccourci | Action |
|-----------|--------|
| Ctrl+C | Interrompre la commande en cours (SIGINT) |
| Ctrl+Z | Suspendre la commande en cours (arrière-plan) |
| Ctrl+D | Fermer le terminal / envoyer EOF |
| Ctrl+L | Effacer l'écran |
| Ctrl+S | Suspendre l'affichage à l'écran |
| Ctrl+Q | Reprendre l'affichage |

## Raccourcis clavier - Historique {#keyboard-shortcuts-history}

| Raccourci | Action |
|-----------|--------|
| Ctrl+R | Recherche incrémentale inversée dans l'historique |
| Haut / Ctrl+P | Commande précédente |
| Bas / Ctrl+N | Commande suivante |
| !! | Exécuter la dernière commande |
| !x | Exécuter la dernière commande commençant par x |
| ^ancien^nouveau | Remplacer ancien par nouveau dans la dernière commande |

## Obtenir Linux {#getting-linux}

- **WSL** (Windows 10+) : meilleure option pour les utilisateurs de Windows, à installer depuis le Microsoft Store
- **VirtualBox** : n'importe quelle distribution en machine virtuelle (2 Go de RAM et 20 Go de disque minimum)
- **VPS dans le cloud** : connexion via SSH
- **macOS** : terminal Unix natif, utiliser `brew` comme gestionnaire de paquets

## Pièges courants {#gotchas}

- `cd` sans argument mène à `~` (répertoire personnel), et non à `/`
- `Ctrl+S` fige la sortie du terminal : utilisez `Ctrl+Q` pour la débloquer (moment de panique fréquent)
- `history -c` efface l'historique en mémoire mais pas le fichier `~/.bash_history` ; utilisez `history -c && history -w` pour effacer les deux
- La complétion par Tab est contextuelle : une pression sur Tab complète, deux pressions affichent toutes les options

## Voir aussi {#see-also}

- [[bash-scripting]] - Fondamentaux du scripting shell
- [[io-redirection-and-pipes]] - stdin/stdout/stderr et tubes (pipes)
- [[wsl]] - Sous-système Windows pour Linux
