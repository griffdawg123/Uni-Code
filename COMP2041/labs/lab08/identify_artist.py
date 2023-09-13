#!/usr/bin/python3
import sys, re, glob, math

wordcounts = {}

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
for song in sys.argv[1:]:
    log_probs = {}
    with open(song) as insong:
        for song_line in insong:
            lyrics = re.split(r"[^a-zA-Z]", song_line.rstrip())
            lyrics = [word.lower() for word in lyrics if word]
            for lyric in lyrics:
                for art in sorted(list(wordcounts.keys())):
                    sum_of_words = 0
                    for l in wordcounts[art]:
                        sum_of_words += wordcounts[art][l]
                    try:
                        ratio = (wordcounts[art][lyric]+1)/sum_of_words
                    except KeyError:
                        ratio = 1/sum_of_words
                    try:
                        log_probs[art] += math.log(ratio)
                    except:
                        log_probs[art] = math.log(ratio)
    max_prob = max(log_probs, key=log_probs.get)
    print(f"{song} most resembles the work of {max_prob} (log-probability={log_probs[max_prob]:.1f})")