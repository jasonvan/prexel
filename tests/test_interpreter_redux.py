import unittest

from prexel.parser.lexer import Lexer
from prexel.parser.interpreter_redux import Interpreter, InterpreterException
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
        name = interpreter.class_name()

        self.assertEqual(name, "Airplane")

    def test_class_body(self):
        """
        Test the class_body() method, which processes FIELD and METHOD tokens
        """
        text = "|Airplane size color take_off()"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        interpreter.start_marker()

        interpreter.class_name()
        fields, methods = interpreter.class_body()

        self.assertEqual(fields, ["size", "color"])
        self.assertEqual(methods, ["take_off()"])

    def test_inheritance(self):
        """
        Test the inheritance() method, which processes an inheritance
        relationship.
        """
        text = "|Room height width >> Kitchen"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)

        interpreter.start_marker()
        interpreter.class_name()
        interpreter.class_body()

        self.assertTrue(interpreter.inheritance())

    def test_inheritance_with_error(self):
        """
        Test the inheritance() method, with an improper syntax
        """
        text = "|Kitchen >>"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)

        interpreter.start_marker()
        interpreter.class_name()

        # Should raise a InterpreterException
        with self.assertRaises(InterpreterException) as context:
            interpreter.inheritance()

        self.assertEqual(context.exception.args[0], "Missing child class "
                                                    "after \">>\"")

    def test_aggregation(self):
        """
        Test the aggregation() method,
        """
        text = "|Kitchen <>-cupboard--> Cupboard"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        interpreter.start_marker()
        interpreter.class_name()
        aggregation = interpreter.aggregation()

        self.assertEqual(aggregation["name"], "Cupboard")
        self.assertEqual(aggregation["instance_name"], "cupboard")

    def test_aggregation_with_missing_aggregation_name(self):
        """
        Test the aggregation() method,
        """
        text = "|Kitchen <>---> Cupboard"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)

        interpreter.start_marker()
        interpreter.class_name()
        aggregation = interpreter.aggregation()

        self.assertEqual(aggregation["name"], "Cupboard")
        self.assertEqual(aggregation["instance_name"], "cupboard")

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
        interpreter.start_marker()
        interpreter.class_name()
        aggregation = interpreter.aggregation(include_following_tokens=False)
        fields, methods = interpreter.class_body()

        self.assertEqual(aggregation["instance_name"], "cupboard")
        self.assertEqual(aggregation["name"], "Cupboard")
        self.assertEqual(fields, ["size", "color"])

    def test_aggregation_special(self):
        """
        Test the aggregation() method using multi-line syntax
        """
        text = "|Class1 <>-> Class2 class_2_field class_2_method()"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        interpreter.start_marker()
        interpreter.class_name()
        interpreter.class_body()
        aggregation = interpreter.aggregation()

        self.assertEqual(aggregation["instance_name"], "class2")
        self.assertEqual(aggregation["name"], "Class2")
        self.assertEqual(aggregation["fields"], ["class_2_field"])
        self.assertEqual(aggregation["methods"], ["class_2_method()"])

    def test_class_delimiter(self):
        """
        Test the inheritance() method, which processes an inheritance
        relationship.
        """
        text = "|Room height width >> Kitchen, Bathroom"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)

        interpreter.start_marker()
        interpreter.class_name()
        interpreter.class_body()
        interpreter.inheritance()
        interpreter.class_name()

        self.assertTrue(interpreter.class_delimiter())

    def test_class_delimiter_with_error(self):
        """
        Test the inheritance() method, which processes an inheritance
        relationship.
        """
        text = "|Room height width >> Kitchen,"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)

        interpreter.start_marker()
        interpreter.class_name()
        interpreter.class_body()
        interpreter.inheritance()
        interpreter.class_name()

        # Should raise a InterpreterException
        with self.assertRaises(InterpreterException) as context:
            interpreter.class_delimiter()

        self.assertEqual(context.exception.args[0], "The is no following "
                                                    "class name.")

    def test_evaluate(self):
        text = "|Kitchen color square_feet show_kitchen() >> Room width height <>--> Door turn_handle(), AnotherRoom field1 field2 <>1--*> Cupboard"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        interpreter.evaluate()

# #
#     def test_evaluate_advanced(self):
#         text = "|Room size >> Kitchen color square_feet show_kitchen() " \
#                "<>*-cupboards--1> Cupboard open()"
#         lexer = Lexer(text)
#
#         interpreter = Interpreter(lexer)
#         diagram = interpreter.evaluate()
#
#         # Main class diagram
#         main = diagram.main
#         self.assertEqual(main.name, "Kitchen")
#         self.assertEqual(main.methods, ["show_kitchen()"])
#         self.assertEqual(main.fields, ["color", "square_feet", "cupboards"])
#
#         # Inheritance diagram
#         inheritance = diagram.inheritance
#         self.assertIsInstance(inheritance, InheritanceDiagramPart)
#
#         # Inherited class diagram
#         parent = diagram.parent
#         self.assertEqual(parent.name, "Room")
#         self.assertIsInstance(parent, ClassDiagramPart)
#
#         # Aggregation diagram
#         aggregation = diagram.aggregation
#         self.assertIsInstance(aggregation, AggregationDiagramPart)
#         self.assertEqual(aggregation.left_multiplicity, "*")
#         self.assertEqual(aggregation.right_multiplicity, "1")
#
#         # Aggregated class diagram
#         aggregated = diagram.aggregated
#         self.assertEqual(aggregated.name, "Cupboard")
#         self.assertEqual(aggregated.methods, ["open()"])
#
#     def test_evaluate_aggregation_first_with_inheritance(self):
#         text = """
# |Room size >> Kitchen <>-cupboard--> Cupboard
# |color
# |show_kitchen()
# """
#         lexer = Lexer(text)
#         interpreter = Interpreter(lexer)
#         diagram = interpreter.evaluate()
#
#         # Main class diagram
#         main = diagram.main
#         self.assertEqual(main.name, "Kitchen")
#         self.assertEqual(main.methods, ["show_kitchen()"])
#         self.assertEqual(main.fields, ["cupboard", "color"])
#
#         # Parent class diagram
#         parent = diagram.parent
#         self.assertEqual(parent.name, "Room")
#         self.assertEqual(parent.fields, ["size"])
#
#         # Aggregation diagram
#         aggregation = diagram.aggregation
#         self.assertIsInstance(aggregation, AggregationDiagramPart)
#         self.assertEqual(aggregation.name, "cupboard")
#         self.assertEqual(aggregation.left_multiplicity, "")
#         self.assertEqual(aggregation.right_multiplicity, "")
#
#         # Aggregated class diagram
#         aggregated = diagram.aggregated
#         self.assertIsInstance(aggregated, ClassDiagramPart)
#         self.assertEqual(aggregated.name, "Cupboard")
#
#     def test_evaluate_aggregation_first(self):
#         text = "|TaskList <>-tasks----*> Task \n |get_the_tasks()"
#
#         lexer = Lexer(text)
#         interpreter = Interpreter(lexer)
#         diagram = interpreter.evaluate()
#
#         # Main class diagram
#         main = diagram.main
#         self.assertEqual(main.name, "TaskList")
#         self.assertEqual(main.methods, ["get_the_tasks()"])
#
#         # Aggregation diagram
#         aggregation = diagram.aggregation
#         self.assertIsInstance(aggregation, AggregationDiagramPart)
#         self.assertEqual(aggregation.left_multiplicity, "")
#         self.assertEqual(aggregation.right_multiplicity, "*")
#
#         # Aggregated class diagram
#         aggregated = diagram.aggregated
#         self.assertIsInstance(aggregated, ClassDiagramPart)
#         self.assertEqual(aggregated.name, "Task")
#
#     def test_evaluate_error(self):
#         text = "|Kitchen color square_feet show_kitchen() <>-cupboards-->"
#         lexer = Lexer(text)
#
#         interpreter = Interpreter(lexer)
#
#         # Test error message
#         with self.assertRaises(InterpreterException) as context:
#             interpreter.evaluate()
#
#         self.assertEqual(context.exception.args[0], "There is no class name following the aggregation.")
