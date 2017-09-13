from prexel.parser.token import Token
from prexel import regex


class Lexer:
    """
    The Lexer class manages splitting an easy-entry string into individual Token objects
    """
    def __init__(self, text):
        self.text = text
        self.position = 0
        self.current = self.text[self.position]
        self.marker_found = False

    def step(self):
        """
        Advance one character in the easy-entry string.
        """
        self.position += 1

        if self.position >= len(self.text):
            self.current = None
        else:
            self.current = self.text[self.position]

    def skip_whitespace(self):
        """
        Step past 1 or more whitespace characters.
        """
        while self.current is not None and self.current.isspace():
            self.step()

    def generate_token_string(self):
        """
        Generate an individual token.
        """
        token_chars = []

        while self.current is not None \
                and not self.current.isspace() \
                and not regex.is_reserved_character(self.current):
            token_chars.append(self.current)
            self.step()

        return ''.join(token_chars)

    def get_token(self):
        """
        Create a Token object for next token.
        :return: Token
        """
        while self.current is not None:
            # Skip any white space
            if self.current.isspace():
                self.skip_whitespace()
                continue
            # Check if current character is the PREXEL marker
            elif self.current == "|":
                self.step()

                # Check and see if the PREXEL marker has already been found.
                # Only the first PREXEL marker will be tokenized. The rest will be ignored.
                if not self.marker_found:
                    self.marker_found = True
                    return Token(Token.START_MARKER, "|")
                else:
                    continue  # Go to next character
            # Check if current character is a comma
            elif self.current == ",":
                self.step()
                return Token(Token.COMMA, ",")
            else:
                # Generate the current token
                token = self.generate_token_string()

                # Check token against a variety of regex to determine what
                # type of Token it is.
                if regex.is_class_name(token):
                    return Token(Token.CLASS_NAME, token)
                elif regex.is_inheritance(token):
                    return Token(Token.INHERITANCE, token)
                elif regex.is_aggregation(token):
                    # Optional groupings returned from regex
                    # <>(* or digit)---(name)---(* or digit)-->
                    aggregation_groups = regex.is_aggregation(token).groups()
                    left_multi, name, right_multi = aggregation_groups

                    values = {
                        "left_multi": left_multi,
                        "name": name,
                        "right_multi": right_multi
                    }

                    return Token(Token.AGGREGATION, values)
                elif regex.is_method_signature(token):
                    return Token(Token.METHOD, token)
                elif regex.is_ignored_token(token):
                    continue  # Skip ignored characters
                else:
                    return Token(Token.FIELD, token)
