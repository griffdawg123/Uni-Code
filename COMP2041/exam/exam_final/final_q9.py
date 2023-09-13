#!/usr/bin/python3
import sys
n = int(sys.argv[1])
file = sys.argv[2]
with open(file) as infile:
    line = infile.readline()
    i = 0
    last_space = -1
    while line:
        if line[i] == " ":
            if i <= n:
                last_space = i
            elif last_space == -1:
                last_space = i
        if i >= n:
            print(line[:last_space+1].lstrip())
            line = line[last_space:]
            last_space = -1
            i=0
        if i >= len(line):
            print(line)
            i=0
            line = infile.readline()
        if not line:
            line = infile.readline()
        i += 1
        
    # if len(line) < n or ' ' not in line:
    #     print(line, end="")
    #     continue
    # space_to_change = -1
    # for i, char in line:
    #     if char == " ":
    #         if i <= n:
    #             space_to_change = i
    #         elif space_to_change == -1:
    #             space_to_change = i
    # print(line[space_to_change])