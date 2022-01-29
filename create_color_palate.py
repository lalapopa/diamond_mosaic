import re
import json
from PIL import ImageColor


def hex_to_rgb(hex_list):
	return  (ImageColor.getcolor(color_hex, 'RGB') for color_hex in hex_list)


color_trigger = r"bgcolor=.........?"
quote_trigger = r"\".*?\""
color_code_trigger = '<td class="style3">(.*?)</td>'
number_trigger = r'\d+'

color_data = []
color_hex_data = []

with open("palate.txt", 'r', encoding='utf-8') as f:
	for i in f:
		x = re.findall(color_trigger, i)
		if x:
			color_hash = re.findall(quote_trigger, x[0])[0]
			# print(color_hash[1:-1])
			color_hex_data.append(color_hash[1:-1])

		y = re.search(color_code_trigger, i)
		if y:
			raw = y.group(1)
			color_code = re.findall(number_trigger, raw)
			# color_data = [val for val in color_code if val]
			if color_code:
				color_data.append(color_code[0])

# print(tuple(color_data))
# print(hex_to_rgb(color_hex_data))

color_dict = dict(zip(color_data, color_hex_data))
color_dict_rgb = dict(zip(tuple(color_data), hex_to_rgb(color_hex_data)))


json_file = json.dumps(color_dict)

with open('colors_data.json', 'w') as f:
	f.write(json_file)

with open('color_rgb_data.json', 'w') as f:
	f.write(json.dumps(color_dict_rgb))
