#!/usr/bin/python3
import sys

n = int(sys.argv[1])
seen = {}
for line in sys.stdin:
    if line not in seen:
        seen[line] = 1
    else:
        seen[line] += 1
    if seen[line] >= n:
        print(f"Snap: {line}", end="")
        break