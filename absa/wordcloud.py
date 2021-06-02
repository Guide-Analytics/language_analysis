# -*- coding: utf-8 -*-
# Language Analysis ABSA v4.0
#
# Text analysis main function
#
# Copyright (C) 2019-2021 Guide Analytics
# Author: Michael Brock Li <michael.brock.li@gmail.com>
#
# URL: <https://guideanalytics.ca>


import json
import requests

lst = ['price', 'speed', 'website', 'quality', 'service']

def load_corpus(corpus_path, ASPECTS):
    """

    :param corpus_path:
    :param ASPECTS:
    :return:
    """

    with open(corpus_path, 'r') as read_file:
        corpus_data = json.load(read_file)
        for aspects in ASPECTS:
            keywords = corpus_data[aspects]



print(load_corpus('../corpus/shipping.json', lst))

