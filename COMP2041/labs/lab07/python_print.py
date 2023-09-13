#!/usr/bin/python3
import re, sys

string = sys.argv[1]
escape = re.search(r'\w+;', string)
for i, char in enumerate(string):
    if char == "'":
        string = string[:i-1]+"\\'"+string[i+1:]
print(f"print('''{string}''')")
# print(escape)
