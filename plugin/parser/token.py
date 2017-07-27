class Token:
    """
    TODO
    """
    PREXEL_MARKER, CLASS_NAME, FIELD, METHOD = (
        "PREXEL_MARKER",
        "CLASS_NAME",
        "FIELD",
        "METHOD"
    )

    def __init__(self, type, value):
        self.type = type
        self.value = value
