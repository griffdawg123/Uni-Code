#!/usr/bin/env python3
import sys

low = int(sys.argv[1])
high = int(sys.argv[2])
f = sys.argv[3]

with open(f, "w") as outfile:
    for i in range(low, high+1):
        print(i, file=outfile)


