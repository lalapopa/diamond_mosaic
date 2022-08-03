# tested only color_convertions in img_convert_color:  <01-08-22, yourname> #
import pytest
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from diamond_mosaic import img_conver_color
from diamond_mosaic import settings


class MosaicImage:
    def __init__(self):
        self.image = Image.open(settings.TEST_PATH + "1200-630-img.jpg")
        self.mosaic_number_w = 20
        self.mosaic_number_h = 10
        self.resize_size_w = 38
        self.resize_size_h = 20
        with open(settings.TEST_PATH + "color_list_correct.npy", "rb") as f:
            self.color_list = np.load(f)
        with open(settings.TEST_PATH + "color_name_correct.npy", "rb") as f:
            self.color_name = np.load(f)


mosaic_image = MosaicImage()


@pytest.mark.parametrize(
    "width, height, mosaic_size, mosaic_size_in_pixel",
    [
        (1, 1, 0.25, (30, 30)),
        (1, 1, 1, (120, 120)),
        (2, 2, 1, (240, 240)),
        (210, 190, 0.25, (6300, 5700)),
    ],
)
def test_mosaic_to_pixel(width, height, mosaic_size, mosaic_size_in_pixel):
    assert (
        img_conver_color.mosaic_to_pixel(width, height, mosaic_size)
        == mosaic_size_in_pixel
    )


def test_image_stats():

    assert img_conver_color.hold_aspect_ratio(
        mosaic_image.image.size,
        mosaic_image.mosaic_number_w,
        mosaic_image.mosaic_number_h,
    ) == (mosaic_image.resize_size_w, mosaic_image.resize_size_h)


def test_image_convert():
    resized_image = mosaic_image.image.resize(
        (mosaic_image.resize_size_w, mosaic_image.resize_size_h)
    )
    a = np.array(resized_image)
    color_list, color_name = img_conver_color.convert_color(a)
    assert (color_list == mosaic_image.color_list).all()
    assert (color_name == mosaic_image.color_name).all()
