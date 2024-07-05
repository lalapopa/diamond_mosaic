import json


def read_json(file_path):
    with open(file_path) as f:
        return json.load(f)


def save_json(dict_data, file_path):
    with open(file_path, "w") as f:
        f.write(json.dumps(dict_data))
