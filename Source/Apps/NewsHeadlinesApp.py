import json
import logging
import os
import random
import sys
import traceback
import requests

import Geometry.Point as PT
import Utilities.Recurrer as AR
from PIL import ImageDraw, ImageFont
import Utilities.TextWrapHelper as TWH

import Apps.BaseApp as BA

fontfamily = 'DejaVuSansMono.ttf'
boldfontfamily = 'DejaVuSansMono-Bold.ttf'


class NewsHeadlinesApp(BA.BaseApp):
    def __init__(self, apphost, rect, newsconfigjson):
        super(NewsHeadlinesApp, self).__init__(apphost, rect)
        self._initnewsparams(newsconfigjson)
        self._bfont = ImageFont.truetype(boldfontfamily, 30)
        self._font = ImageFont.truetype(fontfamily, 22)

        self._newsar = AR.Recurrer(self._refreshtimeoutinmins*60, self._updateheadlines)
        self._displayar = AR.Recurrer(self._displayrefreshtimeoutinmins*60, self.requestUpdate)
        self._latestheadlines = []
        self._updateheadlines()
        self._displayindex = 0

    def _initnewsparams(self, newsconfigjson):
        self._germandict = {}
        try:
            self._api_key = newsconfigjson["newsapikey"]
            self._refreshtimeoutinmins = newsconfigjson["refreshtimeoutinmins"]
            self._topics = newsconfigjson["topicsquery"]
            self._displayrefreshtimeoutinmins = newsconfigjson["displayrefreshtimeoutinmins"]
            self._country = newsconfigjson["country"]
            self._category = newsconfigjson["category"]
        except:
            exc_type, exc_value, exc_tb = sys.exc_info()
            logging.error(
                f"Caught exception. Exception:{traceback.format_exception(exc_type, exc_value, exc_tb)}")

    def requestUpdate(self):
        self.apphost.queue(self)

    def _updateheadlines(self):
        response = self._getlateststories()
        if len(response["articles"]) > 0:
            self._latestheadlines.clear()
            for article in response["articles"]:
                self._latestheadlines.append(article["title"])
            self._displayindex = 0

    def _getlateststories(self):
        try:
            url = f"https://newsapi.org/v2/top-headlines?apiKey={self._api_key}"
            if self._topics is not "":
                url = url + f"&q={self._topics}"
            if self._country is not "":
                url = url + f"&country={self._country}"
            if self._category is not "":
                url = url + f"&category={self._category}"

            logging.debug(f"URL request : {url}")
            response = requests.get(url)
            logging.error(f"Response : {response.ok}")
            return json.loads(response.text)
        except:
            exc_type, exc_value, exc_tb = sys.exc_info()
            logging.error(
                f"Caught exception. Exception:{traceback.format_exception(exc_type, exc_value, exc_tb)}")

        return None

    def _getheadlinetodisplay(self):
        indextouse = -1
        if(self._displayindex < len(self._latestheadlines)):
            indextouse = self._displayindex
            self._displayindex = self._displayindex + 1
            if (self._displayindex >= len(self._latestheadlines)):
                self._displayindex = 0
        
        if(indextouse > -1):
            headlinetoreturn = random.choice(self._latestheadlines)
            #headlinetoreturn = self._latestheadlines[indextouse]
        else:
            headlinetoreturn = "Error! : No news headlines to display"

        return headlinetoreturn

    def update(self, image):
        logging.debug("Updating Latest News")
        headlinetoshow = self._getheadlinetodisplay()
        
        dictDraw = ImageDraw.Draw(image)

        # Fill background with white
        dictDraw.rectangle(self._rect.coords(), fill=255, outline= 255)

        apprectangle = self._rect.shrink(PT.Point(1, 1), PT.Point(1, 1))

        drawrect = apprectangle.shrink(PT.Point(0,1), PT.Point(1,0))

        dictDraw.rounded_rectangle(drawrect.coords(),radius = 4)
        textrect = drawrect.shrink(PT.Point(2,1), PT.Point(2,1))

        TWH.showWrappedText(headlinetoshow,dictDraw,textrect,boldfontfamily,30,6)

