# Tested adding circle function:  <13-08-22, lalapopa> #
import pytest
from PIL import Image, ImageDraw, ImageFont, ImageChops
import numpy as np

import diamond_mosaic.img_to_mosaic as img_to_mosaic
import diamond_mosaic.settings as settings


class MosaicImage:
    def __init__(self):
        self.image = Image.open(settings.TEST_PATH + "1200-630-img.jpg")
        self.mosaic_size = 0.25
        self.mosaic_number_w = 20
        self.mosaic_number_h = 10
        self.resize_size_w = 38
        self.resize_size_h = 20
        with open(settings.TEST_PATH + "color_list_correct.npy", "rb") as f:
            self.color_list = np.load(f)
        with open(settings.TEST_PATH + "color_name_correct.npy", "rb") as f:
            self.color_name = np.load(f)

        with open(
            settings.TEST_PATH + "up_coords_correct.npy",
            "rb",
        ) as f:
            self.up_coords = np.load(f)
        with open(
            settings.TEST_PATH + "down_coords_correct.npy",
            "rb",
        ) as f:
            self.down_coords = np.load(f)
        with open(
            settings.TEST_PATH + "text_coords_correct.npy",
            "rb",
        ) as f:
            self.text_coord = np.load(f)
        with open(settings.TEST_PATH + "encoded_symbols_correct.npy", "rb") as f:
            self.encode_text = np.load(f)
        with open(settings.TEST_PATH + "img-with-circle.npy", "rb") as f:
            self.img_circle = np.load(f)


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
        img_to_mosaic.mosaic_to_pixel(width, height, mosaic_size)
        == mosaic_size_in_pixel
    )


def test_image_stats():

    assert img_to_mosaic.hold_aspect_ratio(
        mosaic_image.image.size,
        mosaic_image.mosaic_number_w,
        mosaic_image.mosaic_number_h,
    ) == (mosaic_image.resize_size_w, mosaic_image.resize_size_h)


def test_image_convert():
    resized_image = mosaic_image.image.resize(
        (mosaic_image.resize_size_w, mosaic_image.resize_size_h)
    )
    a = np.array(resized_image)
    color_list, color_name = img_to_mosaic.convert_color(a)
    assert (color_list == mosaic_image.color_list).all()
    assert (color_name == mosaic_image.color_name).all()


def test_paralell_color_convertion():
    resized_image = mosaic_image.image.resize(
        (mosaic_image.resize_size_w, mosaic_image.resize_size_h)
    )
    a = np.array(resized_image)
    chunks = img_to_mosaic.divide_into_chunks(a)
    color_list, color_name = img_to_mosaic.paralell_color_convertion(chunks)
    assert (color_list == mosaic_image.color_list).all()
    assert (color_name == mosaic_image.color_name).all()


def test_get_ellipse_coord():
    picture_size = img_to_mosaic.mosaic_to_pixel(
        mosaic_image.mosaic_number_w,
        mosaic_image.mosaic_number_h,
        mosaic_image.mosaic_size,
    )
    ready_size_img = Image.new("RGB", picture_size, (255, 255, 255))
    up_coords, down_coords = img_to_mosaic.get_ellipse_coord(
        ready_size_img, mosaic_image.mosaic_size
    )
    assert (up_coords == mosaic_image.up_coords).all()
    assert (down_coords == mosaic_image.down_coords).all()


def test_get_text_coord():
    picture_size = img_to_mosaic.mosaic_to_pixel(
        mosaic_image.mosaic_number_w,
        mosaic_image.mosaic_number_h,
        mosaic_image.mosaic_size,
    )
    ready_size_img = Image.new("RGB", picture_size, (255, 255, 255))
    text_coord = img_to_mosaic.get_text_coord(ready_size_img, mosaic_image.mosaic_size)
    assert (text_coord == mosaic_image.text_coord).all()


def test_get_encoding_text():
    assert (
        mosaic_image.encode_text
        == img_to_mosaic.get_text_labels(mosaic_image.color_name)
    ).all()


def test_add_circle_to_img():
    picture_size = img_to_mosaic.mosaic_to_pixel(
        mosaic_image.mosaic_number_w,
        mosaic_image.mosaic_number_h,
        mosaic_image.mosaic_size,
    )
    ready_size_img = Image.new("RGB", picture_size, (255, 255, 255))
    rdy_img = np.asarray(
        img_to_mosaic.add_circle(
            ready_size_img,
            mosaic_image.up_coords,
            mosaic_image.down_coords,
            mosaic_image.color_list,
        )
    )

    assert (rdy_img == mosaic_image.img_circle).all()
