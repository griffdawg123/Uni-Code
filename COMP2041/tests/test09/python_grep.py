#!/usr/bin/python3

# from enum import unique
import sys, re

regexp = sys.argv[1]
f = sys.argv[2]

with open(f) as infile:
    for line in infile:
        if re.search(regexp, line.rstrip()):
            print(line, end="")
