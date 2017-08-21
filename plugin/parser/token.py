class Token:
    """
    TODO
    """
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
