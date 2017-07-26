import unittest
from prexel.plugin.parser.lexer import Lexer


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

if __name__ == '__main__':
    unittest.main()
