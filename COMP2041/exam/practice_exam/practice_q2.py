#! /usr/bin/python3
import re, sys
matches = 0
for line in sys.stdin:
    if m := re.search(r'3711/', line.rstrip()):
        matches += 1
print(matches)