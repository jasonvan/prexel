import re
from prexel.plugin.parser.token import Token


class Lexer:
    """
    Possible Token list
    Token(CLASS_MARKER, "|")
    Token(AGGREGATION, "<>{1}--{*}>")
    Token(CHARACTER, "AZaz")
    Token(NUMBER, "09")
    Token(MULTIPLE, "*")
    Token(DEPENDENCE, "-->")
    Token(INHERITENCE, "^")
    Token(INTERFACE, "=")
    """

    class_regex = re.complile(r'[A-Z][a-z0-9]*')

    def __init__(self, text):
        self.text = text
        self.position = 0
        self.current = self.text[self.position]

    def step(self):
        self.position += 1
        if self.position >= len(self.text):
            self.current = None
        else:
            self.current = self.text[self.position]

    def skip_whitespace(self):
        while self.current is not None and self.current.isspace():
            self.step()

    def element(self):
        string = ""
        while self.current is not None and not self.current.isspace():
            string += self.current
            self.step()
        return string

    def get_token(self):
        while self.current is not None:
            if self.current.isspace():
                self.skip_whitespace()
                continue
            else:
                element = self.element()

                if self.class_regex.match(element):
                    return Token("Class", element)








