# -*- coding: utf-8 -*-
# Language Analysis ABSA v4.0
#
# Load Corpus from Corpus Bank
#
# Copyright (C) 2019-2021 Guide Analytics
# Author: Michael Brock Li <michael.brock.li@gmail.com>
#
# URL: <https://guideanalytics.ca>


import json


def load_corpus(corpus_path, ASPECTS):
    """
    Load corpus data from the corpus folder (or in other locations if specified in 'corpus_path')
    :param corpus_path: str, path of the corpus datafile
    :param ASPECTS: str, aspect string ONLY
    :return: [] list of keywords, associated with the ASPECT given
    """

    with open(corpus_path, 'r') as read_file:
        corpus_data = json.load(read_file)
        keywords = corpus_data[ASPECTS]

    return keywords, ASPECTS





