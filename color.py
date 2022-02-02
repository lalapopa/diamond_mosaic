import json 
class Color:
	PATH = './color_palette/'
	RGB_FILE = 'color_rgb_data'
	ENCODE_FILE = 'color_encoding'
	HEX_FILE = 'colors_data'

	@classmethod
	def get_color(cls, file):
		with open(cls.PATH + file + ".json") as f:
		    return json.load(f)

