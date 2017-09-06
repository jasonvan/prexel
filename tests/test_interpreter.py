import unittest

from prexel.parser.lexer import Lexer
from prexel.parser.interpreter import Interpreter, InterpreterException
from prexel.parser.token import Token
from prexel.models.diagram import (ClassDiagramPart,
                                   InheritanceDiagramPart,
                                   AggregationDiagramPart)


class TestInterpreter(unittest.TestCase):
    """
    Test cases to exercise the Interpreter class.
    """
    def test_init(self):
        """
        Test the __init__() method.
        """
        text = "|Airplane <>-wings--> Wing"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)

        self.assertEqual(interpreter.current_token.type, Token.START_MARKER)
        self.assertEqual(interpreter.current_token.value, "|")

    def test_process_token(self):
        """
        Test the process_token() method which processes one token at
        a time. Also includes a test to confirm an error message is given
        if an improper token is given.
        """
        text = "|Airplane <>-wings--> Wing"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        interpreter.process_token(Token.START_MARKER)

        # Assert the current token is a CLASS_NAME
        self.assertEqual(interpreter.current_token.type, Token.CLASS_NAME)

        # Test error message is raised when the incorrect token processed
        with self.assertRaises(InterpreterException) as context:
            interpreter.process_token(Token.FIELD)

        self.assertTrue('Invalid Syntax' in str(context.exception))

    def test_start_marker(self):
        """
        Test the start_marker() method, which processes a START_MARKER
        token.
        """
        text = "|Airplane <>-wings--> Wing"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        interpreter.start_marker()

        self.assertEqual(interpreter.current_token.value, "Airplane")
        self.assertEqual(interpreter.current_token.type, Token.CLASS_NAME)

    def test_class_name(self):
        """
        Test the class_name() method, which processes a CLASS_NAME token.
        """
        text = "|Airplane <>-wings--> Wing"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        interpreter.start_marker()

        class_diagram = ClassDiagramPart()

        interpreter.class_name(class_diagram)
        self.assertEqual(class_diagram.name, "Airplane")

    def test_class_body(self):
        """
        Test the class_body() method, which processes FIELD and METHOD tokens
        """
        text = "|Airplane size color take_off()"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        interpreter.start_marker()

        class_diagram = ClassDiagramPart()

        interpreter.class_name(class_diagram)
        interpreter.class_body(class_diagram)

        self.assertEqual(class_diagram.fields, ["size", "color"])
        self.assertEqual(class_diagram.methods, ["take_off()"])

    def test_inheritance(self):
        """
        Test the inheritance() method, which processes an inheritance relationship
        """
        text = "|Room height width >> Kitchen"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        diagram = interpreter.diagram
        class_diagram_part = ClassDiagramPart()

        interpreter.start_marker()
        interpreter.class_name(class_diagram_part)
        interpreter.class_body(class_diagram_part)

        if interpreter.inheritance():
            diagram.parent = class_diagram_part
        else:
            diagram.main = class_diagram_part

        self.assertEqual(diagram.parent.name, "Room")
        self.assertEqual(diagram.parent.fields, ["height", "width"])
        self.assertEqual(diagram.main.name, "Kitchen")

    def test_inheritance_with_error(self):
        """
        Test the inheritance() method, with an improper syntax
        """
        text = "|Kitchen >>"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        class_diagram_part = ClassDiagramPart()

        interpreter.start_marker()
        interpreter.class_name(class_diagram_part)

        # Should raise a InterpreterException
        with self.assertRaises(InterpreterException) as context:
            interpreter.inheritance()

        self.assertEqual(context.exception.args[0], "Missing child class after \">>\"")

    def test_aggregation(self):
        """
        Test the aggregation() method,
        """
        text = "|Kitchen <>-cupboard--> Cupboard"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        diagram = interpreter.diagram
        class_diagram_part = ClassDiagramPart()

        interpreter.start_marker()
        interpreter.class_name(class_diagram_part)
        diagram.main = class_diagram_part
        interpreter.aggregation()

        self.assertEqual(diagram.aggregation.name, "cupboard")
        self.assertEqual(diagram.main.fields, ["cupboard"])
        self.assertEqual(diagram.aggregated.name, "Cupboard")

    def test_aggregation_with_missing_aggregation_name(self):
        """
        Test the aggregation() method,
        """
        text = "|Kitchen <>---> Cupboard"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        diagram = interpreter.diagram
        class_diagram_part = ClassDiagramPart()

        interpreter.start_marker()
        interpreter.class_name(class_diagram_part)
        diagram.main = class_diagram_part
        interpreter.aggregation()

        self.assertEqual(diagram.aggregation.name, "cupboard")
        self.assertEqual(diagram.main.fields, ["cupboard"])
        self.assertEqual(diagram.aggregated.name, "Cupboard")

    def test_aggregation_multi_line(self):
        """
        Test the aggregation() method using multi-line syntax
        """
        text = """
|Kitchen <>-cupboard--> Cupboard
|size
|color"""
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        diagram = interpreter.diagram

        class_diagram_part = ClassDiagramPart()

        interpreter.start_marker()
        interpreter.class_name(class_diagram_part)
        diagram.main = class_diagram_part
        interpreter.aggregation(include_following_tokens=False)
        interpreter.class_body(diagram.main)

        self.assertEqual(diagram.aggregation.name, "cupboard")
        self.assertEqual(diagram.main.fields, ["cupboard", "size", "color"])
        self.assertEqual(diagram.aggregated.name, "Cupboard")

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
        text = "|Room size >> Kitchen color square_feet show_kitchen() " \
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

    def test_evaluate_aggregation_first_with_inheritance(self):
        text = """
|Room size >> Kitchen <>-cupboard--> Cupboard
|color
|show_kitchen()
"""
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        diagram = interpreter.evaluate()

        # Main class diagram
        main = diagram.main
        self.assertEqual(main.name, "Kitchen")
        self.assertEqual(main.methods, ["show_kitchen()"])
        self.assertEqual(main.fields, ["cupboard", "color"])

        # Parent class diagram
        parent = diagram.parent
        self.assertEqual(parent.name, "Room")
        self.assertEqual(parent.fields, ["size"])

        # Aggregation diagram
        aggregation = diagram.aggregation
        self.assertIsInstance(aggregation, AggregationDiagramPart)
        self.assertEqual(aggregation.name, "cupboard")
        self.assertEqual(aggregation.left_multiplicity, "")
        self.assertEqual(aggregation.right_multiplicity, "")

        # Aggregated class diagram
        aggregated = diagram.aggregated
        self.assertIsInstance(aggregated, ClassDiagramPart)
        self.assertEqual(aggregated.name, "Cupboard")

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

        self.assertEqual(context.exception.args[0], "There is no class name following the aggregation.")
