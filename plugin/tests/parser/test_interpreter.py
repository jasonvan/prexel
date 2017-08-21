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

    def test_start_marker(self):
        text = "|Airplane <>-wings--> Wing"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        interpreter.start_marker()

        self.assertEqual(interpreter.current_token.value, "Airplane")
        self.assertEqual(interpreter.current_token.type, Token.CLASS_NAME)

    def test_class_name(self):
        text = "|Airplane <>-wings--> Wing"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        interpreter.start_marker()

        diagram = Diagram()

        interpreter.class_name(diagram)
        self.assertEqual(diagram.name, "Airplane")

    def test_evaluate(self):
        text = "|Kitchen color square_feet show_kitchen()"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        diagrams = interpreter.evaluate()

        self.assertEqual(len(diagrams), 1)

        first_diagram = diagrams[0]

        self.assertEqual(first_diagram.name, "Kitchen")
        self.assertEqual(first_diagram.methods, ["show_kitchen()"])
        self.assertEqual(first_diagram.fields, ["color", "square_feet"])

    def test_evaluate_advanced(self):
        text = "|Kitchen << Room color square_feet show_kitchen() <>-cupboards--> Cupboard open()"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        diagrams = interpreter.evaluate()

        self.assertEqual(len(diagrams), 3)

        first_diagram = diagrams[0]

        self.assertEqual(first_diagram.name, "Kitchen")
        self.assertEqual(first_diagram.methods, ["show_kitchen()"])
        self.assertEqual(first_diagram.fields, ["color", "square_feet", "cupboards"])

        second_diagram = diagrams[1]

        self.assertEqual(second_diagram.name, "Room")
        self.assertEqual(second_diagram.diagram_type, "inheritance")

        third_diagram = diagrams[2]

        self.assertEqual(third_diagram.name, "Cupboard")
        self.assertEqual(third_diagram.methods, ["open()"])

    def test_evaluate_error(self):
        text = "|Kitchen color square_feet show_kitchen() <>-cupboards-->"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)

        # Test error message
        with self.assertRaises(InterpreterException) as context:
            interpreter.evaluate()

        self.assertTrue('Invalid Syntax' in str(context.exception))
