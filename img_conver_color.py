from PIL import Image, ImageDraw, ImageFont
import numpy as np
import time 
import json 
import multiprocessing
import concurrent.futures
import matplotlib.pyplot as plt


from find_close_color import close_color

def mosaic_to_pixel(w, h, m_s_cm):
	#120 = 300 dpi 
	single_mosaic_pixel = 120*m_s_cm
	return (round(w*single_mosaic_pixel), round(h*single_mosaic_pixel))

def add_grid(image, m_size):
	black = [0, 0, 0]
	m_area = list(mosaic_to_pixel(1, 1, mosaic_size))[0]
	image_shape = list(image.size)
	print(f'img_size = {image_shape}, mosaic_size = {m_area}')

	num_lines_x = int((image_shape[0]+1)/m_area)  
	num_lines_y = int((image_shape[1]+1)/m_area)
	lines_x_coord = [num*m_area-1 for num in range(1,num_lines_x+1)]
	lines_y_coord = [num*m_area-1 for num in range(1,num_lines_y+1)]

	img = []
	for i, val in enumerate(np.array(image)):
		if i in lines_y_coord:
			a_row = [black for j in val]
		else:
			a_row = []
			for j, val in enumerate(val):
				if j in lines_x_coord:
					a_row.append(black)
				else:
					a_row.append(val)
		img.append(a_row)
	return Image.fromarray(np.array(img, dtype=np.uint8))

def get_text_coord(img, m_size):
	m_area = list(mosaic_to_pixel(1, 1, m_size))[0]
	quorter_part = m_area*0.1
	image_shape = list(img.size)

	num_dot_x = int((image_shape[0]+1)/m_area)
	num_dot_y = int((image_shape[1]+1)/m_area)

	x_coord = [num*m_area + round(m_area/2)  for num in range(0, num_dot_x)]
	y_coord = [num*m_area + round(m_area/2) for num in range(0, num_dot_y)]

	coord = []
	for y in y_coord:
		for x in x_coord:
			coord.append((x,y))
	return coord

def add_text(image, text_list, coord_list):
	draw = ImageDraw.Draw(image)
	font = ImageFont.truetype('impact.ttf')

	unfolded_text = []
	for i in text_list:
		for j in i:
			unfolded_text.append(j)
	
	for coord, text in zip(coord_list, unfolded_text):
		draw.text(coord, text, fill='white', font=font, 
			stroke_width=2, stroke_fill='black', anchor='mm')
	return image


def get_color_name_in_img(img, color_palate):
	names = []
	for i in img:
		name_row = [get_color_name(pixel, color_palate) for pixel in i]
		names.append(name_row)
	return names

def get_ellipse_coord(img, mosaic_size):
	m_area = list(mosaic_to_pixel(1,1, mosaic_size))[0]
	img_size = list(img.size)
	# print(img_size)
	num_x = int(img_size[0]/m_area)
	num_y = int(img_size[1]/m_area)
	x_coord = [m_area*num for num in range(0, num_x+1)]
	y_coord = [m_area*num for num in range(0, num_y+1)]
	
	coord_up = []
	coord = []
	for x in range(0, num_x):
		for y in range(0, num_y):
			coord.append((x_coord[x],y_coord[y]))
		coord_up.append(coord)
		coord = []

	coord_down = []
	coord = []
	for y in range(1, num_y+1):
		for x in range(1, num_x+1):
			coord.append((x_coord[x], y_coord[y]))
		coord_down.append(coord)
		coord = []

	ready_coord_up = [list(i) for i in transpose(coord_up)]
	# print(ready_coord_up)
	# print(coord_down)
	return ready_coord_up, coord_down

def transpose(matrix):
	return [*zip(*matrix)]

def add_circle(img_plane, up_coord, down_coord, color_list):
	draw = ImageDraw.Draw(img_plane)
	for i, val in enumerate(up_coord):
		for j, x_coord  in enumerate(val):
			# print(f'1 point = {x_coord} 2 point = {down_coord[j][i]}')
			# print(color_list)
			color = tuple(color_list[i][j])
			draw.ellipse([x_coord, down_coord[i][j]], fill=color)
	return img_plane

def get_color_data():
	with open('color_rgb_data.json') as f:
		return json.load(f)
	 
def convert_color(input_colors):
	color_palate = get_color_data()
	converted_color = []
	colors_name = []
	for i in input_colors:
		a_row = [close_color(pixel, color_palate) for pixel in i]
		a_row = [i for i in zip(*a_row)]

		converted_color.append(a_row[0])
		colors_name.append(a_row[1])

	return converted_color, colors_name

def split_weird_array(array):
	print(f'in function array len is {len(array)}')
	for i, value in enumerate(array):
		if i == 0:
			v = value
			if len(array) == 1:
				return np.array(v)
			continue  

		ready_array = np.vstack((v, value))
		v = ready_array
	return ready_array

def hold_aspect_ratio(img_size, m_w, m_h):
	ratio = img_size[0]/img_size[1]
	max_mosaic = max(m_w, m_h)
	return int(ratio*max_mosaic), int(max_mosaic) 

def divide_into_chunks(image):
	cpu_number = multiprocessing.cpu_count()
	img_size = list(image.shape)
	divide = int(img_size[0]/cpu_number)
	chunks = []
	if img_size[0] > cpu_number:
		for val in range(0, cpu_number):
			right_limit = divide*(val+1)
			left_limit = val*divide
			if val == cpu_number - 1:
				right_limit = img_size[0]
				print('cool')
			chunks.append(image[left_limit:right_limit])
	else:
		chunks = [image]
	return chunks

def img_to_mosaic(img_name, mosaic_number_w, mosaic_number_h):
	mosaic_size = 0.25

	image = Image.open(img_name)
	color_palate = get_color_data()

	mosaic_number_w, mosaic_number_h = hold_aspect_ratio(list(image.size), mosaic_number_w, mosaic_number_h)

	resize_img = image.resize((mosaic_number_w, mosaic_number_h), resample=Image.NEAREST)

	print(f'original size = {image.size} px width x height')
	print(f'paper size width: {mosaic_size*mosaic_number_w} cm, height: {mosaic_size*mosaic_number_h} cm')

	a = np.array(resize_img)
	print(f'a = shape is {a.shape}')
	chunks = divide_into_chunks(a)


	color_list = []
	color_name = []
	with concurrent.futures.ProcessPoolExecutor() as exe:
		result = exe.map(convert_color, chunks)	
		for row_color, row_color_name in result:
			color_list.append(row_color)
			color_name.append(row_color_name)

	color_list = split_weird_array(color_list)
	color_name = list(split_weird_array(color_name))

	print(f'Color_name = len is {len(color_name)} {len(color_name[0])}')
	print(f'Color_list = shape is {color_list.shape}')
	print(f'Conver done!')

	# color_name = get_color_name_in_img(color_list, color_palate)

	img_color = Image.fromarray(np.array(color_list, dtype=np.uint8))

	img_bg = Image.new("RGB", img_color.size, (255,255,255))
	ready_size_img = img_bg.resize(
		mosaic_to_pixel(
		mosaic_number_w, 
		mosaic_number_h,
		mosaic_size,
		), resample=Image.BOX
	)
	up_coord, down_coord = get_ellipse_coord(ready_size_img, mosaic_size)

	ready_img = add_circle(ready_size_img, up_coord, down_coord, color_list)
	coord_list = get_text_coord(ready_img, mosaic_size)

	ready_img = add_text(ready_img, color_name, coord_list)
	ready_img.save('result.png')
