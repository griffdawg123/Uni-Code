#! /usr/bin/python3
import sys, re

for line in sys.stdin:
    numbers = [num[1] for num in re.findall(r'(-)?(\d+(\.\d+)?)', line)]
    this_line = line
    for num in numbers:
        this_line = re.sub(num, str(round(float(num))), this_line)
    print(this_line, end="")
