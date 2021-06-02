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

    def __init__(self, text):
        self.text = text

    def grammarFix(self):
        """

        :return:
        """

        parser = GingerIt()
        try:
            result = str(parser.parse(self.text)['result'])
            return result
        except:
            result = str(self.text)
            return result
