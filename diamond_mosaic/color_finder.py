import math


def distance(c1, c2):
    rmean = (c1[0] + c2[0]) / 2
    r = c1[0] - c2[0]
    g = c1[1] - c2[1]
    b = c1[2] - c2[2]
    return math.sqrt(
        (2 + rmean / 256) * r**2 + 4 * g**2 + (2 + (255 - rmean) / 256) * b**2
    )


def close_color(rgb_color, color_data):
    color_name_out = ""
    min_distance = float("inf")
    for color_name, color in color_data.items():
        i_distance = distance(color, rgb_color)
        if i_distance <= min_distance:
            min_distance = i_distance
            color_name_out = color_name
    return tuple(color_data.get(color_name_out)), color_name_out
