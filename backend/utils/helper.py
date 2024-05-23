import json
from os import path

from .constants import models_dir, parts_dir


def get_model_data(model_number: str):
    model_path = path.join(models_dir, f"{model_number}.jsonl")

    try:
        with open(model_path) as file:
            data = json.load(file)
    except BaseException as error:
        raise error

    return {"model_data": data}


def get_part_data(partselect_number: str):
    part_path = path.join(parts_dir, f"{partselect_number}.jsonl")

    try:
        with open(part_path) as file:
            data = json.load(file)
    except BaseException as error:
        raise error

    return {"part_data": data}
