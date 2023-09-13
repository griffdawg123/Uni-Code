#!/usr/bin/python3
import sys
file1 = sys.argv[1]
file2 = sys.argv[2]

with open(file1) as in1:
    with open(file2) as in2:
        lines1 = in1.readlines()
        num1 = len(lines1)
        lines2 = in2.readlines()
        num2 = len(lines2)
        if num1 != num2:
            print(f"Not mirrored: different number of lines: {num1} versus {num2}")
            sys.exit(1)
        for i, line in enumerate(lines1):
            if line != lines2[-1*(i+1)]:
                print(f"Not mirrored: line {i+1} different")
                sys.exit(1)
        print("Mirrored")
