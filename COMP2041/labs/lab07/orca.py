#!/usr/bin/python3
import sys

total=0
for arg in sys.argv[1:]:
    try:
        with open(arg) as infile:
            for line in infile:
                line_as_list = line.split()
                if line_as_list[-1] == "Orca":
                    total+=int(line_as_list[1])
    except:
        print("error")
print("%d Orcas reported" % total)