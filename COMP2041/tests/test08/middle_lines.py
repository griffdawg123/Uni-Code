#!/usr/bin/python3
import sys, re

with open(sys.argv[1]) as infile:
    lines = infile.readlines()
    numlines = len(lines)
    if numlines > 0:
        if numlines % 2 == 0:
            print(lines[int(numlines/2)-1], end='')
            print(lines[int(numlines/2)], end='')
        else:
            print(lines[int((numlines-1)/2)], end='')
        