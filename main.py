# -*- coding: utf-8 -*-
# Language Analysis ABSA v4.0
#
# Main file for passing arguments and main functions
# to run Language Analysis v4.0
#
# Copyright (C) 2019-2021 Guide Analytics
# Author: Michael Brock Li <michael.brock.li@gmail.com>
#
# URL: <https://guideanalytics.ca>


import sys
import os
import random
import yaml
import argparse
import logging
import pandas as pd
import glob

import json
import re

from clean.preprocessing import DataClean
from absa.heatmap import heatmap
from absa.wordcloud import wordcloud

def get_args():
    """
    Arguments for running the Langauge Analysis ABSA program. Here, the argument parameters:

    --corpus: str, corpus path location (currently in .txt file format follow by specific file name types)
    --data: str, data path location (data input location, currently in .csv file format)
    --output: str, output path location for the resulting line chart, heatmap, wordcloud, geomap.

    :return: paras (argument parameters to pass through to the main function below)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--corpus', type=str, default=None, help='locate the corpus folder to use the corpus dataset')
    parser.add_argument('--data', type=str, default=None, help='data folder for data inputs')
    parser.add_argument('--output', type=str, default='line_chart', choices=['line_chart', 'heatmap', 'word_cloud', 'geomap'])
    parser.add_argument('--para', type=str, default='para.yml', help="the path to the parameter file, has to be a yaml file")

    args = parser.parse_args()

    with open(args.para) as fin:
        paras = yaml.safe_load(fin)
    if args.corpus is not None and os.path.exists(args.corpus):
        paras['corpus'] = args.corpus
    if args.data is not None and os.path.exists(args.data):
        paras['data'] = args.data
    paras['output'] = args.output
    if args.output == 'line_chart':
        pass
    elif args.output == 'heatmap':
        paras['heatmap'] = True
    elif args.output == 'word_cloud':
        paras['word_cloud'] = True
    elif args.output == 'geomap':
        pass

    print(paras)
    return paras


def generate_wordcloud(paras):
    """
    Generate a word pair infrastructure that is a dict of key pair list, where the key is the aspect label
    follow by a list of keywords associated with the aspect label

    :param corpus_path: in paras['corpus_path']
    :param data_path: in paras['data_path']
    :return: None (passes a data generation report)
    """

    corpus_path = paras['corpus']
    data_path = paras['data']

    logger_name = os.path.join(paras['log_dir'], "log.txt")
    LOG_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    logging.basicConfig(format=LOG_FORMAT, level=logging.INFO, filename=logger_name, filemode='w')
    logger = logging.getLogger()

    wordcloud()



def generate_heatmap(paras):
    """
    Generate a heatmap infrastructure that is the form of a nested dict ***UPDATE PURPOSE***

    :param corpus_path: in paras['corpus_path']
    :param data_path: in paras['data_path']
    :return: None (passes a data generation report)
    """

    corpus_path = paras['corpus']
    data_path = paras['data']

    logger_name = os.path.join(paras['log_dir'], "log.txt")
    LOG_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    logging.basicConfig(format=LOG_FORMAT, level=logging.INFO, filename=logger_name, filemode='w')
    logger = logging.getLogger()

    heatmap()


def data_input(data_path):
    """

    Combine all csvs in a designated input directory

    :param data_path:
    :return:
    """
    data_path = r''+data_path
    extension = 'csv'

    all_files = [i for i in glob.glob(os.path.join(data_path, '*.{}'.format(extension)))]
    combined_csv = pd.concat([pd.read_csv(f) for f in all_files])

    print(combined_csv.head(5))


def main():
    """
    Main function to execute the language analysis tool
    :return:
    """
    paras = get_args()
    print(paras)
    #paras['data_input'] = data_clean

    #reviews_corpus = list(final_df['reviews'])
    # Partition into sentences
   # reviews_in_sentences = [sent_tokenize(str(review)) for review in reviews_corpus]
   # reviews_length = [len(review) for review in reviews_in_sentences]

    # train orginal bert
    if paras['heatmap'] == True:
        if paras['corpus'] == './corpus' and paras['data'] == './data':
            generate_heatmap(paras)
    if paras['word_cloud'] == True:
        if paras['corpus'] == './corpus' and paras['data'] == './data':
            generate_wordcloud(paras)
    else:
        pass

"""
if '__name__' == '__main__':
    main()
"""
data_input('data/shipping')
