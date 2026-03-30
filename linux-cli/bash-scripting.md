---
title: Bash Scripting
category: patterns
tags: [bash, scripting, shebang, loops, conditionals, functions]
---
# Bash Scripting

Writing and executing shell scripts with conditionals, loops, and functions.

## Key Facts

- Shebang line: `#!/bin/bash` - MUST be first line; tells OS which interpreter to use
- `whereis bash` - find interpreter path for shebang line (usually `/bin/bash`)
- Scripts need [[file-permissions]] execute permission: `chmod u+x script.sh`
- Run script: `./script.sh` (needs execute bit) or `bash script.sh` (does not need execute bit)
- `$1`, `$2`... - positional parameters (command line arguments)
- `$USER`, `$HOME`, `$SHELL`, `$0` - common environment variables
- `echo $SHELL` - show current shell; `cat /etc/shells` - list available shells
- Exit codes: 0 = success, non-zero = failure; used by [[io-redirection-and-pipes]] `&&` and `||`
- Bash is the default shell on most Linux distributions
- [[cron-scheduling]] executes bash scripts on a schedule

## Patterns

```bash
#!/bin/bash
# Basic script with environment variables
echo "User: $USER"
echo "Directory: $(pwd)"
echo "System: $(uname)"
echo "Home: $HOME"

# ---- IF / ELIF / ELSE ----
#!/bin/bash
if [ "$1" == "100" ]; then
    echo "Exact match"
elif [ "$1" -gt 100 ]; then
    echo "Greater than 100"
elif [ "$1" -lt 100 ] && [ "$1" -gt 50 ]; then
    echo "Between 50 and 100"
else
    echo "50 or less"
fi

# Comparison operators (inside [ ]):
# -eq  equal         -ne  not equal
# -gt  greater than  -lt  less than
# -ge  greater/equal -le  less/equal
# ==   string equal  !=   string not equal

# ---- CASE ----
#!/bin/bash
case $1 in
    start)
        echo "Starting..."
        ;;
    stop)
        echo "Stopping..."
        ;;
    *)
        echo "Usage: $0 {start|stop}"
        ;;
esac

# ---- FOR LOOP ----
# One-liner
for n in {1..5}; do echo "$n iteration"; done

# Multi-line with seq
for n in $(seq 10); do
    echo "Step $n"
done

# ---- WHILE LOOP ----
#!/bin/bash
x=1
while [ $x -le 5 ]; do
    echo $x
    let x=x+1
done

# ---- UNTIL LOOP (runs until condition is TRUE) ----
#!/bin/bash
x=1
until [ $x -gt 5 ]; do
    echo $x
    let x=x+1
done

# ---- FUNCTIONS ----
function greet() {
    echo "Hello, $1!"
}
greet "World"

# Function with parameter
function repeat_action() {
    count=$1
    for n in $(seq $count); do
        echo "Iteration $n"
    done
}
repeat_action 3

# ---- MAKING SCRIPT EXECUTABLE ----
chmod u+x myscript.sh
./myscript.sh
# or run without execute bit:
bash myscript.sh
```

## Gotchas

- Shebang must be `#!` not `!#` or `#*` or any other variant
- Spaces in `[ ]` tests are MANDATORY: `[ $x -gt 5 ]` works; `[$x -gt 5]` fails
- `==` works for string comparison in `[[ ]]` but use `-eq` for numeric in `[ ]`
- `chmod u+x` is `chmod` (permissions), NOT `chown` (ownership) - frequent typo
- `./script.sh` requires execute permission; `bash script.sh` does not (bash reads it as input)
- Variables without quotes break on spaces: `"$variable"` is safer than `$variable`
- `while [ $x -gt 5 ]` with x=1 never enters the loop; `until [ $x -gt 5 ]` with x=1 loops 5 times

## See Also

- [[file-permissions]] - making scripts executable
- [[io-redirection-and-pipes]] - using redirection in scripts
- [[cron-scheduling]] - automating script execution
- [[text-editors]] - vim/nano for writing scripts
- https://www.gnu.org/software/bash/manual/bash.html
