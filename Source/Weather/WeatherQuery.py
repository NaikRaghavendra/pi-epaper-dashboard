from datetime import datetime
import Weather.WeatherQueryProxy as WQP

class DayForecast():
    def __init__(self, dayForecastDict):
        self.TimeStamp = datetime.fromtimestamp(dayForecastDict["dt"])
        self.Sunrise = datetime.fromtimestamp(dayForecastDict["sunrise"])
        self.Sunset = datetime.fromtimestamp(dayForecastDict["sunset"])
        self.Moonrise = datetime.fromtimestamp(dayForecastDict["moonrise"])
        self.Moonset = datetime.fromtimestamp(dayForecastDict["moonset"])
        self.Moonphase = dayForecastDict["moon_phase"]
        self.temp_min = dayForecastDict["temp"]["min"]
        self.temp_max = dayForecastDict["temp"]["max"]
        self.pressure = dayForecastDict["pressure"]
        self.humidity = dayForecastDict["humidity"]
        self.dew_ponit = dayForecastDict["dew_point"]
        self.wind_speed = dayForecastDict["wind_speed"] if "wind_speed" in dayForecastDict else 0.0
        self.wind_deg = dayForecastDict["wind_deg"] if "wind_deg" in dayForecastDict else 0.0
        self.wind_gust = dayForecastDict["wind_gust"] if "wind_gust" in dayForecastDict else 0.0
        self.WeatherIconCode = dayForecastDict["weather"][0]["icon"]
        self.WeatherIconDescription = dayForecastDict["weather"][0]["description"]
        self.rain = dayForecastDict["rain"] if "rain" in dayForecastDict else 0.0
        self.clouds = dayForecastDict["clouds"]
        self.pop = dayForecastDict["pop"]
        self.uvi = dayForecastDict["uvi"]


class DailyForecast():
    def __init__(self, dailyArray):
        self.dayforecasts = []
        for day in dailyArray:
            self.dayforecasts.append(DayForecast(day))


class CurrentWeather():
    def __init__(self, dictCurrentWeather):
        self.TimeStamp = datetime.fromtimestamp(dictCurrentWeather["dt"])
        self.Sunrise = datetime.fromtimestamp(dictCurrentWeather["sunrise"])
        self.Sunset = datetime.fromtimestamp(dictCurrentWeather["sunset"])
        self.temp = dictCurrentWeather["temp"]
        self.feels_like = dictCurrentWeather["feels_like"]
        self.pressure = dictCurrentWeather["pressure"]
        self.humidity = dictCurrentWeather["humidity"]
        self.dew_point = dictCurrentWeather["dew_point"]
        self.uvi = dictCurrentWeather["uvi"]
        self.clouds = dictCurrentWeather["clouds"]
        self.visibility = dictCurrentWeather["visibility"]
        self.wind_speed = dictCurrentWeather["wind_speed"] if "wind_speed" in dictCurrentWeather else 0.0
        self.wind_deg = dictCurrentWeather["wind_deg"] if "wind_deg" in dictCurrentWeather else 0.0
        self.wind_gust = dictCurrentWeather["wind_gust"] if "wind_gust" in dictCurrentWeather else 0.0
        self.WeatherIconCode = dictCurrentWeather["weather"][0]["icon"]
        self.WeatherIconDescription = dictCurrentWeather["weather"][0]["description"]


class WeatherModel():
    def __init__(self, lattitude, longitude, wqp:WQP.WeatherQueryProxy):
        self.lat = lattitude
        self.lon = longitude
        self.wqp = wqp
        self.queryWeather()

    def queryWeather(self):
        data = self.wqp.query(self.lat, self.lon)
        self.currentweather = CurrentWeather(data["current"])
        self.dayforecasts = DailyForecast(data["daily"])

    def getRefreshTimeout(self):
        return round(self.wqp.queryInvalidationTimeout.total_seconds())

