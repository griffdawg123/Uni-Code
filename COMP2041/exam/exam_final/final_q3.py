#!/usr/bin/python3
# sed "/|F/d" | cut -d"|" -f3 | cut -d"," -f1 | sort | uniq

import re, sys
seen_names = []
for line in sys.stdin:
    if (m := re.search(r"M\n$", line)):
        fields = line.split("|")
        name = fields[2]
        last_name = name.split(",")[0]
        if last_name not in seen_names:
            seen_names.append(last_name)
seen_names = list(set(seen_names))
seen_names.sort()
for name in seen_names:
    print(name)