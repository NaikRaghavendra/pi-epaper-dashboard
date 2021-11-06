import logging

import Geometry.Point as PT
import Utilities.Recurrer as AR
import Weather.WeatherQuery as WQ
from PIL import ImageDraw, ImageFont

import Apps.BaseApp as BA

fontfamily = 'DejaVuSansMono.ttf'
boldfontfamily = 'DejaVuSansMono-Bold.ttf'


class StatusCurrentWeatherTempApp(BA.BaseApp):
    def __init__(self, apphost, rect, wm: WQ.WeatherModel):
        super(StatusCurrentWeatherTempApp,self).__init__(apphost,rect)
        self._ar = AR.Recurrer(300,self.requestUpdate)
        self._font = ImageFont.truetype(fontfamily, 22)
        self._wm = wm
        self.requestUpdate()

    def requestUpdate(self):
        self._wm.queryWeather()
        self.apphost.queue(self)

    def update(self, image):
        logging.debug("Updating weather ..")
        texttoshow = f"{self._wm.currentweather.temp:2.1f}°C"        
        
        time_draw = ImageDraw.Draw(image)
        # fill background
        time_draw.rectangle(self._rect.coords(), fill = 1, outline= 0, width=2)
        time_draw.text(self._rect.tl.offset(PT.Point(2,-2)).coords(), texttoshow, font = self._font)

        #VH.renderwrappedtext(texttoshow,self._rect, fontfamily, image, True)
