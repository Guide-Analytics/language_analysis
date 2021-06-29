# -*- coding: utf-8 -*-
# Language Analysis ABSA v4.0
#
# Word Pair Extraction v2.0 (Aspect Extraction)
#
# Copyright (C) 2019-2021 Guide Analytics
# Author: Michael Brock Li <michael.brock.li@gmail.com>
#
# URL: <https://guideanalytics.ca>

from absa.load_corpus import *

import spacy
from spacy.matcher import PhraseMatcher
from benepar import BeneparComponent
# load english language model
#nlp = spacy.load('en_core_web_sm',disable=['ner','textcat'])

# Phrase extractor library
nlp_parse = spacy.load('en_core_web_md')
nlp_parse.add_pipe(BeneparComponent('benepar_en3'))

# Keywords extractor library
nlp = spacy.load('en_core_web_sm')


def phrase_extractor(text):
    """
    A complex high-accuracy Neural parser to extract specific list of phrases in a text sentence.
    :param text:
    :return: list, phrases list
    """

    all_phrases = [] # Spacy tokens

    def filter_single_word(word):

        if len(word) > 1:
            return True
        else:
            return False

    spacy_text = nlp_parse(text)
    all_sentences = list(spacy_text.sents)

    for text in all_sentences:
        all_new_phrases = [] # Str type
        phrases = list(text._.children)
        filtered_phrases = filter(filter_single_word, phrases)
        #all_new_phrases.extend(list(filtered_phrases))
        for fp in list(filtered_phrases):
            all_new_phrases.append(str(fp))


        all_phrases.append((str(text), all_new_phrases))

    return all_phrases

def find_keywords(text, corpus, aspect):
    """
    # Finding keywords through associated key words in specific phrasing extraction
    :param text: str
    :param corpus: list
    :param aspect: str
    :return: list, of pair matches
    """
    pair_matches = []
    phrase_matcher = PhraseMatcher(nlp.vocab)

    aspect_pat = [nlp(text) for text in corpus]
    phrase_matcher.add(aspect, None, *aspect_pat)

    doc = nlp(str(text))
    matches = phrase_matcher(doc)

    for match_id, start, end in matches:
        rule_id = nlp.vocab.strings[match_id]  # get the unicode ID, i.e. 'COLOR'
        span = doc[start : end]  # get the matched slice of the doc
        pair_matches.append((str(rule_id), str(span.text)))

    return pair_matches
