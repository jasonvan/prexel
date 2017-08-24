import unittest

from prexel.parser.lexer import Lexer
from prexel.parser.interpreter import Interpreter, InterpreterException
from prexel.parser.token import Token
from prexel.models.diagram import (ClassDiagramPart, 
                                InheritanceDiagramPart,
                            AggregationDiagramPart)


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

        class_diagram = ClassDiagramPart()

        interpreter.class_name(class_diagram)
        self.assertEqual(class_diagram.name, "Airplane")

    def test_evaluate(self):
        text = "|Kitchen color square_feet show_kitchen()"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        diagram = interpreter.evaluate()

        main = diagram.main
        self.assertIsInstance(main, ClassDiagramPart)

        self.assertEqual(main.name, "Kitchen")
        self.assertEqual(main.methods, ["show_kitchen()"])
        self.assertEqual(main.fields, ["color", "square_feet"])

    def test_evaluate_advanced(self):
        text = "|Kitchen << Room color square_feet show_kitchen() " \
               "<>*-cupboards--1> Cupboard open()"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        diagram = interpreter.evaluate()

        # Main class diagram
        main = diagram.main
        self.assertEqual(main.name, "Kitchen")
        self.assertEqual(main.methods, ["show_kitchen()"])
        self.assertEqual(main.fields, ["color", "square_feet", "cupboards"])

        # Inheritance diagram
        inheritance = diagram.inheritance
        self.assertIsInstance(inheritance, InheritanceDiagramPart)

        # Inherited class diagram
        parent = diagram.parent
        self.assertEqual(parent.name, "Room")
        self.assertIsInstance(parent, ClassDiagramPart)

        # Aggregation diagram
        aggregation = diagram.aggregation
        self.assertIsInstance(aggregation, AggregationDiagramPart)
        self.assertEqual(aggregation.left_multiplicity, "*")
        self.assertEqual(aggregation.right_multiplicity, "1")

        # Aggregated class diagram
        aggregated = diagram.aggregated
        self.assertEqual(aggregated.name, "Cupboard")
        self.assertEqual(aggregated.methods, ["open()"])

    def test_evaluate_aggregation_first(self):
        text = "|TaskList <>-tasks----*> Task \n |get_the_tasks()"

        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        diagram = interpreter.evaluate()

        # Main class diagram
        main = diagram.main
        self.assertEqual(main.name, "TaskList")
        self.assertEqual(main.methods, ["get_the_tasks()"])

        # Aggregation diagram
        aggregation = diagram.aggregation
        self.assertIsInstance(aggregation, AggregationDiagramPart)
        self.assertEqual(aggregation.left_multiplicity, "")
        self.assertEqual(aggregation.right_multiplicity, "*")

        # Aggregated class diagram
        aggregated = diagram.aggregated
        self.assertIsInstance(aggregated, ClassDiagramPart)
        self.assertEqual(aggregated.name, "Task")

    def test_evaluate_error(self):
        text = "|Kitchen color square_feet show_kitchen() <>-cupboards-->"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)

        # Test error message
        with self.assertRaises(InterpreterException) as context:
            interpreter.evaluate()

        self.assertTrue('Invalid Syntax' in str(context.exception))
