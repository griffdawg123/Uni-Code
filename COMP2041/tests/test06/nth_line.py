#!/usr/bin/env python3
import sys

line = int(sys.argv[1])
f = sys.argv[2]

with open(f) as infile:
    i = 1
    for l in infile:
        if i == line:
            print(l, end='')
        i += 1


