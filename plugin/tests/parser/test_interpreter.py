import unittest

from prexel.plugin.parser.lexer import Lexer
from prexel.plugin.parser.interpreter import Interpreter, InterpreterException
from prexel.plugin.parser.token import Token


class TestInterpreter(unittest.TestCase):
    def test_init(self):
        text = "|Airplane <>-wings--> Wing"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)

        self.assertEqual(interpreter.current_token.type, Token.PREXEL_MARKER)
        self.assertEqual(interpreter.current_token.value, "|")

    def test_process_token(self):
        text = "|Airplane <>-wings--> Wing"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        interpreter.process_token(Token.PREXEL_MARKER)

        self.assertEqual(interpreter.current_token.type, Token.CLASS_NAME)

        # Test error message
        with self.assertRaises(InterpreterException) as context:
            interpreter.process_token(Token.FIELD)

        self.assertTrue('Invalid Syntax' in str(context.exception))

    def test_expr(self):
        text = "|Kitchen color square_feet show_kitchen()"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        diagram = interpreter.expr()

        self.assertEqual(diagram.name, "Kitchen")
        self.assertEqual(diagram.methods, ["show_kitchen()"])
        self.assertEqual(diagram.fields, ["color", "square_feet"])

