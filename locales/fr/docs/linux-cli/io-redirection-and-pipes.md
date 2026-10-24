---
title: "Redirection d'E/S et tubes"
category: concepts
tags: [linux-cli, redirection, pipes, stdin, stdout, stderr]
level: 3
source_sha256: 3fb685db844db4f00b2137b3c700f5148be9f4a33ab794094fa1f64f76cc3291
translation: machine
translated_at: '2026-10-24'
---
# Redirection d'E/S et tubes {#io-redirection-and-pipes}

Chaque processus sous Linux dispose de trois flux standard : stdin (0), stdout (1) et stderr (2). La redirection envoie ces flux vers des fichiers, et les tubes (pipes) enchaînent les commandes entre elles. Comprendre ce mécanisme est fondamental pour maîtriser le shell.

## Flux standard {#standard-streams}

| Flux | FD | Par défaut | Description |
|--------|------|---------|-------------|
| stdin | 0 | Clavier | Entrée standard |
| stdout | 1 | Terminal | Sortie standard |
| stderr | 2 | Terminal | Sortie d'erreur standard |

## Opérateurs de redirection {#redirection-operators}

```bash
command > file          # stdout to file (overwrite)
command >> file         # stdout to file (append)
command 2> file         # stderr to file
command 2>> file        # stderr to file (append)
command < file          # file as stdin
command > /dev/null     # discard stdout
```

### Combiner les flux {#combining-streams}

```bash
command 1> out.txt 2> err.txt       # stdout and stderr to separate files
command 1> all.txt 2>&1             # both to same file
command &> all.txt                  # shorthand for above (bash)
command > /dev/null 2>&1            # discard all output
```

### Exemples {#examples}

```bash
echo "text" > file.txt              # write to file
echo "text" >> file.txt             # append to file
echo "error" >&2                    # send to stderr
cat > file.txt                      # type from keyboard into file (Ctrl+D to end)
find / -name "*.sh" > found.txt 2> errors.txt  # separate stdout/stderr
```

## Tubes {#pipes}

Envoyer la stdout d'une commande en tant que stdin de la suivante :

```bash
command1 | command2                 # basic pipe
cat file.txt | grep "error"        # filter output
ls -la | less                      # page through output
cat file | grep 'pattern' | wc -l  # count matches
command | tee file.txt              # pipe AND write to file simultaneously
```

## Enchaînement de commandes {#command-chaining}

```bash
cmd1 && cmd2    # run cmd2 ONLY if cmd1 succeeds (exit 0)
cmd1 || cmd2    # run cmd2 ONLY if cmd1 fails (non-zero)
cmd1 ; cmd2     # run cmd2 regardless of cmd1 result
```

### Exemples pratiques {#practical-examples}

```bash
mkdir testdir && touch testdir/file    # create dir then file in it
ls ~/dir || mkdir ~/dir                # list or create if missing
cat file.txt || echo "error reading"   # print or report error
head file.txt && echo "Done"           # print then confirm
```

## Codes de sortie {#exit-codes}

```bash
echo $?        # last command's exit code
exit 0         # success
exit 1         # general error
exit 2         # misuse of builtins
```

Convention : **0 = succès**, valeur non nulle = échec.

```bash
command && echo "success" || echo "failed"
```

## Schémas d'utilisation {#patterns}

### Ne journaliser que les erreurs {#log-errors-only}

```bash
command 2>&1 | grep -i error
```

### Capturer la sortie et l'afficher {#capture-output-and-display}

```bash
command | tee output.log    # show on screen AND save to file
command 2>&1 | tee -a combined.log  # append both streams to log
```

### Exécution silencieuse {#silent-execution}

```bash
command > /dev/null 2>&1    # completely silent
```

## Pièges à éviter {#gotchas}

- `>` écrase le fichier sans avertissement : utilisez `>>` pour ajouter en fin de fichier
- L'ordre de `2>&1` compte : `cmd > file 2>&1` fonctionne, alors que `cmd 2>&1 > file` n'a pas le même effet
- Les tubes ne connectent que stdout : stderr continue d'aller vers le terminal, sauf redirection explicite
- `|` crée un sous-shell : les variables définies dans un tube ne persistent pas à l'extérieur
- `tee` est utile pour déboguer les tubes : insérez-le pour observer les données intermédiaires

## Voir aussi {#see-also}

- [[bash-scripting]] - Utiliser la redirection dans les scripts
- [[text-processing]] - Outils couramment utilisés dans les pipelines
- [[terminal-basics]] - Fondamentaux du shell
