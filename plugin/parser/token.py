class Token:
    """
    TODO
    """
    PREXEL_MARKER, CLASS_NAME, FIELD, METHOD, AGGREGATION = (
        "PREXEL_MARKER",
        "CLASS_NAME",
        "FIELD",
        "METHOD",
        "AGGREGATION"
    )

    def __init__(self, type, value):
        self.type = type
        self.value = value
