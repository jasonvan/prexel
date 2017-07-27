class Token:
    """
    TODO
    """
    CLASS_MARKER, CLASS_NAME, FIELD, METHOD = (
        "CLASS_MARKER",
        "CLASS_NAME",
        "FIELD",
        "METHOD"
    )

    def __init__(self, type, value):
        self.type = type
        self.value = value
