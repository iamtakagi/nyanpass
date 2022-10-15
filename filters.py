from importlib.resources import path
import re
import json
import os 

with open('assets/banned_words.json', 'r') as json_file:
    banned_words = json.load(json_file)

def normalize_text(text):
    blacklist = '[ @\|/:%\$&?\(\)~\.=\+\-_「」（）／　：・”“]+'
    return re.sub(blacklist, '', text)

def filter_links(tweets):
    replyMatch = re.compile(r"@\w+")
    urlMatch = re.compile(r"https?://")
    data = []
    for text in tweets:
        if replyMatch.search(text) or urlMatch.search(text):
            continue
        data.append(text)
    return data

def filter_words(word):
    for w in banned_words:
        word = word.replace(w, '')
    return word
