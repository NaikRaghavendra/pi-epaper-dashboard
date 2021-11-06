
import os
import sys
from datetime import datetime

import logging

from PIL import Image, ImageDraw


class TestDevice():
    def __init__(self, width, height, dumpdir):
        logging.info("Initializing TestDevice")
        self._width = width
        self._height = height
        self._dumpdir = dumpdir


    def width(self):
        return self._width

    def height(self):
        return self._height

    def clear(self):
        self._image = None

    def _gettimestamppostfix(self):
        timestamp = datetime.now()
        return timestamp.strftime("%m%d%Y%H%M%S")

    def _getfilename(self, prefix):
        return f"{self._dumpdir}/{prefix}-{self._gettimestamppostfix()}.jpg"

    def fullupdate(self, image:Image):
        image.save(self._getfilename("FullUpdate"))

    def beginPartUpdate(self, backimage:Image):
        backimage.save(self._getfilename("Background"))

    def partialUpdate(self, image:Image):
        image.save(self._getfilename("PartialUpdate"))
