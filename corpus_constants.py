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
        TECHNOLOGY = "technology"
        INTERNATIONAL = "international"
        COVID = "covid"
        GENERAL = "general"

        self.corpus.extend([PRICE, SPEED, WEBSITE, SERVICE, QUALITY, TECHNOLOGY, INTERNATIONAL, COVID, GENERAL])

        return self.corpus

    def real_estate(self):
        """

        :return:
        """
        self.corpus = list()
        KNOWLEDGE = "knowledgeability"
        PROFESSIONALISM = "professionalism"
        COMMUNICATION = "communication and responsive"
        WEBSITE_TECH = "website and technology"
        VALUE_OF_SERVICE = "value of service"
        REACH_LEAD_GEN = "reach and lead gen"
        FRIENDLINESS = "friendliness"
        HOME_PREP = "home prep"


        self.corpus.extend([KNOWLEDGE, PROFESSIONALISM, COMMUNICATION,
                            WEBSITE_TECH, VALUE_OF_SERVICE, REACH_LEAD_GEN,
                            FRIENDLINESS, HOME_PREP])

        return self.corpus

    def neighbourhoods(self):
        """

        :return:
        """

        self.corpus = list()
        HOUSING = "housing"
        SAFETY = "safety"
        TRANSIT = "transit"
        SHOPPING = "shopping"
        HEALTH = "health"
        ENTERTAINMENT = "entertainment"
        COMMUNITY_CRIME = "community and crime"
        DIVERSITY_INCLUSION = "diversity and inclusion"
        EDUCATION = "education"
        EMPLOYMENT = "employment"
        LOCAL = "local"


        self.corpus.extend([HOUSING, SAFETY, TRANSIT, SHOPPING,
                            HEALTH, ENTERTAINMENT, COMMUNITY_CRIME,
                            DIVERSITY_INCLUSION, EDUCATION, EMPLOYMENT,
                            LOCAL])
        return self.corpus


    def flashlight(self):
        """

        :return:
        """
        self.corpus = list()

        return self.corpus
