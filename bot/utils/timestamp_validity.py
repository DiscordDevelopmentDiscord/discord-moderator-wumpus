from bot.constants import TIMESTAMP_MAKE_BOUNDARIES, TIMESTAMP_RELATIVE_BOUNDARIES
from copy import deepcopy


def make_data_validity(input_data: dict):
    invalid_fields = []
    boundaries = deepcopy(TIMESTAMP_MAKE_BOUNDARIES)
    for item in boundaries:
        input_value = input_data[item["name"]]
        if item["min"] > input_value:
            item["input"] = input_value
            invalid_fields.append(item)
        if item["name"] == "day":
            item["max"] = item["max"](input_data["year"], input_data["month"])
        if item["max"] < input_value:
            item["input"] = input_value
            invalid_fields.append(item)
    return invalid_fields


def relative_data_validity(input_data: dict):
    invalid_fields = []
    boundaries = deepcopy(TIMESTAMP_RELATIVE_BOUNDARIES)
    for item in boundaries:
        input_value = input_data[item["name"]]
        if item["range"] < input_value:
            item["input"] = input_value
            invalid_fields.append(item)
    return invalid_fields
