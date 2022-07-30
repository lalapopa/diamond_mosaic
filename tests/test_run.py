from find_close_color import close_color
from color import Color
import pytest


@pytest.mark.parametrize(
    "in_color, out_color, dmc_color",
    [
        ((123, 123, 123), (107, 128, 132), "3768"),
        ((72, 98, 50), (72, 97, 49), "3345"),
    ],
)
def test_main_run(in_color, out_color, dmc_color):
    color = Color()
    rgb = color.get_color(color.RGB_FILE)
    assert close_color(in_color, rgb) == (out_color, dmc_color)
