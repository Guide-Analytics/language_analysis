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
# from absa.heatmap import heatmap
from absa.wordcloud import wordcloud_output
from absa.text_analysis import aspect_match, sentiment_match, word_match
from absa.load_corpus import load_corpus
from clean.dataframe_clean import *


def get_args():
    """
    Arguments for running the Langauge Analysis ABSA program. Here, the argument parameters:

    --corpus: str, corpus path location (currently in .txt file format follow by specific file name types)
    --data: str, data path location (data input location, currently in .csv file format)
    --output: str, output path location for the resulting line chart, heatmap, wordcloud, geomap.

    :return: paras (argument parameters to pass through to the main function below)
    """
    industry_lst = ['shipping', 'flashlight']
    parser = argparse.ArgumentParser()
    parser.add_argument('--industry', type=str, default=None, choices=industry_lst, help='specify company type')
    parser.add_argument('--corpus', type=str, default=None, help='locate the corpus folder to use the corpus dataset')
    parser.add_argument('--data', type=str, default=None, help='data folder for data inputs')
    parser.add_argument('--output', type=str, default='line_chart', choices=['line_chart', 'heatmap', 'word_cloud', 'geomap'])
    parser.add_argument('--para', type=str, default='para.yml', help="the path to the parameter file, has to be a yaml file")

    args = parser.parse_args()

    with open(args.para) as fin:
        paras = yaml.safe_load(fin)
    if args.industry is not None:
        paras['industry'] = args.industry
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

    return combined_csv


def data_analysis(data, corpus_path, industry):
    """

    :param data:
    :return:
    """
    global industry_corp_const
    from corpus_constants import CorporaConstants
    ic = CorporaConstants()

    if industry == 'shipping':
        industry_corp_const = ic.shipping()

    cleaned_data = data.apply(lambda entry: DataClean(entry['reviews']).use_cleantext(), axis=1)
    data['reviews'] = cleaned_data
    #cleaned_data = data.apply(lambda entry: DataClean(entry['reviews']).use_grammarfix(), axis=1)
    #data['reviews'] = cleaned_data
    for aspects in industry_corp_const:

        corpus_keywords, aspects = load_corpus(corpus_path=corpus_path, ASPECTS=aspects)
        new_data = aspect_match(data=data, keywords=corpus_keywords, ASPECTS=aspects)[0]

        new_data = data_row_filter(data=new_data, col_name=aspects)
        new_data = data_explode(data=new_data, first_col=aspects)
        if new_data.empty:
            print('No aspects detected')
            continue
        else:
            new_data, sentiment_aspect = sentiment_match(data=new_data, ASPECTS=aspects)
            new_data, word_aspect = word_match(data=new_data, keywords=corpus_keywords, ASPECTS=aspects)

            new_data = data_misc_removal(data=new_data)
            new_data = data_filter(data=new_data, first_col=sentiment_aspect, second_col=word_aspect)

            new_data = data_explode(data=new_data, first_col=word_aspect).reset_index(drop=True)
            new_data = data_same_join(data=new_data, main_col=word_aspect)
            new_data = data_drop_dup(data=new_data, subset_col=['author_id', 'reviews', 'det_word', 'asp_word'])
            new_data.to_csv(aspects+'.csv')


def main():
    """
    Main function to execute the language analysis tool
    :return:
    """
     #paras = get_args()
    #print(paras)

    ## Industry and data/corpus path arguments
    industry = 'shipping' # paras['industry']
    data_path = './data/shipping/' # paras['data']
    corpus_path = './corpus/shipping.json' #paras['corpus']

    raw_data = data_input(data_path) # Raw data input
    data_analysis(raw_data, corpus_path, industry) # Data industry with specified industry

    """
    if paras['heatmap'] == True:
        if paras['corpus'] == './corpus' and paras['data'] == './data':
            generate_heatmap(paras)
    if paras['word_cloud'] == True:
        if paras['corpus'] == './corpus' and paras['data'] == './data':
            generate_wordcloud(paras)
    else:
        pass
    """
"""
if '__name__' == '__main__':
    main()
"""
main()
