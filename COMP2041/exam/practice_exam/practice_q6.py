#!/usr/bin/python3
import re, sys

for line in sys.stdin:
    m = re.split(r"\|", line)
    name = m[2]
    name = re.sub(r"([a-zA-Z-]+(\s[a-zA-Z-]+)*), ([a-zA-Z-]+(\s[a-zA-Z-]+)*)", r"\3 \1", name)
    m[2] = name
    print("|".join(m), end="")