#! /usr/bin/python3
import sys

ALPHABET_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHABET_LOWER = "abcdefghijklmnopqrstuvwxyz"

shift = int(sys.argv[1])
for line in sys.stdin:
    new_line = ''
    for letter in line:
        if letter in ALPHABET_UPPER:
            # print(letter, (+shift % 26))
            new_line += ALPHABET_UPPER[(ALPHABET_UPPER.index(letter)+shift) % 26]
        elif letter in ALPHABET_LOWER:
            new_line += ALPHABET_LOWER[(ALPHABET_LOWER.index(letter)+shift) % 26]
        else:
            new_line += letter
    print(new_line, end="")
