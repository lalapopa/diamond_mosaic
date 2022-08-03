import re
import json
import math
from PIL import ImageColor

import diamond_mosaic.settings as settings

file_palette = settings.PATH + settings.RAW_PALETTE_FILE

color_trigger = r"bgcolor=.........?"
quote_trigger = r"\".*?\""
color_dmc_trigger = r'<td class="style3">(.*?)</td>'
number_trigger = r"\d+"


def two_value_coding(i):
    symbols = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "9",
        "J",
        "K",
        "L",
        "M",
        "N",
        "P",
        "4",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        "1",
        "2",
    ]

    k = 2
    n = len(symbols)

    max_combination = math.factorial(n) / math.factorial(n - k)
    if i > max_combination or i <= 0:
        raise Exception(
            f"That number in array can't be without repetition. Should be: 0 < {i} <={max_combination}"
        )

    array = []
    for j in symbols:
        array.append([str(i) + str(j) for i in symbols if i != j])
    x_value = i // n
    y_value = i % n

    return array[y_value][x_value - 1]


def hex_to_rgb(hex_list):
    return (list(ImageColor.getcolor(color_hex, "RGB")) for color_hex in hex_list)


def save_json(dict_data, file_path):
    with open(file_path, "w") as f:
        f.write(json.dumps(dict_data))


def encode_colors(colors):
    return [two_value_coding(i) for i in range(1, len(colors) + 1)]


def decode_palatte(file_palette):
    color_dmc_data = []
    color_hex_data = []

    with open(file_palette, "r", encoding="utf-8") as f:
        for i in f:
            x = re.findall(color_trigger, i)
            if x:
                color_hash = re.findall(quote_trigger, x[0])[0]
                color_hex_data.append(color_hash[1:-1])

            y = re.search(color_dmc_trigger, i)
            if y:
                raw = y.group(1)
                color_code = re.findall(number_trigger, raw)
                if color_code:
                    color_dmc_data.append(color_code[0])

    color_encoding = encode_colors(color_dmc_data)

    color_hex_dict = dict(zip(color_dmc_data, color_hex_data))
    color_rgb_dict = {
        k: v
        for k, v in sorted(
            dict(zip(color_dmc_data, hex_to_rgb(color_hex_data))).items(),
            key=lambda item: item[1][0],
        )
    }

    color_encoding_dict = dict(zip(color_dmc_data, color_encoding))
    return color_hex_dict, color_rgb_dict, color_encoding_dict


def main():
    hex_dict, rgb_dict, encode_dict = decode_palatte(file_palette)
    save_json(hex_dict, settings.PATH + "colors_data.json")
    save_json(rgb_dict, settings.PATH + "color_rgb_data.json")
    save_json(encode_dict, settings.PATH + "color_encoding.json")


if __name__ == "__main__":
    main()
