#!/usr/bin/python3
import sys

seen = set()
for word in sys.argv[1:]:
    if word not in seen:
        print(word, end=" ")
        seen.add(word)
print()