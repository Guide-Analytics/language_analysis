# -*- coding: utf-8 -*-
# Language Analysis ABSA v4.0
#
# Corpus Constants Bank: Based on industry type
#
# Copyright (C) 2019-2021 Guide Analytics
# Author: Michael Brock Li <michael.brock.li@gmail.com>
#
# URL: <https://guideanalytics.ca>


class CorporaConstants():

    def __init__(self):
        self.corpus = None

    def shipping(self):
        """

        :return:
        """
        self.corpus = list()
        PRICE = "price"
        SPEED = "speed"
        WEBSITE = "website"
        SERVICE = "service"
        QUALITY = "quality"
        self.corpus.extend([PRICE, SPEED, WEBSITE, SERVICE, QUALITY])

        return self.corpus

    def flashlight(self):
        """

        :return:
        """
        self.corpus = list()

        return self.corpus
