#!/usr/bin/python3

# from enum import unique
import sys, re

N = int(sys.argv[1])
unique = set()
read_lines = 0
for line in sys.stdin:
    read_lines += 1
    unique.add(re.sub("\s{2,}", " ", line).strip().lower())
    if len(unique) >= N:
        break

if len(unique) >= N:
    print(f"{N} distinct lines seen after {read_lines} lines read.")
else:
    print(f"End of input reached after {read_lines} lines read - {N} different lines not seen.")
