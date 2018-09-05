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

# Get sentence structures (a POS dictionary)
def sent_struct(sentences):
    s = {}

    for sentence in sentences:
        text = nltk.word_tokenize(sentence)

        tagged = nltk.pos_tag(text)

        tags = [i[1] for i in tagged if re.search(r'^\w+$', i[1])]

        joined = ' '.join(tags)

        if joined in s:
            s[joined] += 1
        else:
            s[joined] = 1

    return s

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

def word_grams(words, minn=1, maxn=1):
    if len(words):
        grams = []
        for n in range(minn, maxn + 1):
            ng = nltk.ngrams(words, n)
            for ngram in ng:
                string = ' '.join(str(i) for i in ngram)
                grams.append(string)
        return grams

def unique_grams(struct, minn=1, maxn=1):
    myngrams = []
    for s in struct:
        words = s.split()
        if len(words) >= maxn:
            wg = word_grams(words, minn=minn, maxn=maxn)
            if wg:
                for token in wg:
                    if token not in myngrams:
                        myngrams.append(token)
    return myngrams

def generate_stanza(grammar, stanza):
    found = 0

    for _ in stanza:
        while (found < len(stanza)):
            rs = rand_sent(grammar[found], tags)
            hyph = dic.inserted(rs)
            syll = re.split(r'[\s-]-?', hyph)
            if len(syll) == stanza[found]:
                found += 1
                print(rs)


folder = sys.argv[1] if len(sys.argv) > 1 else 'Misc/Meditations'

files = get_files('/Users/gene/Documents/lit/' + folder)

print('Collecting sentences...')
sentences = get_sentences(files)
print('Done.')

#print('Building structures...')
#struct = sent_struct(sentences)
#print('Done.')
# All sentence structures appearing more than once
#ss = [i for i in struct if struct[i] > 1]

print('Collecting word tags...')
tags = word_tags(sentences)
print('Done.')

#print('Computing key ngrams...')
#myngrams = unique_grams(struct, minn=3, maxn=4)
#print('Done.')

# Choose a random sentence structure
#rs = rand_sent(list(struct.keys()), tags)
#rs = rand_sent(myngrams, tags); print(rs)
#nltk.help.upenn_tagset('RB')

# Hyphenate and count syllables
dic = pyphen.Pyphen(lang='en')
#hyph = dic.inserted(rs)
#syll = re.split(r'[\s-]-?', hyph)
#print('Syllables:', len(syll))

grammar = [
    [
        'NN CC NN',
        'JJ JJ NN',
        'NN IN NN'
    ],
    [
        'NN VB IN',
        'NN RB TO VB',
        'RBS RB VBG'
    ],
    [
        'JJ JJS NNS',
        'NN NN',
        'JJ NN IN NN'
    ],
]

stanza = [5,7,5]

generate_stanza(grammar, stanza)