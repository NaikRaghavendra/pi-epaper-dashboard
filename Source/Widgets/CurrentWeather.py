
import logging
import os

import Geometry.Point as PT
import Geometry.Rectangle as RT
import Utilities.IconProvider as IP
import Weather.WeatherQuery as WQ
from PIL import Image, ImageDraw, ImageFont

fontfamily = 'DejaVuSansMono.ttf'
boldfontfamily = 'DejaVuSansMono-Bold.ttf'


class CurrentWeatherModel():
    def __init__(self, wm: WQ.WeatherModel):
        self.wm = wm

    def refresh(self):
        self.wm.queryWeather()

    def getCurrentTemp(self):
        self.refresh()
        return self.wm.currentweather.temp

    def getFeelsLikeTemp(self):
        self.refresh()
        return self.wm.currentweather.feels_like

    def getMinTemp(self):
        self.refresh()
        return round(self.wm.dayforecasts.dayforecasts[0].temp_min)

    def getMaxTemp(self):
        self.refresh()
        return round(self.wm.dayforecasts.dayforecasts[0].temp_max)

    def getHumidity(self):
        self.refresh()
        return self.wm.currentweather.humidity

    def getWeatherCode(self):
        self.refresh()
        return self.wm.currentweather.WeatherIconCode

    def getRainProbability(self):
        self.refresh()
        return self.wm.dayforecasts.dayforecasts[0].rain


class CurrentWeather():
    def __init__(self, tlx, tly, brx, bry, weathermodel_in):
        self.rect = RT.Rectangle(PT.Point(tlx, tly), PT.Point(brx, bry))
        offset = PT.Point(1, 1)
        self.workingarea = self.rect.offset(offset)

        self.currentweather = weathermodel_in

        self.curtempfont = ImageFont.truetype(fontfamily, 14)
        self.minmaxfont = ImageFont.truetype(fontfamily, 14)
        self.tempfont = ImageFont.truetype(fontfamily, 14)
        self.tempfont = ImageFont.truetype(fontfamily, 14)
        self.keyfont = ImageFont.truetype(fontfamily, 10)
        self.WeatherDetailsFont = ImageFont.truetype(fontfamily, 10)

    def gettextrect(self, drawimage, text, font):
        (width, height) = drawimage.textsize(text, font)
        return RT.Rectangle(PT.Point(0, 0), PT.Point(width, height))

    def displaytextcenteraligned(self, drawimage, text, displayregion, font):
        textrect = self.gettextrect(drawimage, text, font)
        centereddisplayrect = displayregion.alignCenter(textrect)
        drawimage.text(centereddisplayrect.tl.coords(), text, font=font)

    def displayhlvcaligned(self, drawimage, text, displayregion, font):
        textrect = self.gettextrect(drawimage, text, font)
        centereddisplayrect = displayregion.alignCenter(textrect)
        leftcenter = centereddisplayrect.offset(
            PT.Point((displayregion.tl.x - centereddisplayrect.tl.x), 0))
        drawimage.text(leftcenter.tl.coords(), text, font=font)

    def displayhrvcaligned(self, drawimage, text, displayregion, font):
        textrect = self.gettextrect(drawimage, text, font)
        centereddisplayrect = displayregion.alignCenter(textrect)
        leftcenter = centereddisplayrect.offset(
            PT.Point((displayregion.br.x - centereddisplayrect.br.x), 0))
        drawimage.text(leftcenter.tl.coords(), text, font=font)

    def displaykeyvalue(self, drawimage, rect, factor, key, value, keyfont, valuefont):
        logging.info(f"Value: {value}")
        (keyRect, valueRect) = rect.partition_x(factor)
        valueRect = valueRect.offset(PT.Point(5, 0))
        # drawimage.rectangle(keyRect.coords(),outline=0)
        # drawimage.rectangle(valueRect.coords(),outline=0)
        self.displayhrvcaligned(drawimage, key, keyRect, keyfont)
        self.displayhlvcaligned(drawimage, value, valueRect, valuefont)

    def display(self, HBlackimage, HRYimage):
        logging.info("CurrentWeather-Display")
        drawblack = ImageDraw.Draw(HBlackimage)
        drawred = ImageDraw.Draw(HRYimage)

        #drawblack.rectangle(self.rect.coords(), outline =0)

        (iconRect, textrect) = self.workingarea.partition_x(0.38)

        weathercode = self.currentweather.getWeatherCode()

        icondim = iconRect.getMinDimension()
        weathericon = IP.IconProvider().getImageForCode(weathercode, icondim, icondim)
        HBlackimage.paste(weathericon, iconRect.tl.coords())

        textrect = textrect.offset(PT.Point(2, 0))

        (TempRect, DetailsRect) = textrect.partition_y(0.33)
        (FeelsLikeRect, MinMaxRect) = DetailsRect.partition_y(0.5)

        self.displaykeyvalue(drawblack, TempRect, 0.3, "Current:",
                             f"{self.currentweather.getCurrentTemp():>2.1f}°C", self.keyfont, self.curtempfont)
        self.displaykeyvalue(drawblack, FeelsLikeRect, 0.3, "Feels:",
                             f"{self.currentweather.getFeelsLikeTemp():>2.1f}°C", self.keyfont, self.curtempfont)
        self.displaykeyvalue(drawblack, MinMaxRect, 0.3, "Min-Max:",
                             f"{self.currentweather.getMinTemp()}-{self.currentweather.getMaxTemp()}", self.keyfont, self.minmaxfont)

def getMergedRGBImage(blkimage, redimage):
    MergedImageRGB = Image.new('RGB', blkimage.size, (255, 255, 255))
    width, height = blkimage.size
    for x in range(width):
        for y in range(height):
            (r, g, b) = (255, 255, 255)
            if(redimage.getpixel((x, y)) == 0):
                (r, g, b) = (255, 0, 0)
            elif(blkimage.getpixel((x, y)) == 0):
                (r, g, b) = (0, 0, 0)
            MergedImageRGB.putpixel((x, y), (r, g, b))
    return MergedImageRGB


if __name__ == "__main__":

    model = CurrentWeatherModel()
    #app = WindCompass(0,0,295,151,model)
    app = CurrentWeather(50, 50, 213, 110, model)
    HBlackimage = Image.new('1', (296, 152), 255)  # 296*152
    # 296*152  ryimage: red or yellow image
    HRYimage = Image.new('1', (296, 152), 255)

    app.display(HBlackimage, HRYimage)

    mergedImage = getMergedRGBImage(HBlackimage, HRYimage)
    mergedImage.show()
