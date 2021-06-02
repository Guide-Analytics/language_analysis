# -*- coding: utf-8 -*-
# Language Analysis ABSA v4.0
#
# Punctuation Removal Simple Tool
#
# Copyright (C) 2019-2021 Guide Analytics
# Author: Michael Brock Li <michael.brock.li@gmail.com>
#
# URL: <https://guideanalytics.ca>

import re
import string

class PunctuationRemoval(object):
    """
    V1.0 Punctuation Removal - Needs update on actually removing multiple ASCII code symbols for punctuations

    """

    def remove_nuke(self, data):

        """

        :param data:
        :return:
        """
        self.data = data
        self.remove_whitespace()
        # self.remove_punctuation()
        self.remove_emails()
        self.remove_line_char()
        self.remove_single_quotes()
        self.remove_weirdness()
        self.remove_eclipses()
        self.lowercase()

        return self.data

    def lowercase(self):

        """
        :return:
        """

        data = self.data
        try:
            self.data = data.lower()
        except AttributeError:
            self.data = ""

        return self.data

    def remove_whitespace(self):

        """
        :return:
        """

        data = self.data
        try:
            self.data = re.sub(r"^\s+|\s+$", "", data)
        except:
            self.remove_weirdness()
        return self.data

    def remove_weirdness(self):

        """

        :return:
        """

        data = self.data
        try:
            emoji = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
            self.data = emoji.sub(r'', data)
        except:
            pass
        return self.data

    def remove_emails(self):

        """
        :purpose: doesn't really work - only removing @'string' until hits whitespace
        :return:
        """

        data = self.data
        try:
            self.data = re.sub("\S@\\S*\\s?", '', data)
        except:
            self.remove_weirdness()

        return self.data

    def remove_line_char(self):

        """

        :return:
        """

        data = self.data
        try:
            self.data = re.sub('\\s+', ' ', data)
        except:
            self.remove_weirdness()
        return self.data

    def remove_single_quotes(self):

        """

        :return:
        """

        data = self.data
        try:
            self.data = re.sub("\'", "", data)
        except:
            pass
        return self.data

    def remove_punctuation(self):

        """

        :return:
        """

        data = self.data
        try:
            self.data = data.translate(str.maketrans('', '', string.punctuation))
        except AttributeError:
            pass
        return self.data

    def remove_eclipses(self):

        """

        :return:
        """

        data = self.data
        try:
            self.data = data.strip('…')
        except AttributeError:
           pass
        return self.data

    def legacy_remove_punctuations(self):
        """
        Legacy method: Do not use
        :return:
        """
        data = self.data

        punctuations = string.punctuation
        punctuations_pattern = r"[{}]".format(punctuations)
