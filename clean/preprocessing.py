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

from .clean import clean
from textblob import TextBlob
from string import punctuation
from .punctuation import PunctuationRemoval
from .grammar import GrammarTool

import re


class DataClean():
    """
    # Preprocessing of all review entries (not necessarily just reviews in their designated column = 'reviews', but
    # other column entries as well).
    #
    - use_cleantext: cleans all text
    """

    def __init__(self, sentence, model):
        self.model = model
        self.sentence = sentence

    def use_cleantext(self):
        """
        Does everything
        :return:
        """
        self.sentence = clean(str(self.sentence), no_punct=True, no_emoji=True,
                              no_phone_numbers=True, no_emails=True, no_urls=True)

        return self.sentence

    def use_cleantext_BEFORE(self):
        """

        :return:
        """
        self.sentence = clean(str(self.sentence), no_punct=False, no_emoji=False,
                              no_phone_numbers=True, no_emails=True, no_urls=True, lower=False)

        return self.sentence

    def use_cleantext_AFTER(self):

        self.sentence = clean(str(self.sentence), no_punct=False, no_emoji=False,
                              no_phone_numbers=True, no_emails=True, no_urls=True,
                              normalize_whitespace=False, no_line_breaks=True,
                              strip_lines=False, lower=False)

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

    def use_grammarfix(self, version='v1'):
        """
        Fixes grammar mistakes
        :return:
        """
        if version == 'v1':
            gram_sent = GrammarTool(str(self.sentence), model=None, version='v1')
            self.sentence = gram_sent.grammarFix()
        elif version == 'v2':
            gram_sent = GrammarTool(str(self.sentence), model=self.model, version='v2')
            self.sentence = gram_sent.grammarFix_v2()
        else:
            return self.sentence

        return self.sentence

