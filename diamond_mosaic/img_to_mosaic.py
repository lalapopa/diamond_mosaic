from PIL import Image, ImageDraw, ImageFont
import numpy as np
from scipy.spatial import cKDTree
import multiprocessing
import concurrent.futures
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles.fills import PatternFill

import diamond_mosaic.utils as utils
import diamond_mosaic.settings as settings


def mosaic_to_pixel(w, h, m_s_cm, pixel_per_centimeter=120):
    """Convert real mosaic size to pixels
    :w: mosaic amount in width
    :h: mosaic amount in height
    :m_s_cm: mosaic diameter in cm.
    :pixel_per_centimeter: default density of image = 120 ppc (304.8 ppi)
    """
    single_mosaic_pixel = pixel_per_centimeter * m_s_cm
    return (round(w * single_mosaic_pixel), round(h * single_mosaic_pixel))


def add_grid(image, m_size):
    line_width = 1

    m_area = list(mosaic_to_pixel(1, 1, m_size))[0]
    image_shape = list(image.size)
    num_lines_x = int((image_shape[0] + 1) / m_area)
    num_lines_y = int((image_shape[1] + 1) / m_area)
    lines_x_coord = [
        num * m_area - 1 if num != 0 else 0 for num in range(0, num_lines_x + 1)
    ]
    lines_y_coord = [
        num * m_area - 1 if num != 0 else 0 for num in range(0, num_lines_y + 1)
    ]

    draw = ImageDraw.Draw(image)
    for x_coord in lines_x_coord:
        draw.line(
            [(x_coord, 0), (x_coord, image_shape[1])], fill="black", width=line_width
        )
    for y_coord in lines_y_coord:
        draw.line(
            [(0, y_coord), (image_shape[0], y_coord)], fill="black", width=line_width
        )
    return image


def get_text_coord(img, m_size):
    m_area = mosaic_to_pixel(1, 1, m_size)[0]
    num_dot_x = int((img.size[0] + 1) / m_area)
    num_dot_y = int((img.size[1] + 1) / m_area)

    x_coord = [num * m_area + round(m_area / 2) for num in range(0, num_dot_x)]
    y_coord = [num * m_area + round(m_area / 2) for num in range(0, num_dot_y)]

    coord = []
    for y in y_coord:
        for x in x_coord:
            coord.append((x, y))
    return coord


def add_text(image, text_list, m_size):
    draw = ImageDraw.Draw(image)
    m_area = list(mosaic_to_pixel(1, 1, m_size))[0]
    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/quicksand/Quicksand-Regular.ttf",
        int((m_area / 2) + 1),
    )
    coord_list = get_text_coord(image, m_size)

    unfolded_text = [j for i in text_list for j in i]  # flatten list

    for coord, text in zip(coord_list, unfolded_text):
        draw.text(
            coord,
            text,
            fill="white",
            font=font,
            stroke_width=2,
            stroke_fill="black",
            anchor="mm",
        )
    return image


def get_ellipse_coord(img, mosaic_size):
    m_area = list(mosaic_to_pixel(1, 1, mosaic_size))[0]
    num_x = int(img.size[0] / m_area)
    num_y = int(img.size[1] / m_area)
    x_coord = [m_area * num for num in range(0, num_x + 1)]
    y_coord = [m_area * num for num in range(0, num_y + 1)]

    coord_up = []
    for y in range(0, num_y):
        coord = [(x_coord[x], y_coord[y]) for x in range(0, num_x)]
        coord_up.append(coord)

    coord_down = []
    for y in range(1, num_y + 1):
        coord = [(x_coord[x], y_coord[y]) for x in range(1, num_x + 1)]
        coord_down.append(coord)
    return coord_up, coord_down


def add_circle(image, color_list, mosaic_size):

    up_coord, down_coord = get_ellipse_coord(image, mosaic_size)
    draw = ImageDraw.Draw(image)
    for i, val in enumerate(up_coord):
        for j, x_coord in enumerate(val):
            color = tuple(color_list[i][j])
            draw.ellipse([tuple(x_coord), tuple(down_coord[i][j])], fill=color)
    return image


def close_color(rgb_color, color_data):
    rgb_colors = np.array(list(color_data.values()))
    dmc_code = np.array(list(color_data.keys()))
    similar_color_idx = cKDTree(rgb_colors).query(rgb_color, k=1)[1]
    return rgb_colors[similar_color_idx], dmc_code[similar_color_idx]


def convert_color(input_colors):
    color_palette = utils.read_json(settings.DATA_PATH + settings.RGB_FILE)
    color_palette = transform_array_in_dict(color_palette)
    converted_color = []
    colors_name = []
    for i in input_colors:
        row_color_rgb = []
        row_color_dmc_code = []

        row_color_rgb, row_color_dmc_code = close_color(i, color_palette)
        converted_color.append(row_color_rgb)
        colors_name.append(row_color_dmc_code)
    return converted_color, colors_name


def transform_array_in_dict(dict_colors):
    for key, value in dict_colors.items():
        dict_colors[key] = np.array(value)
    return dict_colors


def split_weird_array(array):
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
    ratio = img_size[0] / img_size[1]
    max_mosaic = max(m_w, m_h)
    return int(ratio * max_mosaic), int(max_mosaic)


def divide_into_chunks(image):
    cpu_number = multiprocessing.cpu_count()
    img_size = list(image.shape)
    divide = int(img_size[0] / cpu_number)
    chunks = []
    if img_size[0] > cpu_number:
        for val in range(0, cpu_number):
            right_limit = divide * (val + 1)
            left_limit = val * divide
            if val == cpu_number - 1:
                right_limit = img_size[0]
            chunks.append(image[left_limit:right_limit])
    else:
        chunks = [image]
    return chunks


def unique_count(a):
    unique_value, counts = np.unique(a, return_counts=True)
    a_dict = dict(zip(unique_value, counts))
    sort_a = sorted(a_dict.items(), key=lambda item: item[1])[::-1]
    return dict(sort_a)


def save_color_table(file_name, encode_list):
    encode_result = unique_count(encode_list)

    color_file = utils.read_json(settings.DATA_PATH + settings.HEX_FILE)
    labels_file = utils.read_json(settings.DATA_PATH + settings.LABELS_FILE)

    encode_colors_list = list(labels_file.values())
    hex_colors_list = list(color_file.values())
    dmc_colors_list = list(color_file.keys())

    sorted_encode = sorted(list(encode_result.keys()))
    sorted_dmc_colors = []
    sorted_hex_colors = []

    for i in sorted_encode:
        for j, val in enumerate(encode_colors_list):
            if i == val:
                sorted_dmc_colors.append(dmc_colors_list[j])
                sorted_hex_colors.append(hex_colors_list[j])

    hex_in_img = []
    dmc_in_img = []
    for i in list(encode_result.keys()):
        for j, val in enumerate(encode_colors_list):
            if i == val:
                hex_in_img.append(hex_colors_list[j])
                dmc_in_img.append(dmc_colors_list[j])

    pd_amount = pd.DataFrame(list(encode_result.values()))
    pd_code = pd.DataFrame(dmc_in_img)
    pd_encode = pd.DataFrame(list(encode_result.keys()))

    df = pd.concat([pd_amount, pd_encode, pd_code], axis=1)
    df.reset_index(drop=True, inplace=True)
    df.columns = ["Кол-во", "Символ", "DMC цвет"]

    wb = Workbook()
    ws = wb.active
    for r in dataframe_to_rows(df, index=False, header=True):
        ws.append(r)

    for i in range(0, len(hex_in_img)):
        ws["D" + str(i + 2)].fill = PatternFill(
            "solid", start_color=str(hex_in_img[i][1::])
        )

    ws["F1"].value = "В алфавитном порядке"
    ws["G1"].value = "Символ"
    ws["H1"].value = "DMC цвет"
    ws["I1"].value = "Цвет"
    for i in range(0, len(sorted_dmc_colors)):
        ws["G" + str(i + 2)].value = sorted_encode[i]
        ws["H" + str(i + 2)].value = sorted_dmc_colors[i]
        ws["I" + str(i + 2)].fill = PatternFill(
            "solid", start_color=str(sorted_hex_colors[i])[1::]
        )
    wb.save(file_name + ".xlsx")


def get_text_labels(color_in_img):
    labels_data = utils.read_json(settings.DATA_PATH + settings.LABELS_FILE)
    color_names = list(labels_data.keys())
    labels_values = list(labels_data.values())

    encode_text = []
    for i in color_in_img:
        a_row = [labels_values[color_names.index(pixel)] for pixel in i]
        encode_text.append(a_row)
    return encode_text


def paralell_color_convertion(chunks):
    color_list = []
    color_name = []
    with concurrent.futures.ProcessPoolExecutor() as exe:
        result = exe.map(convert_color, chunks)
        for row_color, row_color_name in result:
            color_list.append(row_color)
            color_name.append(row_color_name)
    color_list = np.array(split_weird_array(color_list))
    color_name = list(split_weird_array(color_name))
    return color_list, color_name


def save_img(file_name, img):
    margin = 3  # cm
    margin_top_pix = list(mosaic_to_pixel(1, 1, margin))[0]
    margin_bottom_pix = margin_top_pix
    margin_left_pix = list(mosaic_to_pixel(1, 1, margin))[0]
    margin_right_pix = margin_left_pix

    res = list(mosaic_to_pixel(1, 1, 2.54))[0]
    w, h = img.size
    new_w = w + margin_right_pix + margin_left_pix
    new_h = h + margin_top_pix + margin_bottom_pix

    img_with_pad = Image.new(img.mode, (new_w, new_h), (255, 255, 255))
    img_with_pad.paste(img, (margin_left_pix, margin_top_pix))

    paper_w = (new_w * margin) / margin_top_pix
    paper_h = (new_h * margin) / margin_top_pix
    print(f"Resolution of PDF = {res} ppi")
    print(f"Paper size width = {paper_w} cm, height = {paper_h} cm.")
    img_with_pad.save(
        file_name + ".pdf",
        "PDF",
        resolution=res,
        author="LALAPOPA",
    )


def img_to_mosaic(img_name, mosaic_number_w, mosaic_number_h):
    mosaic_size = 0.25  # cm

    image = Image.open(img_name)
    mosaic_number_w, mosaic_number_h = hold_aspect_ratio(
        image.size, mosaic_number_w, mosaic_number_h
    )
    resize_img = np.array(image.resize((mosaic_number_w, mosaic_number_h)))

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(f"Original image size: {image.size} px width x height")
    print(
        f"Mosaic picture size width: {mosaic_size*mosaic_number_w} cm, height: {mosaic_size*mosaic_number_h} cm (single cell is {mosaic_size} cm in diameter)"
    )

    chunks = divide_into_chunks(resize_img)
    print(f"Converting colors ...")
    color_list, color_name = paralell_color_convertion(chunks)
    print(f"Done converting colors ...")

    print(
        f"Number of mosaics: {len(color_name[0])}x{len(color_name)} ({len(color_name[0])*len(color_name)} pc)"
    )
    picture_size = mosaic_to_pixel(mosaic_number_w, mosaic_number_h, mosaic_size)
    print(f"Output image have size {picture_size}")
    ready_size_img = Image.new("RGB", picture_size, (255, 255, 255))

    ready_img = add_circle(ready_size_img, color_list, mosaic_size)
    encode_text = get_text_labels(color_name)
    ready_img = add_text(
        ready_img, encode_text, mosaic_size
    )  # todo: this line take most time
    # ready_img = add_grid(ready_img, mosaic_size)
    save_img("result", ready_img)
    save_color_table("table", encode_text)