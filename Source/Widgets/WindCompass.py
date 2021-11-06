import logging
import math
import os

import Geometry.Rectangle as RT
import Geometry.Point as PT

import Weather.WeatherQuery as WQ
from PIL import Image, ImageDraw, ImageFont

fontfamily = 'DejaVuSansMono.ttf'
boldfontfamily = 'DejaVuSansMono-Bold.ttf'

class WindModel():
    def __init__(self, wm:WQ.WeatherModel):
        self.wm = wm

    def refresh(self):
        self.wm.queryWeather()

    def getWindDirection(self):
        self.refresh()
        return self.wm.currentweather.wind_deg + 180

    def getWindSpeed(self):
        self.refresh()
        return self.wm.currentweather.wind_speed

    def getWindGust(self):
        self.refresh()
        return self.wm.currentweather.wind_gust


class WindCompass():
    def __init__(self, rect, windModel_in):
        self._rect : RT.Rectangle = rect
        self.windModel = windModel_in
        self.directionFont = ImageFont.truetype(boldfontfamily, 14)
        self.windspeedFont = ImageFont.truetype(boldfontfamily, 15)

    def drawCardinalMarks(self, imagedraw, center:PT.Point, radius, ticklength, markDirections=False):
        smallradius = radius - ticklength
        cardinaldirections = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        for i in range(8):
            angle = i * (math.pi/4)
            mark_tl = center.offset(PT.Point(int(radius * math.sin(angle)),int(radius * math.cos(angle))))
            mark_br = center.offset(PT.Point(int(smallradius * math.sin(angle)),int(smallradius * math.cos(angle))))

            imagedraw.line((mark_tl.coords(), mark_br.coords()), fill=0, width=1)

            if(markDirections):
                (textwidth, textheight) = imagedraw.textsize(
                    cardinaldirections[i], font=self.directionFont)
                marksRadius = int(
                    (1 * radius) + math.sqrt(math.pow((textheight/2), 2) + math.pow((textwidth/2), 2)))

                text_tl = center.offset(PT.Point(int((marksRadius * math.sin(angle)) - textwidth/2), -int((marksRadius * math.cos(angle)) + textheight/2)))
                imagedraw.text(text_tl.coords(), cardinaldirections[i], fill=0, font=self.directionFont)

    def drawWindDirection(self, imagedraw, center, radius, triangle_height):
        angle = math.radians(self.windModel.getWindDirection())
        arrow_side_half = triangle_height / math.sqrt(3)
        triangle_base_center = center.offset(PT.Point(radius*math.sin(angle),-radius*math.cos(angle)))

        triangle_v1 = triangle_base_center.offset(PT.Point(-int(arrow_side_half*math.cos(angle)),-int(arrow_side_half*math.sin(angle))))

        triangle_v2 = center.offset(PT.Point((radius + triangle_height) * math.sin(angle),-(radius + triangle_height) * math.cos(angle)))

        triangle_v3 = triangle_base_center.offset(PT.Point(arrow_side_half*math.cos(angle),arrow_side_half*math.sin(angle)))

        trianglepoints = [triangle_v1.coords(),triangle_v2.coords(), triangle_v3.coords()]
        imagedraw.polygon(trianglepoints, fill=0)

    def display(self, HBlackimage, HRYimage):
        logging.info("WindCompass-Display")
        drawblack = ImageDraw.Draw(HBlackimage)
        drawred = ImageDraw.Draw(HRYimage)

        offsetForDirections = 14

        width = self._rect.width() - 2*offsetForDirections
        height = self._rect.height() - 2*offsetForDirections

        largecircle_r = int(min(width, height) / 2)

        centeroffset = offsetForDirections + largecircle_r
        center = self._rect.tl.offset(PT.Point(centeroffset, centeroffset))

        smallcicle_r = int(0.72 * largecircle_r)

        largecirclerect = RT.Rectangle(center.offset(PT.Point(-largecircle_r,-largecircle_r)), center.offset(PT.Point(largecircle_r,largecircle_r)))
        smallcirclerect = RT.Rectangle(center.offset(PT.Point(-smallcicle_r,-smallcicle_r)), center.offset(PT.Point(smallcicle_r,smallcicle_r)))

        drawblack.arc(largecirclerect.coords(), 0, 360, fill=0, width=2)
        drawblack.arc(smallcirclerect.coords(), 0, 360, fill=0, width=2)

        tick_length = int(0.1 * largecircle_r)

        self.drawCardinalMarks(drawblack, center,largecircle_r, tick_length, True)
        self.drawCardinalMarks(drawblack, center, smallcicle_r, tick_length)

        self.drawWindDirection(drawred, center, smallcicle_r, (largecircle_r - smallcicle_r))

        windspeedkph = self.windModel.getWindSpeed() * 3.6
        windspeedtext = f"{windspeedkph:>3.1f}\nkph"
        displaytext = windspeedtext
        (text_width, text_height) = drawblack.textsize(
            displaytext, font=self.windspeedFont)

        pt = center.offset(PT.Point(-int(text_width/2),-int(text_height/2)))
        drawblack.text(pt.coords(), displaytext, fill=0, font=self.windspeedFont)


