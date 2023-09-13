#!/bin/dash
grep -E "(COMP2041|COMP9044)" | cut -d'|' -f2,3 | sort | uniq | cut -d'|' -f2 | sort | uniq | cut -d',' -f2 | cut -d' ' -f2 | sort | uniq -c | sort -r | cut -d' ' -f8 | head -1