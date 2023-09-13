#!/usr/bin/python3
import sys

whales={}
for arg in sys.argv[1:]:
    with open(arg) as infile:
        with open("tmpfile.txt", "w") as outfile:
            for line in infile:
                    line_as_list = line.split()
                    name=" ".join(line_as_list[2:]).lower().rstrip("s")
                    count=line_as_list[1]
                    if name not in whales.keys():
                        whales[name] = [1, int(count)]
                    else:
                        whales[name] = [whales[name][0]+1, whales[name][1]+int(count)]
for key in sorted(whales):
    print(f"{key} observations: {whales[key][0]} pods, {whales[key][1]} individuals")
# print("%d Orcas reported" % total)