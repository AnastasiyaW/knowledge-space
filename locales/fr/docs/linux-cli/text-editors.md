---
title: "Éditeurs de texte en terminal"
category: reference
tags: [linux-cli, vim, nano, editors]
level: 3
source_sha256: b0cd44fa78212fbecfecd1af8cce49095b7e1616ac2eefa2cd8b9b696b6e5c30
translation: machine
translated_at: '2026-10-24'
---
# Éditeurs de texte en terminal {#terminal-text-editors}

nano est accessible aux débutants ; vim est l'éditeur de référence des utilisateurs avancés, présent sur pratiquement tous les systèmes Linux. Cette entrée présente les raccourcis et commandes essentiels de ces deux éditeurs.

## Nano {#nano}

Lancement : `nano filename` ou `nano -B filename` (crée une sauvegarde lors de l'enregistrement).

### Opérations sur les fichiers {#file-operations}

| Raccourci | Action |
|----------|--------|
| Ctrl+S | Enregistrer |
| Ctrl+O | Enregistrer sous |
| Ctrl+X | Quitter |
| Ctrl+R | Insérer un fichier |

### Édition {#editing}

| Raccourci | Action |
|----------|--------|
| Ctrl+K | Couper la ligne |
| Alt+6 | Copier la ligne |
| Ctrl+U | Coller |
| Alt+U | Annuler |
| Alt+E | Rétablir |
| Alt+3 | Commenter/décommenter |

### Recherche {#search}

| Raccourci | Action |
|----------|--------|
| Ctrl+W | Rechercher vers l'avant |
| Ctrl+Q | Rechercher vers l'arrière |
| Alt+R | Rechercher et remplacer |
| Alt+W | Occurrence suivante |

### Navigation {#navigation}

| Raccourci | Action |
|----------|--------|
| Ctrl+A / Ctrl+E | Début / fin de ligne |
| Ctrl+Y / Ctrl+V | Page précédente / page suivante |
| Alt+\ / Alt+/ | Début / fin du fichier |
| Alt+G | Aller au numéro de ligne |
| Alt+N | Activer/désactiver les numéros de ligne |

## Vim {#vim}

Éditeur modal avec trois modes principaux : **Normal**, **Insertion**, **Visuel**.

### Changement de mode {#mode-switching}

```sql
i           Insert at cursor
a           Insert after cursor
I / A       Insert at line start / end
o / O       New line below / above, enter insert
Esc         Return to Normal mode
v           Visual mode (character)
V           Visual mode (line)
Ctrl+v      Visual block mode
```

### Déplacement du curseur (Normal) {#cursor-movement-normal}

```text
h j k l     Left, down, up, right
w / b       Next / previous word
0 / $       Start / end of line
^           First non-blank character
gg          Top of file
G           Bottom of file
:[num]      Go to line
Ctrl+d/u    Half page down / up
{ / }       Previous / next paragraph
```

### Édition (Normal) {#editing-normal}

```sql
dd          Delete (cut) line
d$          Delete to end of line
dw          Delete word
cc          Change (delete + insert) line
J           Join line below
r[char]     Replace single character
.           Repeat last command
x           Delete character under cursor
```

### Objets de texte {#text-objects}

```sql
di(         Delete inside parentheses
ci"         Change inside quotes
da{         Delete around braces (including braces)
yi[         Yank inside brackets
```

### Presse-papiers {#clipboard}

```text
yy          Yank (copy) line
p / P       Paste after / before cursor
```

### Enregistrer et quitter {#save-and-exit}

```bash
:w          Save
:wq         Save and quit
:q          Quit (fails if unsaved)
:q!         Force quit without saving
```

### Recherche et remplacement {#search-and-replace}

```text
/pattern    Search forward
?pattern    Search backward
n / N       Next / previous match
:%s/old/new/g    Replace all in file
:%s/old/new/gc   Replace with confirmation
```

### Annuler / Rétablir {#undo-redo}

```text
u           Undo
Ctrl+r      Redo
```

### Fenêtres et onglets {#windows-and-tabs}

```text
:e file     Open file
:tabe       New tab
gt / gT     Next / previous tab
:vsp        Vertical split
Ctrl+ww     Switch between windows
Ctrl+wq     Close window
```

### Marques {#marks}

```text
m{a-z}      Set local mark
'{a-z}      Jump to mark
''          Return to previous position
```

## Pièges courants {#gotchas}

- Vim démarre en mode Normal : appuyer sur des lettres exécute des commandes, sans saisir de texte
- `:q!` abandonne toutes les modifications sans confirmation
- nano affiche les raccourcis clavier en bas de l'écran (`^` signifie Ctrl)
- Vim est préinstallé sur presque tous les systèmes Linux ; nano peut devoir être installé
- Sur de nombreux systèmes, `vi` est en réalité `vim` (Vi IMproved)
- Dans vim, `u` annule une modification à la fois ; `U` annule toutes les modifications de la ligne courante

## Voir aussi {#see-also}

- [[terminal-basics]] - Shell et raccourcis clavier
- [[file-operations]] - Création et affichage de fichiers
