# -*- coding: utf-8 -*-
# Language Analysis ABSA v4.0
#
# Word Pair Extraction v1.0
# There is a 2nd version coming. First version does not cover all anomalies in a sentence structure
# DEPRECRATED
#
# Copyright (C) 2019-2021 Guide Analytics
# Author: Michael Brock Li <michael.brock.li@gmail.com>
#
# URL: <https://guideanalytics.ca>


import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
import gensim
import spacy, en_core_web_sm
nlp = en_core_web_sm.load()

lemmatizer = WordNetLemmatizer()

stop = ['i','me','my','myself','we','our','ours','ourselves','you',"you're","you've","you'll","you'd",'your','yours',
         'yourself','yourselves','he','him','his','himself','she',"she's",'her','hers','herself','it',"it's",'its','itself',
         'they','the','them','their','theirs','themselves','what','which','who','whom','this','that',"that'll",'these',
         'those','am','is','are','was','were','be','been','being','have','has','had','having','do','does','did','doing',
         'a','an','the','and','but','if','or','because','as','until','while','of','at','by','for','with','about','against',
         'between','into','through','during','before','after','above','below','to','from','up','down','in','out','on','off',
         'over','under','again','further','then','once','here','there','when','where','why','how','all','any','both','each',
         'few','more','most','other','some','such','only','own','same','so','than','too','very','s','t','can','will','just',
         'don',"don't",'should',"should've",'now','d','ll','m','o','re','ve','y','ain','aren']


def bigrams(words, bi_min=15, tri_min=10):
    """

    :param words:
    :param bi_min:
    :param tri_min:
    :return:
    """
    bigram = gensim.models.Phrases(words, min_count = bi_min)
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    return bigram_mod


def clean(doc):
    """

    :param doc:
    :return:
    """
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    lemmatized = ''.join(lemmatizer.lemmatize(word) for word in stop_free)
    bigram_mod = bigrams(lemmatized)
    bigram = ''.join(bigram_mod[lemmatized])
    #print(bigram)
    return bigram


def word2vec(word):
    """

    :param word:
    :return:
    """
    from collections import Counter
    from math import sqrt

    # count the characters in word
    cw = Counter(word)
    # precomputes a set of the different characters
    sw = set(cw)
    # precomputes the "length" of the word vector
    lw = sqrt(sum(c*c for c in cw.values()))

    # return a tuple
    return cw, sw, lw


def cosdis(v1, v2):
    """

    :param v1:
    :param v2:
    :return:
    """
    # which characters are common to the two words?
    common = v1[1].intersection(v2[1])
    # by definition of cosine distance we have
    return sum(v1[0][ch]*v2[0][ch] for ch in common)/v1[2]/v2[2]


def check(words, lst_of_keywords):
    """

    :param words:
    :param lst_of_keywords:
    :return:
    """
    return [x for x in words for y in lst_of_keywords if cosdis(word2vec(x), word2vec(y)) > 0.98]


def word_detection(sentence, keywords):
    """

    :param sentence:
    :param keywords:
    :return:
    """

    doc = nlp(sentence)
    data_final = []
    for i, token in enumerate(doc):
        if str(token) not in keywords:
            continue
        for j in range(i+1,len(doc)):
            clause = (((doc[i].dep_ == "amod" and (doc[i].pos_ == 'NOUN' or doc[i].pos_ == 'ADJ'))
                 or doc[j].dep_ == 'compound') or doc[j].dep_ == 'advmod') \
            and ((((doc[j].pos_ == 'ADJ' or doc[j].pos_ == 'NOUN') and
                   (doc[j].dep_ != 'dobj' and doc[j].dep_ != 'amod'))
                  or doc[i].dep_ == 'compound') or doc[j].dep_ == 'advmod' or doc[i].dep_ == 'advmod') \
            and ((((doc[j].dep_ == 'compound' or doc[i].dep_ == 'compound' or doc[j].dep_ == 'compound' or
                    doc[j].dep_ == 'dobj' or doc[j].dep_ == 'appos' or doc[j].dep_ == 'advmod') and
                   doc[j].dep_ != 'amod' ) and
                  (doc[j].pos_ == 'ADJ' or doc[j].pos_ == 'NOUN' or doc[j].pos_ == 'PROPN')) or
                 doc[i].dep_ == 'advmod' or doc[j].dep_ == 'advmod')

            if clause:
                data_final.append([str(doc[j]), token])

    return data_final # aspect_result
