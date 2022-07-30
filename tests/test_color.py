# Continue write make_color.py tests. img_convert_color.py has no changes:  <30-07-22, lalapopa> #
from diamond_mosaic import color_finder
from diamond_mosaic import color
from diamond_mosaic.settings import RGB_FILE, TEST_PATH, RAW_PALETTE_FILE
from diamond_mosaic.color_palette import make_colors
import pytest


@pytest.mark.parametrize(
    "in_color, out_color, dmc_color",
    [
        ((123, 123, 123), (107, 128, 132), "3768"),
        ((72, 98, 50), (72, 97, 49), "3345"),
        ((235, 229, 210), (233, 233, 212), "000"),
        ((254, 254, 254), (255, 255, 255), "5200"),
        ((1, 1, 1), (0, 0, 0), "310"),
    ],
)
def test_color_finder(in_color, out_color, dmc_color):
    rgb = color.get_color(RGB_FILE)
    assert color_finder.close_color(in_color, rgb) == (out_color, dmc_color)


@pytest.mark.parametrize(
    "dmc_color, out_code",
    [
        (1, "2B"),
        (2, "2C"),
    ],
)
def test_color_parser(dmc_color, out_code):
    assert make_colors.two_value_coding(dmc_color) == out_code


def test_decode_palette():
    file_palette = TEST_PATH + RAW_PALETTE_FILE

    color_hex_dict, color_rgb_dict, color_encoding_dict = make_colors.decode_palatte(
        file_palette
    )
    make_colors.save_json(color_hex_dict, TEST_PATH + "color_data_correct.json")
    make_colors.save_json(color_rgb_dict, TEST_PATH + "color_rgb_data_correct.json")
    make_colors.save_json(
        color_encoding_dict, TEST_PATH + "color_encoding_correct.json"
    )
