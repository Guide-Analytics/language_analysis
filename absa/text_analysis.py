# -*- coding: utf-8 -*-
# Language Analysis ABSA v4.0
#
# Text analysis main function
#
# Copyright (C) 2019-2021 Guide Analytics
# Author: Michael Brock Li <michael.brock.li@gmail.com>
#
# URL: <https://guideanalytics.ca>

import time
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from textblob import TextBlob
from textblob import Blobber
from textblob.sentiments import PatternAnalyzer
from .word_pair import word_detection
from .aspect_extraction import *
pa = Blobber(analyzer=PatternAnalyzer())
import nltk
nltk.download('punkt')
import flair

flair_sentiment = flair.models.TextClassifier.load('en-sentiment')

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


def findSentiment_v2(sentence):
    """

    :param sentence:
    :return:
    """
    try:
        s = flair.data.Sentence(sentence)
        flair_sentiment.predict(s)
        if s.labels[0].value == 'POSITIVE':
            return float(s.labels[0].score)
        elif s.labels[0].value == 'NEGATIVE':
            return float(-s.labels[0].score)
        else:
            return float(s.labels[0].score)
    except:
        return 0.0


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


def sentiment_match(data, ASPECTS, col_name='sentences'):
    """

    :param data:
    :param ASPECTS:
    :return:
    """

    new_aspect_name = 'score'
    start = time.time()
    data[new_aspect_name] = data.apply(lambda x: findSentiment_v2(x[col_name]), axis=1)
    end = time.time()
    print(f"Took {end - start} seconds to find sentiment for each sentence.") # If needed to calculate

    return data, new_aspect_name


def word_match(data, keywords, ASPECTS):
    """

    :param data:
    :param ASPECTS:
    :return:
    """

    new_aspect_name = ASPECTS+'_match'
    start = time.time()
    data[new_aspect_name] = data.apply(lambda x: word_detection(x[ASPECTS], keywords), axis=1)
    end = time.time()
    print(f"Took {end - start} seconds to word match for each sentence.") # If needed to calculate

    return data, new_aspect_name


def phrase_match(data, column='reviews'):
    """

    :param keywords:
    :param ASPECTS:
    :return:
    """
    start = time.time()
    data['sent_phrase'] = data.apply(lambda x: phrase_extractor(x[column]), axis=1)
    end = time.time()
    print(f"Took {end - start} seconds to find phrase with corresponding sentences.") # If needed to calculate

    return data


def word_match_v2(data, keywords, ASPECTS, col_name='phrases'):
    """

    :param data:
    :param keywords:
    :param ASPECTS:
    :param col_name:
    :return:
    """

    start = time.time()
    data[ASPECTS] = data.apply(lambda x: find_keywords(x[col_name], keywords, ASPECTS), axis=1)
    end = time.time()
    print(f"Took {end - start} seconds to word match for each sentence.") # If needed to calculate

    return data, ASPECTS


