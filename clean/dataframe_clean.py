# -*- coding: utf-8 -*-
# Language Analysis ABSA v4.0
#
# Dataframe Cleaning Tool
# Alpha version (NEEDS TO BE UPDATED)
# Some of the functionalities in here will be used for final data processing
#
# Copyright (C) 2019-2021 Guide Analytics
# Author: Michael Brock Li <michael.brock.li@gmail.com>
#
# URL: <https://guideanalytics.ca>

from itertools import chain
import pandas as pd

def data_misc_removal(data):
    """

    :param data:
    :return:
    """
    try:
        data = data.drop(data.filter(regex="Unname"), axis=1, inplace=False)
    except:
        pass

    try:
        data = data.drop(data.filter(regex="_cleaned"), axis=1, inplace=False)
    except:
        pass

    return data


def data_filter(data, first_col, second_col):
    """

    :param data:
    :param first_col:
    :param second_col: typically used in detected list of words (likely chance this not be detected)
    :return:
    """
    data = data[data[first_col].notna()]
    data = data[data[second_col].notna()]
    data = data[data[second_col].map(lambda d: d != [])]
    #data = data.dropna(subset=[first_col, second_col])

    return data


def data_explode(data, first_col):
    """

    :param data:
    :return:
    """
    try:
        data = data.explode(first_col)
    except KeyError:
        print('Key doesnt exist - because column was not created')
        return data

    return data


def data_drop_dup(data, subset_col):
    """

    :param data:
    :param subset_col: [] list
    :return:
    """
    data = data.drop_duplicates(subset_col)

    return data


def data_tuple_v1(data, main_col, first_col='asp_word', second_col='det_word'):
    """

    :param first_data:
    :param second_data:
    :param main_col: ASPECTS typically
    :param first_col:
    :param second_col:
    :return:
    """
    try:
        if data[main_col].tolist() == []:
            data[first_col] = ''
            data[second_col] = ''
        else:
            data[first_col] = pd.DataFrame(data[main_col].tolist(), index=data.index)[0]
            data[second_col] = pd.DataFrame(data[main_col].tolist(), index=data.index)[1]
    except KeyError:
        print('Key doesnt exist - because column was not created')
        data[first_col] = ''
        data[second_col] = ''

    return data


def data_row_filter(data, col_name):
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


def data_tuple(data, col_name, col_lst):
    """

    :param data:
    :param col_name:
    :param col_lst:
    :return:
    """
    for n, col in enumerate(col_lst):
        data[col] = data[col_name].apply(lambda col: col[n])

    data = data.drop(col_name, axis=1)
    return data


def data_tuple_v2(data, col_name, col_lst):
    """

    :param data:
    :param col_name:
    :param col_lst:
    :return:
    """
    data = pd.DataFrame(list(chain.from_iterable(data[col_name])), columns=col_lst)\
             .reset_index(drop=True)

    return data


def data_string_join(data, col_name):
    """

    :param data:
    :param col_name:
    :return:
    """


    return
