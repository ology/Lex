import sys
import os
import re
import random
import nltk
import pyphen

def get_files(path):
    file_list = []
    for fn in os.listdir(path):
        name = path + '/' + fn
        if name.endswith('.txt'):
            file_list.append(name)
    return file_list

def get_sentences(files):
    sentences = []
    for f in files:
        fh = open(f, encoding='ISO-8859-1')
        data = fh.read()
        fh.close()
        sentences.extend(nltk.sent_tokenize(data))
    return sentences

# Get all POS tags and their word instances
def word_tags(sentences):
    t = {}

    for sentence in sentences:
        text = nltk.word_tokenize(sentence)

        tagged = nltk.pos_tag(text)

        for tag in tagged:
            key = tag[1]
            key = re.sub(r'\W', '', key)
            if key:
                val = tag[0].lower()
                val = re.sub(r"^'(\w+)$", '\1', val)
                if re.search(r'[A-Za-z]', val):
                    if key not in t:
                        t[key] = []
                    if val not in t[key]:
                        t[key].append(val)

    return t

# Simulate a sentence based on a random structure and POS wordlists
def rand_sent(ss, tags):
    choice = random.choice(ss)
    #print('Choice:', choice)
    choice = choice.split()

    w = []

    for i, c in enumerate(choice):
        x = random.choice(tags[c])
        if i == 0:
            x = x.title()
        w.append(x)

    sent = ' '.join(w) + '.'

    return sent


def generate_stanza(grammar, stanza):
    found = 0

    dic = pyphen.Pyphen(lang='en')

    for _ in stanza:
        while (found < len(stanza)):
            rs = rand_sent(grammar[found], tags)
            hyph = dic.inserted(rs)
            syll = re.split(r'[\s-]-?', hyph)
            if len(syll) == stanza[found]:
                found += 1
                print(rs)


folder = sys.argv[1] if len(sys.argv) > 1 else '/Users/gene/Documents/lit/Misc/Meditations'
files = get_files(folder)

print('Collecting sentences...')
sentences = get_sentences(files)
print('Done.')

print('Collecting word tags...')
tags = word_tags(sentences)
print('Done.')

grammar = [
    [
        'NN NN',
        'JJ JJ NN',
        'NN IN NN',
        'WRB RB NNS'
    ],
    [
        'NN VB IN',
        'NN VBZ TO VB',
        'NN VBN JJ NN',
        'IN NNP VBD NN VB'
    ],
    [
        'NNS NN',
        'JJ NN IN NN',
        'NN IN NNP',
        'NN'
    ],
]

stanza = [5,7,5]

generate_stanza(grammar, stanza)
