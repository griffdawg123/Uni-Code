#!/usr/bin/python3
import sys, re

with open(sys.argv[1]) as infile:
    lines = infile.readlines()
    for line in sorted(sorted(lines), key=len):
        print(line, end='')
        