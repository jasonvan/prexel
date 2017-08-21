import unittest
from prexel.plugin.parser.lexer import Lexer
from prexel.plugin.parser.token import Token


class TestLexer(unittest.TestCase):
    def test_step(self):
        text = "|Kitchen get_cabinet()"
        lexer = Lexer(text)

        for _ in range(5):
            lexer.step()

        self.assertEqual(lexer.current, "h")

    def test_step_end_of_text(self):
        text = "|Kitchen"
        lexer = Lexer(text)

        for _ in range(8):
            lexer.step()

        self.assertEqual(lexer.current, None)

    def test_element(self):
        text = "|Kitchen color square_feet show_kitchen()"

        lexer = Lexer(text)

        lexer.step()  # skip "|"
        result = lexer.element()

        self.assertEqual(result, "Kitchen")

        lexer.step()  # skip whitespace
        result = lexer.element()

        self.assertEqual(result, "color")

    def test_skip_whitespace(self):
        text = "|Kitchen    color"

        lexer = Lexer(text)

        lexer.step()  # skip "|"
        lexer.element()  # get first element
        lexer.skip_whitespace()

        self.assertEqual(lexer.current, "c")

    def test_get_token(self):
        text = "|Kitchen color square_feet show_kitchen()"

        lexer = Lexer(text)
        token = lexer.get_token()

        # Check that the token is a prexel marker
        self.assertEqual(token.type, Token.PREXEL_MARKER)

        token = lexer.get_token()

        # Check that the token is a class name
        self.assertEqual(token.type, Token.CLASS_NAME)

        token = lexer.get_token()

        # Check that the token is a field
        self.assertEqual(token.type, Token.FIELD)

        # Check that the token is a field
        token = lexer.get_token()
        self.assertEqual(token.type, Token.FIELD)

        # Check that the token is a method
        token = lexer.get_token()
        self.assertEqual(token.type, Token.METHOD)

    def test_get_token_with_inheritence(self):
        text = "|Kitchen << Room"

        lexer = Lexer(text)
        token = lexer.get_token()

        # Check that the token is a prexel marker
        self.assertEqual(token.type, Token.PREXEL_MARKER)

        token = lexer.get_token()

        # Check that the token is a class name
        self.assertEqual(token.type, Token.CLASS_NAME)

        token = lexer.get_token()

        # Check that the token is an inheritance token
        self.assertEqual(token.type, Token.INHERITANCE)

        token = lexer.get_token()

        # Check that the token is a class name
        self.assertEqual(token.type, Token.CLASS_NAME)

    def test_get_token_with_aggregation(self):
        text = "|Airplane <>-wings--> Wing"

        lexer = Lexer(text)
        token = lexer.get_token()

        # Check that the token is a prexel marker
        self.assertEqual(token.type, Token.PREXEL_MARKER)

        token = lexer.get_token()

        # Check that the token is a class name
        self.assertEqual(token.type, Token.CLASS_NAME)

        token = lexer.get_token()

        # Check that the token is an aggregation
        self.assertEqual(token.type, Token.AGGREGATION)
        self.assertEqual(token.value["left_multi"], "")
        self.assertEqual(token.value["name"], "wings")
        self.assertEqual(token.value["right_multi"], "")

        token = lexer.get_token()

        # Check that the token is a class name
        self.assertEqual(token.type, Token.CLASS_NAME)

    def test_get_token_with_aggregation_error(self):
        text = "|Airplane length <> Wing"

        lexer = Lexer(text)
        token = lexer.get_token()

        # Check that the token is a prexel marker
        self.assertEqual(token.type, Token.PREXEL_MARKER)

        token = lexer.get_token()

        # Check that the token is a class name
        self.assertEqual(token.type, Token.CLASS_NAME)

        token = lexer.get_token()

        # Check that the token is a field
        self.assertEqual(token.type, Token.FIELD)

        token = lexer.get_token()

        # Check that token is the "Wing" values and not "<>"
        # which should have been skipped
        self.assertEqual(token.type, Token.CLASS_NAME)
        self.assertEqual(token.value, "Wing")

if __name__ == '__main__':
    unittest.main()
