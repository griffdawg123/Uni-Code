#!/bin/dash
cut -d'|' -f2,3 | sort | uniq | cut -d',' -f2 | cut -d' ' -f2 | sort