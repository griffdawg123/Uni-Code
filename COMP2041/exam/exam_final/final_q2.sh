#!/bin/dash
# sed "/F/d" | cut -d"|" -f3 
sed "/|F/d" | cut -d"|" -f3 | cut -d"," -f1 | sort | uniq