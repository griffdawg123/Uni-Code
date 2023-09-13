#!/bin/dash
sort -k2 | cut -d'|' -f2 | uniq -c | grep -E "^\s*2" | cut -d" " -f8 | sort -n