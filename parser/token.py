"""
Code in this class is based on https://ruslanspivak.com/lsbasi-part6/
"""


class Token:
    """
     _____ 
    |Token|
    |-----|
    |type |
    |value|
    |_____|

    """
    START_MARKER, \
        CLASS_NAME, \
        FIELD, \
        METHOD, \
        AGGREGATION, \
        INHERITANCE, \
        COMMA = (
            "START_MARKER",
            "CLASS_NAME",
            "FIELD",
            "METHOD",
            "AGGREGATION",
            "INHERITANCE",
            "COMMA"
    )

    def __init__(self, type, value):
        self.type = type
        self.value = value
