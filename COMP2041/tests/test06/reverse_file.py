#!/usr/bin/env python3
import sys

with open(sys.argv[1]) as infile:
    with open(sys.argv[2], "w") as outfile:
        for line in reversed(list(infile)):
            print(line, file=outfile, end='')