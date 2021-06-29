# -*- coding: utf-8 -*-
# Language Analysis ABSA v4.0
#
# Heatmap output file function
#
# Copyright (C) 2019-2021 Guide Analytics
# Author: Michael Brock Li <michael.brock.li@gmail.com>
#
# URL: <https://guideanalytics.ca>

from clean.preprocessing import DataClean
import pandas as pd

###### Call using df.query (for simple SQL functions)

def heatmap(data, descriptions='test'):
    """
    Query .....
    :param data
    :return:
    """

    import numpy as np
    from sklearn.preprocessing import MinMaxScaler
    scaler=MinMaxScaler(feature_range=(0, 100))

    def normalize(data):
        """

        :param data: parameter data is of form of a column, containing sentiment scores
        :return:
        """
        column_maxes = data
        """
        ## old code
        from sklearn import preprocessing

        x = data # returns a numpy array
        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(x)
        return x_scaled
        
        """

    data = data[['companyName', 'score', 'asp_word']]
    #data = data.apply(lambda x: normalize(x['score']), axis=1)
    data['new_score'] = scaler.fit_transform(data[['score']])
    data = data.groupby(['companyName'], as_index=False).mean().transform(lambda x: x).reset_index().apply(lambda x: x[['asp_word', 'new_score']].to_dict('r'))

    #data = data.groupby(['companyName', 'asp_word'], as_index=False).mean().transform(lambda x: x)\
               #.groupby(['companyName']).transform(lambda x: x)
    print(data.to_json('test.json', indent=2))


def wordcloud(data):
    """
    Query .....
    :param data:
    :return:
    """

    import copy
    """
    Json format - simply querying of first_keyword (asp_word), second_keyword (det_word), sentiment_score (score),
    sentences, companyName
    
    """
    data = data[['author_id', 'asp_word', 'det_word', 'score', 'reviews', 'companyName']]
    new_data = copy.deepcopy(data)
    new_data.loc[:, 'reviews'] = new_data['reviews'].apply(lambda x: DataClean(x, model=None).use_cleantext_AFTER())
    new_data = new_data.groupby(['asp_word', 'det_word', 'score', 'companyName'])
    new_data = new_data.apply(lambda x: x.to_dict('r'))
    new_data.to_json('test.json', indent=2)



#data = pd.read_csv('../test.csv')
#heatmap(data)
