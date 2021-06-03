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
    :param second_col:
    :return:
    """
    data = data[data[first_col].notna()]
    data = data[data[second_col].notna()]
    data = data[data[second_col].map(lambda d: d != [])]
    data = data.dropna(subset=[first_col, second_col])

    return data


def data_explode(data, first_col):
    """

    :param data:
    :return:
    """
    data = data.explode(first_col)

    return data


def data_drop_dup(data, subset_col):
    """

    :param data:
    :param subset_col: [] list
    :return:
    """
    data = data.drop_duplicates(subset_col)

    return data


def data_same_join(data, main_col, first_col='det_word', second_col='asp_word'):
    """

    :param first_data:
    :param second_data:
    :param main_col: ASPECTS typically
    :param first_col:
    :param second_col:
    :return:
    """

    data = data.join(pd.DataFrame(pd.DataFrame(data[main_col].tolist(), columns=[first_col, second_col])))

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
