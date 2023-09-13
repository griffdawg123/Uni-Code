#!/bin/dash
# curl --location --silent http://www.timetable.unsw.edu.au/2022/COMPKENS.html|grep -Eo "COMP[0-9]{4}"|sort|uniq
curl --location --silent http://www.timetable.unsw.edu.au/2022/$1KENS.html|grep -Eo "$1[0-9]{4}.html\">.+"|cut -b1-8,15-|sed -n 0~2p| sed -e 's/>/ /g' | cut -d'<' -f1 |sort |uniq
# curl --location --silent http://www.timetable.unsw.edu.au/2022/COMPKENS.html|grep -E "COMP[0-9]{4}"|sed -e 's/>/ /g'| grep -vE 'COMP.*COMP'|head