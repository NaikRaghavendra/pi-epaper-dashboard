
import os
import sys
import cairosvg

from io import BytesIO
from PIL import Image, ImageOps

picdirectory = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 'pic/')

class IconProvider():
	def __init__(self):
		self.iconpaths = {}
		self.iconpaths["sunrise"] = os.path.join(picdirectory,"weathericons/sunrise.svg")
		self.iconpaths["sunset"] = os.path.join(picdirectory,"weathericons/sunset.svg")
		self.iconpaths["sun"] = os.path.join(picdirectory,"weathericons/sun.svg")

		self.iconpaths["01d"] = os.path.join(picdirectory,"weathericons/clearsky.svg")
		self.iconpaths["01n"] = os.path.join(picdirectory,"weathericons/clearsky.svg")
		self.iconpaths["02d"] = os.path.join(picdirectory,"weathericons/fewclouds.svg")
		self.iconpaths["02n"] = os.path.join(picdirectory,"weathericons/fewclouds.svg")
		self.iconpaths["03d"] = os.path.join(picdirectory,"weathericons/scatteredclouds.svg")
		self.iconpaths["03n"] = os.path.join(picdirectory,"weathericons/scatteredclouds.svg")
		self.iconpaths["04d"] = os.path.join(picdirectory,"weathericons/brokenclouds.svg")
		self.iconpaths["04n"] = os.path.join(picdirectory,"weathericons/brokenclouds.svg")
		self.iconpaths["09d"] = os.path.join(picdirectory,"weathericons/showerrain.svg")
		self.iconpaths["09n"] = os.path.join(picdirectory,"weathericons/showerrain.svg")
		self.iconpaths["10d"] = os.path.join(picdirectory,"weathericons/rain.svg")
		self.iconpaths["10n"] = os.path.join(picdirectory,"weathericons/rain.svg")
		self.iconpaths["11d"] = os.path.join(picdirectory,"weathericons/thunderstorm.svg")
		self.iconpaths["11n"] = os.path.join(picdirectory,"weathericons/thunderstorm.svg")
		self.iconpaths["13d"] = os.path.join(picdirectory,"weathericons/snow.svg")
		self.iconpaths["13n"] = os.path.join(picdirectory,"weathericons/snow.svg")
		self.iconpaths["50d"] = os.path.join(picdirectory,"weathericons/mist.svg")
		self.iconpaths["50n"] = os.path.join(picdirectory,"weathericons/mist.svg")

	def getImageForCode(self, code, width_in, height_in, bInvert = False):
		return self.getgenericIcon(code,width_in,height_in, bInvert)


	def getgenericIcon(self, iconid, width_in, height_in, bInvert = False):
		if(iconid in self.iconpaths):
			iobytes = BytesIO()
			cairosvg.svg2png(url=self.iconpaths[iconid], write_to = iobytes,output_width=width_in, output_height=height_in)
			image = Image.open(iobytes)
			if image.mode == 'RGBA':
				bg = Image.new('RGB', image.size, (255, 255, 255))
				bg.paste(image, (0, 0), image)
				image = bg
		if(bInvert):
			image = ImageOps.invert(image)
		image = image.convert("1")
		return image


if __name__ == "__main__":
	ip = IconProvider()
	ip.getgenericIcon("sunrise", 20,20)
	ip.getgenericIcon("sunrise", 40,40)
	ip.getgenericIcon("sunrise", 200,200)
	
