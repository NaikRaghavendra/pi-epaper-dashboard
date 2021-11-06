import logging
import time

import Geometry.Point as PT
import Utilities.Recurrer as AR
from PIL import ImageDraw, ImageFont

import Apps.BaseApp as BA

fontfamily = 'DejaVuSansMono.ttf'
boldfontfamily = 'DejaVuSansMono-Bold.ttf'


class StatusClockApp(BA.BaseApp):
    def __init__(self, apphost, rect):
        super(StatusClockApp,self).__init__(apphost, rect)
        self._ar = AR.MinuteRecurrer(1,self.requestUpdate)
        self._bfont = ImageFont.truetype(boldfontfamily, 22)
        self.requestUpdate()

    def requestUpdate(self):
        self.apphost.queue(self)

    def update(self, image):
        logging.debug("StatusClockApp: updating")
        texttoshow = time.strftime('%H:%M')
        logging.debug(f"StatusClockApp: {texttoshow}")
        
        time_draw = ImageDraw.Draw(image)
        # fill background
        time_draw.rounded_rectangle(self._rect.coords(), fill = 1, radius = 4, outline=0, width=2)
        time_draw.text(self._rect.tl.offset(PT.Point(0,-2)).coords(),texttoshow,font=self._bfont)
