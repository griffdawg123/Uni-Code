#! /usr/bin/python3
import sys

inlines = [line for line in sys.stdin]
for i, line in enumerate(inlines):
    if line[0] == "#":
        index = int(line.strip("#").rstrip())
        inlines[i] = inlines[index-1]
for line in inlines:
    print(line, end="")