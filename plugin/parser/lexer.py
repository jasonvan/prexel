class Lexer:
    """
    Code referenced:
    https://ruslanspivak.com/lsbasi-part6/
    http://jayconrod.com/posts/37/a-simple-interpreter-from-scratch-in-python-part-1

    Possible Token list
    Token(CLASS_MARKER, "|")
    Token(AGGREGATION, "<>{1}--{*}>")
    Token(DEPENDENCE, "-->")
    Token(INHERITENCE, "^")
    Token(INTERFACE, "=")
    """
    def __init__(self, text):
        self.text = text
        self.pos = 0
