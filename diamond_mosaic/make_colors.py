import os
import re
import math
from pathlib import Path
from PIL import ImageColor

from .settings import (
    PATH,
    LABELS_FILE,
    RAW_PALETTE_FILE,
    RGB_FILE,
    HEX_FILE,
    DATA_PATH,
)
from .utils import save_json

FILE_PALETTE = PATH + RAW_PALETTE_FILE

color_trigger = r"(bgcolor=.........?)|(data-title=........?)"
quote_trigger = r"\".*?\""
color_dmc_trigger = (
    r'(<td class="style3">(.*?)<\/td>)|(<div class="ribbon">(.*?)<\/div>)'
)

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


def encode_colors(colors):
    return [two_value_coding(i) for i in range(1, len(colors) + 1)]


def decode_palatte(file_palette):
    color_dmc_data = []
    color_hex_data = []

    with open(file_palette, "r", encoding="utf-8") as f:
        for i in f:
            x = re.findall(color_trigger, i)
            print(x)
            if x:
                color_hash = re.findall(quote_trigger, x[0])[0]
                if len(color_hash) == 9:  # "#aaaaaa"
                    color_hex_data.append(color_hash[1:-1])
                elif len(color_hash) == 8:  # "aaaaaa"
                    color_hex_data.append("#" + color_hash[1:-1])
                else:
                    raise NameError("Your data '{file_palette}' has broken color value")

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
    hex_dict, rgb_dict, encode_dict = decode_palatte(FILE_PALETTE)

    Path(DATA_PATH).mkdir(parents=True, exist_ok=True)

    save_json(hex_dict, DATA_PATH + HEX_FILE)
    save_json(rgb_dict, DATA_PATH + RGB_FILE)
    save_json(encode_dict, DATA_PATH + LABELS_FILE)


if __name__ == "__main__":
    main()
