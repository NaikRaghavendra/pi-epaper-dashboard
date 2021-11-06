import requests
import json
from datetime import datetime, timedelta
import logging

bLoadWeatherModelFromFile = False

class WeatherQueryProxy():
    def __init__(self, apikey, refreshtimeoutinminutes):
        self.queryCache = {}
        self.api_key = apikey
        self.queryInvalidationTimeout = timedelta(minutes = refreshtimeoutinminutes)

    def query(self, lat, lon):
        if(bLoadWeatherModelFromFile):
            with open("C:\\Users\\IC005540\\Desktop\\Weather.json", "r") as infile:
                return json.load(infile)
        else:
            return self.queryCheckCache(lat,lon)


    def queryServer(self, lat, lon):
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
        response = requests.get(url)
        data = json.loads(response.text)
        return data

    def queryServerAndFillCache(self, lat,lon, internalcachekey):
        data = self.queryServer(lat,lon)
        self.queryCache[internalcachekey][0] = datetime.now()
        self.queryCache[internalcachekey][1] = data

    def queryCheckCache(self, lat, lon):
        internalcachekey = f"{lat}-{lon}"
        now = datetime.now()

        if internalcachekey in self.queryCache:
            cachedvaluesince = now - self.queryCache[internalcachekey][0]
            logging.info(f"CachedValueSince {cachedvaluesince}")
            if cachedvaluesince > self.queryInvalidationTimeout:
                logging.info(f"Cache Period Lapsed - requerrying")
                self.queryServerAndFillCache(lat,lon,internalcachekey)
            return self.queryCache[internalcachekey][1]
        else:
            logging.info(f"Querying First time for  {internalcachekey}")
            self.queryCache[internalcachekey] = []
            data = self.queryServer(lat,lon)
            self.queryCache[internalcachekey].append(now)
            self.queryCache[internalcachekey].append(data)
            return self.queryCache[internalcachekey][1]
