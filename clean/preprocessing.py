# -*- coding: utf-8 -*-
# Language Analysis ABSA v4.0
#
# Preprocessing data to clean and adjust anomalies in dataset
# - Data cleanup for any user-generated content
# - Unicode (corrupted inputs) to corrected output
# - Punctuation and weird markers
# - Regex expressions and pure stopwords removals
#
# Copyright (C) 2019-2021 Guide Analytics
# Author: Michael Brock Li <michael.brock.li@gmail.com>
#
# URL: <https://guideanalytics.ca>

from clean import clean

import re

from textblob import TextBlob
from string import punctuation
from punctuation import PunctuationRemoval
from grammar import GrammarTool


class DataClean():
    """
    # Preprocessing of all review entries (not necessarily just reviews in their designated column = 'reviews', but
    # other column entries as well).
    #
    - use_cleantext: cleans all text
    """

    def __init__(self, sentence):
        self.clean = ""
        self.sentence = sentence

    def use_cleantext(self):
        """
        Does everything
        :return:
        """
        self.sentence = clean(self.sentence, no_punct=True, no_emoji=True,
                              no_phone_numbers=True, no_emails=True, no_urls=True)

        return self.sentence

    def use_puncremoval(self):
        """
        Only removes Punctuations
        :return:
        """
        sentence = self.sentence
        sent = PunctuationRemoval()
        self.sentence = sent.remove_nuke(self.sentence)
        self.sentence = clean(self.sentence, no_punct=True)

        return self.sentence

    def use_cleanphrase(self):
        """
        Only cleans sentence phrases
        :return:
        """
        sentence = re.sub(r"(?:\@|https?\://)\S+|\n+", "", self.sentence.lower())
        # Fix spelling errors in comments!
        sent = TextBlob(sentence)
        sent.correct()
        clean = ""
        for sentence in sent.sentences:
            words = sentence.words
            # Remove punctuations
            words = [''.join(c for c in s if c not in punctuation) for s in words]
            words = [s for s in words if s]
            clean += " ".join(words)
            clean += ". "
        self.clean = clean

        return self.clean

    def use_grammarfix(self):
        """
        Fixes grammar mistakes
        :return:
        """
        gram_sent = GrammarTool(self.sentence)
        result = gram_sent.grammarFix()

        return result



test = DataClean('I have worm!!!!')

result = test.use_grammarfix()
print(result)
print(type(result))
