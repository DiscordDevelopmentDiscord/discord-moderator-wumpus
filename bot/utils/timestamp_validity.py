from bot.constants import TIMESTAMP_MAKE_BOUNDARIES, TIMESTAMP_RELATIVE_BOUNDARIES
from copy import deepcopy


def make_data_validity(year: int, month: int, day: int, hour: int, minute: int, utc: int):
    invalid_fields = []
    boundaries = deepcopy(TIMESTAMP_MAKE_BOUNDARIES)
    for item in boundaries:
        input_value = locals()[item["name"]]
        if item["min"] > input_value:
            item["input"] = input_value
            invalid_fields.append(item)
        if item["name"] == "day":
            item["max"] = item["max"](year, month)
        if item["max"] < input_value:
            item["input"] = input_value
            invalid_fields.append(item)
    return invalid_fields


def relative_data_validity(days: int, hours: int, minutes: int):
    invalid_fields = []
    boundaries = deepcopy(TIMESTAMP_RELATIVE_BOUNDARIES)
    for item in boundaries:
        input_value = locals()[item["name"]]
        if item["range"] < input_value:
            item["input"] = input_value
            invalid_fields.append(item)
    return invalid_fields
