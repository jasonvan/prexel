import unittest


class TestLexer(unittest.TestCase):
    """
    Token list
    Token(CLASS_MARKER, "|")
    Token(AGGREGATION, "<>{1}--{*}>")
    Token(DEPENDENCE, "-->")
    Token(INHERITENCE, "^")
    Token(INTERFACE, "=")
    """
    def test_advance(self):
        pass

    def test_handle_whitespace(self):
        pass
