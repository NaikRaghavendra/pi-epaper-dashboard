
import os
import sys

import logging

from PIL import Image, ImageDraw

libdir = os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__)))), 'lib/RaspberryPi_JetsonNano/python/lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V2


class EPaperDisplay():
    def __init__(self):
        logging.info("Initializing EPD")
        self._epd = epd2in13_V2.EPD()
        self._epd.init(self._epd.FULL_UPDATE)

    def width(self):
        return self._epd.width

    def height(self):
        return self._epd.height

    def clear(self):
        self._epd.Clear(0xFF)
        

    def fullupdate(self, image:Image):
        self.clear()
        self._epd.init(self._epd.FULL_UPDATE)
        self._epd.display(self._epd.getbuffer(image))

    def beginPartUpdate(self, backimage:Image):
        logging.info("Setting epd mode to Part update")
        self._epd.init(self._epd.FULL_UPDATE)
        self._epd.displayPartBaseImage(self._epd.getbuffer(backimage))
        self._epd.init(self._epd.PART_UPDATE)

    def partialUpdate(self, image:Image):
        self._epd.displayPartial(self._epd.getbuffer(image))
