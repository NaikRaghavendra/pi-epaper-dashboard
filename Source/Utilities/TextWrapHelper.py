import logging
import os 
import sys
libdir = os.path.dirname(
    os.path.dirname(os.path.realpath(__file__)))
if os.path.exists(libdir):
    sys.path.append(libdir)

import Geometry.Point as PT
import Geometry.Rectangle as RT
import Utilities.Recurrer as AR
import Weather.WeatherQuery as WQ
import textwrap

from PIL import ImageDraw, ImageFont,Image

fontfamily = 'DejaVuSansMono.ttf'
boldfontfamily = 'DejaVuSansMono-Bold.ttf'

def getRectFromBounds(bounds):
    return RT.Rectangle(PT.Point(bounds[0],bounds[1]), PT.Point(bounds[2], bounds[3]))


def showWrappedText(text, draw, rect:RT.Rectangle, fontname, requestedsize, minfont):
    charactercount = len(text)

    texttoshow = ''
    fonttouse = None

    for size in range(minfont, 200):
        testfont = ImageFont.truetype(fontname, size)
        characterbounds = draw.textbbox(rect.tl.coords(),'X',testfont)
        characterwidth = characterbounds[2] - characterbounds[0]
              
        charactersperrow = int(rect.width()/characterwidth)
        wrappedlines = textwrap.wrap(text,charactersperrow)
        multilinetext = '\n'.join(wrappedlines)
        offsetrect = rect.shrink(PT.Point(1,1),PT.Point(1,1))
        multilinebounds = draw.multiline_textbbox(offsetrect.coords(),multilinetext,font=testfont)
        multilinerect = getRectFromBounds(multilinebounds)

        if(not rect.includes(multilinerect)):
            break
        fonttouse = testfont
        texttoshow = multilinetext

    if texttoshow is not '' and fonttouse is not None:
        draw.text(rect.tl.coords(),texttoshow,fill = 0, font = fonttouse)

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(message)s', level=logging.DEBUG) 

    image = Image.new('1', (250,122), 1)
    draw = ImageDraw.Draw(image)

    rect = RT.Rectangle(PT.Point(0,0), PT.Point(250,122))

    (top,bottom) = rect.partition_y(0.5)

    top = top.shrink(PT.Point(1,1), PT.Point(1,1))
    bottom = bottom.shrink(PT.Point(1,1), PT.Point(1,1))

    font = ImageFont.truetype(fontfamily, 22)
    bfont = ImageFont.truetype(boldfontfamily, 30)

    draw = ImageDraw.Draw(image)
    draw.rectangle(top.coords(),outline=0,width=1)

    showWrappedText("This is perhaps the longer text to be shown in such a small window",draw,top,boldfontfamily,30 ,10)
    image.show()

    showWrappedText("Klien Text",draw,top,boldfontfamily,30,10)
    image.show()

    showWrappedText("This is perhaps the longer text to be shown in such a small window and it is too small to fit such a small region, good attempt but still i wont fit here. all the best",draw,top,boldfontfamily,30 ,10)
    image.show()


    