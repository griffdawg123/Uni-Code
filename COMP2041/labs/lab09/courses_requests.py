#!/usr/bin/python3
import re
import sys
import urllib.request
from bs4 import BeautifulSoup
import requests

faculty=sys.argv[1]
def course_code(href):
    return href and re.compile(faculty+"[0-9]{4}").search(href)

url = "http://www.timetable.unsw.edu.au/2022/"+faculty+"KENS.html"

IGNORE_WEBPAGE_ELEMENTS = set("[document] head meta style script title".split())
# soup = BeautifulSoup()
headers = {'Accept-Encoding': 'identity'}
r = requests.get(url, headers=headers)
html = r.text
soup = BeautifulSoup(html, 'html.parser')
links = list(soup.find_all(href=course_code))
courses = []
for i, link in enumerate(links):
    if i % 2 == 0:
        courses.append(link.string+' '+links[i+1].string)
print(*sorted(list(set(courses))), sep='\n')


# course_lines = []
# for line in links:
#     if m := re.search(faculty+"[0-9]{4}.html\">.+", line):
#         if line.count(faculty) == 1:
#             course_lines.append(m.group()[:8]+' '+m.group()[15:-9])
# print(*sorted(list(set(course_lines))), sep='\n')
# print(r.text)