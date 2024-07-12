import pytest
import numpy as np

from diamond_mosaic.color_finder import close_color
from diamond_mosaic.color import get_color

from diamond_mosaic.config import DATA_PATH, RGB_FILE, TEST_PATH, RAW_PALETTE_FILE
from diamond_mosaic import make_colors


@pytest.mark.parametrize(
    "in_color, out_color, dmc_color",
    [
        (np.array([123, 123, 123]), np.array([107, 128, 132]), "3768"),
        (np.array([72, 98, 50]), np.array([72, 97, 49]), "3345"),
        (np.array([235, 229, 210]), np.array([233, 233, 212]), "000"),
        (np.array([254, 254, 254]), np.array([255, 255, 255]), "5200"),
        (np.array([0, 0, 0]), np.array([0, 0, 0]), "310"),
    ],
)
def test_color_finder(in_color, out_color, dmc_color):
    rgb = get_color(DATA_PATH + RGB_FILE)
    rgb_color_value, dmc_code = close_color(in_color, rgb)
    assert dmc_code == dmc_color
    assert (rgb_color_value == out_color).all()


@pytest.mark.parametrize(
    "dmc_color, out_code",
    [
        (1, "2B"),
        (2, "2C"),
        (6, "29"),
    ],
)
def test_color_encoding(dmc_color, out_code):
    assert make_colors.two_value_coding(dmc_color) == out_code


def test_parse_raw_palette_file():
    file_palette = TEST_PATH + RAW_PALETTE_FILE

    color_hex_dict, color_rgb_dict, color_encoding_dict = make_colors.decode_palatte(
        file_palette
    )
    color_data_correct = get_color(TEST_PATH + "color_data_correct.json")
    color_rgb_data_correct = get_color(TEST_PATH + "color_rgb_data_correct.json")
    color_encode_data_correct = get_color(TEST_PATH + "color_encoding_correct.json")
    assert color_hex_dict == color_data_correct
    assert color_rgb_dict == color_rgb_data_correct
    assert color_encoding_dict == color_encode_data_correct
