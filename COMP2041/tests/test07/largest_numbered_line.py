#!/usr/bin/python3
import sys, re

matched_lines = []
largest_num = 0
for line in sys.stdin:
    temp = re.findall(r'[-]?\d+[\.]?\d*', line)
    res = list(map(float, temp))
    for num in res:
        if num > largest_num:
            matched_lines = []
            matched_lines.append(line)
            largest_num = num
        elif num == largest_num:
            matched_lines.append(line)
if len(matched_lines) > 0:
    for line in matched_lines:
        print(line, end="")