#!/usr/bin/python3
import re, sys

total=0
for arg in sys.argv[1:]:
    with open(arg) as infile:
        for line in infile:
            numbers = re.split(r"\D+", line)
            for number in numbers:
                if number:
                    total+=int(number)
print("%d" % total)