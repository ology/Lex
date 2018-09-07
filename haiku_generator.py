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

    for c in choice:
        x = random.choice(tags[c])
        w.append(x)

    sent = ' '.join(w)
    sent = sent.capitalize()

    return sent


def generate_stanza(grammar, stanza, tags):
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

generate_stanza(grammar, stanza, tags)

"""
nltk.help.upenn_tagset()

CC: conjunction, coordinating
    & 'n and both but either et for less minus neither nor or plus so
    therefore times v. versus vs. whether yet
CD: numeral, cardinal
    mid-1890 nine-thirty forty-two one-tenth ten million 0.5 one forty-
    seven 1987 twenty '79 zero two 78-degrees eighty-four IX '60s .025
    fifteen 271,124 dozen quintillion DM2,000 ...
DT: determiner
    all an another any both del each either every half la many much nary
    neither no some such that the them these this those
EX: existential there
    there
FW: foreign word
    gemeinschaft hund ich jeux habeas Haementeria Herr K'ang-si vous
    lutihaw alai je jour objets salutaris fille quibusdam pas trop Monte
    terram fiche oui corporis ...
IN: preposition or conjunction, subordinating
    astride among uppon whether out inside pro despite on by throughout
    below within for towards near behind atop around if like until below
    next into if beside ...
JJ: adjective or numeral, ordinal
    third ill-mannered pre-war regrettable oiled calamitous first separable
    ectoplasmic battery-powered participatory fourth still-to-be-named
    multilingual multi-disciplinary ...
JJR: adjective, comparative
    bleaker braver breezier briefer brighter brisker broader bumper busier
    calmer cheaper choosier cleaner clearer closer colder commoner costlier
    cozier creamier crunchier cuter ...
JJS: adjective, superlative
    calmest cheapest choicest classiest cleanest clearest closest commonest
    corniest costliest crassest creepiest crudest cutest darkest deadliest
    dearest deepest densest dinkiest ...
MD: modal auxiliary
    can cannot could couldn't dare may might must need ought shall should
    shouldn't will would
NN: noun, common, singular or mass
    common-carrier cabbage knuckle-duster Casino afghan shed thermostat
    investment slide humour falloff slick wind hyena override subhumanity
    machinist ...
NNP: noun, proper, singular
    Motown Venneboerger Czestochwa Ranzer Conchita Trumplane Christos
    Oceanside Escobar Kreisler Sawyer Cougar Yvette Ervin ODI Darryl CTCA
    Shannon A.K.C. Meltex Liverpool ...
NNPS: noun, proper, plural
    Americans Americas Amharas Amityvilles Amusements Anarcho-Syndicalists
    Andalusians Andes Andruses Angels Animals Anthony Antilles Antiques
    Apache Apaches Apocrypha ...
NNS: noun, common, plural
    undergraduates scotches bric-a-brac products bodyguards facets coasts
    divestitures storehouses designs clubs fragrances averages
    subjectivists apprehensions muses factory-jobs ...
PDT: pre-determiner
    all both half many quite such sure this
PRP: pronoun, personal
    hers herself him himself hisself it itself me myself one oneself ours
    ourselves ownself self she thee theirs them themselves they thou thy us
PRP$: pronoun, possessive
    her his mine my our ours their thy your
RB: adverb
    occasionally unabatingly maddeningly adventurously professedly
    stirringly prominently technologically magisterially predominately
    swiftly fiscally pitilessly ...
RBR: adverb, comparative
    further gloomier grander graver greater grimmer harder harsher
    healthier heavier higher however larger later leaner lengthier less-
    perfectly lesser lonelier longer louder lower more ...
RBS: adverb, superlative
    best biggest bluntest earliest farthest first furthest hardest
    heartiest highest largest least less most nearest second tightest worst
RP: particle
    aboard about across along apart around aside at away back before behind
    by crop down ever fast for forth from go high i.e. in into just later
    low more off on open out over per pie raising start teeth that through
    under unto up up-pp upon whole with you
TO: "to" as preposition or infinitive marker
    to
UH: interjection
    Goodbye Goody Gosh Wow Jeepers Jee-sus Hubba Hey Kee-reist Oops amen
    huh howdy uh dammit whammo shucks heck anyways whodunnit honey golly
    man baby diddle hush sonuvabitch ...
VB: verb, base form
    ask assemble assess assign assume atone attention avoid bake balkanize
    bank begin behold believe bend benefit bevel beware bless boil bomb
    boost brace break bring broil brush build ...
VBD: verb, past tense
    dipped pleaded swiped regummed soaked tidied convened halted registered
    cushioned exacted snubbed strode aimed adopted belied figgered
    speculated wore appreciated contemplated ...
VBG: verb, present participle or gerund
    telegraphing stirring focusing angering judging stalling lactating
    hankerin' alleging veering capping approaching traveling besieging
    encrypting interrupting erasing wincing ...
VBN: verb, past participle
    multihulled dilapidated aerosolized chaired languished panelized used
    experimented flourished imitated reunifed factored condensed sheared
    unsettled primed dubbed desired ...
VBP: verb, present tense, not 3rd person singular
    predominate wrap resort sue twist spill cure lengthen brush terminate
    appear tend stray glisten obtain comprise detest tease attract
    emphasize mold postpone sever return wag ...
VBZ: verb, present tense, 3rd person singular
    bases reconstructs marks mixes displeases seals carps weaves snatches
    slumps stretches authorizes smolders pictures emerges stockpiles
    seduces fizzes uses bolsters slaps speaks pleads ...
WDT: WH-determiner
    that what whatever which whichever
WP: WH-pronoun
    that what whatever whatsoever which who whom whosoever
WP$: WH-pronoun, possessive
    whose
WRB: Wh-adverb
    how however whence whenever where whereby whereever wherein whereof why
"""
