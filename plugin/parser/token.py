"""
Code in this class is based on https://ruslanspivak.com/lsbasi-part6/
"""


class Token:
    PREXEL_MARKER, CLASS_NAME, FIELD, METHOD, AGGREGATION, INHERITANCE = (
        "PREXEL_MARKER",
        "CLASS_NAME",
        "FIELD",
        "METHOD",
        "AGGREGATION",
        "INHERITANCE"
    )

    def __init__(self, type, value):
        self.type = type
        self.value = value
