#!/usr/bin/python3
import sys, re, glob

wordcounts = {}
lyric = sys.argv[1]
for file in glob.glob("lyrics/*.txt"):
    with open(file) as infile:
        artist = file.split("/")[1].split(".")[0].replace("_", " ")
        wordcounts[artist] = {}
        for line in infile:
            words = re.split(r"[^a-zA-Z]", line.rstrip())
            words = [word for word in words if word]
            for word in words:
                if word.lower() not in wordcounts[artist]:
                    wordcounts[artist][word.lower()] = 1
                else:
                    wordcounts[artist][word.lower()] += 1
# print(list(wordcounts.keys()).sort())
for art in sorted(list(wordcounts.keys())):
    sum_of_words = 0
    for l in wordcounts[art]:
        sum_of_words += wordcounts[art][l]
    try:
        ratio = wordcounts[art][lyric]/sum_of_words
        print(f"{wordcounts[art][lyric]:4}/{sum_of_words:6} = {ratio:.9f} {art}")
    except KeyError:
        print(f"{0:4}/{sum_of_words:6} = {0:.9f} {art}")
# print(f"{lyric} occurred {wordcount} times")