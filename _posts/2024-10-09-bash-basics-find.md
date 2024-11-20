---
layout: post
title:  "Bash Basics: find"
date:   2020-05-02 +0100
categories: [notes, tech]
---

`find` is a Command that traverses the file system below a given directory and finds files according to whichever rules it's given. This is usually the quickest way to find specific files in a tree

## Useful Examples
```bash
# Find a file with a name
find . -name hello.py  # Match exactly
find . -name "*.py"   # Match a pattern

# Find recently modified files (in minutes - *note* the minus sign - no "-" means exactly)
find . -mmin -100 # in minutes
find . -mtime -100m # in any units

# Find files of a particular size (exactly, or [+/-])
find . -size +10M

# Find files of a particular type, e.g. binary
find . -type b

# Execute a command on every file found - {} expands to the name of the file
# -print reinstates the default printing behaviour of find
find . -type d -perm 777 -print -exec rm -f {} \;
```
