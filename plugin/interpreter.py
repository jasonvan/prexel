# Code based on https://ruslanspivak.com/lsbasi-part6/
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0


class Interpreter:
    pass