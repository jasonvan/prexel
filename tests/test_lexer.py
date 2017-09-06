import unittest
from prexel.parser.lexer import Lexer
from prexel.parser.token import Token


class TestLexer(unittest.TestCase):
    """
    Test cases to exercise the Lexer class.
    """
    def test_step(self):
        """
        Test the step() method, which steps forward in the string one character.
        """
        text = "|Kitchen get_cabinet()"
        lexer = Lexer(text)

        for _ in range(5):
            lexer.step()

        self.assertEqual(lexer.current, "h")

    def test_step_end_of_text(self):
        """
        Test the step() method going all the way to the end of the string.
        """
        text = "|Kitchen"
        lexer = Lexer(text)

        for _ in range(8):
            lexer.step()

        self.assertEqual(lexer.current, None)

    def test_skip_whitespace(self):
        """
        Test the skip_whitespace() method, which will advance the self.current pointer past
        all whitespace character until the next non-whitespace character.
        """
        text = "|Kitchen    color \n\n size"
        lexer = Lexer(text)

        # Skip "|"
        lexer.step()

        # Get first token, e.g., "Kitchen"
        lexer.generate_token_string()

        # Skip the following whitespace
        lexer.skip_whitespace()

        # Assert correct character at current pointer
        self.assertEqual(lexer.current, "c")

        # Get second token, e.g., "color"
        lexer.generate_token_string()

        # Skip the newline character
        lexer.skip_whitespace()

        # Assert correct character at current pointer
        self.assertEqual(lexer.current, "s")

    def test_generate_token_string(self):
        """
        Test the generate_token_string() method, which creates strings that will be turned into Token object
        """
        text = "|Kitchen color square_feet show_kitchen()"
        lexer = Lexer(text)

        # Skip "|"
        lexer.step()
        self.assertEqual(lexer.generate_token_string(), "Kitchen")

        # Skip whitespace between "Kitchen" and "color"
        lexer.skip_whitespace()
        self.assertEqual(lexer.generate_token_string(), "color")

    def test_get_token(self):
        """
        Test the get_token() method, which turns a token string into a Token object
        """
        text = "|Kitchen color square_feet show_kitchen()"
        lexer = Lexer(text)

        # Check that the token is a PREXEL marker
        self.assertEqual(lexer.get_token().type, Token.START_MARKER)

        # Check that the token is a class name
        self.assertEqual(lexer.get_token().type, Token.CLASS_NAME)

        # Check that the token is a field
        self.assertEqual(lexer.get_token().type, Token.FIELD)

        # Check that the token is a field
        self.assertEqual(lexer.get_token().type, Token.FIELD)

        # Check that the token is a method
        self.assertEqual(lexer.get_token().type, Token.METHOD)

    def test_get_token_with_inheritance(self):
        """
        Test the get_token() method with an inheritance Token
        """
        text = "|Kitchen >> Room"
        lexer = Lexer(text)

        # Check that the token is a PREXEL marker
        self.assertEqual(lexer.get_token().type, Token.START_MARKER)

        # Check that the token is a class name
        self.assertEqual(lexer.get_token().type, Token.CLASS_NAME)

        # Check that the token is an inheritance token
        self.assertEqual(lexer.get_token().type, Token.INHERITANCE)

        # Check that the token is a class name
        self.assertEqual(lexer.get_token().type, Token.CLASS_NAME)

    def test_get_token_with_aggregation(self):
        """
        Test the get_token() method with an aggregation Token
        """
        text = "|Airplane <>-wings--> Wing"
        lexer = Lexer(text)

        # Check that the token is a PREXEL marker
        self.assertEqual(lexer.get_token().type, Token.START_MARKER)

        # Check that the token is a class name
        self.assertEqual(lexer.get_token().type, Token.CLASS_NAME)

        # Check that the token is an aggregation
        token = lexer.get_token()
        self.assertEqual(token.type, Token.AGGREGATION)
        self.assertEqual(token.value["left_multi"], "")
        self.assertEqual(token.value["name"], "wings")
        self.assertEqual(token.value["right_multi"], "")

        # Check that the token is a class name
        self.assertEqual(lexer.get_token().type, Token.CLASS_NAME)

    def test_get_token_with_aggregation_error(self):
        """
        Test the get_token() method with an aggregation Token that is not correct
        """
        text = "|Airplane length <> Wing"
        lexer = Lexer(text)

        # Check that the token is a prexel marker
        self.assertEqual(lexer.get_token().type, Token.START_MARKER)

        # Check that the token is a class name
        self.assertEqual(lexer.get_token().type, Token.CLASS_NAME)

        # Check that the token is a field
        self.assertEqual(lexer.get_token().type, Token.FIELD)

        # Check that token is the "Wing" values and not "<>"
        # which should have been skipped
        token = lexer.get_token()
        self.assertEqual(token.type, Token.CLASS_NAME)
        self.assertEqual(token.value, "Wing")

    def test_get_token_skip_extra_prexel_markets(self):
        """
        Test the get_token() method with extra PREXEL markers
        """
        text = "|Room >> Kitchen \n|arrange_kitchen()\n|place_floor_cabinet()"
        lexer = Lexer(text)

        lexer.get_token()  # PREXEL marker
        lexer.get_token()  # "Room"
        lexer.get_token()  # ">>"
        lexer.get_token()  # "Kitchen"

        # Skip extra "|" tokens
        self.assertEqual(lexer.get_token().type, Token.METHOD)
        self.assertEqual(lexer.get_token().type, Token.METHOD)

if __name__ == '__main__':
    unittest.main()
