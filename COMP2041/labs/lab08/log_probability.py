#!/usr/bin/python3
import sys, re, glob, math

wordcounts = {}
for file in glob.glob("lyrics/*.txt"):
    artist = file.split("/")[1].split(".")[0].replace("_", " ")
    wordcounts[artist] = {}
# print(sorted(list(wordcounts.keys())))
# lyric = sys.argv[1]
for file in glob.glob("lyrics/*.txt"):
    with open(file) as infile:
        artist = file.split("/")[1].split(".")[0].replace("_", " ")
        for line in infile:
            words = re.split(r"[^a-zA-Z]", line.rstrip())
            words = [word for word in words if word]
            for word in words:
                if word in wordcounts[artist]:
                    wordcounts[artist][word.lower()] += 1
                else:
                    for art in sorted(list(wordcounts.keys())):
                            # print(art)
                            if word.lower() not in wordcounts[art]:
                                # if word == 'hello':
                                    # print(f"{word} not found yet for {art}")
                                wordcounts[art][word.lower()] = 1
# print('hello' in wordcounts['Ed Sheeran'])
# print(list(wordcounts.keys()).sort())
for file in glob.glob("lyrics/*.txt"):
    sum_of_words = 0
    with open(file) as infile:
        for line in infile:
            words = re.split(r"[^a-zA-Z]", line.rstrip())
            words = [word for word in words if word]
            sum_of_words += len(words)
    art = file.split("/")[1].split(".")[0].replace("_", " ")
    # print(f"{art}: {sum_of_words}")
    log_probability = 1
    for word in sys.argv[1:]:
        # print(art)
        # print(word)
        ratio = wordcounts[art][word.rstrip().lower()]/sum_of_words
        log_probability += math.log(ratio)
    print(f"{log_probability:10.5f} {art}")


    