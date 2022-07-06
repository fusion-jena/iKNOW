import json

# import numpy as np


def append_boolean_list(lst):
    for i, sublst in enumerate(lst[1:]):
        for j, el in enumerate(sublst):
            lst[i+1][j] = [el, False]

    return json.dumps(lst)
