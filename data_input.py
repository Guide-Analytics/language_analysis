# -*- coding: utf-8 -*-
# Language Analysis ABSA v4.0
#
# Data Input file
#
# Copyright (C) 2019-2021 Guide Analytics
# Author: Michael Brock Li <michael.brock.li@gmail.com>
#
# URL: <https://guideanalytics.ca>

import os
import glob
import pandas as pd
import json


def data_input(data_path, data_type='.csv'):
    """

    Combine all csvs in a designated input directory

    :param data_path:
    :return:
    """
    if data_type == '.csv':
        data_output = csv_data(data_path, data_type)
    else:
        data_output = json_data(data_path, type='.json')

    return data_output


def json_data(data_path, type='.json'):
    """

    Combine all jsons in a designated input directory.
    JSON outputs are usually from a scraper
    :param data_path:
    :param type:
    :return:
    """
    if data_path.endswith(type):
        json_files = [data_path]
    else:
        json_files = [data_path+pos_json for pos_json in os.listdir(data_path) if pos_json.endswith(type)]
        print(json_files)

    small_dfs = []
    for file in json_files:
        f = open(file, encoding='utf-8')
        json_data = json.load(f)
        f.close()
        df = pd.json_normalize(json_data, 'reviews', ['title', 'scrapedAt', 'categoryName', 'address', 'totalScore',
                                                      'reviewsCount', 'location', 'url'], record_prefix='')
        small_dfs.append(df)

    final_df = pd.concat(small_dfs, ignore_index=True)
    final_df = final_df.rename(columns={'text': 'reviews', 'reviewerId':'author_id', 'title': 'companyName'})

    ## Arbitrary Select method (will not be used in the future)
    final_df = final_df[['companyName', 'author_id', 'name', 'reviews', 'categoryName', 'totalScore',
                         'url', 'reviewId', 'reviewUrl', 'reviewerUrl']]

    final_df = final_df.dropna(subset=['reviews'])

    final_df.to_csv('test.csv')

    return final_df


def csv_data(data_path, type='csv'):
    """

    :param data_path:
    :param type:
    :return:
    """
    data_path = r''+data_path
    extension = 'csv'

    all_files = [i for i in glob.glob(os.path.join(data_path, '*.{}'.format(extension)))]
    combined_csv = pd.concat([pd.read_csv(f) for f in all_files])
    return combined_csv


def parquet_data(data_path, type='parquet'):
    return
