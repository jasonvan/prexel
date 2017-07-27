import re

REGEX = {
    "class_name": re.compile(r'^[A-Z][a-z0-9]*$'),
    "method_signature": re.compile(r'^([^(){}]*)\((.*)\)$'),
    "aggregation": re.compile("^<>([*\d])?[-]*(.*)?[-]*([*\d])?[-]*>$")
}
