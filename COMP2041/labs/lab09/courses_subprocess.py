#!/usr/bin/python3
from asyncio.subprocess import PIPE
from multiprocessing.connection import Pipe
import subprocess, sys
import re
faculty = sys.argv[1].rstrip()
# subprocess.Popen("curl --location --silent http://www.timetable.unsw.edu.au/2022/"+faculty+"KENS.html", stdout=PIPE).stdout.read()
# print(output)
result = ''
try:
    # curl --location --silent http://www.timetable.unsw.edu.au/2022/$1KENS.html|grep -Eo "$1[0-9]{4}.html\">.+"|cut -b1-8,15-|sed -n 0~2p| sed -e 's/>/ /g' | cut -d'<' -f1 |sort |uniq
    result = subprocess.run(f'curl --location --silent http://www.timetable.unsw.edu.au/2022/{faculty}KENS.html', shell=True, capture_output=True, text=True)
    # print(result.stdout)
except subprocess.CalledProcessError as e:
    print(e.output)
lines = result.stdout.split('\n')
# print(lines)
course_lines = []
for line in lines:
    if m := re.search(faculty+"[0-9]{4}.html\">.+", line):
        if line.count(faculty) == 1:
            course_lines.append(m.group()[:8]+' '+m.group()[15:-9])
print(*sorted(list(set(course_lines))), sep='\n')