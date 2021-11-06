import logging
import os

import Utilities.IconProvider as IP
import Weather.WeatherQuery as WQ
from PIL import Image, ImageDraw, ImageFont


lat = "15.414260"
lon = "73.934112"

fontfamily = 'DejaVuSansMono.ttf'
boldfontfamily = 'DejaVuSansMono-Bold.ttf'

class SunPositionModel():
    def __init__(self, wm:WQ.WeatherModel):
        self.wm = wm

    def refresh(self):
        self.wm.queryWeather()

    def getsunrise(self):
        self.refresh()
        return self.wm.currentweather.Sunrise

    def getsunset(self):
        self.refresh()
        return self.wm.currentweather.Sunset

    def getcurrenttime(self):
        self.refresh()
        return self.wm.currentweather.TimeStamp


class SunPosition():
    def __init__(self, tlx, tly, brx, bry, sunmodel_in):
        self.tlx = tlx
        self.tly = tly
        self.brx = brx
        self.bry = bry

        self.iconwidth = 20
        self.iconheight = 20
        self.sunmodel = sunmodel_in

        ip = IP.IconProvider()

        self.sunrise = Image.new('1', (self.iconwidth, self.iconheight), 0)
        self.sunset = Image.new('1', (self.iconwidth, self.iconheight), 0)
        self.sun = Image.new('1', (self.iconwidth, self.iconheight), 0)

        self.sunrise = ip.getImageForCode(
            "sunrise", self.iconwidth, self.iconheight)
        self.sunset = ip.getImageForCode(
            "sunset", self.iconwidth, self.iconheight)
        self.sun = ip.getImageForCode("sun", self.iconwidth, self.iconheight)

        self.Hourfont = ImageFont.truetype(boldfontfamily, 16)

    def display(self, HBlackimage, HRYimage):
        logging.info("SunPosition-Display")
        drawblack = ImageDraw.Draw(HBlackimage)
        drawred = ImageDraw.Draw(HRYimage)

        leftoffset = 0
        rightoffset = 0
        topoffset = 2
        bottomoffset = 0

        sunrise_icon_tlx = self.tlx + leftoffset
        sunrise_icon_tly = self.tly + topoffset
        sunrise_icon_brx = sunrise_icon_tlx + self.sunrise.width
        sunrise_icon_bry = sunrise_icon_tly + self.sunrise.height

        sunset_icon_tlx = self.brx - rightoffset - self.sunset.width
        sunset_icon_tly = self.tly + topoffset
        sunset_icon_brx = sunset_icon_tlx + self.sunset.width
        sunset_icon_bry = sunset_icon_tly + self.sunset.height

        scaleoffset_y = 5

        major_tick_height = 7
        minor_tick_height = 3

        scale_tlx = sunrise_icon_tlx + int(self.sunrise.width/2)
        scale_tly = sunrise_icon_bry + scaleoffset_y + major_tick_height
        scale_bry = scale_tly
        scale_brx = sunset_icon_tlx + int(self.sunset.width/2)

        drawblack.line((scale_tlx, scale_tly, scale_brx,
                       scale_bry), fill=0, width=2)

        scaleMark_tly = scale_tly - scaleoffset_y
        scaleMark_bry = scale_tly + scaleoffset_y

        drawblack.line((scale_tlx, scaleMark_tly, scale_tlx,
                       scaleMark_bry), fill=0, width=1)
        drawblack.line((scale_brx, scaleMark_tly, scale_brx,
                       scaleMark_bry), fill=0, width=1)

        sunrise_verticaloffset = 4
        sunrise_icon_bry_new = scaleMark_bry + sunrise_verticaloffset

        HBlackimage.paste(
            self.sunrise, (sunrise_icon_tlx, sunrise_icon_bry_new))
        HBlackimage.paste(self.sunset, (sunset_icon_tlx, sunrise_icon_bry_new))

        risetosetminutes = int(
            (self.sunmodel.getsunset() - self.sunmodel.getsunrise()).total_seconds() / 60)

        scalewidth = scale_brx - scale_tlx
        pixelsperminute = scalewidth / risetosetminutes

        sunriseToNextHourOffset = 60 - self.sunmodel.getsunrise().minute
        firstHourAfterSunRise = self.sunmodel.getsunrise().hour + 1
        lastHourBeforeSunset = self.sunmodel.getsunset().hour
        numberofhourmarks = lastHourBeforeSunset - firstHourAfterSunRise + 1

        for i in range(numberofhourmarks):
            hoursAfterSunrise = firstHourAfterSunRise + i
            hourisEven = hoursAfterSunrise % 2 == 0
            linethickness = 2 if hourisEven else 1
            lineheight = major_tick_height if hourisEven else minor_tick_height

            houroffset = int(
                ((60 * i) + sunriseToNextHourOffset) * pixelsperminute)

            mark_tlx = scale_tlx + houroffset
            mark_tly = scale_tly
            mark_brx = mark_tlx
            mark_bry = mark_tly - lineheight

            drawblack.line((mark_tlx, mark_tly, mark_brx,
                           mark_bry), fill=0, width=linethickness)

            if(hoursAfterSunrise % 4 == 0):
                textmark = f"{hoursAfterSunrise}"
                (textwidth, textheight) = drawblack.textsize(
                    textmark, font=self.Hourfont)
                text_tlx = mark_tlx - int(textwidth/2)
                drawblack.text((text_tlx, mark_tly), textmark,
                               fill=0, font=self.Hourfont)

        if(self.sunmodel.getcurrenttime() > self.sunmodel.getsunrise() and self.sunmodel.getcurrenttime() < self.sunmodel.getsunset()):
            nowoffsetfromsunrise = int((self.sunmodel.getcurrenttime(
            ) - self.sunmodel.getsunrise()).total_seconds() / 60)
            nowsunicon_tlx = scale_tlx + \
                int(nowoffsetfromsunrise*pixelsperminute) - \
                int(self.sun.width/2)
            nowsunicon_tly = self.tly + topoffset + 3
            logging.info(f"Sun Positioned at {nowsunicon_tlx}")
            HBlackimage.paste(self.sun, (nowsunicon_tlx, nowsunicon_tly))


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

    model = SunPositionModel()
    app = SunPosition(100, 50, 295, 120, model)
    HBlackimage = Image.new('1', (296, 152), 255)  # 296*152
    # 296*152  ryimage: red or yellow image
    HRYimage = Image.new('1', (296, 152), 255)

    app.display(HBlackimage, HRYimage)

    mergedImage = getMergedRGBImage(HBlackimage, HRYimage)
    mergedImage.show()
