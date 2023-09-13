#!/usr/bin/python3
import sys, re
for line in sys.stdin:
    words = line.split(" ")
    # print(words)
    new_words = []
    for word in words:
        counts = []
        for char in word.strip():
            counts.append(word.lower().count(char.lower()))
        # print(len(set(counts)))
        if len(set(counts)) == 1:
            new_words.append(word.strip())
    print(" ".join(new_words))