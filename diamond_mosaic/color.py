import json


def get_color(file_path):
    with open(file_path) as f:
        return json.load(f)
