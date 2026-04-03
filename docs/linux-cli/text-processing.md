---
title: Text Processing Tools
category: reference
tags: [linux-cli, awk, sed, sort, uniq, cut, tr, text]
---

# Text Processing Tools

Command-line utilities for transforming, filtering, and analyzing text data. These tools chain together via pipes to form powerful data processing pipelines.

## wc - Word Count

```bash
wc file.txt         # lines, words, bytes
wc -l file.txt      # count lines only
wc -w file.txt      # count words only
wc -c file.txt      # count bytes
cat file | wc -l    # count lines via pipe
```

## sort

```bash
sort file.txt               # sort lines alphabetically
sort -r file.txt            # reverse order
sort -n file.txt            # numeric sort
sort -k2 file.txt           # sort by 2nd field
sort -t: -k3 -n /etc/passwd # sort by UID (field 3, colon delimiter)
sort -u file.txt            # sort and remove duplicates
```

## uniq

Removes **consecutive** duplicate lines only - always `sort` first for full dedup.

```bash
uniq file.txt               # remove consecutive duplicates
uniq -c file.txt            # prefix with occurrence count
uniq -d file.txt            # show only duplicates
sort file | uniq            # remove ALL duplicates
sort file | uniq -c | sort -rn  # frequency count (most common first)
```

## cut

```bash
cut -d: -f1 /etc/passwd     # first field, colon delimiter
cut -d, -f2,4 file.csv      # 2nd and 4th fields, comma delimiter
cut -c1-10 file.txt         # first 10 characters per line
```

## awk

```bash
awk '{print $1}' file              # print first column (whitespace-delimited)
awk -F: '{print $1}' /etc/passwd   # colon delimiter, print usernames
awk '{print NR, $0}' file          # line number + full line
awk '$3 > 1000' /etc/passwd        # filter where field 3 > 1000
awk '{sum += $1} END {print sum}' file  # sum first column
```

## sed - Stream Editor

```bash
sed 's/old/new/' file           # replace first occurrence per line
sed 's/old/new/g' file          # replace all occurrences
sed -i 's/old/new/g' file       # in-place edit (modifies file)
sed -n '5,10p' file             # print lines 5-10 only
sed '/pattern/d' file           # delete lines matching pattern
sed 's/^/prefix/' file          # add prefix to each line
```

## tr - Translate Characters

```bash
tr 'a-z' 'A-Z' < file          # lowercase to uppercase
tr -d '\r' < file.txt           # remove carriage returns (Windows line endings)
tr -s ' ' < file                # squeeze multiple spaces into one
```

## Patterns

### Top 10 Most Frequent Words

```bash
cat file | tr ' ' '\n' | sort | uniq -c | sort -rn | head -10
```

### Extract Usernames from passwd

```bash
cut -d: -f1 /etc/passwd | sort
```

### CSV Column Sum

```bash
awk -F, '{sum += $3} END {print sum}' data.csv
```

### Remove Blank Lines

```bash
sed '/^$/d' file
grep -v '^$' file    # alternative
```

### Find and Replace Across Files

```bash
grep -rl "old" . | xargs sed -i 's/old/new/g'
```

## Gotchas

- `uniq` only removes **adjacent** duplicates - pipe through `sort` first
- `sed -i` modifies files in place with no undo - back up first or use `sed -i.bak`
- `awk` field numbering starts at `$1` (not `$0` - that is the entire line)
- `tr` reads from stdin only - use `< file` redirection, not `tr 'a' 'b' file`
- `cut` cannot reorder fields - `cut -f3,1` outputs fields in original order (1,3)

## See Also

- [[file-search-and-grep]] - Finding and filtering content
- [[io-redirection-and-pipes]] - Piping tools together
- [[bash-scripting]] - Using these tools in scripts
