import asyncio
import logging
import signal
import os
import sys
import traceback

import yaml
from PIL import Image, ImageDraw

import Apps.MainWeather as AWMA
import Apps.StatusClock as ACA
import Apps.StatusCurrentTemp as SCT
import Apps.StatusCurrentWeather as SCW
import Device.EPDDevice as EPD
import Device.TestDevice as TD
import Geometry.Point as PT
import Geometry.Rectangle as RT
import Weather.WeatherQuery as WQ
import Weather.WeatherQueryProxy as WQP


class AppHost:
    def __init__(self, device):
        self._epd = device
        self._initcfg()
        self._initvips()
        self._initloop()
        self._initqueue()
        self._initdevice()
        self._initsignal()
        self._initweathermodel()
        self._initapps()
        self._runforever()
    
    def _initcfg(self):
        configpath = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'Config.yml')       
        with open(configpath, "r") as ymlfile:
            self._config = yaml.load(ymlfile,yaml.Loader)

    def _initweathermodel(self):
        apikey = self._config["weather"]["openweathermapapikey"]
        refreshtimeout = self._config["weather"]["refreshtimeoutinmins"]
        self._wqp = WQP.WeatherQueryProxy(apikey,refreshtimeout)

        lat = self._config["weather"]["lat"]
        lon = self._config["weather"]["lon"]
        self._wm = WQ.WeatherModel(lat,lon, self._wqp)

    def _initvips(self):
        return

    async def refreshworker(self):
        logging.info("Refresh worker thread started ..")
        while True:
            refreshapp = await self._queue.get()
            logging.info(f"Refreshing {refreshapp}")
            try:
                self._refreshapp(refreshapp)
            except:
                exc_type, exc_value, exc_tb = sys.exc_info()
                logging.error(
                    f"Caught exception in refreshworker, Exception:{traceback.format_exception(exc_type, exc_value, exc_tb)}")
            logging.info(f"Refresh Returning {refreshapp}")

    def _refreshapp(self, refreshapp):
        refreshapp.update(self._image)
        self._epd.partialUpdate(self._image)

    def _initqueue(self):
        self._queue = asyncio.Queue()
        self._refreshtask = self._loop.create_task(self.refreshworker())

    def _runforever(self):
        self._loop.run_forever()

    def _initapps(self):
        screenrect = RT.Rectangle(PT.Point(0, 0), PT.Point(self._epd.height(), self._epd.width()))
        apprect = screenrect.shrink(PT.Point(2,2),PT.Point(2,2))
        (statusrect,mainapprect) = apprect.partition_y(22/screenrect.height())
        (statuslhsrect, statusrhsrect) = statusrect.partition_x(0.55)
        (statusunusedrhsrect,statusclockrect) = statusrhsrect.partition_x(0.4)
        (statustemprect, statuscwrect) = statuslhsrect.partition_x(0.7)

        mainapprect = mainapprect.shrink(PT.Point(0,1),PT.Point(0,1))

        self._applist = []
        self._applist.append(ACA.StatusClockApp(self, statusclockrect))
        self._applist.append(SCT.StatusCurrentWeatherTempApp(self, statustemprect,self._wm))
        self._applist.append(SCW.StatusCurrentWeatherIconApp(self, statuscwrect,self._wm))
        self._applist.append(AWMA.MainWeatherApp(self, mainapprect,self._wm))
        self._applist[-1].requestUpdate()

    def _initloop(self):
        self._loop = asyncio.get_event_loop()

    def _initdevice(self):
        self._clear()
        self._setbackgroundimage()

    def _clear(self):
        self._epd.clear()

    def _setbackgroundimage(self):
        self._image = Image.new('1', (self._epd.height(), self._epd.width()), 255)
        draw = ImageDraw.Draw(self._image)
        borderrect = RT.Rectangle(PT.Point(0,0), PT.Point(self._epd.height(),self._epd.width()))
        borderrect = borderrect.shrink(PT.Point(0,0), PT.Point(1,1))
        draw.rectangle(borderrect.coords(), fill=255, outline=0)
        self._epd.beginPartUpdate(self._image)

    def _initsignal(self):
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signal, frame):
        logging.info('Event loop terminated, exiting application')
        self._loop.stop()
        sys.exit(0)

    def queue(self, baseapp):
        logging.info(f'Queue called : Queue size: {self._queue.qsize()}')
        self._queue.put_nowait(baseapp)


if __name__ == "__main__":
    logging.basicConfig(
            format='%(asctime)s %(message)s', level=logging.DEBUG)
    ah = AppHost(EPD.EPaperDisplay())
    #ah = AppHost(TD.TestDevice(122,250, "/home/pi/dump"))
