import json

import pandas as pd


def get_list_from_csv(path: str, header=None):
    frame = pd.read_csv(path, header=header, quotechar="'")
    frame_list = frame.values.tolist()

    return frame_list


def get_list_from_csv_first10rows(path: str, header=None):
    frame = pd.read_csv(path, header=header, quotechar="'", nrows=11)
    frame_list = frame.values.tolist()

    return frame_list


def get_json_from_csv(path: str, header=None):
    frame = pd.read_csv(path, header=header)
    json_data = frame.to_json()
    json.loads(json_data)

    return json_data
