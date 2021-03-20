import sys
import os
import nltk
import markovify

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

folder = sys.argv[1]      if len(sys.argv) > 1 else '/home/gene/Documents/lit/Misc/Meditations'
n      = int(sys.argv[2]) if len(sys.argv) > 2 else 10
chars  = int(sys.argv[3]) if len(sys.argv) > 3 else 100
states = int(sys.argv[4]) if len(sys.argv) > 4 else 2

files = get_files(folder)

sentences = get_sentences(files)

text_model = markovify.Text(sentences, state_size=states)

for i in range(n):
    ss = None
    while ss == None:
        ss = text_model.make_short_sentence(chars)
    print(i, ss)
