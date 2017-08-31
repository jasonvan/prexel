import re

REGEX = {
    "class_name": re.compile(r'^[A-Z]\w*$'),
    "method_signature": re.compile(r'^([^(){}]+)\((.*)\)$'),
    "aggregation": re.compile('^<>([\d*]?)-+(\w*)-*([\d*]?)>$'),
    "inheritance": re.compile('^<<$'),
    "ignored_characters": ("<<>", "<>>", "<>", "<<>>")
}


def is_class_name(value):
    return REGEX["class_name"].match(value)


def is_method_signature(value):
    return REGEX["method_signature"].match(value)


def is_inheritance(value):
    return REGEX["inheritance"].match(value)


def is_aggregation(value):
    return REGEX["aggregation"].match(value)


def is_ignored_character(value):
    return value in REGEX["ignored_characters"]
