class Lexer:
    """
    Code referenced:
    https://ruslanspivak.com/lsbasi-part6/
    http://jayconrod.com/posts/37/a-simple-interpreter-from-scratch-in-python-part-1
    """
    def __init__(self, text):
        self.text = text
        self.pos = 0
