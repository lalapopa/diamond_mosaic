import math
import numpy as np
from PIL import ImageColor


def distance(c1, c2):
    rgb1 = np.array(c1)
    rgb2 = np.array(c2)

    rmean = (rgb1[0] + rgb2[0]) / 2
    r = rgb1[0] - rgb2[0]
    g = rgb1[1] - rgb2[1]
    b = rgb1[2] - rgb2[2]
    return math.sqrt(
        (2 + rmean / 256) * r ** 2 + 4 * g ** 2 + (2 + (255 - rmean) / 256) * b ** 2
    )


def close_color(rgb_color, color_palate):
    color_data = color_palate
    color_data_rgb = list(tuple(val) for val in color_data.values())
    color_name_data = list(i for i in color_data.keys())

    index = 0
    min_distance = 1000
    for i, color in enumerate(color_data_rgb):
        i_distance = distance(color, rgb_color)
        if i_distance <= min_distance:
            min_distance = i_distance
            index = i

    return color_data_rgb[index], color_name_data[index]
