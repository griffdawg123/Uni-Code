#!/usr/bin/python3
import sys, re

wordcount = 0
lyric = sys.argv[1]
for line in sys.stdin:
    words = re.split(r"[^a-zA-Z]", line.rstrip())
    words = [word for word in words if word]
    for word in words:
        if word.lower().rstrip() == lyric.lower().rstrip():
            wordcount += 1
print(f"{lyric} occurred {wordcount} times")