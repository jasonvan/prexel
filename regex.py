import re

REGEX = {
    "class_name": re.compile(r'^[A-Z]\w*$'),
    "method_signature": re.compile(r'^([^(){}]+)\((.*)\)$'),
    "aggregation": re.compile('^<>([\d*]?)-+(\w*)-*([\d*]?)>$'),
    "inheritance": re.compile('^<<$')
}
