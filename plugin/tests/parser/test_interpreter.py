import unittest

from prexel.plugin.parser.lexer import Lexer
from prexel.plugin.parser.interpreter import Interpreter, InterpreterException
from prexel.plugin.parser.token import Token
from prexel.plugin.models.diagram import Diagram


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

    def test_prexel(self):
        text = "|Airplane <>-wings--> Wing"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        interpreter.prexel()

        self.assertEqual(interpreter.current_token.value, "Airplane")
        self.assertEqual(interpreter.current_token.type, Token.CLASS_NAME)

    def test_class_name(self):
        text = "|Airplane <>-wings--> Wing"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        interpreter.prexel()

        diagram = Diagram()

        interpreter.class_name(diagram)
        self.assertEqual(diagram.name, "Airplane")

    def test_expr(self):
        text = "|Kitchen color square_feet show_kitchen()"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        diagrams = interpreter.expr()

        self.assertEqual(len(diagrams), 1)

        first_diagram = diagrams[0]

        self.assertEqual(first_diagram.name, "Kitchen")
        self.assertEqual(first_diagram.methods, ["show_kitchen()"])
        self.assertEqual(first_diagram.fields, ["color", "square_feet"])

    def test_expr_advanced(self):
        text = "|Kitchen color square_feet show_kitchen() <>-cupboards--> Cupboard open()"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        diagrams = interpreter.expr()

        self.assertEqual(len(diagrams), 2)

        first_diagram = diagrams[0]

        self.assertEqual(first_diagram.name, "Kitchen")
        self.assertEqual(first_diagram.methods, ["show_kitchen()"])
        self.assertEqual(first_diagram.fields, ["color", "square_feet", "cupboards"])

        second_diagram = diagrams[1]

        self.assertEqual(second_diagram.name, "Cupboard")
        self.assertEqual(second_diagram.methods, ["open()"])

