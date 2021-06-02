# -*- coding: utf-8 -*-
# Language Analysis ABSA v4.0
#
# Text analysis main function
#
# Copyright (C) 2019-2021 Guide Analytics
# Author: Michael Brock Li <michael.brock.li@gmail.com>
#
# URL: <https://guideanalytics.ca>

import pandas as pd
import numpy as np
import string
import re
import time
import nltk
import pdb
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from textblob import TextBlob
from textblob import Blobber
from textblob.sentiments import PatternAnalyzer
pa = Blobber(analyzer=PatternAnalyzer())
import nltk
nltk.download('punkt')


def checkPresence(sentence, keywords):
    """

    :param sentence: represented by a string
    :param keywords: a list of keywords
    :return: True, if the sentence contains any of the keywords; False, otherwise
    """
    for keyword in keywords:
        if keyword in word_tokenize(sentence):
            return True
    return False


# Via Textblob API
def findSentiment(sentence):
    """
    Simple Sentiment Extraction using Textblob (a reliable NLP library)
    :param sentence:
    :return: float, sentiment score in float format for the sentence
    """
    if sentence == '':
        return float("nan")
    else:
        textblob_result = TextBlob(str(sentence))
        return textblob_result.sentiment.polarity #(pa(sentence).sentiment[0])


def filteredReview(reviews, keywords):
    """

    :param reviews: a list of list of sentences. (A review is represented by a list of sentences)
    :param keywords: a list of keywords
    :return: a list of filtered review which contains the keywords.
             an empty string for a review that contains no keyword.
    """
    reviews_in_sentences = sent_tokenize(str(reviews))
    ret = []
    for sentences in reviews_in_sentences:
        if checkPresence(sentences.lower(), keywords):
            ret.append(sentences)
    return ret


def aspect_match(data, keywords, ASPECTS, column='reviews'):
    """

    :param keywords:
    :param ASPECTS:
    :return:
    """
    start = time.time()
    data[ASPECTS] = data.apply(lambda x: filteredReview(x[column], keywords), axis=1)
    end = time.time()
    print(f"Took {end - start} seconds to match sentences into aspects.") # If needed to calculate

    return data, keywords, ASPECTS


def sentiment_match(data, ASPECTS):
    """

    :param data:
    :param ASPECTS:
    :return:
    """
    start = time.time()
    data[ASPECTS] = data.apply(lambda x: findSentiment())
    end = time.time()
    print(f"Took {end - start} seconds to find sentiment for each sentence.") # If needed to calculate

    return data



def row_filter_output(data, col_name):
    """

    :param data:
    :param col_name: Usually takes in ASPECT column names
    :return:
    """
    data = data[data[col_name].notna()]
    data = data.drop_duplicates(subset=['author_id', 'reviews'])
    data = data[data[col_name].map(lambda d: str(d) != "")]
    data = data[data[col_name].map(lambda d: len(d)) > 0]

    return data



