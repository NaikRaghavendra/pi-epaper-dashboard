import logging

import Geometry.Point as PT
import Geometry.Rectangle as RT
import Utilities.Recurrer as AR
import Utilities.IconProvider as IP
import Weather.WeatherQuery as WQ
from PIL import Image, ImageDraw

import Apps.BaseApp as BA

recurrertimeout = 300


class StatusCurrentWeatherIconApp(BA.BaseApp):
    def __init__(self, apphost, rect:RT.Rectangle, wm: WQ.WeatherModel):
        super(StatusCurrentWeatherIconApp,self).__init__(apphost, rect)        
        self._ar = AR.Recurrer(recurrertimeout,self.requestUpdate)
        self._wm = wm
        self._ip = IP.IconProvider()
        self.requestUpdate()
    

    def requestUpdate(self):
        self._wm.queryWeather()
        self.apphost.queue(self)

    def update(self, image:Image):
        logging.debug("StatusCurrentWeatherIconApp: Updating weather icon ..")

        iconrect = RT.Rectangle(PT.Point(0,0), PT.Point(self._rect.getMinDimension(), self._rect.getMinDimension()))
        iconrect = iconrect.shrink(PT.Point(2,2), PT.Point(2,2))

        weathericon = self._ip.getImageForCode(self._wm.currentweather.WeatherIconCode,iconrect.width(),iconrect.height())
        
        iconrect = self._rect.alignCenter(iconrect)

        draw = ImageDraw.Draw(image)
        draw.rectangle(self._rect.coords(), fill = 1,outline=0, width=2)
        tlcopied = (iconrect.tl.x, iconrect.tl.y)
        image.paste(weathericon,tlcopied)
