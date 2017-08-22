import unittest

from prexel.plugin.parser.lexer import Lexer
from prexel.plugin.parser.interpreter import Interpreter, InterpreterException
from prexel.plugin.parser.token import Token
from prexel.plugin.models.diagram import (ClassDiagram,
                                          InheritanceDiagram,
                                          AggregationDiagram)


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

        class_diagram = ClassDiagram()

        interpreter.class_name(class_diagram)
        self.assertEqual(class_diagram.name, "Airplane")

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
        text = "|Kitchen << Room color square_feet show_kitchen() " \
               "<>*-cupboards--1> Cupboard open()"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        diagrams = interpreter.evaluate()

        self.assertEqual(len(diagrams), 5)

        # Main class diagram
        main_class_diagram = diagrams[0]
        self.assertEqual(main_class_diagram.name, "Kitchen")
        self.assertEqual(main_class_diagram.methods, ["show_kitchen()"])
        self.assertEqual(main_class_diagram.fields, ["color", "square_feet",
                                                     "cupboards"])

        # Inheritance diagram
        inheritance_diagram = diagrams[1]
        self.assertIsInstance(inheritance_diagram, InheritanceDiagram)

        # Inherited class diagram
        inherited_class_diagram = diagrams[2]
        self.assertEqual(inherited_class_diagram.name, "Room")
        self.assertIsInstance(inherited_class_diagram, ClassDiagram)

        # Aggregation diagram
        aggregation_diagram = diagrams[3]
        self.assertIsInstance(aggregation_diagram, AggregationDiagram)
        self.assertEqual(aggregation_diagram.left_multiplicity, "*")
        self.assertEqual(aggregation_diagram.right_multiplicity, "1")

        # Aggregated class diagram
        aggregated_class_diagram = diagrams[4]
        self.assertEqual(aggregated_class_diagram.name, "Cupboard")
        self.assertEqual(aggregated_class_diagram.methods, ["open()"])

    def test_evaluate_aggregation_first(self):
        text = "|TaskList <>-tasks----*> Task \n |get_the_tasks()"

        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        diagrams = interpreter.evaluate()

        # Main class diagram
        main_class_diagram = diagrams[0]
        self.assertEqual(main_class_diagram.name, "TaskList")
        self.assertEqual(main_class_diagram.methods, ["get_the_tasks()"])

        # Aggregation diagram
        aggregation_diagram = diagrams[1]
        self.assertIsInstance(aggregation_diagram, AggregationDiagram)
        self.assertEqual(aggregation_diagram.left_multiplicity, "")
        self.assertEqual(aggregation_diagram.right_multiplicity, "*")

        # Aggregated class diagram
        aggregated_class_diagrams = diagrams[2]
        self.assertEqual(aggregated_class_diagrams.name, "Task")

    def test_evaluate_error(self):
        text = "|Kitchen color square_feet show_kitchen() <>-cupboards-->"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)

        # Test error message
        with self.assertRaises(InterpreterException) as context:
            interpreter.evaluate()

        self.assertTrue('Invalid Syntax' in str(context.exception))
