import logging

import Geometry.Point as PT
import Utilities.Recurrer as AR
import Widgets.CurrentWeather as CW
import Widgets.SunPosition as SP
import Widgets.WindCompass as WC
import Weather.WeatherQuery as WQ
from PIL import ImageDraw

import Apps.BaseApp as BA

fontfamily = 'DejaVuSansMono.ttf'
boldfontfamily = 'DejaVuSansMono-Bold.ttf'


class MainWeatherApp(BA.BaseApp):
    def __init__(self, apphost, rect, wm:WQ.WeatherModel):
        super(MainWeatherApp,self).__init__(apphost,rect)
        self._ar = AR.Recurrer(300,self.requestUpdate)
        self._wm = wm

        windcompside = self._rect.getMinDimension()
        (windcomprect, rightrect) = self._rect.partition_x(windcompside/self._rect.width())

        self._wc = WC.WindCompass(windcomprect,WC.WindModel(self._wm))

        rightrect = rightrect.shrink(PT.Point(0,1), PT.Point(0,0))
        (currentweatherrect, sunpositionrect) = rightrect.partition_y(0.37) 

        cw_coords = currentweatherrect.coords()
        self._cw = CW.CurrentWeather(cw_coords[0],cw_coords[1],cw_coords[2],cw_coords[3],CW.CurrentWeatherModel(self._wm))

        sp_coords = sunpositionrect.coords()
        self._sp = SP.SunPosition(sp_coords[0],sp_coords[1],sp_coords[2],sp_coords[3],SP.SunPositionModel(self._wm))


    def requestUpdate(self):
        self.apphost.queue(self)

    def update(self, image):
        logging.debug("Updating weather ..")
        
        dictDraw = ImageDraw.Draw(image)

        # fill background
        dictDraw.rectangle(self._rect.coords(), fill = 255)

        self._wc.display(image, image)
        self._sp.display(image, image)
        self._cw.display(image, image)
