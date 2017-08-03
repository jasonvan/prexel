from prexel.plugin.parser.token import Token
from prexel.plugin import REGEX


class Lexer:
    """
    Possible Token list
    Token(CLASS_MARKER, "|")
    Token(AGGREGATION, "<>{1}--{*}>")
    Token(MULTIPLE, "*")
    Token(DEPENDENCE, "-->")
    Token(INHERITENCE, "^")
    Token(INTERFACE, "=")
    """

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
            elif self.current == "|":
                self.step()
                return Token(Token.PREXEL_MARKER, "|")
            else:
                element = self.element()

                # Check element against some regex
                if REGEX["class_name"].match(element):
                    self.step()
                    return Token(Token.CLASS_NAME, element)

                aggregation = REGEX["aggregation"].match(element)

                if aggregation:
                    # Optional groupings returned from regex
                    # <>(* or digit)---(name)---(* or digit)-->
                    left_multi, name, right_multi = aggregation.groups()

                    values = {
                        "left_multi": left_multi,
                        "name": name,
                        "right_multi": right_multi
                    }

                    self.step()
                    return Token(Token.AGGREGATION, values)

                if REGEX["method_signature"].match(element):
                    self.step()
                    return Token(Token.METHOD, element)
                else:
                    self.step()
                    return Token(Token.FIELD, element)
