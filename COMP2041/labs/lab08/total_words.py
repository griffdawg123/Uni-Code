#!/usr/bin/python3
import sys, re

wordcount = 0
for line in sys.stdin:
    words = re.split(r"[^a-zA-Z]", line.rstrip())
    words = [word for word in words if word]
    wordcount += len(words)
print(f"{wordcount} words")