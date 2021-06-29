# -*- coding: utf-8 -*-
# Language Analysis ABSA v4.0
#
# Grammar Tool (Fixes and updates)
# NEED MORE UPDATES
#
# Copyright (C) 2019-2021 Guide Analytics
# Author: Michael Brock Li <michael.brock.li@gmail.com>
#
# URL: <https://guideanalytics.ca>

from gingerit.gingerit import GingerIt

class GrammarTool(object):

    def __init__(self, text, model, version):
        """

        :param text:
        """
        if version == 'v2':
            self.gf = model

        self.text = str(text)

    def grammarFix(self):
        """
        GingerIt grammar fix tool will has its limitations (cuase it's not going to process
        large sentences. Use GingerIT for shorter sentences
        :return:
        """

        parser = GingerIt()
        try:
            result = str(parser.parse(self.text)['result'])
            return result
        except:
            result = self.text
            return result

    def grammarFix_v2(self):
        """
        Gramform tool ..
        :return:
        """
        corrected_sentence = self.gf.correct(self.text)
        try:
            corrected_sentence = corrected_sentence[0]
        except IndexError:
            corrected_sentence = self.text

        return corrected_sentence
