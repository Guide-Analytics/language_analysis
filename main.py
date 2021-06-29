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

import nltk
import pandas as pd
pd.options.mode.chained_assignment = None

nltk.download('wordnet')
nltk.download('punkt')

import benepar
benepar.download('benepar_en3')

import yaml
import argparse
import logging


from absa.text_analysis import *
from clean.dataframe_clean import *
from data_input import *
from absa.load_corpus import *
from absa.output_files import *


def get_args():
    """
    Arguments for running the Langauge Analysis ABSA program. Here, the argument parameters:

    --corpus: str, corpus path location (currently in .txt file format follow by specific file name types)
    --data: str, data path location (data input location, currently in .csv file format)
    --output: str, output path location for the resulting line chart, heatmap, wordcloud, geomap.

    :return: paras (argument parameters to pass through to the main function below)
    """
    industry_lst = ['shipping', 'flashlight']
    datatype_lst = ['csv', 'json', 'parquet']

    parser = argparse.ArgumentParser()
    parser.add_argument('--industry', type=str, default=None, choices=industry_lst, help='specify company type')
    parser.add_argument('--corpus', type=str, default=None, help='locate the corpus folder to use the corpus dataset')
    parser.add_argument('--data', type=str, default=None, help='data folder for data inputs')
    parser.add_argument('--data_type', type=str, default='csv', choices=datatype_lst, help='file_type')
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
    paras['data_type'] = args.data_type
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


def data_analysis(data, corpus_path, aspects, industry):
    """

    :param data:
    :return:
    """

    corpus_keywords, aspects = load_corpus(corpus_path=corpus_path, ASPECTS=aspects)
    new_data = aspect_match(data=data, keywords=corpus_keywords, ASPECTS=aspects)[0]

    new_data = data_row_filter(data=new_data, col_name=aspects)
    new_data = data_explode(data=new_data, first_col=aspects)
    if new_data.empty:
        print('No aspects detected')
    else:
        new_data, sentiment_aspect = sentiment_match(data=new_data, ASPECTS=aspects)
        new_data, word_aspect = word_match(data=new_data, keywords=corpus_keywords, ASPECTS=aspects)

        new_data = data_misc_removal(data=new_data)
        new_data = data_filter(data=new_data, first_col=sentiment_aspect, second_col=word_aspect)

        new_data = data_explode(data=new_data, first_col=word_aspect).reset_index(drop=True)
        new_data = data_tuple_v1(data=new_data, main_col=word_aspect)
        new_data = data_drop_dup(data=new_data, subset_col=['author_id', 'reviews', 'det_word', 'asp_word'])

    return new_data


def data_analysis_v2(data, corpus_path, aspects, industry):
    """

    :param data:
    :param corpus_path:
    :param aspects:
    :param industry:
    :return:
    """
    corpus_keywords, aspects = load_corpus(corpus_path=corpus_path, ASPECTS=aspects)
    new_data = phrase_match(data=data)
    check = new_data

    ## Sentence phrases is a list --> explode to multiple sentences with corresponding phrases
    check = data_explode(data=check, first_col='sent_phrase')
    check = data_tuple(data=check, col_name='sent_phrase', col_lst=['sentences', 'phrases'])

    ## Phrases is a list --> explode to multiple phrases with corresponding sentence
    check = data_explode(data=check, first_col='phrases')

    check = sentiment_match(data=check, ASPECTS=aspects)[0]
    check = word_match_v2(data=check, keywords=corpus_keywords, ASPECTS=aspects)[0]

    new_data = data_filter(data=check, first_col='phrases', second_col=aspects)
    new_data = data_misc_removal(data=new_data)
    new_data = data_explode(data=new_data, first_col=aspects)
    new_data = data_tuple_v1(data=new_data, main_col=aspects)

    new_data = new_data.drop(aspects, axis=1)
    new_data.to_csv(aspects+'.csv')

    return new_data




def main():
    """
    Main function to execute the language analysis tool
    :return:
    """

    #paras = get_args()
    #print(paras)

    from clean.preprocessing import DataClean
    from gramformer import Gramformer

    gf = Gramformer(models = 2, use_gpu=False)
    all_data = []
    global industry_corp_const

    from corpus_constants import CorporaConstants
    ic = CorporaConstants()

    ## Industry and data/corpus path arguments
    industry = 'neighbourhoods' # paras['industry']
    data_path = 'data/neighbourhoods/tripadvisor/'  # paras['data']
    corpus_path = './corpus/neighbourhoods.json' #paras['corpus']

    ## Data Load and Clean

    raw_data = data_input(data_path, '.csv') # Raw data input
    raw_data.to_csv('test.csv')
    raw_data['reviews'] = raw_data.apply(lambda entry: DataClean(entry['reviews'], model=None)\
                                  .use_cleantext_BEFORE(), axis=1)

    # raw_data['reviews'] = raw_data.apply(lambda entry: DataClean(entry['reviews'], model=gf)\
                                  #.use_grammarfix(version='v2'), axis=1)

    if industry == 'shipping':
        industry_corp_const = ic.shipping()
    elif industry == 'real_estate':
        industry_corp_const = ic.real_estate()
    elif industry == 'neighbourhoods':
        industry_corp_const = ic.neighbourhoods()

    for aspects in industry_corp_const:
        print(aspects)
        data = data_analysis_v2(raw_data, corpus_path, aspects, industry) # Data industry with specified industry
        all_data.append(data)

    all_data_df = pd.concat(all_data)
    all_data_df.to_csv('neighbourhoods.csv')

    """
    if paras['heatmap'] == True:
        if paras['corpus'] == './corpus' and paras['data'] == './data':
            generate_heatmap(paras)
    """
    #heatmap(all_data_df)
    """
    if paras['word_cloud'] == True:
        if paras['corpus'] == './corpus' and paras['data'] == './data':
            generate_wordcloud(paras)
    """
    ## --> generate_wordcloud()
    #wordcloud(all_data_df)

"""
if '__name__' == '__main__':
    main()
"""
main()
