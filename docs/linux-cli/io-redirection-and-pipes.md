---
title: I/O Redirection and Pipes
category: concepts
tags: [linux-cli, redirection, pipes, stdin, stdout, stderr]
---

# I/O Redirection and Pipes

Every process in Linux has three standard streams: stdin (0), stdout (1), and stderr (2). Redirection sends these streams to files, and pipes chain commands together. Understanding this is fundamental to shell proficiency.

## Standard Streams

| Stream | FD | Default | Description |
|--------|------|---------|-------------|
| stdin | 0 | Keyboard | Standard input |
| stdout | 1 | Terminal | Standard output |
| stderr | 2 | Terminal | Standard error |

## Redirection Operators

```bash
command > file          # stdout to file (overwrite)
command >> file         # stdout to file (append)
command 2> file         # stderr to file
command 2>> file        # stderr to file (append)
command < file          # file as stdin
command > /dev/null     # discard stdout
```

### Combining Streams

```bash
command 1> out.txt 2> err.txt       # stdout and stderr to separate files
command 1> all.txt 2>&1             # both to same file
command &> all.txt                  # shorthand for above (bash)
command > /dev/null 2>&1            # discard all output
```

### Examples

```bash
echo "text" > file.txt              # write to file
echo "text" >> file.txt             # append to file
echo "error" >&2                    # send to stderr
cat > file.txt                      # type from keyboard into file (Ctrl+D to end)
find / -name "*.sh" > found.txt 2> errors.txt  # separate stdout/stderr
```

## Pipes

Send stdout of one command as stdin to the next:

```bash
command1 | command2                 # basic pipe
cat file.txt | grep "error"        # filter output
ls -la | less                      # page through output
cat file | grep 'pattern' | wc -l  # count matches
command | tee file.txt              # pipe AND write to file simultaneously
```

## Command Chaining

```bash
cmd1 && cmd2    # run cmd2 ONLY if cmd1 succeeds (exit 0)
cmd1 || cmd2    # run cmd2 ONLY if cmd1 fails (non-zero)
cmd1 ; cmd2     # run cmd2 regardless of cmd1 result
```

### Practical Examples

```bash
mkdir testdir && touch testdir/file    # create dir then file in it
ls ~/dir || mkdir ~/dir                # list or create if missing
cat file.txt || echo "error reading"   # print or report error
head file.txt && echo "Done"           # print then confirm
```

## Exit Codes

```bash
echo $?        # last command's exit code
exit 0         # success
exit 1         # general error
exit 2         # misuse of builtins
```

Convention: **0 = success**, non-zero = failure.

```bash
command && echo "success" || echo "failed"
```

## Patterns

### Log Errors Only

```bash
command 2>&1 | grep -i error
```

### Capture Output and Display

```bash
command | tee output.log    # show on screen AND save to file
command 2>&1 | tee -a combined.log  # append both streams to log
```

### Silent Execution

```bash
command > /dev/null 2>&1    # completely silent
```

## Gotchas

- `>` overwrites without warning - use `>>` to append
- `2>&1` order matters: `cmd > file 2>&1` works, `cmd 2>&1 > file` does not do the same thing
- Pipes connect stdout only - stderr still goes to terminal unless redirected
- `|` creates a subshell - variables set inside a pipe don't persist outside
- `tee` is useful for debugging pipes: insert it to see intermediate data

## See Also

- [[bash-scripting]] - Using redirection in scripts
- [[text-processing]] - Tools commonly used in pipelines
- [[terminal-basics]] - Shell fundamentals
