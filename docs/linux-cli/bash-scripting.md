---
title: Bash Scripting
category: reference
tags: [linux-cli, bash, scripting, shell, automation]
---

# Bash Scripting

Bash scripts automate command sequences. This entry covers script structure, variables, conditionals, loops, functions, and debugging - everything needed to write robust shell scripts.

## Script Basics

```bash
#!/bin/bash                   # shebang - must be first line
#!/usr/bin/env bash            # more portable alternative

chmod u+x script.sh           # make executable
./script.sh                   # run from current directory
bash script.sh                # run without execute permission
```

### Robust Script Header

```bash
#!/bin/bash
set -euo pipefail
# -e: exit on any error
# -u: error on unset variables
# -o pipefail: fail if any pipe command fails
```

## Variables

```bash
name="Alice"          # assign (NO spaces around =)
echo $name            # use variable
echo "${name}!"       # braces for interpolation

readonly MAX=100      # constant
unset name            # delete variable

# Command substitution
current_dir=$(pwd)
files=$(ls -la)

# Arithmetic
x=5
y=$((x + 3))
let z=x*2
```

## Script Arguments

```bash
$0    # script name
$1    # first argument
$2    # second argument
$#    # number of arguments
$@    # all arguments as separate words
$*    # all arguments as single string
$?    # exit code of last command
$$    # current process PID
```

## Conditionals

### if / elif / else

```bash
if [ $1 -eq 100 ]; then
    echo "equal to 100"
elif [ $1 -gt 100 ]; then
    echo "greater than 100"
else
    echo "less than 100"
fi
```

### Numeric Operators

| Op | Meaning |
|----|---------|
| `-eq` | equal |
| `-ne` | not equal |
| `-gt` | greater than |
| `-lt` | less than |
| `-ge` | greater or equal |
| `-le` | less or equal |

### String Comparison

```bash
[ "$str1" == "$str2" ]    # equal
[ "$str1" != "$str2" ]    # not equal
[ -z "$str" ]             # empty
[ -n "$str" ]             # non-empty
```

### File Tests

```bash
[ -f "$file" ]    # regular file exists
[ -d "$dir" ]     # directory exists
[ -e "$path" ]    # path exists (any type)
[ -r "$file" ]    # readable
[ -w "$file" ]    # writable
[ -x "$file" ]    # executable
```

### Logical Operators

```bash
[ cond1 ] && [ cond2 ]   # AND
[ cond1 ] || [ cond2 ]   # OR
! [ cond ]               # NOT
[[ cond1 && cond2 ]]     # AND (bash-specific double bracket)
```

### case Statement

```bash
case $1 in
    "start")
        echo "Starting..."
        ;;
    "stop"|"halt")
        echo "Stopping..."
        ;;
    [0-9]*)
        echo "Starts with a digit"
        ;;
    *)
        echo "Unknown option"
        ;;
esac
```

## Loops

### for Loop

```bash
for n in {1..5}; do echo "$n"; done          # range
for item in apple banana cherry; do           # list
    echo "$item"
done
for ((i=0; i<5; i++)); do echo "$i"; done    # C-style
for n in $(seq 1 10); do echo "$n"; done     # seq
```

### while Loop

```bash
x=1
while [ $x -le 5 ]; do
    echo $x
    let x=x+1
done

# Read file line by line
while IFS= read -r line; do
    echo "$line"
done < input.txt
```

### until Loop (runs while condition is FALSE)

```bash
x=1
until [ $x -ge 5 ]; do
    echo $x
    let x=x+1
done
```

### Loop Control

```bash
break      # exit loop
continue   # skip to next iteration
```

## Functions

```bash
function my_func() {
    echo "Arg 1: $1"
    local var="local variable"   # local scope
    return 0                     # exit code
}

my_func "argument"               # call
result=$(my_func "arg")          # capture output
```

## Input

```bash
read -p "Enter name: " name    # prompt and read
read -s -p "Password: " pass   # silent input
read -t 10 input               # timeout after 10 seconds
read -a arr                    # read into array
```

## Parameter Expansion

```bash
${var:-default}      # use default if unset/empty
${var:=default}      # assign default if unset/empty
${#var}              # string length
${var#prefix}        # remove shortest prefix
${var%suffix}        # remove shortest suffix
${var/old/new}       # replace first occurrence
${var//old/new}      # replace all occurrences
```

## Arrays

```bash
arr=("one" "two" "three")
echo ${arr[0]}       # first element
echo ${arr[@]}       # all elements
echo ${#arr[@]}      # array length
```

## Brace Expansion

```bash
echo {a,b,c}         # a b c
echo {1..5}          # 1 2 3 4 5
echo file{1..3}.txt  # file1.txt file2.txt file3.txt
```

## Debugging

```bash
bash -x script.sh    # trace execution
bash -n script.sh    # syntax check only
set -x               # enable trace inside script
set +x               # disable trace
```

## Gotchas

- **No spaces** around `=` in variable assignment: `x=5` not `x = 5`
- Always **quote variables**: `"$var"` prevents word splitting and globbing
- `[` is a command (requires spaces): `[ "$x" -eq 5 ]` not `["$x" -eq 5]`
- `[[` is bash-specific (not POSIX) but safer - supports `&&`, `||`, regex
- Exit code 0 = success, non-zero = failure (opposite of most programming languages)
- `local` keyword only works inside functions
- `set -e` does not catch failures in pipes unless combined with `set -o pipefail`

## See Also

- [[terminal-basics]] - Shell fundamentals
- [[io-redirection-and-pipes]] - Stream redirection
- [[cron-and-scheduling]] - Scheduling scripts
- [[text-processing]] - awk, sed in scripts
