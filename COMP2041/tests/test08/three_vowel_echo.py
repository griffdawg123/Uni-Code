#!/usr/bin/python3
import sys, re
for arg in sys.argv[1:]:
    if m := re.search('[aeiouAEIOU]{3,}', arg):
        print(arg+' ', end='')
print()