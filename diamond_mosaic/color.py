import json
from diamond_mosaic.settings import PATH


def get_color(file_name):
    with open(PATH + file_name) as f:
        return json.load(f)
